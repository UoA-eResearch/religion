#!/usr/bin/env python

import csv
import sys
import re
import json

fn = sys.argv[1]
o = {}

with open(fn) as f:
  reader = csv.DictReader(f)
  for row in reader:
    code = row['Code']
    if len(code) == 6:
      o[code] = {"desc": row['Description']}
      for k,v in row.items():
        if "religious" in k:
          year = int(k[:4])
          if year not in o[code]:
            o[code][year] = {}
          religion = k[107:]
          if v == '..C':
            v = None
          else:
            v = int(v)
          o[code][year][religion] = v

print(json.dumps(o, sort_keys=True, indent=4))
