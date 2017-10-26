local json = require('json')
local items = require('output/luatable-items').equipDataTb
local ships = require('output/luatable-ships').shipDataTb

ship_json = io.open('output/ships.json', 'w')
io.output(ship_json)
io.write(json.stringify(ships))
io.close(ship_json)

item_json = io.open('output/items.json', 'w')
io.output(item_json)
io.write(json.stringify(items))
io.close(item_json)
