import http.client
import json
import Logger.main as Logger
import urllib
import requests
from enum import Enum

class HttpHandler:
    """ this http handler know to send post requests to the server, mainly use for db
    this class is also singleton when you define the url and port is unmutable.
    """

    __instance = None

    class Constants(Enum):
        #db commands
        INSERT_TO_DB = "/db/insert/"
        GET_COLLECTION = "/db/getCollection/"

        #server consts
        DEFAULT_URL = "127.0.0.1"
        DEFAULT_PORT = '8000'


    def __init__(self, url=Constants.DEFAULT_URL, port=Constants.DEFAULT_PORT):# FIXME : replace with constants
        """this class define as singleton. the default url is localHost and the default port is 80"""
        if HttpHandler.__instance is None:
            # self.logger = Logger.setup_logger('HttpHandler.log')
            self.url = url
            self.port = port
            HttpHandler.__instance = self

    def insert_to_db_json_file(self, json_file_path):
        with open(json_file_path, 'r') as f:
            json_file = json.load(f)
            self.insert_to_db_json_object(json_file)

    def insert_to_db_json_object(self, json_object):
        self.__post(HttpHandler.Constants.INSERT_TO_DB, json_object)

    def get_collection(self, db_name, league, season, filter = None):
        request = {"db_name": db_name, "TournamentName": league, "SeasonName": season, "filter": filter}
        self.__post(HttpHandler.Constants.GET_COLLECTION, request)

    def __post(self, command, json_object):
        # self.logger.info("send post request to : {}".format(self.url.value + ':' + self.port.value + command.value))
        res = requests.post(self.url.value + ':' + self.port.value + command.value, data=json_object, json=json_object)
        for c in res:
            print(c)
        if res.status_code != 200:
          print("the http post request to url : {} with command : {} return with status : {} and reason {}".format(self.url, command.value, res.status_code, res.reason))
        else:
            print("the http post request to url : {} with command : {} return with status : {} and reason {}".format(self.url, command.value, res.status_code, res.reason))
        return res



httpHandler = HttpHandler()

response = httpHandler.get_collection("soccer_db", "Italy", "_14-15")
print(response)
