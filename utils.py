import json

def nedb2json(nedbFilename, jsonFilename):
    jsonFile = open(jsonFilename, 'w')
    with open(nedbFilename, 'r') as nedbFile:
        jsonFile.write('[')
        for line in nedbFile:
            jsonFile.write(line[:-1] + ',\n')
        jsonFile.write(']')
    jsonFile.close()

def json2dic(json, masterKey):
    dic = {}
    for entry in json:
        dic[entry[masterKey]] = entry
    return dic

def jsonFile2dic(jsonFilename, masterKey):
    dic = {}
    with open(jsonFilename) as jsonFile:
        dic = json2dic(json.load(jsonFile), masterKey)
    return dic