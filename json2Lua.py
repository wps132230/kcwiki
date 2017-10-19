import requests
import json
import utils

# Directory name of db file
dbDicName = "db/"

# Map from wctf ship id to kcwiki ship id
stypeMap = {1:2, 2:3, 3:4, 4:5, 5:5,
            6:9, 7:9, 8:9, 9:7, 10:11,
            11:18, 12:16, 13:13, 14:13, 15:17,
            16:19, 17:20, 18:9, 19:2, 20:9,
            21:21, 22:None, 23:5, 24:16, 25:None,
            26:None, 27:None, 28:3, 29:22, 30:7,
            31:1, 32:7}
ship_namesuffix = {}
ship_classes = {}
entities = {}

def _getWikiId(wikiShipRemodel, prevOrNext):
    if prevOrNext not in wikiShipRemodel:
        return -1
    else:
        return wikiShips[wikiShipRemodel[prevOrNext]]['wiki_id']

# Generate one entry of the lua table
# from two sources: 'zh.kcwiki.org' and 'Who calls the fleet'.
def generate(wikiShip, wctfShip):
    luaTableEntryStr = ""
    luaTableEntryStr +=  '   ["{}"] = {{'.format(wikiShip['wiki_id']) + '\n'
    luaTableEntryStr +=  '       ["ID"] = {},'.format(wctfShip['id']) + '\n'
    luaTableEntryStr +=  '       ["图鉴号"] = {},'.format(wctfShip['no']) + '\n'
    luaTableEntryStr +=  '       ["日文名"] = "{}",'.format(wctfShip['name']['ja_jp'] + ship_namesuffix[wctfShip['name']['suffix']]['ja_jp']) + '\n'
    luaTableEntryStr +=  '       ["假名"] = "{}",'.format(wctfShip['name']['ja_kana'] + ship_namesuffix[wctfShip['name']['suffix']]['ja_kana']) + '\n'
    luaTableEntryStr +=  '       ["中文名"] = "{}",'.format(wctfShip['name']['zh_cn'] + ship_namesuffix[wctfShip['name']['suffix']]['zh_cn']) + '\n'
    luaTableEntryStr +=  '       ["舰种"] = {},'.format(stypeMap[wctfShip['type']]) + '\n'
    luaTableEntryStr +=  '       ["级别"] = {{"{}",{}}},'.format(ship_classes[wctfShip['class']]['zh_cn'] + '型', wctfShip['class_no']) + '\n'
    luaTableEntryStr +=  '       ["数据"] = {' + '\n'
    luaTableEntryStr +=  '           ["耐久"] = {{{},{}}},'.format(wctfShip['stats']['hp'], wctfShip['hp_max']) + '\n'
    luaTableEntryStr +=  '           ["火力"] = {{{},{}}},'.format(wctfShip['stats']['fire'], wctfShip["fire_max"]) + '\n'
    luaTableEntryStr +=  '           ["雷装"] = {{{},{}}},'.format(wctfShip['stats']['torpedo'], wctfShip["torpedo_max"]) + '\n'
    luaTableEntryStr +=  '           ["对空"] = {{{},{}}},'.format(wctfShip['stats']['aa'], wctfShip["aa_max"]) + '\n'
    luaTableEntryStr +=  '           ["装甲"] = {{{},{}}},'.format(wctfShip['stats']['armor'], wctfShip["armor_max"]) + '\n'
    luaTableEntryStr +=  '           ["对潜"] = {{{},{}}},'.format(wctfShip['stats']['asw'], wctfShip["asw_max"]) + '\n'
    luaTableEntryStr +=  '           ["回避"] = {{{},{}}},'.format(wctfShip['stats']['evasion'], wctfShip["evasion_max"]) + '\n'
    luaTableEntryStr +=  '           ["索敌"] = {{{},{}}},'.format(wctfShip['stats']['los'], wctfShip["los_max"]) + '\n'
    luaTableEntryStr +=  '           ["运"] = {{{},{}}},'.format(wctfShip['stats']['luck'], wctfShip["luck_max"]) + '\n'
    luaTableEntryStr +=  '           ["速力"] = {{{},{}}},'.format(wctfShip['stat']['speed']) + '\n'
    luaTableEntryStr +=  '           ["射程"] = {{{},{}}},'.format(wctfShip['stat']['range']) + '\n'
    luaTableEntryStr +=  '           ["稀有度"] = {{{},{}}}'.format(wctfShip['rare']) + '\n'
    luaTableEntryStr +=  '       }},'
    luaTableEntryStr +=  '       ["装备"] = {{'
    slot = len(wctfShip['slot'])
    if slot == 0:
        luaTableEntryStr +=  '           ["格数"] = {{{}}},'.format(slot) + '\n'
        luaTableEntryStr +=  '           ["搭载"] = {{}},'
        luaTableEntryStr +=  '           ["初期装备"] = {{}}'
    elif slot == 1:
        luaTableEntryStr +=  '           ["格数"] = {{{}}},'.format(slot) + '\n'
        luaTableEntryStr +=  '           ["搭载"] = {{{}}},'.format(wctfShip['slot'][0]) + '\n'
        luaTableEntryStr +=  '           ["初期装备"] = {{{}}}'.format(wikiShip['']) + '\n'
    luaTableEntryStr +=  '       }},' + '\n'
    luaTableEntryStr +=  '       ["获得"] = {["掉落"] = 1,["改造"] = 0,["建造"] = 1,["时间"] = {}},'.format(, wctfShip['buildtime']) + '\n'
    luaTableEntryStr +=  '       ["消耗"] = {{["燃料"] = {},["弹药"] = {}}},'.format(wctfShip['consum']['fuel'], wctfShip['consum']['ammo']) + '\n'
    luaTableEntryStr +=  '       ["改修"] = {{["火力"] = {},["雷装"] = {},["对空"] = {},["装甲"] = {}}},'.format(wctfShip['modernization'][0], wctfShip['modernization'][1], wctfShip['modernization'][2], wctfShip['modernization'][3]) + '\n'
    luaTableEntryStr +=  '       ["解体"] = {{["燃料"] = {},["弹药"] = {},["钢材"] = {},["铝"] = {}}},'.format(wctfShip['scrap'][0], wctfShip['scrap'][1],wctfShip['scrap'][2],wctfShip['scrap'][3])
    luaTableEntryStr +=  '       ["改造"] = {["等级"] = {},["弹药"] = {},["钢材"] = {},["改造前"] = "-1",["改造后"] = "001a"},'.format(wctfShip['remodel']['next_lvl'], wctfShip['remodel_cost']['ammo'], wctfShip['remodel_cost']['steel'], _getWikiId(wctfShip['remodel'], 'prev'), _getWikiId(wctfShip['remodel'], 'next')) + '\n'
    luaTableEntryStr +=  '       ["画师"] = "{}",'.format(entities[wctfShip['rels'['cv']]]) + '\n'
    luaTableEntryStr +=  '       ["声优"] = "{}"'.format(entities[wctfShip['rels']['illustrator']]) + '\n'
    luaTableEntryStr +=  '   },' + '\n'
    return luaTableEntryStr

def main():
    # Convert nedb to json
    # utils.nedb2json(dbDicName + 'ships.nedb', dbDicName + 'ships.json')
    # utils.nedb2json(dbDicName + 'ship_namesuffix.nedb', dbDicName + 'ship_namesuffix.json')
    # utils.nedb2json(dbDicName + 'ship_classes.nedb', dbDicName + 'ship_classes.json')
    # utils.nedb2json(dbDicName + 'entities.nedb', dbDicName + 'entiteis.json')

    # Load dictionary from json file
    ships = utils.jsonFile2dic(dbDicName + "ships.json", masterKey = "id")
    ship_namesuffix = utils.jsonFile2dic(dbDicName + 'ship_namesuffix.json', masterKey = "id")
    ship_classes = utils.jsonFile2dic(dbDicName + 'ship_classes.json', masterKey = 'id')
    entities = utils.jsonFile2dic(dbDicName + 'entities.json', masterKey = 'id')

main()

# http://media.kcwiki.moe/kcdata/slotitem/all.json