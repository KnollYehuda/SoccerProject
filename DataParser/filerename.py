import json
import os

# dataset_folder = "..\\DataBase\\"

dataset_folder = '/Users/meornbru/Desktop/Redwood/'


def rename_single_file(directory, filename):
    if filename == '.DS_Store':
        return
    with open(directory + filename) as json_file:
        match = json.load(json_file)
        league = str(match['MatchMetaData']['TournamentName']).replace(' ', '_')
        season = 'S' + str(match['MatchMetaData']['SeasonName']).replace('/', '-')
        round_number = str(match['MatchMetaData']['RoundId'])
        # print(round_number)
        if 1 <= int(round_number) <= 9:
            round_number = 'R0' + str(match['MatchMetaData']['RoundId'])
        else:
            round_number = 'R' + str(match['MatchMetaData']['RoundId'])

        # FIXME
        # There are team names with special characters
        # e.g.: Alavֳ©s_vs_Deportivo-La-Coruֳ±a
        home_team = str(match['MatchMetaData']['HomeTeamFullName']).rstrip().replace(' ', '-')
        away_team = str(match['MatchMetaData']['AwayTeamFullName']).rstrip().replace(' ', '-')
        renamed_file_name = '{}{}'.format(('_'.join((league, season, round_number, home_team, 'vs', away_team))), '.json')

        os.rename('{}{}'.format(directory, filename), '{}{}'.format(directory, renamed_file_name))

        print('Source: {}{}\n'.format(directory, filename))
        print('Destination: {}{}\n'.format(directory, renamed_file_name))


def rename_all_files_in_directory(directory):
    for filename in os.listdir(directory):
        rename_single_file(directory, filename)


def rename_all_files_in_dataset(dataset_folder):
    for folder in os.listdir(dataset_folder):
        # print('Working on {}{}\\'.format(dataset_folder, folder))
        if folder != '.DS_Store':
            print('{}{}/'.format(dataset_folder, folder))
            rename_all_files_in_directory('{}{}/'.format(dataset_folder, folder))
            print('Done')


rename_all_files_in_dataset(dataset_folder)