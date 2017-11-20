all: rmdbs fetch lua json pack

fetch:
	wget -i sh/fetch_list -P db/

ships2lua:
	python3 ships2lua.py

items2lua:
	python3 items2lua.py

lua: ships2lua items2lua

json:
	lua lua2json.lua

clean:
	rm -f db/entities.json
	rm -f db/item_types.json
	rm -f db/items.json
	rm -f db/ship_classes.json
	rm -f db/ship_namesuffix.json
	rm -f db/ship_series.json
	rm -f db/ship_types.json
	rm -f db/ships.json
	rm output/*

rmdbs:
	rm -f db/entities.nedb
	rm -f db/item_types.nedb
	rm -f db/items.nedb
	rm -f db/ship_classes.nedb
	rm -f db/ship_namesuffix.nedb
	rm -f db/ship_series.nedb
	rm -f db/ship_types.nedb
	rm -f db/ships.nedb

pack:
	bash sh/pack.sh
