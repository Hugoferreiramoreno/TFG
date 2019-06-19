"""
.. module:: elastic_bulk
   :platform: Unix, Windows
   :synopsis: Documentation for the elastic_bulk module in charge of the massive upload from a json file to the db

.. moduleauthor:: Hugo Ferreira Moreno <hugo.ferreira@estudiante.uam.es>

"""
import os
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def decode_nginx_log(_nginx_fd):
	"""Function that parse the source information from a json.

	Args:
		_nginx_fd (:obj:`str`): The name of the json file.

	Returns:
		Object: The json object generated

	"""
	with open(_nginx_fd, encoding='utf-8') as json_file:
		for each_line in json_file:
			yield json.loads(each_line)

def es_add_bulk(nginx_file):
	"""Function that bulk the information from a json.

	Args:
		nginx_file (:obj:`str`): The name of the json file.

	"""
	elastic = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
	k = ({
			"_index": "keywords",
			"_type" : "doc",
			"_source": registro,
		} for  registro in decode_nginx_log(nginx_file))
	helpers.bulk(elastic, k)

def main():
	"""Main function of the elastic_bulk module.

	"""
	path = os.path.join(os.path.dirname(os.getcwd()), "data", "prueba", "pruebabulk"+".json")
	es_add_bulk(path)

if __name__ == "__main__":
	main()
