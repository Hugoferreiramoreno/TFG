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


def concept_extraction(es,list_keywords,mode,model,reach=10000):

	if es or list_keywords or mode or model or reach is None:
		return None
	query={}
	bool={}
	should={}
	counter=0
	array_lemma=[]
	top30=list_keywords[29][1]
	for key,value in list_keywords: #A
		if counter < reach:	#B
			counter+=1
			aux_query={}
			aux_query["query"]=key
			if model ==0:	#C
				increase=value
			else: #D
				increase=((value*(1/top30))**1.1)
			aux_query["boost"]= 1+increase
			array_lemma.append(aux_query)
			#E
	array_match=[]
	for aux in array_lemma:#F
		lemma={}
		if mode ==0:#G
			lemma["lemma"]=aux
		elif mode ==1:#H
			lemma["concepto.lemma"]=aux
		array_match.append(lemma)
		#I
	arrray_should=[]
	for aux2 in array_match:
		match={}
		match["match_phrase"]=aux2
		arrray_should.append(match)
	should["should"]=arrray_should
	bool["bool"]=should
	query["query"]=bool
	return  es.search(index='concepts',body=query,size= "20")#J

def extract_list(es,list_keywords,mode,model,reach=10000):
	if es or list_keywords or mode or model or reach is None:
		return None
	
	query={}
	match={}
	lemma={}
	counter=0
	query_aux={}
	aux=0
	reference=0
	reference_original=0
	list={}
	
	results=concept_extraction(es,list_keywords,mode,model,reach)
	for data in results["hits"]["hits"]:
		reference_original +=data['_score']
	reference=reference_original
	for a,b in list_keywords:
		if counter < reach:
			query_aux["query"]=a
			query_aux["boost"]=1
			list[a]=a
			lemma={}
			if mode == 0:
				lemma["lemma"]=query_aux
			elif mode ==1:
				lemma["concepto.lemma"]=aux
			match["match"]=lemma
			query["query"]=match
			results= es.search(index='concepts',body=query,size= "10")
			for data in results["hits"]["hits"]:
					list_keywords[counter]=data['_source']['lemma'],b
					results2=concept_extraction(es,list_keywords,mode,model,reach)
					aux=0
					for data2 in results2["hits"]["hits"]:
						aux +=data2['_score']
					if(aux > reference):
						reference=aux
						list[a]=data['_source']['lemma']
			reference=reference_original
			list_keywords[counter]=list[a],b
			counter+=1
	return list

def search_results(es,file):
	if es is None:
		return None
	if file is None:
		return None
	if es.indices.exists(index='results_concepts') == False:
		es.indices.create(index='results_concepts', ignore=400)
	if es.indices.exists(index='results_list') == False:
		es.indices.create(index='results_list', ignore=400)
	else:
		print("Busqueda previa detectada")
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
		print("Mostrando conceptos")
		aux=es.search(index='results_concepts',body=query,size= "20")
		if len(aux["hits"]["hits"]) != 0:
			for result in aux["hits"]["hits"]:
				print (result['_source']['conceptos'])
		print("Mostrando listado palabras clave / concepto ")
		aux=es.search(index='results_list',body=query,size= "1000")
		if len(aux["hits"]["hits"]) != 0:
			for result in aux["hits"]["hits"]:
				print (result['_source']['list'])
			return True
		return None

def insert_concept_results(es,file,index_name,data):
	if es or file or index_name or data is None:
		return None
	dic = {}
	dic["texto"]=file
	dic["conceptos"]=[]
	for result in data:
		conceptos = {}
		conceptos["lemma"]=result['_source']['lemma']
		dic["conceptos"].append(conceptos)		
	return (es.index(index=index_name, doc_type='doc', body=dic))
	
def insert_list_results(es,file,index_name,data):
	if es or file or index_name or data is None:
		return None
	dic = {}
	dic["texto"]=file
	dic["list"]=[]
	for key in data:
		conceptos = {}
		conceptos["keyword"]=key
		conceptos["concept"]=data[key]
		dic["list"].append(conceptos)		
	return (es.index(index=index_name, doc_type='doc', body=dic))	

if __name__ == "__main__":
	if len(sys.argv) != 5 :
		print ("Usage: python elastic file mode model reach")
		sys.exit(1)
	es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
	
	search= search_results(es,sys.argv[1])
	if search is None:
		print("estoy aqui")
		dir=os.path.join(os.path.dirname(os.getcwd()),"result","keywords_list",sys.argv[1]+".txt")

		list_keywords=[]
		counter=0
		with open(dir,"r",encoding="utf-8") as keywords_list:
			for linea in keywords_list:
				if len(linea) >1:
					list_keywords.append((linea.split("\t")[0],float(linea.split("\t")[1])))
		
		results= concept_extraction(es,list_keywords,int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
		for data in results["hits"]["hits"]:
			print (data['_source']['lemma']) 
			print (data['_score'])
		insert_concept_results(es,sys.argv[1],'results_concepts',results["hits"]["hits"])
		
		results= extract_list(es,list_keywords,int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
		for clave in results:
			print (clave,results[clave])
		insert_list_results(es,sys.argv[1],'results_list',results)



