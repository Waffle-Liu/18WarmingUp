#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import sys
# sys.path.append('..')
import json
import os
# from main import session

for i in [1,2,3,4,5,6,7,8,9]:
	f=open(str(i)+".json","w")
	json_content = {"id": i, "loan": [[0, 0, 0, 0]], "chip": [], "type": 0, "material": [], "invest": [0, 0, 0, 0, 0], "sale": 0, "cash": 0, "result": 0, "product": [], "storage": 300, "fee": 0, "store_cost": 0, "curr_price": 0, "value": 0}
	f.write(json.dumps(json_content))
	f.close()
	
f = open("game.txt","w")
f.write("1")
f.close()

if os.path.exists("log.json"):
	os.remove("log.json")
# session.clear()