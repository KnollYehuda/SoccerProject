import unittest
from soccerUI.HttpHandlers.mongoDB_API import mongo_API
import time

class MyTestCase(unittest.TestCase):
    mongoApi = mongo_API()
    print(mongoApi.get_ip_and_port())
    db_name='testDB'
    db_collection='testCollection'
    res_list = []
    special_key_val = {'HomeTeamName': ["home team test name"],
                       'AwayTeamName': ["away team test name"],
                       'homeTeamSecondHalfTestGoals': 3,
                       'AwayTeamFirstHalfSubTest': 7,
                       'RoundIdTest': 12}

    def test_insert_Json_File(self):
        self.res_list = self.mongoApi.insert_json_file('/Users/meornbru/PycharmProjects/SoccerProject/DataParser/testJson.json',
                                       db_name=self.db_name,
                                       collection=self.db_collection)
        assert len(self.res_list) == 5

    def test_get_collection_without_key_val(self):
        mongoApi = mongo_API()
        res_Cursor = mongoApi.get_collection(db_name=self.db_name, collection=self.db_collection)

        res = [json for json in res_Cursor]
        res_Cursor.close()

        for r in res:
            del r['_id']

        for index in range(len(self.res_list)):
            assert res[index] == self.res_list[index]

    def test_get_collection_with_key_val(self):
        mongoApi = mongo_API()
        res_Cursor = mongoApi.get_collection(db_name=self.db_name, collection=self.db_collection, filter=self.special_key_val)

        res = [json for json in res_Cursor]
        res_Cursor.close()

        for r in res:
            del r['_id']

        for index in range(len(self.res_list)):
            assert res[index] == self.res_list[index]

        for k, v in self.special_key_val.items():
            res_Cursor = mongoApi.get_collection(self.db_name, self.db_collection, {k: v})
            res = [json for json in res_Cursor]
            res_Cursor.close()
            assert res[0][k] == v


if __name__ == '__main__':
    unittest.main()