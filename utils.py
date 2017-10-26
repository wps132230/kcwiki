import json

def nedb2json(nedbFilename, jsonFilename):
    jsonFile = open(jsonFilename, 'w', encoding='utf_8')
    with open(nedbFilename, 'r', encoding='utf_8') as nedbFile:
        jsonFile.write('[\n')
        line = nedbFile.readline()
        while line:
            in_line = line.rstrip() + ','
            line = nedbFile.readline()
            if not line:
                in_line = in_line.rstrip(',')
            jsonFile.write(in_line + '\n')
        jsonFile.write(']')
    jsonFile.close()

def json2dic(json, masterKey):
    dic = {}
    for entry in json:
        if not entry[masterKey]:
            continue
        dic[entry[masterKey]] = entry
    return dic

def jsonFile2dic(jsonFilename, masterKey):
    dic = {}
    with open(jsonFilename, 'r', encoding='utf_8') as jsonFile:
        dic = json2dic(json.load(jsonFile), masterKey)
    return dic