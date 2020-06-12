from joblib import dump, load

from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier, LGBMModel
from catboost import CatBoostClassifier

from xgboost import plot_importance, plot_tree

from soccerUI.HttpHandlers.mongoDB_API import mongo_API
from DataParser.RedWoodParser import RedWoodParser
import json

import csv
import numpy
from model.dataManger import DataManger, FileDataManger
from model.soccer_predict_model import SoccerPredictModel
from model.Data_Predict_Organizer import Data_Predict_Organizer

from sklearn.feature_selection import RFECV
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import os

redwood_parser = RedWoodParser()

path_prefix = '/Users/meornbru/PycharmProjects/SoccerProject/model/JobLibModels2/England/XGBClassifier'
game_json_path = '/Users/meornbru/PycharmProjects/SoccerProject/Redwood/Germany_18-19/Collman_TeamStatistics_English_352_809_133026.json'
json_game = {}
features_vector = []

model = load('/Users/meornbru/PycharmProjects/SoccerProject/model/JobLibModels/England/RandomForestClassifier/sp_model_0,6.joblib')


def display_coef(values, features, model_name, clazz):
    ziped_h = zip(values, features)
    sorted_zip = sorted(ziped_h, key=lambda x: x[1])
    values2 = [x for x, y in sorted_zip[-5:]]
    features2 = [y for x, y in sorted_zip[-5:]]

    y_pos = numpy.arange(len(values2))
    plt.barh(y_pos, features2, align='center', alpha=0.5)
    plt.yticks(y_pos, values2)
    plt.ylabel('val')
    plt.title('model : {}, class : {}'.format(model_name, clazz))
    plt.show()

with open(game_json_path) as game :
    json_game = redwood_parser.parse_json_to_filterd_json(json.load(game))
    features_vector = redwood_parser.get_game_features_vector(json_game)

#model._Booster.feature_names = features_vector
plot_tree(model)
fig = plt.gcf()
fig.set_size_inches(150, 100)
fig.savefig('treePic/tree_{}.png'.format('england-60acc'))

# for file in os.listdir(path_prefix):
#     model = load(path_prefix + '/' + file)
#     if model.booster == 'gblinear':
#         coef = model.coef_
#
#         # display_coef(features_vector, coef[0], model.booster, 'draw')
#         # display_coef(features_vector, coef[1], model.booster, 'home')
#         # display_coef(features_vector, coef[2], model.booster, 'away')
#     elif model.booster == 'gbtree':
#         model._Booster.feature_names = features_vector
#         display_coef(features_vector, model.feature_importances_, model.booster, 'gbtree')
#
#         plot_tree(model)
#         fig = plt.gcf()
#         fig.set_size_inches(150, 100)
#         fig.savefig('treePic/tree_{}.png'.format(file))


