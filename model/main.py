from soccerUI.HttpHandlers.mongoDB_API import mongo_API
from DataParser.RedWoodParser import RedWoodParser
import csv
import numpy
from model.dataManger import DataManger
from model.soccer_predict_model import SoccerPredictModel
from model.Data_Predict_Organizer import Data_Predict_Organizer

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
#from lightgbm import LGBMClassifier
# from catboost import CatBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

db_connector = mongo_API()
data_manger = DataManger(db_connector)
redwoodParser = RedWoodParser()
model = XGBClassifier(max_depth=3, booster='gblinear')
#model = RandomForestClassifier()
#model = CatBoostClassifier()
#model = LGBMClassifier()
#model = KNeighborsClassifier()
data_predict_org = Data_Predict_Organizer()

sp_model_english = SoccerPredictModel(model, redwoodParser, data_manger, 'England', data_predict_org)
sp_model_english.train(7, 0.1)

number_of_last_game = 6

res_eng_12_4_19_1 = sp_model_english.predict_proba('Leicester', 'Newcastle', number_of_last_game)

res_eng_13_4_19_1 = sp_model_english.predict_proba('Tottenham', 'Huddersfield', number_of_last_game)
res_eng_13_4_19_2 = sp_model_english.predict_proba('Burnley', 'Cardiff', number_of_last_game)
res_eng_13_4_19_3 = sp_model_english.predict_proba('Brighton', 'Bournemouth', number_of_last_game)
res_eng_13_4_19_4 = sp_model_english.predict_proba('Fulham', 'Everton', number_of_last_game)
res_eng_13_4_19_5 = sp_model_english.predict_proba('Southampton', 'Wolves', number_of_last_game)
res_eng_13_4_19_6 = sp_model_english.predict_proba('Manchester United', 'West Ham', number_of_last_game)

res_eng_14_4_19_1 = sp_model_english.predict_proba('Palace', 'Manchester City', number_of_last_game)
res_eng_14_4_19_2 = sp_model_english.predict_proba('Liverpool', 'Chelsea', number_of_last_game)

res_eng_17_4_19_1 = sp_model_english.predict_proba('Manchester City', 'Tottenham', number_of_last_game)

res_eng_20_4_19_1 = sp_model_english.predict_proba('Bournemouth', 'Fulham', number_of_last_game)
res_eng_20_4_19_2 = sp_model_english.predict_proba('Huddersfield', 'Watford', number_of_last_game)
res_eng_20_4_19_3 = sp_model_english.predict_proba('West Ham', 'Leicester', number_of_last_game)
res_eng_20_4_19_4 = sp_model_english.predict_proba('Wolves', 'Brighton', number_of_last_game)
res_eng_20_4_19_5 = sp_model_english.predict_proba('Newcastle', 'Southampton', number_of_last_game)

res_eng_21_4_19_1 = sp_model_english.predict_proba('Everton', 'Manchester United', number_of_last_game)
res_eng_21_4_19_2 = sp_model_english.predict_proba('Cardiff', 'Liverpool', number_of_last_game)
res_eng_21_4_19_3 = sp_model_english.predict_proba('Arsenal', 'Palace', number_of_last_game)

res_eng_4_5_19_1 = sp_model_english.predict_proba('Cardiff', 'Palace', number_of_last_game)

res_eng_11_5_19_1 = sp_model_english.predict_proba('Palace', 'Bournemouth', number_of_last_game)
res_eng_11_5_19_2 = sp_model_english.predict_proba('Fulham', 'Newcastle', number_of_last_game)
res_eng_11_5_19_3 = sp_model_english.predict_proba('Watford', 'West Ham', number_of_last_game)

print('12/4/19 games : ')
print('Leicester vs Newcastle : {}'.format(res_eng_12_4_19_1))

print('13/4/19 games : ')
print('Tottenham vs Huddersfield : {}'.format(res_eng_13_4_19_1))
print('Burnley vs Cardiff : {}'.format(res_eng_13_4_19_2))
print('Brighton vs Bournemouth : {}'.format(res_eng_13_4_19_3))
print('Fulham vs Everton : {}'.format(res_eng_13_4_19_4))
print('Southampton vs Wolves : {}'.format(res_eng_13_4_19_5))
print('Manchester United vs West Ham : {}'.format(res_eng_13_4_19_6))

print('14/4/19 games : ')
print('Palace vs Manchester City : {}'.format(res_eng_14_4_19_1))
print('Liverpool vs Chelsea : {}'.format(res_eng_14_4_19_2))

print('17/4/19 games : ')
print('Manchester City vs Tottenham : {}'.format(res_eng_17_4_19_1))

print('20/4/19 games : ')
print('Manchester City vs Tottenham : {}'.format(res_eng_17_4_19_1))
print('Bournemouth vs Fulham : {}'.format(res_eng_20_4_19_1))
print('Huddersfield vs Watford : {}'.format(res_eng_20_4_19_2))
print('West Ham vs Leicester : {}'.format(res_eng_20_4_19_3))
print('Wolves vs Brighton : {}'.format(res_eng_20_4_19_4))
print('Newcastle vs Southampton : {}'.format(res_eng_20_4_19_5))

print('21/4/19 games : ')
print('Everton vs Manchester United : {}'.format(res_eng_21_4_19_1))
print('Cardiff vs Liverpool: {}'.format(res_eng_21_4_19_2))
print('Arsenal vs Palace: {}'.format(res_eng_21_4_19_3))

print('4/05/19 games : ')
print('Cardiff vs Palace: {}'.format(res_eng_4_5_19_1))

print('11/05/19 games : ')
print('Palace vs Bournemouth: {}'.format(res_eng_11_5_19_1))
print('Fulham vs Newcastle: {}'.format(res_eng_11_5_19_2))
print('Watford vs West Ham: {}'.format(res_eng_11_5_19_3))

model_spain = XGBClassifier(max_depth=3, booster='gblinear')
sp_model_spain = SoccerPredictModel(model_spain, redwoodParser, data_manger, 'Spain', data_predict_org)
sp_model_spain.train(3, 0.1)

res_spain_13_4_19_1 = sp_model_spain.predict_proba("Espanyol", "Alavés", 3)
res_spain_13_4_19_2 = sp_model_spain.predict_proba("Huesca", "Barcelona", 3)
res_spain_13_4_19_3 = sp_model_spain.predict_proba("Atletico Madrid", "Celta Vigo", 3)
res_spain_13_4_19_4 = sp_model_spain.predict_proba("Sevilla", "Betis", 3)

res_spain_14_4_19_1 = sp_model_spain.predict_proba("Bilbao", "Rayo", 3)
res_spain_14_4_19_2 = sp_model_spain.predict_proba("Real Sociedad", "Eibar", 3)
res_spain_14_4_19_3 = sp_model_spain.predict_proba("Girona", "Villareal", 3)
res_spain_14_4_19_4 = sp_model_spain.predict_proba("Valencia", "Levante", 3)
res_spain_14_4_19_5 = sp_model_spain.predict_proba("Valladolid", "Getafe", 3)

res_spain_20_4_19_1 = sp_model_spain.predict_proba("Celta Vigo", "Girona", 3)
res_spain_20_4_19_2 = sp_model_spain.predict_proba("Eibar", "Atletico Madrid", 3)
res_spain_20_4_19_3 = sp_model_spain.predict_proba("Rayo", "Huesca", 3)
res_spain_20_4_19_4 = sp_model_spain.predict_proba("Barcelona", "Real Sociedad", 3)

res_spain_21_4_19_1 = sp_model_spain.predict_proba("Levante", "Espanyol", 3)
res_spain_21_4_19_2 = sp_model_spain.predict_proba("Getafe", "Sevilla", 3)
res_spain_21_4_19_3 = sp_model_spain.predict_proba("Real Madrid", "Bilbao", 3)
res_spain_21_4_19_4 = sp_model_spain.predict_proba("Villareal", "Leganes", 3)
res_spain_21_4_19_5 = sp_model_spain.predict_proba("Betis", "Valencia", 3)

res_spain_11_5_19_1 = sp_model_spain.predict_proba('Rayo', 'Valladolid', 3)
res_spain_11_5_19_2 = sp_model_spain.predict_proba('Real Sociedad', 'Real Madrid', 3)
res_spain_11_5_19_3 = sp_model_spain.predict_proba('Bilbao', 'Celta Vigo', 3)
res_spain_11_5_19_4 = sp_model_spain.predict_proba('Girona', 'Levante', 3)
res_spain_11_5_19_5 = sp_model_spain.predict_proba('Villareal', 'Eibar', 3)
res_spain_11_5_19_6 = sp_model_spain.predict_proba('Leganes', 'Espanyol', 3)
res_spain_11_5_19_7 = sp_model_spain.predict_proba('Atletico Madrid', 'Sevilla', 3)

print('spain : ')
print('13/3/19 : ')
print("Espanyol vs Alavés : {}".format(res_spain_13_4_19_1))
print("Huesca vs Barcelona : {}".format(res_spain_13_4_19_2))
print("Atletico Madrid vs Celta Vigo : {}".format(res_spain_13_4_19_3))
print("Sevilla vs Betis : {}".format(res_spain_13_4_19_4))

print('14/3/19 : ')
print("Valladolid vs Getafe : {}".format(res_spain_14_4_19_5))
print("Bilbao vs Rayo : {}".format(res_spain_14_4_19_1))
print("Real Sociedad vs Eibar : {}".format(res_spain_14_4_19_2))
print("Girona vs Villareal : {}".format(res_spain_14_4_19_3))
print("Valencia vs Levante : {}".format(res_spain_14_4_19_4))

print('20/4/19 games : ')
print("Celta Vigo vs Girona : {}".format(res_spain_20_4_19_1))
print("Eibar vs Atletico Madrid : {}".format(res_spain_20_4_19_2))
print("Rayo vs Huesca : {}".format(res_spain_20_4_19_3))
print("Barcelona vs Real Sociedad : {}".format(res_spain_20_4_19_4))

print('21/4/19 games : ')
print("Levante vs Espanyol : {}".format(res_spain_21_4_19_1))
print("Getafe vs Sevilla : {}".format(res_spain_21_4_19_2))
print("Real Madrid vs Bilbao : {}".format(res_spain_21_4_19_3))
print("Villareal vs Real Madrid : {}".format(res_spain_21_4_19_4))
print("Betis vs Valencia : {}".format(res_spain_21_4_19_5))

print('11/05/19 games : ')
print("Rayo vs Valladolid : {}".format(res_spain_11_5_19_1))
print("Real Sociedad vs Valencia : {}".format(res_spain_11_5_19_2))
print("Bilbao vs Celta Vigo : {}".format(res_spain_11_5_19_3))
print("Girona vs Levante : {}".format(res_spain_11_5_19_4))
print("Villareal vs Eibar : {}".format(res_spain_11_5_19_5))
print("Leganes vs Espanyol : {}".format(res_spain_11_5_19_6))
print("Atletico Madrid vs Sevilla : {}".format(res_spain_11_5_19_7))

model_germany = XGBClassifier(max_depth=3, booster='gblinear')
sp_model_germany = SoccerPredictModel(model_germany, redwoodParser, data_manger, 'Germany', data_predict_org)
sp_model_germany.train(3, 0.1)

res_germany_12_4_19_1 = sp_model_germany.predict_proba("Nurnberg", "Schalke", 3)

res_germany_13_4_19_1 = sp_model_germany.predict_proba("Hannover", "Monchengladbach", 3)
res_germany_13_4_19_2 = sp_model_germany.predict_proba("Bremen", "Freiburg", 3)
res_germany_13_4_19_3 = sp_model_germany.predict_proba("RB Leipzig", "Wolfsburg", 3)
res_germany_13_4_19_4 = sp_model_germany.predict_proba("Stuttgart", "Leverkusen", 3)
res_germany_13_4_19_5 = sp_model_germany.predict_proba("Dortmund", "Mainz", 3)

res_germany_14_4_19_1 = sp_model_germany.predict_proba("Hoffenheim", "Hertha", 3)
res_germany_14_4_19_2 = sp_model_germany.predict_proba("Fortuna Dusseldorf", "Bayern", 3)
res_germany_14_4_19_3 = sp_model_germany.predict_proba("Frankfurt", "Augsburg", 3)

print('Germany : ')
print('12/3/19 : ')
print("Nurnberg vs Schalke : {}".format(res_germany_12_4_19_1))

print('13/3/19 : ')
print("Hannover vs Monchengladbach : {}".format(res_germany_13_4_19_1))
print("Bremen vs Freiburg : {}".format(res_germany_13_4_19_2))
print("RB Leipzig vs Wolfsburg : {}".format(res_germany_13_4_19_3))
print("Stuttgart vs Leverkusen : {}".format(res_germany_13_4_19_4))
print("Dortmund vs Mainz : {}".format(res_germany_13_4_19_5))

print('14/3/19 : ')
print("Hoffenheim vs Hertha : {}".format(res_germany_14_4_19_1))
print("Fortuna Dusseldorf vs Bayern : {}".format(res_germany_14_4_19_2))
print("Frankfurt vs Augsburg : {}".format(res_germany_14_4_19_3))


model_italy = XGBClassifier(max_depth=3, booster='gblinear')
sp_model_italy = SoccerPredictModel(model_italy, redwoodParser, data_manger, 'Italy', data_predict_org)
sp_model_italy.train(7, 0.1)

res_italy_08_4_19_1 = sp_model_italy.predict_proba("Bologna", "Chievo", 7)

res_italy_13_4_19_1 = sp_model_italy.predict_proba("SPAL 1907 Ferrara", "Juventus", 7)
res_italy_13_4_19_2 = sp_model_italy.predict_proba("Roma", "Udinese", 7)
res_italy_13_4_19_3 = sp_model_italy.predict_proba("Milan", "Lazio", 7)

res_italy_14_4_19_1 = sp_model_italy.predict_proba("Torino", "Cagliari", 7)
res_italy_14_4_19_2 = sp_model_italy.predict_proba("Sampdoria", "Genoa", 7)
res_italy_14_4_19_3 = sp_model_italy.predict_proba("Sassuolo", "Parma", 7)
res_italy_14_4_19_4 = sp_model_italy.predict_proba("Fiorentina", "Bologna", 7)
res_italy_14_4_19_5 = sp_model_italy.predict_proba("Chievo", "Napoli", 7)
res_italy_14_4_19_6 = sp_model_italy.predict_proba("Frosinone", "Inter", 7)

res_italy_20_4_19_1 = sp_model_italy.predict_proba("Parma", "Milan", 7)
res_italy_20_4_19_2 = sp_model_italy.predict_proba("Bologna", "Sampdoria", 7)
res_italy_20_4_19_3 = sp_model_italy.predict_proba("Cagliari", "Frosinone", 7)
res_italy_20_4_19_4 = sp_model_italy.predict_proba("Empoli", "SPAL 1907 Ferrara", 7)
res_italy_20_4_19_5 = sp_model_italy.predict_proba("Genoa", "Torino", 7)
res_italy_20_4_19_6 = sp_model_italy.predict_proba("Lazio", "Chievo", 7)
res_italy_20_4_19_7 = sp_model_italy.predict_proba("Udinese", "Sassuolo", 7)
res_italy_20_4_19_8 = sp_model_italy.predict_proba("Juventus", "Fiorentina", 7)
res_italy_20_4_19_9 = sp_model_italy.predict_proba("Inter", "Roma", 7)

print('italy : ')
print('08/3/19 : ')
print("Bologna vs Chievo : {}".format(res_italy_08_4_19_1))

print('13/3/19 : ')
print("SPAL 1907 Ferrara vs Juventus : {}".format(res_italy_13_4_19_1))
print("Roma vs Udinese : {}".format(res_italy_13_4_19_2))
print("Milan vs Lazio : {}".format(res_italy_13_4_19_3))

print('14/3/19 : ')
print("Torino vs Cagliari : {}".format(res_italy_14_4_19_1))
print("Sampdoria vs Genoa : {}".format(res_italy_14_4_19_2))
print("Sassuolo vs Parma : {}".format(res_italy_14_4_19_3))
print("Fiorentina vs Bologna : {}".format(res_italy_14_4_19_4))
print("Chievo vs Napoli : {}".format(res_italy_14_4_19_5))
print("Frosinone vs Inter : {}".format(res_italy_14_4_19_6))

print('20/4/19 games : ')
print("Parma vs Milan : {}".format(res_italy_20_4_19_1))
print("Bologna vs Sampdoria : {}".format(res_italy_20_4_19_2))
print("Cagliari vs Frosinone : {}".format(res_italy_20_4_19_3))
print("Empoli vs SPAL 1907 Ferrara : {}".format(res_italy_20_4_19_4))
print("Genoa vs Torino : {}".format(res_italy_20_4_19_5))
print("Lazio vs Chievo : {}".format(res_italy_20_4_19_6))
print("Udinese vs Sassuolo : {}".format(res_italy_20_4_19_7))
print("Juventus vs Fiorentina : {}".format(res_italy_20_4_19_8))
print("Inter vs Roma : {}".format(res_italy_20_4_19_9))


##########################################
#GridSearchCV england
##########################################
model = XGBClassifier()
parameters = {'n_estimators': [100, 150, 200, 250, 300, 350], 'max_depth':[3,4,5,6,7,8,9,10],'booster': ['gblinear','gbtree'], 'objective':['reg:linear', 'multi:softprob'] }
grid_search = GridSearchCV(estimator=model, param_grid=parameters, cv=10, n_jobs=-1)
sp_model_eng_gs = SoccerPredictModel(model, redwoodParser, data_manger, 'England', data_predict_org)
sp_model_eng_gs.train(7,0.1)

print("Best score: %0.3f" % grid_search.best_score_)
print("Best parameters set:")
best_parameters=grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print("\t%s: %r" % (param_name, best_parameters[param_name]))