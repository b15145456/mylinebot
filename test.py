import json
  
# Opening JSON file
f = open('menu.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)
print(data)