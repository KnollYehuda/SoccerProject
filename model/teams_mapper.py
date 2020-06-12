import os
import json

# ENGLAND_TEAMS = {'Liverpool', 'Leicester', 'Watford', 'Chelsea', 'Stoke', 'Swansea', 'Aston Villa', 'Southampton', 'West Ham', 'Cardiff', 'Burnley', 'Arsenal', 'Everton', 'Middlesbrough', 'Sunderland', 'Huddersfield', 'Manchester City', 'Fulham', 'Manchester United', 'Tottenham', 'West Brom', 'Palace', 'Wolves', 'Bournemouth', 'Brighton', 'Newcastle', 'Norwich', 'Hull'}
# SPAIN_TEAMS = {'Valencia', 'Levante', 'Deportivo', 'Granada', 'Celta Vigo', 'Getafe', 'Valladolid', 'Sevilla', 'Cordoba', 'Malaga', 'Elche', 'Betis', 'Rayo', 'Eibar', 'Bilbao', 'Real Sociedad', 'Alavֳ©s', 'Barcelona', 'Osasuna', 'Leganes', 'Villareal', 'Real Madrid', 'Atletico Madrid', 'Las Palmas', 'Gijon', 'Almeria', 'Girona', 'Espanyol'}
# ITALY_TEAMS = {'Torino', 'Crotone', 'Frosinone', 'Benevento Calcio', 'Juventus', 'Empoli', 'Parma', 'Chievo', 'Cagliari', 'Carpi', 'Genoa', 'SPAL 1907 Ferrara', 'Milan', 'Atalanta', 'Inter', 'Udinese', 'Fiorentina', 'Verona', 'Lazio', 'Napoli', 'Palermo', 'Sampdoria', 'Sassuolo', 'Cesena', 'Roma', 'Pescara', 'Bologna'}
# GERMANY_TEAMS = {'Hoffenheim', 'Schalke', 'Bremen', 'Hamburg', 'Hannover', 'Dortmund', 'Darmstadt', 'Monchengladbach', 'Bayern', 'Frankfurt', 'Fortuna Dusseldorf', 'Augsburg', 'Stuttgart', 'Leverkusen', 'RB Leipzig', 'Mainz', 'Koln', 'Wolfsburg', 'Freiburg', 'Wolves', 'Ingolstadt', 'Nurnberg', 'Hertha'}
#
#
# ENGLAND_KEYS = {'Liverpool', 'Leicester City', 'Watford', 'Chelsea', 'Stoke', 'Swansea', 'Aston Villa', 'Southampton', 'WestHam', 'Cardiff City', 'Burnley', 'Arsenal', 'Everton', 'Middlesbrough', 'Sunderland', 'Huddersfield', 'Manchester City', 'Fulham', 'Manchester United', 'Tottenham', 'West Brom', 'Palace', 'Wolves', 'Bournemouth', 'Brighton', 'Newcastle United', 'Norwich', 'Hull'}
# SPAIN_KEYS = {'Valencia','Levante','Deportivo','Granada', 'Celta de Vigo', 'Getafe', 'Valladolid', 'Sevilla', 'Cordoba', 'Malaga', 'Elche', 'Betis', 'Rayo Vallecano', 'Eibar', 'Bilbao', 'Real Sociedad', 'Alaves', 'Barcelona', 'Osasuna', 'Leganes', 'Villarreal', 'Real Madrid', 'Atletico Madrid', 'Las Palmas', 'Gijon', 'Almeria', 'Girona', 'Espanyol'}
# ITALY_KEYS = {'Torino', 'Crotone', 'Frosinone', 'Benevento Calcio', 'Juventus', 'Empoli', 'Parma', 'Chievo', 'Cagliari', 'Carpi', 'Genoa', 'SPAL', 'Milan', 'Atalanta', 'Inter', 'Udinese', 'Fiorentina', 'Verona', 'Lazio', 'Napoli', 'Palermo', 'Sampdoria', 'Sassuolo', 'Cesena', 'Roma', 'Pescara', 'Bologna'}
# GERMANY_KEYS = {'TSG 1899 Hoffenheim', 'Schalke 04', 'Werder Bremen', 'Hamburg', 'Hannover', 'Borussia Dortmund', 'Darmstadt', 'Borussia Monchengladbach', 'Bayern München', 'Eintracht Frankfurt', 'Fortuna Dusseldorf', 'Augsburg', 'Stuttgart', 'Bayer 04 Leverkusen', 'RB Leipzig', 'FSV Mainz 05', 'Koln', 'VfL Wolfsburg', 'Freiburg', 'Wolves', 'Ingolstadt', 'Nürnberg', 'Hertha Berlin'}


TEAM_DICT = {#Germany
             'Nürnberg': 'Nurnberg',
             'Hertha Berlin': 'Hertha',
             'Freiburg': 'Freiburg',
             'Ingolstadt': 'Ingolstadt',
             'FSV Mainz 05': 'Mainz',
             'Koln': 'Koln',
             'VfL Wolfsburg': 'Wolfsburg',
             'Stuttgart': 'Stuttgart',
             'Bayer 04 Leverkusen': 'Leverkusen',
             'RB Leipzig': 'RB Leipzig',
             'Bayern München': 'Bayern',
             'Eintracht Frankfurt': 'Frankfurt',
             'Fortuna Dusseldorf': 'Fortuna Dusseldorf',
             'Augsburg': 'Augsburg',
             'TSG 1899 Hoffenheim': 'Hoffenheim',
             'Schalke 04': 'Schalke',
             'Werder Bremen': 'Bremen',
             'Hamburg': 'Hamburg',
             'Hannover 96': 'Hannover',
             'Borussia Dortmund': 'Dortmund',
             'Darmstadt': 'Darmstadt',
             'Borussia Monchengladbach': 'Monchengladbach',
             #Italy
             'Pescara': 'Pescara',
             'Bologna': 'Bologna',
             'Sampdoria': 'Sampdoria',
             'Sassuolo': 'Sassuolo',
             'Cesena': 'Cesena',
             'Roma': 'Roma',
             'Lazio': 'Lazio',
             'Napoli': 'Napoli',
             'Palermo': 'Palermo',
             'Udinese': 'Udinese',
             'Fiorentina': 'Fiorentina',
             'Verona': 'Verona',
             'Milan': 'Milan',
             'Atalanta': 'Atalanta',
             'Inter': 'Inter',
             'Carpi': 'Carpi',
             'Genoa': 'Genoa',
             'SPAL': 'SPAL 1907 Ferrara',
             'Juventus': 'Juventus',
             'Empoli': 'Empoli',
             'Parma': 'Parma',
             'Chievo': 'Chievo',
             'Cagliari': 'Cagliari',
             'Torino': 'Torino',
             'Crotone': 'Crotone',
             'Frosinone':'Frosinone',
             'Benevento Calcio':'Benevento Calcio',
             #Spain
             'Las Palmas': 'Las Palmas',
             'Gijon': 'Gijon',
             'Girona': 'Girona',
             'Espanyol': 'Espanyol',
             'Almeria': 'Almeria',
             'Leganes': 'Leganes',
             'Villarreal': 'Villareal',
             'Real Madrid': 'Real Madrid',
             'Atletico Madrid': 'Atletico Madrid',
             'Alaves': 'Alavֳ©s',
             'Barcelona': 'Barcelona',
             'Osasuna': 'Osasuna',
             'Rayo Vallecano': 'Rayo',
             'Eibar': 'Eibar',
             'Athletic Club': 'Bilbao',
             'Real Sociedad': 'Real Sociedad',
             'Valencia': 'Valencia',
             'Levante': 'Levante',
             'Deportivo': 'Deportivo',
             'Granada': 'Granada',
             'Celta de Vigo': 'Celta Vigo',
             'Getafe': 'Getafe',
             'Real Valladolid': 'Valladolid',
             'Sevilla': 'Sevilla',
             'Cordoba': 'Cordoba',
             'Malaga': 'Malaga',
             'Elche': 'Elche',
             'Betis': 'Betis',
             'Huesca': 'Huesca',
             'Alaves': 'Alavés',
             #England
             'Liverpool': 'Liverpool',
             'Leicester City': 'Leicester',
             'Watford': 'Watford',
             'Chelsea': 'Chelsea',
             'Stoke': 'Stoke',
             'Swansea': 'Swansea',
             'Aston Villa': 'Aston Villa',
             'Southampton': 'Southampton',
             'WestHam': 'West Ham',
             'Cardiff City': 'Cardiff',
             'Burnley': 'Burnley',
             'Arsenal': 'Arsenal',
             'Everton': 'Everton',
             'Middlesbrough': 'Middlesbrough',
             'Sunderland': 'Sunderland',
             'Huddersfield': 'Huddersfield',
             'Manchester City': 'Manchester City',
             'Fulham': 'Fulham',
             'Manchester United': 'Manchester United',
             'Tottenham': 'Tottenham',
             'West Brom': 'West Brom',
             'Crystal Palace': 'Palace',
             'Wolves': 'Wolves',
             'Bournemouth': 'Bournemouth',
             'Brighton': 'Brighton',
             'Newcastle United': 'Newcastle',
             'Norwich': 'Norwich',
             'Hull': 'Hull'}


class TeamMapper:

    def map(self):
        return TEAM_DICT.get(self)



# spain_14_15 = 'D:\Desktop\Studies\Redwood\Germany_14-15'
# spain_15_16 = 'D:\Desktop\Studies\Redwood\Germany_15-16'
# spain_16_17 = 'D:\Desktop\Studies\Redwood\Germany_16-17'
# spain_17_18 = 'D:\Desktop\Studies\Redwood\Germany_17-18'
# spain_18_19 = 'D:\Desktop\Studies\Redwood\Germany_18-19'
#
# spain_path = [spain_14_15, spain_15_16, spain_16_17, spain_17_18, spain_18_19]
#
# for path in spain_path:
#     for filename in os.listdir(path):
#         # print(filename+',')
#         data = json.load(open(path+'\\'+filename))
#         # print(data['HomeTeam']['Name'])
#         if data['HomeTeam']['Name'] == 'Wolves':
#             print(data['HomeTeam']['FullName'])
#
# for value in ENGLAND_TEAMS:
#     for key in ENGLAND_KEYS:
#         TEAM_DICT[key] = value

#

# print(TeamMapper.Map('Alaves'))
