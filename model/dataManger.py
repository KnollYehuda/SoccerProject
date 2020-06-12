import json
import os

class DataManger:
    """  data manger that knows to get data from Mongo server """

    db_connector = None

    def __init__(self, db_Connector):
        self.db_connector = db_Connector

    def get_season(self, db_name, season_name, filter=None):
        return self.db_connector.get_collection(db_name, season_name, filter=filter)


class FileDataManger(DataManger):
    """ data manger that knows to get data from files replace the file string """
    dir_path = '..\\Redwood'

    def get_season(self, db_name, season_name, filter=None):
        json_list = []

        for json_file in os.listdir(self.dir_path + '/' + season_name):
            with open(self.dir_path + '/' + season_name + '/' + json_file) as game_json_file:
                json_list.append(json.load(game_json_file))

        return json_list