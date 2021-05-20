
CSV=data/Mass-2010-blocks-by-race/nhgis0038_csv/nhgis0038_ds172_2010_block.csv
GEOJSON=data/ma-2010-blocks.geojson
NDJSON=data/ma-2010-blocks.ndjson
SHP=data/Mass-2010-blocks-by-race/nhgis0038_shape/nhgis0038_shapefile_tl2010_250_block_2010/MA_block_2010.shp

$(CSV): data/Mass-2010-blocks-by-race/nhgis0038_csv.zip
	unzip -d $(dir $@) $^
	touch $@

$(SHP): data/Mass-2010-blocks-by-race/nhgis0038_shape.zip
	unzip $^
	unzip data/Mass-2010-blocks-by-race/nhgis0038_shape/nhgis0038_shapefile_tl2010_250_block_2010.zip
	touch $@

$(NDJSON): $(SHP)
	fio cat $^ > $@

$(GEOJSON): $(NDJSON)
	cat $^ | fio collect > $@

csv: $(CSV)
	pipenv run ./speedtest.py $^

geojson: $(GEOJSON)
	pipenv run ./speedtest.py $^

ndjson: $(NDJSON)
	pipenv run ./speedtest.py $^

shp: $(SHP)
	pipenv run ./speedtest.py $^

all: $(CSV) $(GEOJSON) $(NDJSON) $(SHP)
	pipenv run ./speedtest.py $^

data/shp/blocks.shp: $(SHP) $(CSV)
	mkdir -p $(dir $@)
	ogr2ogr -f 'ESRI Shapefile' \
		-sql 'SELECT * FROM MA_block_2010 JOIN "$(CSV)".nhgis0038_ds172_2010_block ON MA_block_2010.GISJOIN = nhgis0038_ds172_2010_block.GISJOIN' \
		$@ $(SHP)
