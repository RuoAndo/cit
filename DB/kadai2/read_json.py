import json
import sys

args = sys.argv
#with open('twitter.json') as f:
with open(args[1]) as f:
    di = json.load(f)

print(str(di['text']))

#for k, v in di['user'].items():  
#   print(f'{k}: {v}')
