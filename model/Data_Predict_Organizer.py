from datetime import datetime

from Logger import main as log_class

"""Data Predict Organizer job is to take data from the DB and organize it to vector that the model can use to predict_proba.
    the organizer can change the number of game or the number of params we use to predict_proba. """

class Data_Predict_Organizer:
    """basic class for Data Predict Organizer any other Data Predict Organizer need to inherit from this class and implemnt the method"""

    # def __init__(self):
    #     # self.logger = log_class.setup_logger('SoccerPredictModel.log')

    def orgnaize_json(self, home_team_name, away_team_name, data, num_of_last_games=0):
        home_team_vector = []
        away_team_vector = []

        for game in data:
            if game['HomeTeamName'] == home_team_name:
                home_team_vector.append(game)
            if game['AwayTeamName'] == away_team_name:
                away_team_vector.append(game)

        #self.logger.info('home team vector size : {}, away team vector size : {}'.format(len(home_team_vector),len(away_team_vector)))

        if num_of_last_games == 0 or len(home_team_vector) < num_of_last_games or len(away_team_vector) < num_of_last_games:
            num_of_last_games = min(len(home_team_vector), len(away_team_vector))
            #self.logger.info('orgnaize_json, change the number of last games to : {}'.format(num_of_last_games))

        avg_game_json = self.parse_to_average_json_for_predict(home_team_vector[-num_of_last_games:],away_team_vector[-num_of_last_games:])

        return avg_game_json

    def parse_to_average_json_for_predict(self, home_team_game_list, away_team_game_list):
        final_json = {}
        general_game_data = ('TotalMatchTime', 'FirstHalfMatchTime', 'SecondHalfMatchTime')

        final_json['Date'] = datetime.today().strftime('%Y-%m-%d')
        final_json['TournamentName'] = home_team_game_list[0]['TournamentName']
        # TODO : change this to current season and round
        final_json['SeasonName'] = home_team_game_list[0]['SeasonName']
        final_json['RoundId'] = home_team_game_list[0]['RoundId']

        final_json['HomeTeamName'] = home_team_game_list[0]['HomeTeamName']
        final_json['AwayTeamName'] = away_team_game_list[0]['AwayTeamName']

        #set all the home team data
        for game in home_team_game_list:
            for key, val in game.items():
                if key.startswith('HomeTeam') or key in general_game_data:
                    if key != 'HomeTeamName':
                        counter = final_json.get(key, 0)
                        counter += val
                        final_json[key] = counter

        # set all the home team data
        for game in away_team_game_list:
            for key, val in game.items():
                if key.startswith('AwayTeam') or key in general_game_data:
                    if key != 'AwayTeamName':
                        counter = final_json.get(key, 0)
                        counter += val
                        final_json[key] = counter

        for key, val in final_json.items():
            if type(val) is not str and key is not 'RoundId':
                if key in general_game_data:
                    final_json[key] = val / (len(home_team_game_list) * 2)
                else:
                    final_json[key] = val / len(home_team_game_list)

        #print('parse_to_average_json_for_predict : {}'.format(final_json))

        return final_json


