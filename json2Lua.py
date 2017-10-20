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
# Tranform equip list to string , eg.'a,b,c,d'
def equip2str(equip):
    formated_equip = []
    for e in equip:
        if isinstance(e, str):
            formated_equip.append('-1')
        else:
            formated_equip.append(str(e))
    return ','.join(formated_equip)

# Tranform slot list to string, eg.'a,b,c,d'
def slot2str(slot):
    formated_slot = []
    for s in slot:
        formated_slot.append(str(s))
    return ','.join(formated_slot)

def safe_suffix(suffix, lan):
    if not suffix:
        return ''
    return ship_namesuffix[suffix][lan]

# Generate one entry of the lua table
# from two sources: 'zh.kcwiki.org' and 'Who calls the fleet'.
def generate(wikiShip, wctfShip):
    luaTableEntryStr = ""
    luaTableEntryStr +=  '   ["{}"] = {{\n'.format(wikiShip['wiki_id'])
    luaTableEntryStr +=  '       ["ID"] = {},\n'.format(wctfShip['id'])
    luaTableEntryStr +=  '       ["图鉴号"] = {},\n'.format(wctfShip['no'])
    luaTableEntryStr +=  '       ["日文名"] = "{}",\n'.format(wctfShip['name']['ja_jp'] + safe_suffix(wctfShip['name']['suffix'],'ja_jp'))
    luaTableEntryStr +=  '       ["假名"] = "{}",\n'.format(wctfShip['name']['ja_kana'] + safe_suffix(wctfShip['name']['suffix'],'ja_kana'))
    luaTableEntryStr +=  '       ["中文名"] = "{}",\n'.format(wctfShip['name']['zh_cn'] + safe_suffix(wctfShip['name']['suffix'],'zh_cn'))
    luaTableEntryStr +=  '       ["舰种"] = {},\n'.format(stypeMap[wctfShip['type']])
    luaTableEntryStr +=  '       ["级别"] = {{"{}",{}}},\n'.format(ship_classes[wctfShip['class']]['name']['zh_cn'] + '型', wctfShip['class_no'])
    luaTableEntryStr +=  '       ["数据"] = {\n'
    luaTableEntryStr +=  '           ["耐久"] = {{{},{}}},\n'.format(wctfShip['stat']['hp'], wctfShip['stat']['hp_max'])
    luaTableEntryStr +=  '           ["火力"] = {{{},{}}},\n'.format(wctfShip['stat']['fire'], wctfShip['stat']['fire_max'])
    luaTableEntryStr +=  '           ["雷装"] = {{{},{}}},\n'.format(wctfShip['stat']['torpedo'], wctfShip['stat']['torpedo_max'])
    luaTableEntryStr +=  '           ["对空"] = {{{},{}}},\n'.format(wctfShip['stat']['aa'], wctfShip['stat']['aa_max'])
    luaTableEntryStr +=  '           ["装甲"] = {{{},{}}},\n'.format(wctfShip['stat']['armor'], wctfShip['stat']['armor_max'])
    luaTableEntryStr +=  '           ["对潜"] = {{{},{}}},\n'.format(wctfShip['stat']['asw'], wctfShip['stat']['asw_max'])
    luaTableEntryStr +=  '           ["回避"] = {{{},{}}},\n'.format(wctfShip['stat']['evasion'], wctfShip['stat']['evasion_max'])
    luaTableEntryStr +=  '           ["索敌"] = {{{},{}}},\n'.format(wctfShip['stat']['los'], wctfShip['stat']['los_max'])
    luaTableEntryStr +=  '           ["运"] = {{{},{}}},\n'.format(wctfShip['stat']['luck'], wctfShip['stat']['luck_max'])
    luaTableEntryStr +=  '           ["速力"] = {},\n'.format(wctfShip['stat']['speed'])
    luaTableEntryStr +=  '           ["射程"] = {},\n'.format(wctfShip['stat']['range'])
    luaTableEntryStr +=  '           ["稀有度"] = {}\n'.format(wctfShip['rare'])
    luaTableEntryStr +=  '       }},\n'
    luaTableEntryStr +=  '       ["装备"] = {{\n'
    slot_size = len(wctfShip['slot'])
    luaTableEntryStr +=  '           ["格数"] = {},\n'.format(slot_size)
    luaTableEntryStr +=  '           ["搭载"] = {{{0}}},\n'.format(slot2str(wctfShip['slot']))
    luaTableEntryStr +=  '           ["初期装备"] = {{{0}}}\n'.format(equip2str(wctfShip['equip']))
    luaTableEntryStr +=  '       }},\n'
    luaTableEntryStr +=  '       ["获得"] = {{["掉落"] = 1,["改造"] = 0,["建造"] = 1,["时间"] = {0}}},\n'.format(wctfShip['buildtime'])
    luaTableEntryStr +=  '       ["消耗"] = {{["燃料"] = {},["弹药"] = {}}},\n'.format(wctfShip['consum']['fuel'], wctfShip['consum']['ammo'])
    luaTableEntryStr +=  '       ["改修"] = {{["火力"] = {},["雷装"] = {},["对空"] = {},["装甲"] = {}}},\n'.format(wctfShip['modernization'][0], wctfShip['modernization'][1], wctfShip['modernization'][2], wctfShip['modernization'][3])
    luaTableEntryStr +=  '       ["解体"] = {{["燃料"] = {},["弹药"] = {},["钢材"] = {},["铝"] = {}}},\n'.format(wctfShip['scrap'][0], wctfShip['scrap'][1],wctfShip['scrap'][2],wctfShip['scrap'][3])
    luaTableEntryStr +=  '       ["改造"] = {["等级"] = {},["弹药"] = {},["钢材"] = {},["改造前"] = "-1",["改造后"] = "001a"},\n'.format(wctfShip['remodel']['next_lvl'], wctfShip['remodel_cost']['ammo'], wctfShip['remodel_cost']['steel'], _getWikiId(wctfShip['remodel'], 'prev'), _getWikiId(wctfShip['remodel'], 'next'))
    luaTableEntryStr +=  '       ["画师"] = "{}",\n'.format(entities[wctfShip['rels']['illustrator']]['name']['ja_jp'])
    luaTableEntryStr +=  '       ["声优"] = "{}"\n'.format(entities[wctfShip['rels']['cv']]['name']['ja_jp'])
    luaTableEntryStr +=  '   },\n'
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