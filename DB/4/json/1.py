import json

with open('twitter.json') as f:
    di = json.load(f)

print(str(di['id']))
print(di['user']['name'])

#for k, v in di.items():  
#    print(f'{k}: {v}')