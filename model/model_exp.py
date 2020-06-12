import unittest
import csv
from soccerUI.HttpHandlers.mongoDB_API import mongo_API
from DataParser.RedWoodParser import RedWoodParser
import numpy
from model.dataManger import DataManger
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from model.soccer_predict_model import SoccerPredictModel
from model.Data_Predict_Organizer import Data_Predict_Organizer
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from catboost import CatBoostClassifier


def get_winner_from_char(char):
    if char == 'D':
        return 0
    if char == 'H':
        return 1
    if char == 'A':
        return 2

def get_winner_from_prob(prob):
    max = 0
    max_index = 0

    for index in range(0, 3):
        if prob[index] > max:
            max = prob[index]
            max_index = index

    # the prob vecotr return that the first place is home and second is draw
    if max_index == 0:
        return 1

    if max_index == 1:
        return 0

    return max_index

def test(sp_model, number_of_last_games, file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        success = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print('home team : {}, away team : {} winner : {}'.format(row[1], row[2], get_winner_from_char(row[5])))
                line_count += 1
                res = sp_model.predict_proba(row[1], row[2], number_of_last_games)
                #print('home team : {}, away team : {} result : {}'.format(row[1], row[2], res))
                p = get_winner_from_prob(list(res.values()))
                #print(' predict_proba : {} actual : {}'.format(p, get_winner_from_char(row[5])))
                if p == get_winner_from_char(row[5]):
                    #print('great success')
                    success += 1

        print('################  num of last games : {} , test result : {} #########################'.format(number_of_last_games, success / line_count))
        return success / line_count



class MyTestCase(unittest.TestCase):

    english_csv_file = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/english_season-1819_csv.csv'
    spain_csv_file = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/spain_season-1819_csv.csv'
    germany_csv_file = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/germany_season-1819_csv.csv'
    italy_csv_file = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/italy_season-1819_csv.csv'

    english_xg_result = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/english_xg_result.csv'


    def test_basic_model_english_xg(self):
        db_connector = mongo_API()
        data_manger = DataManger(db_connector)
        redwoodParser = RedWoodParser()
        ignore_list = ['Date', 'TournamentName', 'SeasonName', 'RoundId', 'HomeTeamName', 'AwayTeamName']
        redwoodParser.set_ignore_list(ignore_list)
        model = XGBClassifier(max_depth=5, booster='gblinear')
        data_predict_org = Data_Predict_Organizer()

        sp_model = SoccerPredictModel(model, redwoodParser, data_manger, 'England', data_predict_org)
        sp_model.train(7, 0.1)

        test(sp_model, 6, self.english_csv_file)

    def test_basic_model_english_random_forest(self):
        db_connector = mongo_API()
        data_manger = DataManger(db_connector)
        redwoodParser = RedWoodParser()
        model = RandomForestClassifier()
        data_predict_org = Data_Predict_Organizer()

        sp_model = SoccerPredictModel(model, redwoodParser, data_manger, 'England', data_predict_org)
        sp_model.train(7, 0.1)

        test(sp_model, 10, self.english_csv_file)

    def test_basic_model_english_KNN(self):
        db_connector = mongo_API()
        data_manger = DataManger(db_connector)
        redwoodParser = RedWoodParser()
        model = KNeighborsClassifier(n_neighbors = 3,)
        data_predict_org = Data_Predict_Organizer()

        sp_model = SoccerPredictModel(model, redwoodParser, data_manger, 'England', data_predict_org)
        sp_model.train(7, 0.1)

        test(sp_model, 6, self.english_csv_file)

    def test_grid_search_english_model_xgboost(self):
        # general things:
        db_connector = mongo_API()
        data_manger = DataManger(db_connector)
        redwoodParser = RedWoodParser()
        data_predict_org = Data_Predict_Organizer()

        # model params
        max_depths = range(1, 22, 1)
        learning_rates = [x/20 for x in range(1, 21)]
        n_estimators = range(50, 400, 50)
        objectives = ["binary:logistic","reg:linear", "reg:logistic", "binary:logistic", "binary:logitraw", "count:poisson", "multi:softmax", "multi:softprob", "rank:pairwise"]
        boosters = ['gbtree', 'gblinear']
        gammas = [x/20 for x in range(0, 105, 5)]
        min_child_weights = [x/2 for x in range(0,21)]
        max_delta_steps = range(0, 10, 1)
        subsamples = [x/20 for x in range(0, 21)]
        colsample_bytrees = [x/20 for x in range(0, 21)]
        #reg_alpha = 0
        #reg_lambda = 1
        base_score = [x/20 for x in range(1, 21)]
        num_of_games = range(0, 15)

        test_results = []

        for md in max_depths:
            for lr in learning_rates:
                for ne in n_estimators:
                    for obj in objectives:
                        for booster in boosters:
                            for g in gammas:
                                for min_child_w in min_child_weights:
                                    for max_delta_step in max_delta_steps:
                                        for sub_sample in subsamples:
                                            for cb in colsample_bytrees:
                                                for bs in base_score:
                                                    model = XGBClassifier(max_depth=md, learning_rate=lr, n_estimators=ne, objective=obj, booster=booster, gamma=g, min_child_weight=min_child_w, max_delta_step=max_delta_step, subsample=sub_sample, colsample_bytree=cb, base_score=bs)
                                                    sp_model = SoccerPredictModel(model, redwoodParser, data_manger, 'England', data_predict_org)
                                                    sp_model.train(7, 0.1)
                                                    for num in num_of_games:
                                                        res = test(sp_model, num, self.english_csv_file)
                                                        test_results.append({'max_depth':md, 'learning_rate':lr, 'n_estimators':ne, 'objective':obj, 'booster':booster, 'gamma':g, 'min_child_weight':min_child_w, 'max_delta_step':max_delta_step, 'subsample':sub_sample, 'colsample_bytree':cb, 'base_score':bs, 'res':res})

        print(test_results)
        with open(self.english_xg_result) as res_file:
            # save fields names
            for k,v in test_results[0].items():
                res_file.write(k + ',')

            for result in test_results:
                for k,v in result.items():
                    res_file.write(v + ',')







    def test_basic_model_spain(self):
        db_connector = mongo_API()
        data_manger = DataManger(db_connector)
        redwoodParser = RedWoodParser()
        model = XGBClassifier(max_depth=4, booster='gblinear')
        data_predict_org = Data_Predict_Organizer()

        sp_model_spain = SoccerPredictModel(model, redwoodParser, data_manger, 'Spain', data_predict_org)
        sp_model_spain.train(7, 0.1)

        test(sp_model_spain, 3, self.spain_csv_file)


    def test_basic_model_germany(self):
        db_connector = mongo_API()
        data_manger = DataManger(db_connector)
        redwoodParser = RedWoodParser()
        model = XGBClassifier(max_depth=4, booster='gblinear')
        data_predict_org = Data_Predict_Organizer()

        sp_model_germany = SoccerPredictModel(model, redwoodParser, data_manger, 'Germany', data_predict_org)
        sp_model_germany.train(7, 0.1)

        test(sp_model_germany, 3, self.germany_csv_file)

    def test_basic_model_italy(self):
        db_connector = mongo_API()
        data_manger = DataManger(db_connector)
        redwoodParser = RedWoodParser()
        model = XGBClassifier(max_depth=3, booster='gblinear')
        data_predict_org = Data_Predict_Organizer()

        sp_model_italy = SoccerPredictModel(model, redwoodParser, data_manger, 'Italy', data_predict_org)
        sp_model_italy.train(7, 0.1)

        test(sp_model_italy, 7, self.italy_csv_file)





if __name__ == '__main__':
    unittest.main()
