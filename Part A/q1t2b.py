import pymongo
from pprint import pprint

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fitbit_data"]
collection = db["data"]

pipeline = [
    {
        '$project': {
            '_id': 0,
            'datetime': 1,
            'p_1_calories': '$person_1_fitbit.calories',
            'p_2_calories': '$person_2_fitbit.calories',
            'day': {
                '$toInt': {
                    '$substr': [
                        '$datetime', 8, 2
                    ]
                }
            },
            'month': {
                '$toInt': {
                    '$substr': [
                        '$datetime', 5, 2
                    ]
                }
            }
        }
    }, {
        '$match': {
            'month': 7
        }
    }, {
        '$group': {
            '_id': '$month',
            'person_1_avg': {
                '$avg': '$p_1_calories'
            },
            'person_2_avg': {
                '$avg': '$p_2_calories'
            }
        }
    }
]

pprint(list(collection.aggregate(pipeline)))
