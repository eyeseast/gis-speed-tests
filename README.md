# GIS Speed tests

I want to see how long it takes to read through files in various formats.

| path                           | function           | count  | time           |
| ------------------------------ | ------------------ | ------ | -------------- |
| nhgis0038_ds172_2010_block.csv | read_csv           | 157509 | 0:00:00.869328 |
| ma-2010-blocks.geojson         | read_geojson       | 155463 | 0:00:12.225532 |
| ma-2010-blocks.geojson         | read_geojson_fiona | 155463 | 0:00:38.971221 |
| ma-2010-blocks.ndjson          | read_json_nl       | 155463 | 0:00:06.262876 |
| ma-2010-blocks.ndjson          | read_geojson_fiona | 1      | 0:00:00.242557 |
| MA_block_2010.shp              | read_shp           | 155463 | 0:00:07.643704 |
