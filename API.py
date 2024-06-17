#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import simdjson as json
import shapely
from tqdm.auto import tqdm
import time

s = time.time()
churches = json.load(open("churches.geojson"))
print(f'{len(churches["features"])} churches loaded in {time.time()-s:.2f}s')

s = time.time()
schools = json.load(open("schools.geojson"))
print(f'{len(schools["features"])} schools loaded in {time.time()-s:.2f}s')

s = time.time()
townhalls = json.load(open("townhalls.geojson"))
print(f'{len(townhalls["features"])} townhalls loaded in {time.time()-s:.2f}s')

app = FastAPI(root_path="/OSM_API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_centroid(feature):
    geom = feature["geometry"]
    try:
        return shapely.from_geojson(json.dumps(geom)).centroid
    except:
        if geom["type"] in ["MultiPolygon", "MultiLineString"]:
            geom["coordinates"] = [part for part in geom["coordinates"] if len(part) > 1]
        try:
            return shapely.from_geojson(json.dumps(geom)).centroid
        except Exception as e:
            return shapely.from_geojson(json.dumps(geom)).representative_point()

for dataset in [churches, schools, townhalls]:
    centroids = 0
    for feature in tqdm(dataset["features"]):
        centroid = get_centroid(feature)
        if centroid:
            centroids += 1
            feature["properties"]["lat"] = centroid.y
            feature["properties"]["lng"] = centroid.x
        else:
            feature["properties"]["lat"] = 0
            feature["properties"]["lng"] = 0
    print(f"{centroids} centroids calculated for {len(dataset['features'])} features")

@app.get("/")
def get(bounds:str, dataset:str = "churches", keys:str = None, centroid_only:bool = False, limit:int = 100):
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
    features = []
    for feature in data["features"]:
        if feature["properties"].get("lat", 0) > bounds[1] and feature["properties"].get("lat", 0) < bounds[3] and feature["properties"].get("lng", 0) > bounds[0] and feature["properties"].get("lng", 0) < bounds[2]:
            feature = {"type": "Feature", "properties": feature["properties"], "geometry": feature["geometry"]}
            if keys:
                feature["properties"] = {key: feature["properties"].get(key) for key in keys.split(",")}
            if centroid_only:
                feature["geometry"] = {"type": "Point", "coordinates": [feature["properties"].get("lng", 0), feature["properties"].get("lat", 0)]}
            features.append(feature)
            if len(features) == limit:
                break
    return {"type": "FeatureCollection", "features": features}