# RedWoodParser will filter RedWood's Json files into a new 2D-format Json file
# and will return the path to new file.

# from Logger import main as lg ..
import os
import json
import re


DATASET_FOLDER = '..\\DataBase\\alldataset\\'
PARSED_DATASET_FOLDER = '..\\DataBase\\parsed_dataset\\'


class RedWoodParser:

    ignore_list = ['HomeTeamFullTimeGoal', 'AwayTeamFullTimeGoal']

    def parse_one_file(self, season, match):
        single_match_path = '{}{}\\{}'.format(DATASET_FOLDER, season, match)

        final_json = {}
        try:
            json_file = json.load(open(single_match_path))

            return self.parse_json_to_filterd_json(json_file)

        except:
            print('Error with JSON file or directory.')
            # my_logger.error('Error with JSON file or directory.')

    def parse_one_season(self, season):
        season_folder_path = '{}{}\\'.format(DATASET_FOLDER, season)
        parsed_season_folder = '{}{}\\'.format(PARSED_DATASET_FOLDER, season)

        if not os.path.exists(parsed_season_folder):
            os.makedirs(parsed_season_folder)
            print("Directory ", parsed_season_folder, " was created\n")

        for match_file in os.listdir(season_folder_path):
            # print('Working on {}{}'.format(season_folder, match_file))
            self.parse_one_file(season, match_file)

    def parse_all_dataset(self, dataset_folder_path):
        if not os.path.exists(PARSED_DATASET_FOLDER):
            os.makedirs(PARSED_DATASET_FOLDER)
            print("Directory ", PARSED_DATASET_FOLDER, " was created\n")

        for season in os.listdir(dataset_folder_path):
            print('Working on {}{}'.format(dataset_folder_path, season))

            if season != '.DS_Store':
                # season_folder_path = '{}{}\\'.format(dataset_folder, season_folder)
                self.parse_one_season(season)
                # print('Done {}'.format(season))

    def parse_json_to_filterd_json(self, json_object):
        try:
            final_json = {}
            # General full time stats
            final_json['Date'] = json_object['MatchMetaData']['Kickoff']
            final_json['TournamentName'] = json_object['MatchMetaData']['TournamentName']
            final_json['SeasonName'] = json_object['MatchMetaData']['SeasonName']
            final_json['RoundId'] = json_object['MatchMetaData']['RoundId']
            final_json['HomeTeamName'] = json_object['MatchMetaData']['HomeTeamName']
            final_json['AwayTeamName'] = json_object['MatchMetaData']['AwayTeamName']
            final_json['TotalMatchTime'] = json_object['MatchMetaData']['MatchTime'] / 60
            final_json['FirstHalfMatchTime'] = json_object['MatchTime'][0]['Seconds'] / 60
            final_json['SecondHalfMatchTime'] = json_object['MatchTime'][1]['Seconds'] / 60

            # Home team's full time stats
            final_json['HomeTeamFullTimeAttackRatio'] = json_object['HomeTeam']['Summary']['AttackingEventsRatio']
            for event in json_object['HomeTeam']['Summary']['EventStatistics']:
                final_json['HomeTeamFullTime{}'.format(re.sub(r"([ -])", '', event['Name']))] = event['Count']

            # Home team's first half stats
            final_json['HomeTeamFirstHalfAttackRatio'] = json_object['HomeTeam']['Periods'][0]['AttackingEventsRatio']
            for event in json_object['HomeTeam']['Periods'][0]['EventStatistics']:
                final_json['HomeTeamFirstHalf{}'.format(re.sub(r"([ -])", '', event['Name']))] = event['Count']

            # Home team's second half stats
            final_json['HomeTeamSecondHalfAttackRatio'] = json_object['HomeTeam']['Periods'][1]['AttackingEventsRatio']
            for event in json_object['HomeTeam']['Periods'][1]['EventStatistics']:
                final_json['HomeTeamSecondHalf{}'.format(re.sub(r"([ -])", '', event['Name']))] = event['Count']

            ###

            # Away team's full time stats
            final_json['AwayTeamFullTimeAttackRatio'] = json_object['AwayTeam']['Summary']['AttackingEventsRatio']
            for event in json_object['AwayTeam']['Summary']['EventStatistics']:
                final_json['AwayTeamFullTime{}'.format(re.sub(r"([ -])", '', event['Name']))] = event['Count']

            # Away team's first half stats
            final_json['AwayTeamFirstHalfAttackRatio'] = json_object['AwayTeam']['Periods'][0]['AttackingEventsRatio']
            for event in json_object['AwayTeam']['Periods'][0]['EventStatistics']:
                final_json['AwayTeamFirstHalf{}'.format(re.sub(r"([ -])", '', event['Name']))] = event['Count']

            # Away team's second half stats
            final_json['AwayTeamSecondHalfAttackRatio'] = json_object['AwayTeam']['Periods'][1]['AttackingEventsRatio']
            for event in json_object['AwayTeam']['Periods'][1]['EventStatistics']:
                final_json['AwayTeamSecondHalf{}'.format(re.sub(r"([ -])", '', event['Name']))] = event['Count']


            ###

            # print(final_json)
            #parsed_match_file_path = '{}{}\\{}'.format(PARSED_DATASET_FOLDER, season, match)
            #print(parsed_match_file_path)

            #with open(parsed_match_file_path, 'w') as outfile:
                #json.dump(final_json, outfile)
                # my_logger.info(f'New file has been created : "2D_filtered_{get_name(path)}" in{date.datetime.now()}')

            # print('Done {}'.format(single_match_path))
            return final_json
        except:
            print('error with json : ', json_object)
            return None

    def parse_season_to_vector(self, json):
        ''' get season json and parse it to array of arryas, each array is game
        return the sesaon array of games and the winners vector'''
        season = []
        #first thing, parse the raw json to one dim json
        for game in json:
            result = self.parse_json_to_filterd_json(game)
            if result is not None:
                season.append(result)

        vector = []
        winners_vector = []


        for game in season:
            game_vector, winner = self.get_game_vector(game)
            winners_vector.append(winner)
            vector.append(game_vector)

        return vector, winners_vector

    def get_game_vector(self, json_game):
        """parse the json to vector of nums"""
        game_vector = []
        winner = self.get_winner(json_game)
        for key, val in json_game.items():
            if not self.ignore_list.__contains__(key):
                if type(val) is str:
                    # every string become a number
                    # TODO : need to change the hase to more claver thing
                    game_vector.append(val.__hash__())
                else:
                    game_vector.append(val)

        return game_vector, winner

    def get_game_features_vector(self, json_game):
        """parse the json to vector of nums"""
        game_vector = []
        for key, val in json_game.items():
            if not self.ignore_list.__contains__(key):
                game_vector.append(key)

        return game_vector

    def get_winner(self, json):
        '''Home team win retun 1
        Tie return 0
        Away team return 2'''
        home_team_goal = json['HomeTeamFullTimeGoal']
        away_team_goal = json['AwayTeamFullTimeGoal']

        if home_team_goal == away_team_goal:
            return 0
        if home_team_goal > away_team_goal:
            return 1
        if away_team_goal > home_team_goal:
            return 2

    def set_ignore_list(self, custom_ignore_list):
        for elem in custom_ignore_list:
            self.ignore_list.append(elem)


# rwp = RedWoodParser()
# rwp.parse_all_dataset(DATASET_FOLDER)
# my_logger = lg.setup_logger('json_log.log')