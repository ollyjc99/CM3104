import pymongo
from pprint import pprint

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fitbit_data"]
collection = db["data"]

pipeline = [
    {
        '$project': {
            'datetime': 1,
            'hour': {'$toInt': {'$substr': ['$datetime', 11, 2]}},
            'person_1_fitbit': 1,
            'person_2_fitbit': 1
        }
    }, {
        '$addFields': {
            'time_of_day': {
                '$cond': {
                    'if': {'$and': [{'$gte': ['$hour', 7]}, {'$lte': ['$hour', 12]}]},
                    'then': 'morning',
                    'else': {
                        '$cond': {
                            'if': {'$and': [{'$gte': ['$hour', 13]}, {'$lte': ['$hour', 19]}]},
                            'then': 'day',
                            'else': 'night'}}}}
        }
    },
    {
        '$project': {'hour': 0}
    },
    {
        '$out': 'new_data'
    }
]

pprint(list(collection.aggregate(pipeline)))
