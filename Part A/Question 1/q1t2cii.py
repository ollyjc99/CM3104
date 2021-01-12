import pymongo
from pprint import pprint

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fitbit_data"]
collection = db["new_data"]

pipeline = [
    {
        '$project': {
            '_id': 1,
            'datetime': 1,
            'month': {'$toInt': {'$substr': ['$datetime', 5, 2]}},
            'p_1_s': '$person_1_fitbit.steps',
            'p_2_s': '$person_2_fitbit.steps',
            'time_of_day': 1
        }
    },
    {
        '$match': {
            'time_of_day': 'morning',
            'month': 8
        }
    },
    {
        '$group': {
            '_id': '$month',
            'person_1_steps': {'$sum': '$p_1_s'},
            'person_2_steps': {'$sum': '$p_2_s'}
        }
    },
    {
        '$project': {
            'most_steps': {'$cond': {'if': {'$gt': ['$person_1_steps', '$person_2_steps']},
                    'then': 'Person 1',
                    'else': 'Person 2'}},
            'steps': {'$max': ['$person_1_steps', '$person_2_steps']}
        }
    }
]

pprint(list(collection.aggregate(pipeline)))
