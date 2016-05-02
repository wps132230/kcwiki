import json

def init_json_data():
    jsonDict = {'author' : '878083'}
    with open('data.json', 'w') as fp:
        json.dump(jsonDict, fp)

def add_new_json_data(key, value):
    with open('data.json') as fp:
        jsonDict = json.load(fp)

    jsonDict.update({key : value})

    with open('data.json', 'w') as fp:
        json.dump(jsonDict, fp)