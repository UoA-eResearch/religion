#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import simdjson as json
import shapely
from tqdm.auto import tqdm
import time
from osm2geojson import json2shapes
import geopandas as gpd

s = time.time()
churches = gpd.read_parquet("churches.parquet")
schools = gpd.read_parquet("schools.parquet")
townhalls = gpd.read_parquet("townhalls.parquet")
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
    s = time.time()
    filtered_data = data[
        data["lng"].between(bounds[0], bounds[2]) &
        data["lat"].between(bounds[1], bounds[3])
    ]
    print(f"Filtered data in {time.time() - s} seconds")
    if len(filtered_data) > limit:
        filtered_data = filtered_data.sample(limit)
        print(f"Sampled data in {time.time() - s} seconds")
    records = filtered_data.drop(columns="geometry").to_dict(orient="records")
    print(f"Converted data in {time.time() - s} seconds")
    return records