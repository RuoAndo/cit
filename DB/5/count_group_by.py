# coding: utf-8

import json
import sys

args = sys.argv
#with open('twitter.json') as f:
with open(args[1]) as f:
    di = json.load(f)

#print(str(di['text']))
#dict1=dict

kv = []

# dictionary‚ğg‚Á‚ÄAkey-value‚ğ•Û‘¶‚·‚éB

for i in di:
	#print(i)
	key = []
	value = []
	for k, v in i.items():  
		if k== "eyeColor":
			key.append(i['name'])
			value.append(v)
			dict1=dict(zip(key,value))
			#print(dict1)
			kv.append(dict1)

#print(kv)		

import numpy as np
f = np.array(kv).flatten()
	
#print(f)

values = []

for i in f:
	values.append(str(list(i.values())))

#print(values)

import collections
c = collections.Counter(values)
print(c)