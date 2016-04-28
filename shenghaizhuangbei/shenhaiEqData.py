#coding=utf-8
import codecs

print '=================== start ======================'

fileIn = open('shenhaizhuangbei.txt','r')
fileOut = codecs.open('luaShenhaiEqData.txt','w','utf-8')

line = fileIn.readline()
eqDict = {}
num = 0

while(line):
    lineStr = line.strip().split('|')
    eqDict[lineStr[0].split('=')[1]] = {}
    for element in lineStr[1:]:
        eqDict[lineStr[0].split('=')[1]][element.split('=')[0]] = element.split('=')[1]
    line = fileIn.readline()
    num = num + 1 

eqList = sorted(eqDict.iteritems(), key = lambda d:d[0], reverse = False) 

## write lua script
string = 'local p = {}\np.equipDataTb = {\n'
for eq in eqList:
    string += '\t' + '["' + eq[0] + '"] = {\n'
    string += '\t'*2 + u'["日文名称"] = "' + unicode(eq[1]['日文装备名字'], 'utf-8') + '",\n'
    string += '\t'*2 + u'["中文名称"] = "' + unicode(eq[1]['中文装备名字'], 'utf-8') + '",\n'
    string += '\t'*2 + u'["类别"] = "' + unicode(eq[1]['装备类型'], 'utf-8')+ '",\n'
    string += '\t'*2 + u'["图标"] = "' + unicode(eq[1]['图标'], 'utf-8') + '",\n'
    string += '\t'*2 + u'["稀有度"] = "' + unicode(eq[1]['等级'], 'utf-8') + '",\n'
    string += '\t'*2 + u'["属性"] = {'
    if eq[1].has_key('火力'):
        string += u'["火力"] = "' + unicode(eq[1]['火力'], 'utf-8') + '",'
    if eq[1].has_key('雷装'):
        string += u'["雷装"] = "' + unicode(eq[1]['雷装'], 'utf-8') + '",'
    if eq[1].has_key('回避'):
        string += u'["回避"] = "' + unicode(eq[1]['回避'], 'utf-8') + '",'
    if eq[1].has_key('对空'):
        string += u'["对空"] = "' + unicode(eq[1]['对空'], 'utf-8') + '",'
    if eq[1].has_key('对潜'):
        string += u'["对潜"] = "' + unicode(eq[1]['对潜'], 'utf-8') + '",'
    if eq[1].has_key('射程'):
        string += u'["射程"] = "' + unicode(eq[1]['射程'], 'utf-8') + '",'
    if eq[1].has_key('索敌'):
        string += u'["索敌"] = "' + unicode(eq[1]['索敌'], 'utf-8') + '",'
    if eq[1].has_key('爆装'):
        string += u'["爆装"] = "' + unicode(eq[1]['爆装'], 'utf-8') + '",'
    if eq[1].has_key('命中'):
        string += u'["命中"] = "' + unicode(eq[1]['命中'], 'utf-8') + '",'
    string = string[:-1]
    string += '},\n'
    string += '\t'*2 + u'["备注"] = "' + unicode(eq[1]['备注'], 'utf-8') + '"\n'
    string += '\t},\n'
fileOut.write(string)
##
