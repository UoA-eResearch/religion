#!/usr/bin/env python3

import csv
import sys
import re
import json

files = sys.argv[1:]
o = {}

for fn in files:
  with open(fn) as f:
    reader = csv.DictReader(f)
    for row in reader:
      #"Year","Area_type","Area_code","Area_description","Religious_affiliation_total_responses_code","Religious_affiliation_total_responses_description","Census_usually_resident_population_count","Religious_affiliation_total_responses_percent"
      if row["Area_type"] == "Statistical Area 2":
        code = row["Area_code"]
        year = row["Year"]
        religion = row["Religious_affiliation_total_responses_description"]
        count = row["Census_usually_resident_population_count"]
        if count == "C":
          count = None
        else:
          count = int(count)
        if code not in o:
          o[code] = {}
        if year not in o[code]:
          o[code][year] = {}
        o[code][year][religion] = count

print(json.dumps(o, sort_keys=True, indent=4))
