from xgboost import XGBClassifier
from soccerUI.HttpHandlers.mongoDB_API import mongo_API
from DataParser.RedWoodParser import RedWoodParser
import csv
import numpy
from model.dataManger import DataManger, FileDataManger
from model.soccer_predict_model import SoccerPredictModel
from model.Data_Predict_Organizer import Data_Predict_Organizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from joblib import dump

################### Parameters for model XGBClassifier ###################
n_estimators = 'n_estimators'
n_estimators_list = [100, 150, 200, 250, 300, 350]

max_depth = 'max_depth'
max_depth_list = [3, 4, 5, 6, 7, 8, 9, 10]

booster = 'booster'
booster_list = ['gblinear', 'gbtree']

objective = 'objective'
objective_list = ['reg:linear', 'multi:softprob']

learning_rate = 'learning_rate'
learning_rate_List = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

base_score = 'base_score'
base_score_list = [0.2, 0.3, 0.5, 0.6, 0.7]

num_of_last_games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

parameters_XGB = {n_estimators: n_estimators_list, max_depth: max_depth_list, booster: booster_list, objective: objective_list, learning_rate: learning_rate_List, base_score: base_score_list}
csv_list_XGB = [['estimator', 'm_depth', 'boost', 'obj', 'l_rate', 'b_score', 'n_games', 'acc']]

################### Parameters for model KNeighborsClassifier ###################
n_neighbors = 'n_neighbors'
n_neighbors_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

weights = 'weights'
weights_list = ['uniform', 'distance']

algorithm = 'algorithm'
algorithm_list = ['ball_tree', 'kd_tree', 'brute', 'auto']
p = 'p'
p_list = [1, 2, 3, 4, 5]

parameters_KNN = {n_neighbors: n_neighbors_list, weights: weights_list, algorithm: algorithm_list, p: p_list}
csv_list_KNN = [['n_neighbor', 'weight', 'algo', 'power', 'n_games', 'accurate_percentage']]

################### Parameters for model RandomForestClassifier ###################
n_estimators_RF = 'n_estimators'
n_estimators_rf_list = [7, 8, 9, 10, 11, 12, 13]

criterion = 'criterion'
criterion_list = ['gini', 'entropy']

bootstrap = 'bootstrap'
bootstrap_list = [True, False]

warm_start = 'warm_start'
warm_start_list = [True, False]

parameters_random_forest = {n_estimators_RF: n_estimators_rf_list, criterion: criterion_list, bootstrap: bootstrap_list, warm_start: warm_start_list}
csv_list_random_forest = [[n_estimators_RF, criterion, bootstrap, warm_start]]

################### Parameters for model LGBMClassifier ###################
boosting_type = 'boosting_type'
boosting_type_list = ['gbdt', 'dart', 'goss', 'rf']

objective_lgbm = 'objective'
objective_lgbm_list = ['lambdarank', 'regression', 'binary', 'multiclass']

parameters_LGBM = {boosting_type: boosting_type_list, learning_rate: learning_rate_List, n_estimators: n_estimators_list, objective_lgbm :objective_lgbm_list}
csv_list_LGBM = [[boosting_type, learning_rate, n_estimators, objective_lgbm, 'n_games', 'acc']]

################### Parameters for model CatBoostClassifier ###################
iterations = 'iterations'
iterations_list = [300, 400, 500, 600, 700]

depth_cat_boost = 'depth'
depth_cat_boost_list = [4, 5, 6, 7, 8]

boosting_type_cat_boost = 'boosting_type'
boosting_type_cat_boost_list = ['Ordered', 'Plain']

parameters_cat_boost = {iterations: iterations_list, learning_rate: learning_rate_List, depth_cat_boost: depth_cat_boost_list, boosting_type_cat_boost: boosting_type_cat_boost_list}
csv_list_cat_boost = [[iterations, learning_rate, depth_cat_boost, boosting_type_cat_boost, 'n_games', 'acc']]

################### Leagues ###################
england_leg = 'England'
spain_leg = 'Spain'
italy_leg = 'Italy'
germany_leg = 'Germany'

################### global params ###################
db_connector = mongo_API()
data_manger = FileDataManger(db_connector)
redwoodParser = RedWoodParser()
data_predict_org = Data_Predict_Organizer()
                                #<leaugeName>/<modelName>/sp_model_<accurate>.joblib
joblib_save_path = 'JobLibModels/{}/{}/sp_model_{}.joblib'
                                      #<leauge>/<modelName>/test_result.csv
csv_test_result_path = 'csvTestResult/{}/{}/test_result.csv'

home_team = 'HomeTeam'
away_team = 'AwayTeam'
real_winner = 'RealWinner'

################### test data utils ###################
english_csv_file_test_data = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/english_season-1819_csv.csv'
spain_csv_file_test_data = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/spain_season-1819_csv.csv'
italy_csv_file_test_data = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/italy_season-1819_csv.csv'
germany_csv_file_test_data = '/Users/meornbru/PycharmProjects/SoccerProject/model/test_files/germany_season-1819_csv.csv'

def get_winner_from_char(char):
    if char == 'D':
        return 0
    if char == 'H':
        return 1
    if char == 'A':
        return 2

def get_winner_from_prob(prob):
    h = prob['HomeTeam']
    d = prob['Draw']
    a = prob['AwayTeam']

    if h >= a and h >= d:
        return 1
    elif a >= h and a >= d:
        return 2
    elif d >= a and d >= h:
        return 0

    return -1

def get_test_data(path):
    games_list = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                game = {}
                game[home_team] = row[1]
                game[away_team] = row[2]
                game[real_winner] = get_winner_from_char(row[5])
                games_list.append(game)

    return games_list


################### grid search ###################
def search_XGBClassifier(league, test_data, silent_param=True):
    results = []
    current_max_accurate = 0
    final_most_acc = ''

    for estimator in parameters_XGB[n_estimators]:
        for m_depth in parameters_XGB[max_depth]:
            for boost in parameters_XGB[booster]:
                for obj in parameters_XGB[objective]:
                    for l_rate in parameters_XGB[learning_rate]:
                        for b_score in parameters_XGB[base_score]:
                            model = XGBClassifier(max_depth=m_depth, estimator=estimator, booster=boost, objective=obj, learning_rate=l_rate, silent=silent_param, base_score=b_score)
                            sp_model = SoccerPredictModel(model, redwoodParser, data_manger, league, data_predict_org)
                            sp_model.train(7, 0.1)

                            for n_games in num_of_last_games:
                                accurate_result = 0
                                for game in test_data:
                                    res__proba = sp_model.predict(game[home_team], game[away_team], n_games)
                                    res = get_winner_from_prob(res__proba)

                                    if res == -1:
                                        print('error -1')

                                    if res == game[real_winner]:
                                        accurate_result += 1

                                accurate_percentage = accurate_result / len(test_data)
                                results.append([estimator, m_depth, boost, obj, l_rate, b_score, n_games, accurate_percentage])
                                print('estimator : {}, m_depth : {}, boost : {}, obj : {}, l_rate : {}, b_score : {}, n_games : {}, acc : {} '.format(estimator, m_depth, boost, obj, l_rate, b_score, n_games, accurate_percentage))

                                if accurate_percentage > current_max_accurate:
                                    current_max_accurate = accurate_percentage
                                    final_most_acc = '{},{},{},{},{},{},{},{} '.format(estimator, m_depth, boost, obj, l_rate, b_score, n_games, accurate_percentage)
                                    print('save model : {}'.format(final_most_acc))
                                    dump(sp_model.get_model(), joblib_save_path.format(league, 'XGBClassifier', accurate_percentage.__str__().replace('.', ',')))

    return results, final_most_acc


def search_KNN(league, test_data):
    results = []
    current_max_accurate = 0
    final_most_acc = ''

    for n_neighbor in parameters_KNN[n_neighbors]:
        for weight in parameters_KNN[weights]:
            for algo in parameters_KNN[algorithm]:
                for power in parameters_KNN[p]:
                    model = KNeighborsClassifier(n_neighbors=n_neighbor, weights=weight, algorithm=algo, p=power)
                    sp_model_knn = SoccerPredictModel(model, redwoodParser, data_manger, league, data_predict_org)
                    sp_model_knn.train(7, 0.1)

                    for n_games in num_of_last_games:
                        accurate_result = 0
                        for game in test_data:
                            res__proba = sp_model_knn.predict(game[home_team], game[away_team], n_games)
                            res = get_winner_from_prob(res__proba)

                            if res == game[real_winner]:
                                accurate_result += 1

                        accurate_percentage = accurate_result / len(test_data)
                        results.append([n_neighbor, weight, algo, power, n_games, accurate_percentage])
                        print('n_neighbor : {}, weight : {}, algo : {}, power : {}, n_games : {}, acc : {} '.format(n_neighbor, weight, algo, power, n_games, accurate_percentage))

                        if accurate_percentage > current_max_accurate:
                            current_max_accurate = accurate_percentage
                            final_most_acc = '{},{},{},{},{},{}'.format(n_neighbor, weight, algo, power, n_games,accurate_percentage)
                            print('save model : {}'.format(final_most_acc))
                            dump(sp_model_knn.get_model(), joblib_save_path.format(league, 'KNeighborsClassifier',accurate_percentage.__str__().replace('.', ',')))

    return results, final_most_acc


def search_RF(league, test_data):
    results = []
    current_max_accurate = 0
    final_most_acc = ''

    for n_est in parameters_random_forest[n_estimators_RF]:
        for crit in parameters_random_forest[criterion]:
            for bootstrap_param in parameters_random_forest[bootstrap]:
                for warm_s in parameters_random_forest[warm_start]:
                    model = RandomForestClassifier(n_estimators=n_est, criterion=crit, bootstrap=bootstrap_param, warm_start=warm_s)
                    sp_model_rf = SoccerPredictModel(model, redwoodParser, data_manger, league, data_predict_org)
                    sp_model_rf.train(7, 0.1)

                    for n_games in num_of_last_games:
                        accurate_result = 0
                        for game in test_data:
                            res__proba = sp_model_rf.predict(game[home_team], game[away_team], n_games)
                            res = get_winner_from_prob(res__proba)

                            if res == game[real_winner]:
                                accurate_result += 1

                        accurate_percentage = accurate_result / len(test_data)
                        results.append([n_est, crit, bootstrap_param, warm_s, n_games, accurate_percentage])
                        print('n_est : {}, crit : {}, bootstrap_param : {}, warm_s : {}, n_games : {}, acc : {} '.format(n_est, crit, bootstrap_param, warm_s, n_games, accurate_percentage))

                        if accurate_percentage > current_max_accurate:
                            current_max_accurate = accurate_percentage
                            final_most_acc = '{},{},{},{},{},{}'.format(n_est, crit, bootstrap_param, warm_s, n_games, accurate_percentage)
                            print('save model : {}'.format(final_most_acc))
                            dump(sp_model_rf.get_model(), joblib_save_path.format(league, 'RandomForestClassifier',accurate_percentage.__str__().replace('.', ',')))

    return results, final_most_acc


def search_lgbm(league, test_data):
    results = []
    current_max_accurate = 0
    final_most_acc = ''

    for b_type in parameters_LGBM[boosting_type]:
        for l_rate in parameters_LGBM[learning_rate]:
            for n_est in parameters_LGBM[n_estimators]:
                for obj in parameters_LGBM[objective_lgbm]:
                    model = LGBMClassifier(boosting_type=b_type, learning_rate=l_rate, n_estimators=n_est, objective=obj)
                    sp_model_LGBM = SoccerPredictModel(model, redwoodParser, data_manger, league, data_predict_org)
                    sp_model_LGBM.train(7, 0.1)

                    for n_games in num_of_last_games:
                        accurate_result = 0
                        for game in test_data:
                            res__proba = sp_model_LGBM.predict(game[home_team], game[away_team], n_games)
                            res = get_winner_from_prob(res__proba)

                            if res == game[real_winner]:
                                accurate_result += 1

                        accurate_percentage = accurate_result / len(test_data)
                        results.append([b_type, l_rate, n_est, obj, n_games, accurate_percentage])
                        print('b_type : {}, l_rate : {}, n_est : {}, obj : {}, n_games : {}, acc : {} '.format(b_type, l_rate, n_est, obj, n_games, accurate_percentage))

                        if accurate_percentage > current_max_accurate:
                            current_max_accurate = accurate_percentage
                            final_most_acc = '{},{},{},{},{},{}'.format(b_type, l_rate, n_est, obj, n_games, accurate_percentage)
                            print('save model : {}'.format(final_most_acc))
                            dump(sp_model_LGBM.get_model(), joblib_save_path.format(league, 'LGBMClassifier',accurate_percentage.__str__().replace('.', ',')))

    return results, final_most_acc

def search_cat_boost(league, test_data):
    results = []
    current_max_accurate = 0
    final_most_acc = ''

    #[iterations, learning_rate, depth_cat_boost, boosting_type_cat_boost]

    for iter in parameters_cat_boost[iterations]:
        for l_rate in parameters_cat_boost[learning_rate]:
            for dep in parameters_cat_boost[depth_cat_boost]:
                for b_type in parameters_cat_boost[boosting_type_cat_boost]:
                    model = CatBoostClassifier(iterations=iter, learning_rate=l_rate, depth=dep, boosting_type=b_type, loss_function='MultiClass', silent=True)
                    sp_model_cat_boost = SoccerPredictModel(model, redwoodParser, data_manger, league, data_predict_org)
                    sp_model_cat_boost.train(7, 0.1)

                    for n_games in num_of_last_games:
                        accurate_result = 0
                        for game in test_data:
                            res__proba = sp_model_cat_boost.predict(game[home_team], game[away_team], n_games)
                            res = get_winner_from_prob(res__proba)

                            if res == game[real_winner]:
                                accurate_result += 1

                        accurate_percentage = accurate_result / len(test_data)
                        results.append([iter, l_rate, dep, b_type, n_games, accurate_percentage])
                        print('iter : {}, l_rate : {}, dep : {}, obj : {}, n_games : {}, acc : {} '.format(iter, l_rate, dep, b_type, n_games, accurate_percentage))

                        if accurate_percentage > current_max_accurate:
                            current_max_accurate = accurate_percentage
                            final_most_acc = '{},{},{},{},{},{}'.format(iter, l_rate, dep, b_type, n_games, accurate_percentage)
                            print('save model : {}'.format(final_most_acc))
                            dump(sp_model_cat_boost.get_model(), joblib_save_path.format(league, 'CatBoostClassifier',accurate_percentage.__str__().replace('.', ',')))

    return results, final_most_acc

def write_result_to_csv(csv_path, results, best_result, csv_list):
    csv_list.append(best_result.split(","))

    for res in results:
        csv_list.append(res)

    with open(csv_path, 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(csv_list)

################### main ###################
##### england #####
# print('###################################### start england ######################################')
# english_test_data = get_test_data(english_csv_file_test_data)
#
# print('################### start england XGBClassifier ###################')
# results_xgb_england, best_model_string_xgb_england = search_XGBClassifier(england_leg, english_test_data)
# write_result_to_csv(csv_test_result_path.format(england_leg, 'XGBClassifier'), results_xgb_england, best_model_string_xgb_england, csv_list_XGB.copy())
# print('################### finish england XGBClassifier ###################')
#
# print('################### start england KNeighborsClassifier ###################')
# results_knn_england, best_model_string_knn_england = search_KNN(england_leg, english_test_data)
# write_result_to_csv(csv_test_result_path.format(england_leg, 'KNeighborsClassifier'), results_knn_england, best_model_string_knn_england, csv_list_KNN.copy())
# print('################### finish england KNeighborsClassifier ###################')
#
# print('################### start england RandomForestClassifier ###################')
# results_rf_england, best_model_string_rf_england = search_RF(england_leg, english_test_data)
# write_result_to_csv(csv_test_result_path.format(england_leg, 'RandomForestClassifier'), results_rf_england, best_model_string_rf_england, csv_list_random_forest.copy())
# print('################### finish england RandomForestClassifier ###################')
#
# #print('################### start england LGBMClassifier ###################')
# #results_lgbm_england, best_model_string_lgbm_england = search_lgbm(england_leg, english_test_data)
# #write_result_to_csv(csv_test_result_path.format(england_leg, 'LGBMClassifier'), results_lgbm_england, best_model_string_lgbm_england, csv_list_LGBM.copy())
# #print('################### finish england LGBMClassifier ###################')
#
# print('################### start england CatBoostClassifier ###################')
# results_cat_boost_england, best_model_string_cat_boost_england = search_cat_boost(england_leg, english_test_data)
# write_result_to_csv(csv_test_result_path.format(england_leg, 'CatBoostClassifier'), results_cat_boost_england, best_model_string_cat_boost_england, csv_list_cat_boost.copy())
# print('################### finish england CatBoostClassifier ###################')
#
# print('###################################### finish england ######################################')
#
# ##### spain #####
# print('###################################### start spain ######################################')
# spain_test_data = get_test_data(spain_csv_file_test_data)
#
# print('################### start spain XGBClassifier ###################')
# results_xgb_spain, best_model_string_xgb_spain = search_XGBClassifier(spain_leg, spain_test_data)
# write_result_to_csv(csv_test_result_path.format(spain_leg, 'XGBClassifier'), results_xgb_spain, best_model_string_xgb_spain, csv_list_XGB.copy())
# print('################### finish spain XGBClassifier ###################')
#
# print('################### start spain KNeighborsClassifier ###################')
# results_knn_spain, best_model_string_knn_spain = search_KNN(spain_leg, spain_test_data)
# write_result_to_csv(csv_test_result_path.format(spain_leg, 'KNeighborsClassifier'), results_knn_spain, best_model_string_knn_spain, csv_list_KNN.copy())
# print('################### finish spain KNeighborsClassifier ###################')
#
# print('################### start spain RandomForestClassifier ###################')
# results_rf_spain, best_model_string_rf_spain = search_RF(spain_leg, spain_test_data)
# write_result_to_csv(csv_test_result_path.format(spain_leg, 'RandomForestClassifier'), results_rf_spain, best_model_string_rf_spain, csv_list_random_forest.copy())
# print('################### finish spain RandomForestClassifier ###################')
#
# #print('################### start spain LGBMClassifier ###################')
# #results_lgbm_spain, best_model_string_lgbm_spain = search_lgbm(spain_leg, spain_test_data)
# #write_result_to_csv(csv_test_result_path.format(spain_leg, 'LGBMClassifier'), results_lgbm_spain, best_model_string_lgbm_spain, csv_list_LGBM.copy())
# #print('################### finish spain LGBMClassifier ###################')
#
# print('################### start spain CatBoostClassifier ###################')
# results_cat_boost_spain, best_model_string_cat_boost_spain = search_cat_boost(spain_leg, spain_test_data)
# write_result_to_csv(csv_test_result_path.format(spain_leg, 'CatBoostClassifier'), results_cat_boost_spain, best_model_string_cat_boost_spain, csv_list_cat_boost.copy())
# print('################### finish spain CatBoostClassifier ###################')
#
# print('###################################### finish spain ######################################')
##### Italy #####
print('###################################### start italy ######################################')
italy_test_data = get_test_data(italy_csv_file_test_data)

print('################### start italy XGBClassifier ###################')
results_xgb_italy, best_model_string_xgb_italy = search_XGBClassifier(italy_leg, italy_test_data)
write_result_to_csv(csv_test_result_path.format(italy_leg, 'XGBClassifier'), results_xgb_italy, best_model_string_xgb_italy, csv_list_XGB.copy())
print('################### finish italy XGBClassifier ###################')

print('################### start italy KNeighborsClassifier ###################')
results_knn_italy, best_model_string_knn_italy = search_KNN(italy_leg, italy_test_data)
write_result_to_csv(csv_test_result_path.format(italy_leg, 'KNeighborsClassifier'), results_knn_italy, best_model_string_knn_italy, csv_list_KNN.copy())
print('################### finish italy KNeighborsClassifier ###################')

print('################### start italy RandomForestClassifier ###################')
results_rf_italy, best_model_string_rf_italy = search_RF(italy_leg, italy_test_data)
write_result_to_csv(csv_test_result_path.format(italy_leg, 'RandomForestClassifier'), results_rf_italy, best_model_string_rf_italy, csv_list_random_forest.copy())
print('################### finish italy RandomForestClassifier ###################')

#print('################### start italy LGBMClassifier ###################')
#results_lgbm_spain, best_model_string_lgbm_spain = search_lgbm(italy_leg, italy_test_data)
#write_result_to_csv(csv_test_result_path.format(italy_leg, 'LGBMClassifier'), results_lgbm_italy, best_model_string_lgbm_italy, csv_list_LGBM.copy())
#print('################### finish italy LGBMClassifier ###################')

print('################### start italy CatBoostClassifier ###################')
results_cat_boost_italy, best_model_string_cat_boost_italy = search_cat_boost(italy_leg, italy_test_data)
write_result_to_csv(csv_test_result_path.format(italy_leg, 'CatBoostClassifier'), results_cat_boost_italy, best_model_string_cat_boost_italy, csv_list_cat_boost.copy())
print('################### finish italy CatBoostClassifier ###################')

print('###################################### finish italy ######################################')
# ##### germany #####
# print('###################################### start germany ######################################')
# germany_test_data = get_test_data(germany_csv_file_test_data)
#
# print('################### start germany CatBoostClassifier ###################')
# results_cat_boost_germany, best_model_string_cat_boost_germany = search_cat_boost(germany_leg, germany_test_data)
# write_result_to_csv(csv_test_result_path.format(germany_leg, 'CatBoostClassifier'), results_cat_boost_germany, best_model_string_cat_boost_germany, csv_list_cat_boost.copy())
# print('################### finish germany CatBoostClassifier ###################')
#
# print('###################################### finish germany ######################################')