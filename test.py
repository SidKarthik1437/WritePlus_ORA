import json
with open('./gl.json', 'r') as file:
    loc_data = json.load(file)
loc = 'India'
for idx, country in enumerate(loc_data):
        if country['country_name'] == loc:
            print(idx)