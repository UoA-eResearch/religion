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
        tags = feature["properties"]["tags"]
        if feature["shape"].is_empty:
            continue
        filtered_shapes.append({
            "lat": feature["shape"].centroid.y,
            "lng": feature["shape"].centroid.x,
            "name": tags.get("name"),
            "religion": tags.get("religion"),
            "denomination": tags.get("denomination"),
            "start_date": tags.get("start_date")
        })
    df = pd.DataFrame(filtered_shapes)
    return df

s = time.time()
churches = load("churches")
schools = load("schools")
townhalls = load("townhalls")
print(f"Loaded data in {time.time() - s} seconds")

app = FastAPI(root_path="/OSM_API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get(bounds:str = "-90,-180,90,180", dataset:str = "churches", limit:int = 100):
    try:
        bounds = list(map(float, bounds.split(",")))
        if len(bounds) != 4:
            raise ValueError
    except:
        raise HTTPException(status_code=400, detail="Invalid bounds")
    if dataset == "churches":
        data = churches
    elif dataset == "schools":
        data = schools
    elif dataset == "townhalls":
        data = townhalls
    else:
        raise HTTPException(status_code=400, detail="Invalid dataset")
    filtered_data = data[
        data["lng"].between(bounds[0], bounds[2]) &
        data["lat"].between(bounds[1], bounds[3])
    ]
    if len(filtered_data) > limit:
        filtered_data = filtered_data.sample(limit)
    return filtered_data.to_dict(orient="records")