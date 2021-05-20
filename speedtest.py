#!/usr/bin/env python
import csv
import datetime
import json
from dataclasses import dataclass, asdict, fields
from pathlib import Path

import click
import fiona
from tabulate import tabulate
from tqdm import tqdm


@click.command()
@click.argument(
    "filenames",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        allow_dash=False,
    ),
    nargs=-1,
)
def speedtest(filenames):
    results = []
    for filename in filenames:

        path = Path(filename)
        readers = FILE_TYPES[path.suffix]

        for reader in readers:
            result = Result(path.name, reader.__name__, 0, datetime.timedelta(0))
            start = datetime.datetime.now()
            result.count = reader(path)
            end = datetime.datetime.now()
            result.time = end - start

            results.append(result)

    click.echo(tabulate(map(asdict, results), headers="keys", tablefmt="github"))


def read_csv(path):
    count = 0
    with path.open() as f:
        reader = tqdm(csv.reader(f))
        for row in reader:
            count += 1

    return count


def read_geojson(path):
    count = 0
    with path.open() as f:
        fc = json.load(f)
        for feature in tqdm(fc["features"]):
            count += 1
    return count


def read_json_nl(path):
    count = 0
    with path.open() as f:
        for line in tqdm(f):
            line = json.loads(line.strip())
            count += 1
    return count


def read_geojson_fiona(path):
    count = 0
    with fiona.open(path) as source:
        for feature in source:
            count += 1
    return count


def read_shp(path):
    count = 0
    with fiona.open(path) as fc:
        for feature in tqdm(fc):
            count += 1
    return count


FILE_TYPES = {
    ".csv": [read_csv],
    ".geojson": [read_geojson, read_geojson_fiona],
    ".shp": [read_shp],
    ".ndjson": [read_json_nl, read_geojson_fiona],
}


@dataclass
class Result:
    path: Path
    function: str
    count: int
    time: datetime.timedelta

    def __str__(self):
        return "\t".join(
            map(str, [self.path.name, self.function, self.count, self.time.seconds])
        )


if __name__ == "__main__":
    speedtest()