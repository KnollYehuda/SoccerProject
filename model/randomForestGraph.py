import os
from sklearn.tree import export_graphviz
import six
import pydot
from sklearn import tree
from DataParser.RedWoodParser import RedWoodParser
import json
from joblib import dump, load

redwood_parser = RedWoodParser()

path_prefix = '/Users/meornbru/PycharmProjects/SoccerProject/model/JobLibModels2/England/XGBClassifier'
game_json_path = '/Users/meornbru/PycharmProjects/SoccerProject/Redwood/Germany_18-19/Collman_TeamStatistics_English_352_809_133026.json'
json_game = {}
features_vector = []

with open(game_json_path) as game :
    json_game = redwood_parser.parse_json_to_filterd_json(json.load(game))
    features_vector = redwood_parser.get_game_features_vector(json_game)

dotfile = six.StringIO()
i_tree = 0
estimator = load('/Users/meornbru/PycharmProjects/SoccerProject/model/JobLibModels/Spain/RandomForestClassifier/sp_model_0,49645390070921985.joblib')

col = features_vector

for tree_in_forest in estimator.estimators_:
    export_graphviz(tree_in_forest,out_file='tree.dot',
    feature_names=col,
    filled=True,
    rounded=True)
    (graph,) = pydot.graph_from_dot_file('tree.dot')
    name = 'tree' + str(i_tree)
    graph.write_png(name+  '.png')
    os.system('dot -Tpng tree.dot -o tree.png')
    i_tree +=1