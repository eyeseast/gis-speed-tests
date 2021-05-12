#!/usr/bin/env python
import csv
import datetime
import json
from dataclasses import dataclass
from pathlib import Path

import click
import fiona
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
        reader = FILE_TYPES[path.suffix]

        result = Result(path, 0, datetime.timedelta(0))
        start = datetime.datetime.now()
        result.count = reader(path)
        end = datetime.datetime.now()
        result.time = end - start

        results.append(result)

    click.echo("\t".join(["Filename", "Count", "Time"]))
    for result in results:
        click.echo(result)


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


def read_shp(path):
    count = 0
    with fiona.open(path) as fc:
        for feature in tqdm(fc):
            count += 1
    return count


FILE_TYPES = {
    ".csv": read_csv,
    ".geojson": read_geojson,
    ".shp": read_shp,
    ".ndjson": read_json_nl,
}


@dataclass
class Result:
    path: Path
    count: int
    time: datetime.timedelta

    def __str__(self):
        return "\t".join(map(str, [self.path.name, self.count, self.time.seconds]))


if __name__ == "__main__":
    speedtest()