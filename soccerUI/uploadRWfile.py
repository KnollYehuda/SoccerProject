from DataParser import RedWoodParser as dataparser
from soccerUI.HttpHandlers.mongoDB_API import mongo_API as mgd
import json

# get JSON season file
# for each game => upload to DB with relevant League and Season


def upload_to_db():
    file_path = input("Enter Json file path: ")
    print(file_path)
    season_file = json.load(open(file_path, 'r'))
    for game in season_file['Season']:
        print(game)
        game_to_db = dataparser.parse(game)
        print(game_to_db)
        mgd.insert_json_object(game_to_db)


if __name__ == '__main__':
    upload_to_db()

