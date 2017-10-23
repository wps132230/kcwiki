import utils
import requests

kcDataJsonURL = 'http://kcwikizh.github.io/kcdata/ship/all.json'


def fetchKCDataJson(url):
    '''
    Fetch the kcwiki data
    '''
    response = requests.get(url)
    json_raw = response.json()
    data_json = dict()
    for _entry in json_raw:
        if not _entry['id'] or not _entry['sort_no']:
            continue
        data_json[_entry['id']] = _entry
    return data_json


# Directory name of db file
DBFOLDER = 'db/'

# Map from wctf ship id to kcwiki ship id
STYPE_MAP = {1: 2, 2: 3, 3: 4, 4: 5, 5: 5,
             6: 9, 7: 9, 8: 9, 9: 7, 10: 11,
             11: 18, 12: 16, 13: 13, 14: 13, 15: 17,
             16: 19, 17: 20, 18: 9, 19: 2, 20: 9,
             21: 21, 22: None, 23: 5, 24: 16, 25: None,
             26: None, 27: None, 28: 3, 29: 22, 30: 7,
             31: 1, 32: 7}
SHIP_NAME_SUFFIX = {}
SHIP_CLASSES = {}
WIKI_SHIPS = {}
ENTITIES = {}


def equip2str(equip):
    '''
    Tranform equip list to string , eg.'a,b,c,d'
    '''
    formated_equip = []
    for e in equip:
        if isinstance(e, str):
            formated_equip.append('-1')
        else:
            formated_equip.append(str(e))
    return ','.join(formated_equip)


def slot2str(slot):
    '''
    Tranform slot list to string, eg.'a,b,c,d'
    '''
    formated_slot = []
    for s in slot:
        formated_slot.append(str(s))
    return ','.join(formated_slot)


def safe_suffix(suffix, lan):
    if not suffix:
        return ''
    if not suffix in SHIP_NAME_SUFFIX or not lan in SHIP_NAME_SUFFIX[suffix]:
        return ''
    return SHIP_NAME_SUFFIX[suffix][lan]


costMap = {
    'ammo': '弹药',
    'steel': '钢材',
    'fuel': '燃料',
}


def remodel2str(remodel_cost, ship_remodel, base_lvl):
    '''
    Gen the remodel info
    '''
    if not isinstance(base_lvl, str):
        base_lvl = '0'
    remodel_cost_list = list()
    if isinstance(remodel_cost, dict):
        for cost_type, cost in remodel_cost.items():
            remodel_cost_list.append(
                '["{}"] = {}'.format(costMap[cost_type], cost))
    remodel_cost_str = ','.join(remodel_cost_list)
    remodel_lvl_str = '["等级"] = 0'
    if ship_remodel and 'next_lvl' in ship_remodel:
        remodel_lvl_str = '["等级"] = {}'.format(ship_remodel['next_lvl'])
    if ship_remodel and 'prev_loop' in ship_remodel:
        remodel_lvl_str = '["等级"] = {}'.format(base_lvl)
    remodel_before_str = '["改造前"] = "-1"'
    remodel_after_str = '["改造后"] = "-1"'
    if ship_remodel and 'next' in ship_remodel:
        remodel_after_str = '["改造后"] = "{}"'.format(
            WIKI_SHIPS[ship_remodel['next']]['wiki_id'])
    if ship_remodel and 'prev' in ship_remodel:
        remodel_before_str = '["改造前"] = "{}"'.format(
            WIKI_SHIPS[ship_remodel['prev']]['wiki_id'])
    return '        ["改造"] = {{{},{},{},{}}},\n'.format(remodel_lvl_str, remodel_cost_str, remodel_before_str, remodel_after_str)


def generate(wiki_ship, wctf_ship, table_dict):
    '''
    Generate one entry of the lua table
    from two sources: 'zh.kcwiki.org' and 'Who calls the fleet'.
    '''
    entry_str = ''
    entry_str += '    ["{}"] = {{\n'.format(wiki_ship['wiki_id'])
    entry_str += '        ["ID"] = {},\n'.format(wctf_ship['id'])
    entry_str += '        ["图鉴号"] = {},\n'.format(wctf_ship['no'])
    entry_str += '        ["日文名"] = "{}",\n'.format(
        wctf_ship['name']['ja_jp'] + safe_suffix(wctf_ship['name']['suffix'], 'ja_jp'))
    entry_str += '        ["假名"] = "{}",\n'.format(
        wctf_ship['name']['ja_kana'] + safe_suffix(wctf_ship['name']['suffix'], 'ja_kana'))
    entry_str += '        ["中文名"] = "{}",\n'.format(
        wctf_ship['name']['zh_cn'] + safe_suffix(wctf_ship['name']['suffix'], 'zh_cn'))
    entry_str += '        ["舰种"] = {},\n'.format(
        STYPE_MAP[wctf_ship['type']])
    entry_str += '        ["级别"] = {{"{}",{}}},\n'.format(
        SHIP_CLASSES[wctf_ship['class']]['name']['zh_cn'] + '型', wctf_ship['class_no'] if wctf_ship['class_no'] else '0')
    entry_str += '        ["数据"] = {\n'
    entry_str += '            ["耐久"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['hp'], wctf_ship['stat']['hp_max'])
    entry_str += '            ["火力"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['fire'], wctf_ship['stat']['fire_max'])
    entry_str += '            ["雷装"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['torpedo'], wctf_ship['stat']['torpedo_max'])
    entry_str += '            ["对空"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['aa'], wctf_ship['stat']['aa_max'])
    entry_str += '            ["装甲"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['armor'], wctf_ship['stat']['armor_max'])
    entry_str += '            ["对潜"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['asw'], wctf_ship['stat']['asw_max'])
    entry_str += '            ["回避"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['evasion'], wctf_ship['stat']['evasion_max'])
    entry_str += '            ["索敌"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['los'], wctf_ship['stat']['los_max'])
    entry_str += '            ["运"] = {{{},{}}},\n'.format(
        wctf_ship['stat']['luck'], wctf_ship['stat']['luck_max'])
    entry_str += '            ["速力"] = {},\n'.format(
        wctf_ship['stat']['speed'])
    entry_str += '            ["射程"] = {},\n'.format(
        wctf_ship['stat']['range'])
    entry_str += '            ["稀有度"] = {}\n'.format(wctf_ship['rare'])
    entry_str += '        }},\n'
    entry_str += '        ["装备"] = {{\n'
    slot_size = len(wctf_ship['slot'])
    entry_str += '            ["格数"] = {},\n'.format(slot_size)
    entry_str += '            ["搭载"] = {{{}}},\n'.format(
        slot2str(wctf_ship['slot']))
    entry_str += '            ["初期装备"] = {{{}}}\n'.format(
        equip2str(wctf_ship['equip']))
    entry_str += '        }},\n'
    can_drop = 1 if ('can_drop' in wiki_ship and wiki_ship['can_drop']) else 0
    can_remodel = 1 if 'after_lv' in wiki_ship and wiki_ship['after_lv'] else 0
    can_build = 1 if 'can_construct' in wiki_ship and wiki_ship['after_lv'] else 0
    entry_str += '        ["获得"] = {{["掉落"] = {},["改造"] = {},["建造"] = {},["时间"] = {}}},\n'.format(
        can_drop, can_remodel, can_build, wctf_ship['buildtime'])
    entry_str += '        ["消耗"] = {{["燃料"] = {},["弹药"] = {}}},\n'.format(
        wctf_ship['consum']['fuel'], wctf_ship['consum']['ammo'])
    entry_str += '        ["改修"] = {{["火力"] = {},["雷装"] = {},["对空"] = {},["装甲"] = {}}},\n'.format(
        wctf_ship['modernization'][0], wctf_ship['modernization'][1], wctf_ship['modernization'][2], wctf_ship['modernization'][3])
    entry_str += '        ["解体"] = {{["燃料"] = {},["弹药"] = {},["钢材"] = {},["铝"] = {}}},\n'.format(
        wctf_ship['scrap'][0], wctf_ship['scrap'][1], wctf_ship['scrap'][2], wctf_ship['scrap'][3])
    entry_str += remodel2str(wctf_ship['remodel_cost'],
                             wctf_ship['remodel'], wctf_ship['base_lvl'])
    entry_str += '        ["画师"] = "{}",\n'.format(
        ENTITIES[wctf_ship['rels']['illustrator']]['name']['ja_jp'] if wctf_ship['rels']['illustrator'] else '未知')
    entry_str += '        ["声优"] = "{}"\n'.format(
        ENTITIES[wctf_ship['rels']['cv']]['name']['ja_jp'] if wctf_ship['rels']['cv'] else '未知')
    entry_str += '    },\n'
    table_dict[wiki_ship['wiki_id']] = entry_str

# Convert nedb to json
# utils.nedb2json(DBFOLDER + 'ships.nedb', DBFOLDER + 'ships.json')
# utils.nedb2json(DBFOLDER + 'SHIP_NAME_SUFFIX.nedb', DBFOLDER + 'SHIP_NAME_SUFFIX.json')
# utils.nedb2json(DBFOLDER + 'ship_classes.nedb', DBFOLDER + 'ship_classes.json')
# utils.nedb2json(DBFOLDER + 'entities.nedb', DBFOLDER + 'entiteis.json')


# Load dictionary from json file
SHIPS = utils.jsonFile2dic(DBFOLDER + 'ships.json', masterKey='id')
SHIP_NAME_SUFFIX = utils.jsonFile2dic(
    DBFOLDER + 'ship_namesuffix.json', masterKey='id')
SHIP_CLASSES = utils.jsonFile2dic(
    DBFOLDER + 'ship_classes.json', masterKey='id')
ENTITIES = utils.jsonFile2dic(DBFOLDER + 'entities.json', masterKey='id')
WIKI_SHIPS = fetchKCDataJson(kcDataJsonURL)
LUATABLE_STR = ''
LUATABLE_DICT = dict()
for ship_id, ship in SHIPS.items():
    if ship_id in WIKI_SHIPS:
        generate(WIKI_SHIPS[ship_id], ship, LUATABLE_DICT)

for key, entry in sorted(LUATABLE_DICT.items()):
    LUATABLE_STR += entry

with open('out.txt', 'w', encoding='utf_8') as fwtxt:
    fwtxt.write(LUATABLE_STR)
    fwtxt.close()
