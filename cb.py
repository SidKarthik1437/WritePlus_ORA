import json
with open('./gl.json', 'r') as file:
    loc_data = json.load(file)
loc = 'India'
print([country['country_code'] for idx, country in enumerate(loc_data) if country['country_name'] == loc][0])