#!/bin/bash

curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];node["amenity"="place_of_worship"];out geom;' > churches_nodes.json
curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];way["amenity"="place_of_worship"];out geom;' > churches_ways.json
curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];relation["amenity"="place_of_worship"];out geom;' > churches_relations.json

curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];node["amenity"="townhall"];out geom;' > townhalls_nodes.json
curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];way["amenity"="townhall"];out geom;' > townhalls_ways.json
curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];relation["amenity"="townhall"];out geom;' > townhalls_relations.json

curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];node["amenity"="school"];out geom;' > schools_nodes.json
curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];way["amenity"="school"];out geom;' > schools_ways.json
curl 'https://overpass-api.de/api/interpreter' --data '[out:json][timeout:9999];relation["amenity"="school"];out geom;' > schools_relations.json