#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import simdjson as json
import shapely
from tqdm.auto import tqdm
import time
from osm2geojson import json2shapes
import pandas as pd

def load(prefix="churches"):
    nodes = json.load(open(f"{prefix}_nodes.json"))
    print(f'Loaded {len(nodes["elements"])} nodes')
    ways = json.load(open(f"{prefix}_ways.json"))
    print(f'Loaded {len(ways["elements"])} ways')
    relations = json.load(open(f"{prefix}_relations.json"))
    print(f'Loaded {len(relations["elements"])} relations')
    shapes = []
    try:
        shapes.extend(json2shapes(nodes))
    except:
        print("Unable to parse nodes")
    try:
        shapes.extend(json2shapes(ways))
    except:
        print("Unable to parse ways")
    try:
        shapes.extend(json2shapes(relations))
    except:
        print("Unable to parse relations")
    filtered_shapes = []
    for feature in tqdm(shapes):
        if feature["shape"].is_empty:
            continue
        tags = feature["properties"]["tags"]
        if prefix == "churches":
            filtered_shapes.append({
                "lat": feature["shape"].centroid.y,
                "lng": feature["shape"].centroid.x,
                "name": tags.get("name"),
                "religion": tags.get("religion"),
                "denomination": tags.get("denomination"),
                "start_date": tags.get("start_date")
            })
        else:
            filtered_shapes.append({
                "lat": feature["shape"].centroid.y,
                "lng": feature["shape"].centroid.x,
                "name": tags.get("name"),
                "start_date": tags.get("start_date")
            })

    df = pd.DataFrame(filtered_shapes)
    return df

load("churches").to_csv("churches.csv")
load("schools").to_csv("schools.csv")
load("townhalls").to_csv("townhalls.csv")