"""!@package elastic.py
Documentation for the elasticsearch module.
For More details check the documentation of each function.
"""
import json
import sys
import numpy as np
import re
import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers


#PRUEBAS DE BUSQUEDA

def analiza_texto(es,conceptolema,modo,modelo,alcance=10000):
	query={}
	bool={}
	should={}
	contador=0
	arraydelemas=[]
	top30=conceptolema[29][1]
	for a,b in conceptolema:
		if contador < alcance:
			contador+=1
			conceptolema2={}
			conceptolema2["query"]=a
			if modelo ==0:
				incremento=b
			else:
				incremento=((b*(1/top30))**1.1)
			conceptolema2["boost"]= 1+incremento
			arraydelemas.append(conceptolema2)
	arraydematch=[]
	for cosa2 in arraydelemas:
		lemma={}
		if modo ==0:
			lemma["lemma"]=cosa2
		elif modo ==1:
			lemma["concepto.lemma"]=cosa2
		arraydematch.append(lemma)
	arraydeshould=[]
	for aux in arraydematch:
		match={}
		match["match_phrase"]=aux
		arraydeshould.append(match)
	should["should"]=arraydeshould
	bool["bool"]=should
	query["query"]=bool
	return  es.search(index='keywords',body=query,size= "20")

def search_results(es,file):
	if es is None:
		return -1
	if file is None:
		return -2
	if es.indices.exists(index='results_concepts') == False:
		es.indices.create(index='results_concepts', ignore=400)
	if es.indices.exists(index='results_list') == False:
		es.indices.create(index='results_list', ignore=400)
	else:
		query={}
		dic = {}
		dic["query"]=file
		dic["boost"]=1
		file={}
		file["texto"]=dic
		match={}
		match["match_phrase"]=file
		should={}
		should["should"]=match
		bool={}
		bool["bool"]=should
		query["query"]=bool
		control=False
		aux=es.search(index='results_concepts',body=query,size= "20")
		if len(aux["hits"]["hits"]) != 0:
			print("estoy aqui")
			for result in aux["hits"]["hits"]:
				print (result['_source']['conceptos'])
		aux=es.search(index='results_list',body=query,size= "1000")
		if len(aux["hits"]["hits"]) != 0:
			for result in aux["hits"]["hits"]:
				print (result['_source']['lista'])
			return True
		return None

def insert_concept_results(es,file,index_name,data):
	dic = {}
	dic["texto"]=file
	dic["conceptos"]=[]
	for result in data:
		conceptos = {}
		conceptos["lemma"]=result['_source']['lemma']
		dic["conceptos"].append(conceptos)		
	print (es.index(index=index_name, doc_type='doc', body=dic))
	
def insert_list_results(es,file,index_name,data):
	dic = {}
	dic["texto"]=file
	dic["listado"]=[]
	for a,b in data:
		conceptos = {}
		conceptos["keyword"]=a
		conceptos["concept"]=b
		dic["conceptos"].append(conceptos)		
	return es.index(index=index_name, doc_type='doc', body=dic)	

if __name__ == "__main__":
	if len(sys.argv) != 5 :
		print ("Usage: python elastic file modo modelo alcance")
		sys.exit(1)
	es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
	
	search= search_results(es,sys.argv[1])
	if search is None:
		dir=os.path.join(os.path.dirname(os.getcwd()),"result","keywords_list",sys.argv[1]+".txt")

		conceptolema=[]
		contador=0
		with open(dir,"r",encoding="utf-8") as keywords_list:
			for linea in keywords_list:
				if len(linea) >1:
					conceptolema.append((linea.split("\t")[0],float(linea.split("\t")[1])))
		
		results= analiza_texto(es,conceptolema,int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
		for data in results["hits"]["hits"]:
			print (data['_source']['lemma']) 
			print (data['_score'])
		insert_concept_results(es,sys.argv[1],'results_concepts',results["hits"]["hits"])




