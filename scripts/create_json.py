"""
.. module:: create_json
   :platform: Unix, Windows
   :synopsis: Documentation of the module create_json that creates the json.

.. moduleauthor:: Hugo Ferreira Moreno <hugo.ferreira@estudiante.uam.es>

"""

import os
import sys
import json
import re

def single_json(file_name):
	"""Function that creates a single json from the babelnet index format 

	Args:
		file_name: (:obj:`str`): The name of the index file.

	"""
	if file_name is None:
		return None
	if file_name is "":
		return None 
	directory = os.path.join(os.path.dirname(os.getcwd()), "data", "json", "bulk"+".json")
	with open(file_name, encoding="utf-8") as file:
		with open(directory, "w+", encoding="utf-8") as outfile:
			for line in file:
				aux = re.sub(r'[^\w+ -.\t]', '', line)
				dic = {}
				row = aux.split("\t")
				dic["id"] = row[0]
				dic["lemma"] = row[1]
				dic["concepto"] = []
				for tupla in row[2:]:
					conceptos = {}
					concept = tupla.split("_")
					conceptos["lemma"] = concept[0]
					conceptos["importancia"] = concept[1]
					dic["concepto"].append(conceptos)
				json.dump(dic, outfile, ensure_ascii=False)
				print("", file=outfile)
	return 1

def multiple_json(file_name):
	"""Function that creates multiple json (one for every row) from the babelnet index format 

	Args:
		file_name: (:obj:`str`): The name of the index file.

	"""
	if file_name is None:
		return None
	if file_name is "":
		return None 
	with open(file_name, encoding="utf-8") as file:
		for line in file:
			aux = re.sub(r'[^\w+ -.\t]', '', line)
			dic = {}
			row = aux.split("\t")
			dic["id"] = row[0]
			dic["lemma"] = row[1]
			dic["concepto"] = []
			for tupla in row[2:]:
				conceptos = {}
				concept = tupla.split("_")
				conceptos["lemma"] = concept[0]
				conceptos["importancia"] = concept[1]
				dic["concepto"].append(conceptos)
			directory = os.path.join(os.path.dirname(os.getcwd()), "data", "json", row[0]+".json")
			with open(directory, "w", encoding="utf-8") as outfile:
				json.dump(dic, outfile, ensure_ascii=False)
	return 1

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("""Usage: python create_json.py mode data_origin \n mode can either be 0 for a having multiple json create from a file
		( best practice for single append)or 1 for create an unique json with all the data(best practice for bulk append usually when > 250)""")
	if int(sys.argv[1]) == 0:
		multiple_json(sys.argv[2])
	elif int(sys.argv[1]) == 1:
		single_json(sys.argv[2])
