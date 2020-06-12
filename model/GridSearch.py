from soccerUI.HttpHandlers.mongoDB_API import mongo_API
from DataParser.RedWoodParser import RedWoodParser
import csv
import numpy
from model.dataManger import DataManger, FileDataManger
from model.soccer_predict_model import SoccerPredictModel
from model.Data_Predict_Organizer import Data_Predict_Organizer

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
#from lightgbm import LGBMClassifier
# from catboost import CatBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import csv


########### Utils ###########
def get_winner_from_char(char):
    if char == 'D':
        return 0
    if char == 'H':
        return 1
    if char == 'A':
        return 2

########### General USAGE ###########
db_connector = mongo_API()
data_manger = FileDataManger(db_connector)
redwoodParser = RedWoodParser()
data_predict_org = Data_Predict_Organizer()
fake_model = XGBClassifier()

########### Train Data ###########
def get_train_data(sp_model):
    train_data_json_list = sp_model.set_data_after_parse()

    train_data_vector = []
    train_winners_vector = []

    for game in train_data_json_list:
        game_vector, winner = redwoodParser.get_game_vector(game)
        train_data_vector.append(game_vector)
        train_winners_vector.append(winner)

    return train_data_vector, train_winners_vector


########### Test Data ###########
def get_test_data(csv_file_path, data, num_of_last_games):
    test_vector_list = []
    test_winner_list = []

    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        success = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                home_team = row[1]
                away_team = row[2]
                winner_char = row[5]

                avg_json = data_predict_org.orgnaize_json(home_team, away_team, data, num_of_last_games)
                game_vector = redwoodParser.get_game_vector(avg_json)[0]
                test_vector_list.append(numpy.array(game_vector))
                test_winner_list.append(get_winner_from_char(winner_char))

    return test_vector_list, test_winner_list


def test_model(model, league, params, csv_test_file_path, num_of_last_games_list, cv=5):
    sp_model = SoccerPredictModel(fake_model, redwoodParser, data_manger, league, data_predict_org)
    grid_search = GridSearchCV(estimator=model, param_grid=params, n_jobs=-1, cv=cv)

    # get the train data and train the model
    train_data_vector, train_winners_vector = get_train_data(sp_model)
    print('train the model : ')
    grid_search.fit(numpy.array(train_data_vector), numpy.array(train_winners_vector))

    print('grid_search : {}'.format(grid_search))
    print('grid_search, best_estimator_ : {}'.format(grid_search.best_estimator_))
    print('grid_search, best_params_ : {}'.format(grid_search.best_params_))
    print('grid_search, best_score_ : {}'.format(grid_search.best_score_))

    result = []

    for num in num_of_last_games_list:
        # get the test data
        test_vector_list, test_winner_list = get_test_data(csv_test_file_path, sp_model.get_data_after_parse(), num)

        # test the model and get the score
        score = grid_search.score(numpy.array(test_vector_list), numpy.array(test_winner_list))
        print('score for num of last games: {} score : {}'.format(num, score))

        result.append([num, score])
    print('grid_search.cv_results_ : {}'.format(grid_search.cv_results_))
    return result, grid_search.best_estimator_


def write_result_to_csv(league, model, model_name, result_to_save):
    csv_list = [['booster', 'learning_rate', 'max_depth', 'n_estimators', 'objective', 'num_of_last_games', 'score']]

    for res in result_to_save:
        csv_list.append([model.booster, model.learning_rate, model.max_depth, model.n_estimators, model.objective,res[0], res[1]])

    with open('{}_{}_test_result.csv'.format(league, model_name), 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(csv_list)


model = XGBClassifier()
test_league = 'England'
#parameters = {'n_estimators': [100, 150, 200, 250, 300, 350], 'max_depth':[3, 4, 5, 6, 7, 8, 9, 10],'booster': ['gblinear','gbtree'], 'objective':['reg:linear', 'multi:softprob'], 'learning_rate':[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] }
parameters = { 'max_depth':[3, 4, 5],'booster': ['gblinear','gbtree'], 'objective':['reg:linear', 'multi:softprob'] }
english_csv_file = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/english_season-1819_csv.csv'
num_of_last_games = range(1, 11)
res = test_model(model, test_league, parameters, english_csv_file, num_of_last_games, cv=10)
redwoodParser.set_ignore_list(['HomeTeamFullTimeGoal', 'AwayTeamFullTimeGoal', 'Date', 'TournamentName', 'SeasonName', 'RoundId', 'HomeTeamName', 'AwayTeamName'])
write_result_to_csv(test_league, res[1], 'XGBClassifier', res[0])


print('res : {}'.format(res[0]))



