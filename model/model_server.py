from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS,cross_origin

from soccerUI.HttpHandlers.mongoDB_API import mongo_API
from DataParser.RedWoodParser import RedWoodParser

from model.dataManger import FileDataManger
from model.soccer_predict_model import SoccerPredictModel
from model.Data_Predict_Organizer import Data_Predict_Organizer

from model.teams_mapper import TeamMapper as mapper

# from xgboost import XGBClassifier

from joblib import load

app = Flask(__name__)
api = Api(app)
API = CORS(app, supports_credentials=True)

get_db_connector = mongo_API()
data_manger = FileDataManger(get_db_connector)
redwoodParser = RedWoodParser()
data_predict_org = Data_Predict_Organizer()


class ModelServer(Resource):

    def get(self, league, home_team, away_team):
        sp_model_file_name = ''

        print('get : {}/{}/{}'.format(league, home_team, away_team))

        if league in ['England', 'Spain', 'Italy', 'Germany']:
            sp_model_file_name = 'modelForProd/' + league.lower() + '_sp_model.joblib'
        else:
            return "league : {} is not supported".format(league), 404

        print('load {}'.format(sp_model_file_name))
        model = load(sp_model_file_name)

        get_db_connector = mongo_API()
        get_data_manger = FileDataManger(get_db_connector)
        get_redwoodParser = RedWoodParser()
        get_data_predict_org = Data_Predict_Organizer()

        sp_model = SoccerPredictModel(model, get_redwoodParser, get_data_manger, league, get_data_predict_org)
        mapped_home_team = mapper.map(home_team)
        print(mapped_home_team)
        mapped_away_team = mapper.map(away_team)
        print(mapped_away_team)
        res = sp_model.predict(mapped_home_team, mapped_away_team, 6)
        print(res)

        return res, 200


api.add_resource(ModelServer, '/predict/<string:league>/<string:home_team>/<string:away_team>/')

app.run(debug=True)