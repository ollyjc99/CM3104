import json
import os
import time


def main():
    root = 'fitbit_data/'
    json_dict = get_jsons(root)
    sorted_dict = sort_json(json_dict)


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


def sort_json(json):
    new_dict = {}
    for person in json.keys():
        new_dict[person] = {}
        for data in json[person].keys():
            for file in json[person][data]:
                print(file)


if __name__ == "__main__":
    main()
