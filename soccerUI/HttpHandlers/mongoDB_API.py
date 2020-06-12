import json
from pymongo import MongoClient
import Logger.main as logger

class mongo_API:
    """ this is singleton class
     the class connect to the mongoDB
     the default ip is localhost and the default port is 27017 """
    __instance = None
    __mongo_url = 'mongodb://admin:admin123@ds151805.mlab.com:51805/soccer_db'

    @staticmethod
    def get_instance(self, url = __mongo_url):  # FIXME : replace with constants
        """ Static access method.
        default ip is : 'localhost' and default port is : 27017 """
        if mongo_API.__instance is None:
            mongo_API.instance = mongo_API(url)
        return mongo_API.instance

    def __init__(self, url = __mongo_url) -> object:  # FIXME : replace with constants
        """ default ip is : 'localhost' and default port is : 27017 """
        print("monogo init")
        if mongo_API.__instance is None:
            # self.logger = logger.setup_logger('mongoDbLogger.log')
            self.url = url
            self.client = MongoClient(url)
            mongo_API.__instance = self

    def close_connection(self):
        if mongo_API.__instance is not None:
            mongo_API.__instance.client.close()
            mongo_API.__instance = None

    def insert_json_file(self, json_path, db_name='default', collection='default'):
        with open(json_path) as f:
            json_object = json.load(f)
            return self.insert_json_object(json_object, db_name, collection)

    def insert_json_object(self, json_object, db_name='default', collection='default'):
        db = self.__instance.client[db_name]
        collection = db[collection]
        result =  collection.insert(json_object)
        return result

    def get_collection(self, db_name, collection, filter=None):
        """ db_name should be results if you look for results from games.
         the collection should be the name of the league and the season example "England Premier League18/19"
         key_val is optional, you can look for specific things by key val dict.
         if you leave this field empty you get the whole collection.
         return cursor object."""

        db = self.__instance.client[db_name]
        collection = db[collection]
        res = collection.find(filter=filter)
        return res



#mongoApi = mongo_API()
# mongoApi.insert_json_file(parser.parse('C:\\Users\\Snir\\PycharmProjects\\SoccerProject\\DataParser\\PL1.json'))

#mongoApi.insert_json_file('/Users/meornbru/PycharmProjects/SoccerProject/DataParser/testJson.json', 'testDB', 'testCollection')#
#c = mongoApi.get_collection('soccer_db', 'Italy_14-15')
#for line in c:
#    print(line)
#"HomeTeamName" : ["home team test name"],
#"AwayTeamName" : ["away team test name"],
#"homeTeamSecondHalfTestGoals" : 3,
#"AwayTeamFirstHalfSubTest" : 7,
#"RoundIdTest" : 12

# print(mongoAPI.export_json('soccerResultsDB', 'PL'))
