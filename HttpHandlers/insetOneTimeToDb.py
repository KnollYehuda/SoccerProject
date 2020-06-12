import pymongo
import json
import os

from pymongo import MongoClient

mongo_server_path = 'mongodb://admin:admin123@ds151805.mlab.com:51805/soccer_db'

client = MongoClient()

client = MongoClient()

db = client['soccer_db']

#change this to your local path
redwood = '/Users/meornbru/Desktop/Redwood'
for dir in os.listdir(redwood):
    if dir != '.DS_Store':
        for f in os.listdir(redwood + '/' + dir):
            if f != '.DS_Store':
                p = '{}/{}/{}'.format(redwood, dir, f)
                print(p)
                with open(p) as pt:
                    j = json.load(pt)
                    db[dir].insert_one(j)
