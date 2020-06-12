from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy
from catboost import CatBoostClassifier
from Logger import main as log_class


class SoccerPredictModel:
    """
    this class is to mange all the things for the ML
    the Model : ML model, using python library for ML
    data_parser : we get the data as raw data, the parser will convert the data to vector so the ML can use it
    cache : cache mechanism, if we predict game already do not predict it again
    data_manger : will manage the data, will know how to import the data(from DB or elsewhere)
    """

    __model = None
    __data_parser = None
    __data_manger = None
    __league = None
    __db_name = 'soccer_db'
    __seasons = ['14-15', '15-16', '16-17', '17-18', '18-19']
    __data_after_parse = None
    __data_predict_organizer = None

    def __init__(self, model, data_parser, data_manger, league, data_predict_organizer):
        self.__model = model
        self.__data_parser = data_parser
        self.__data_manger = data_manger
        self.__league = league
        self.__data_predict_organizer = data_predict_organizer
        # self.logger = log_class.setup_logger('SoccerPredictModel.log')

    def predict(self, home_team_name, away_team_name, num_of_last_games):
        """ API for using the model and get prediction"""
        # self.logger.info('predict for home team : {}, away team : {} num of last games : {}'.format(home_team_name, away_team_name, num_of_last_games))

        self.set_data_after_parse()

        #print('data after parse size : {}'.format(len(self.__data_after_parse)))

        avg_game_json = self.__data_predict_organizer.orgnaize_json(home_team_name, away_team_name, self.__data_after_parse, num_of_last_games)

        game_vector, winner = self.__data_parser.get_game_vector(avg_game_json)

        res = self.__model.predict_proba(numpy.array(game_vector).reshape((1, -1)))

        return {"HomeTeam":(res[0][1] * 100),"Draw":(res[0][0] * 100 ),"AwayTeam":(res[0][2] * 100)}

    def train(self, random_seed, test_size):
        """ API for model train
        :param test_size:
        :param random_seed:
        """
        #self.logger.info('train, with random_seed : {} and test_size : {}'.format(random_seed, test_size))

        all_games_vector = []
        winners_vector = []

        self.set_data_after_parse()

        for game in self.__data_after_parse:
            game_vector, winner = self.__data_parser.get_game_vector(game)
            all_games_vector.append(game_vector)
            winners_vector.append(winner)

        # use the model to train
        # X is the vectors and Y is the label
        X_train, X_test, y_train, y_test = train_test_split(numpy.array(all_games_vector), numpy.array(winners_vector), test_size=test_size, random_state=random_seed)
        # self.logger.info('train, train size : {}, test size : {} '.format(len(X_train), len(X_test)))

        self.__model.fit(X_train, y_train)
        # self.logger.info('train, model : {}'.format(self.__model))

        # try to predict on the test set, and print the accuracy
        #y_pred = self.__model.predict(X_test)
        #predictions = [round(value) for value in y_pred]
        # evaluate predictions
        #accuracy = accuracy_score(y_test, predictions)
        # self.logger.info("train, Accuracy: %.2f%%" % (accuracy * 100.0))

        # save the trained model using the data_manger

    def set_data_after_parse(self, data_after_parse_parm=None):
        data = []
        data_after_parse = []

        if self.__data_after_parse != None:
            return self.__data_after_parse

        elif data_after_parse_parm != None:
            self.__data_after_parse = data_after_parse_parm
        else :
            # get the data from the data_manger
            for season in self.__seasons:
                data.append(self.__data_manger.get_season(self.__db_name, self.__league + '_' + season))

            for season in data:
                for game in season:
                    game_after_parse = self.__data_parser.parse_json_to_filterd_json(game)
                    if game_after_parse is not None:
                        data_after_parse.append(game_after_parse)

            self.__data_after_parse = data_after_parse
        return self.__data_after_parse

    def get_data_after_parse(self):
        return self.__data_after_parse

    def get_model(self):
        return self.__model