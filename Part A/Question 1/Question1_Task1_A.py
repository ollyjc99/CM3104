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
            'p_1_steps': '$person_1_fitbit.steps',
            'p_2_steps': '$person_2_fitbit.steps',
            'day': {'$toInt': {'$substr': ['$datetime', 8, 2]}},
            'month': {'$toInt': {'$substr': ['$datetime', 5, 2]}}}
    },
    {
        '$match': {
            'month': {'$eq': 7}}
    },
    {
        '$group': {
            '_id': '$day',
            'person_1_steps': {'$sum': '$p_1_steps'},
            'person_2_steps': {'$sum': '$p_2_steps'}
        }
    },
    {
        '$sort': {'_id': 1}
    }
]

pprint(list(collection.aggregate(pipeline)))
