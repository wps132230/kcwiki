import json

dic = {}
f = open('miao', 'w')
f2 = open('shiptype', 'r')
for line in f2:
    first = line.split()[0]
    second = first.split('=')
    dic[int(second[0])] = second[1].encode('utf-8')

# with open('shipTypeMap.json', 'w') as fp:
#     json.dump(dic, fp)
print dic
