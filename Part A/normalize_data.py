import json
import os
import time
from datetime import datetime


def main():
    root = 'fitbit_data/'
    json_dict = get_jsons(root)
    sorted_dict = sort_json(json_dict)

    write_json(sorted_dict)


def get_jsons(root):
    json_dict = {}
    for person in os.scandir(root):
        json_dict[person.name] = {}
        for data in os.scandir(person):
            json_dict[person.name][data.name] = []
            for file in os.scandir(data):
                with open(file, "r") as read_file:
                    json_dict[person.name][data.name].append(json.load(read_file))
    return json_dict


def sort_json(json_dict):
    new_dict = {}
    for person in json_dict.keys():
        new_dict[person] = {}
        for data in json_dict[person].keys():
            for file in json_dict[person][data]:
                for point in file:
                    items = list(point.items())
                    if items[0][1] not in new_dict[person].keys():
                        new_dict[person][items[0][1]] = {}
                        new_dict[person][items[0][1]]["datetime"] = datetime.strptime(items[0][1], '%m/%d/%y %H:%M:%S').isoformat()
                        new_dict[person][items[0][1]][person] = {}
                    new_dict[person][items[0][1]][person][data] = float(items[1][1])
    return new_dict


def write_json(json_dict):
    if not os.path.exists("data/"):
        os.makedirs("data/")
    with open("data/data.json", "w"):
        pass

    for person in json_dict.keys():
        for timestamp in json_dict[person].keys():
            with open("data/data.json", "a") as json_file:
                json.dump(dict[person][timestamp], json_file, indent=2)


if __name__ == "__main__":
    main()
