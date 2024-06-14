#!/bin/bash

curl --get 'https://osm.buntinglabs.com/v1/osm/extract' \
         --data "tags=amenity=place_of_worship" \
         --data "api_key=$API_KEY" \
         > churches.geojson

curl --get 'https://osm.buntinglabs.com/v1/osm/extract' \
         --data "tags=amenity=townhall" \
         --data "api_key=$API_KEY" \
         > townhalls.geojson

curl --get 'https://osm.buntinglabs.com/v1/osm/extract' \
         --data "tags=amenity=school" \
         --data "api_key=$API_KEY" \
         > schools.geojson