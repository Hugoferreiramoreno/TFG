"""@package elastic_bulk.py
Documentation for the elastic_bulk module in charge of the massive upload from a json file to the db.
"""
import sys
import numpy as np
import re
import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import requests, json, os


def decode_nginx_log(_nginx_fd):
	"""!@brief  Function that parse the source information from a json.
	!@param _nginx_fd The file that contains the json
	"""
	with open(_nginx_fd,encoding='utf-8') as f:
		for each_line in f:
			yield json.loads(each_line)

def es_add_bulk(nginx_file):
	"""!@brief  Function that bulk the information from a json.
	!@param nginx_fd The file that contains the json
	"""
	es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
	k = ({
			"_index": "concepts",
			"_type" : "doc",
			"_source": registro,
		 } for  registro in decode_nginx_log(nginx_file))
	helpers.bulk(es, k)
	
if __name__ == "__main__":
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	dir=os.path.join(os.path.dirname(os.getcwd()),"data","json",sys.argv[1]+".json")
	es_add_bulk(dir)
