"""!@package create_json_bulk.py
Documentation of the module create_json_bulk that create many json.
"""
import json
import sys
import numpy as np
import re
import os

#contador = 0 

dir=os.path.join(os.path.dirname(os.getcwd()),"data","prueba","pruebabulk"+".json")

		

with open(sys.argv[1],encoding="utf-8") as file:
	with open(dir,"w+",encoding="utf-8") as outfile:
		for line in file:
				aux=re.sub(r'[^\w+ -.\t]', '', line)
				todo={}
				row = aux.split("\t")
				todo["id"]=row[0]
				todo["lemma"]=row[1]
				todo["concepto"]=[]
				for tupla in row[2:]:
					conceptos={}
					concept=tupla.split("_")
					conceptos["lemma"]=concept[0]
					conceptos["importancia"]=concept[1]
					todo["concepto"].append(conceptos)
				json.dump(todo, outfile,ensure_ascii=False)
				print("",file=outfile)

