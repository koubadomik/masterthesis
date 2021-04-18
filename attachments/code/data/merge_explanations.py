import sys
import os
import json
from collections import Counter

PATH = sys.argv[1]
files = [x for x in os.listdir(PATH) if os.path.isfile(x)]

for file in files:    
    doc = []
    with open(file, "r") as f:
        doc = json.load(f)
    
    keys = []
    for item in doc:
        keys = keys + list(item[0]["behavior"]["summary"].keys())
    keys = set(keys)
    
    merged = {}
    for key in keys:
        merged[key] = []

    for item in doc:
        item = item[0]["behavior"]["summary"]
        for key in keys:
            if key in item:
                merged[key] += item[key]
    
    for key in keys:
        r = Counter(merged[key])
        r = sorted(r.items(), key = lambda pair:  pair[1], reverse=True)
        merged[key] = r

    name = file.split(".")[0]
    with open(f"merged/{name}-merged.json", 'w') as f:
        json.dump(merged,f, indent=2)