
import json
import sys
import numpy as np
import re
import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from ws import Grampal
import unittest
import spacy
from keywords import *
from create_json import single_json, multiple_json
from elastic import *

class TestGrampal(unittest.TestCase):

	def test_analiza_estandar(self):
		ginstance = Grampal()
		respuesta = ginstance.analiza("Soy una prueba")
		self.assertEqual(respuesta.status_code, 200, "Funcionamiento estandar")
	def test_analiza_servidor(self):
		ginstance = Grampal('http://leptis.lllf.uam.es/api/soyunaprueba')
		respuesta = ginstance.analiza("Soy una prueba")
		self.assertEqual(respuesta.status_code, 404, "No hay respuesta del servidor")
	def test_analiza_empty(self):
		ginstance = Grampal()
		respuesta = ginstance.analiza("")
		self.assertEqual(respuesta, None, "El texto a analizar no puede estar vacío")
	def test_analiza_none(self):
		ginstance = Grampal()
		respuesta = ginstance.analiza(None)
		self.assertEqual(respuesta, None, "El paramatro texto no puede estar a None")
	def test_info_syntactic_empty(self):
		ginstance = Grampal()
		self.assertEqual(ginstance.info_syntactic(""), None, "El texto a analizar no puede estar vacío")
	def test_info_syntactic_none(self):
		ginstance = Grampal()
		self.assertEqual(ginstance.info_syntactic(None), None, "El texto a analizar no puede estar a None")
	def test_info_syntactic_estandar(self):
		ginstance = Grampal()
		respuesta = ginstance.analiza("Soy")
		self.assertEqual(ginstance.info_syntactic(respuesta.text), "V", "El texto a analizar no puede estar a None")
	def test_info_lemma_empty(self):
		ginstance = Grampal()
		self.assertEqual(ginstance.info_lemma(""), None, "El texto a analizar no puede estar vacío")
	def test_info_lemma_none(self):
		ginstance = Grampal()
		self.assertEqual(ginstance.info_lemma(None), None, "El texto a analizar no puede estar a None")
	def test_info_lemma_estandar(self):
		ginstance = Grampal()
		respuesta = ginstance.analiza("Soy")
		self.assertEqual(ginstance.info_lemma(respuesta.text), "SER", "El texto a analizar no puede estar a None")
	def test_info_orig_empty(self):
		ginstance = Grampal()
		self.assertEqual(ginstance.info_orig(""), None, "El texto a analizar no puede estar vacío")
	def test_info_orig_none(self):
		ginstance = Grampal()
		self.assertEqual(ginstance.info_orig(None), None, "El texto a analizar no puede estar a None")
	def test_info_orig_estandar(self):
		ginstance = Grampal()
		respuesta = ginstance.analiza("Soy")
		self.assertEqual(ginstance.info_orig(respuesta.text), "Soy", "El texto a analizar no puede estar a None")
	
class TestKeywords(unittest.TestCase):
	def test_create_graph_grampal_none(self):
		self.assertEqual(create_graph_grampal(None, 2), None, "El grafo a analizar no puede estar a None")
	def test_create_graph_grampal_k(self):
		self.assertEqual(create_graph_grampal("Soy un ejemplo", 0), -1, "El coeficiente de correlación no puede ser <= a 1")
	def test_create_graph_grampal_estandar(self):
		MODEL = "es_core_news_sm"
		nlp = spacy.load(MODEL)
		self.assertNotEqual(create_graph_grampal(nlp("Soy un ejemplo"), 2), None, "Caso estandar")
	def test_create_graph_spacy_none(self):
		self.assertEqual(create_graph_spacy(None, 2), None, "El grafo a analizar no puede estar a None")
	def test_create_graph_spacy_k(self):
		self.assertEqual(create_graph_spacy("Soy un ejemplo", 0), -1, "El coeficiente de correlación no puede ser <= a 1")
	def test_create_graph_spacy_estandar(self):
		MODEL = "es_core_news_sm"
		nlp = spacy.load(MODEL)
		self.assertNotEqual(create_graph_spacy(nlp("Soy un ejemplo"), 2), None, "Caso estandar")
	def test_pagerank_none(self):
		self.assertEqual(pagerank(None), None, "El grafo a analizar no puede estar a None")
	def test_pagerank_values(self):
		graph = igraph.Graph()
		self.assertEqual(pagerank(graph), -1, "El numero de valores del grafo no puede ser <=0")
	def test_topnodes_none(self):
		self.assertEqual(topnodes(None,1), None, "El grafo a analizar no puede estar a None")
	def test_topnodes_values(self):
		graph = igraph.Graph()
		self.assertEqual(topnodes(graph,0), -1, "El numero de nodos del top tiene que ser >0")
	def test_sort_values_none(self):
		self.assertEqual(sort_values(None), None, "El grafo a ordenar no puede estar a None")
	def test_sort_occurences_none(self):
		self.assertEqual(sort_occurences(None), None, "El grafo a ordenar no puede estar a None")
	def test_concatenate_candidates_spacy_none1(self):
		self.assertEqual(concatenate_candidates_spacy(None,2,"prueba"), None, "El grafo a analizar no puede estar a None")
	def test_concatenate_candidates_spacy_none2(self):
		self.assertEqual(concatenate_candidates_spacy(igraph.Graph(),None,"prueba"), None, "Los nodos a analizar no puede estar a None")
	def test_concatenate_candidates_spacy_none3(self):
		self.assertEqual(concatenate_candidates_spacy(igraph.Graph(),2,None), None, "El texto a analizar no puede estar a None")
	def test_concatenate_candidates_grampal_none1(self):
		self.assertEqual(concatenate_candidates_grampal(None,2,"prueba"), None, "El grafo a analizar no puede estar a None")
	def test_concatenate_candidates_grampal_none2(self):
		self.assertEqual(concatenate_candidates_grampal(igraph.Graph(),None,"prueba"), None, "Los nodos a analizar no puede estar a None")
	def test_concatenate_candidates_grampal_none3(self):
		self.assertEqual(concatenate_candidates_grampal(igraph.Graph(),2,None), None, "El texto a analizar no puede estar a None")
	def test_custom_tokenizer_estandar(self):
		nlp = spacy.load("es_core_news_sm")
		self.assertNotEqual(custom_tokenizer(nlp), None, "Funcionamiento estandar")
	def test_custom_tokenizer_none(self):
		self.assertEqual(custom_tokenizer(None), None, "nlp no puedo estar a None")

class TestCreate_json(unittest.TestCase):
	def test_single_json_none(self):
		self.assertEqual(single_json(None), None, "Se requiere un fichero de entrada")
	def test_single_json_empty(self):
		self.assertEqual(single_json(""), None, "Se requiere un fichero de entrada")
	def test_multiple_json_none(self):
		self.assertEqual(multiple_json(None), None, "Se requiere un fichero de entrada")
	def test_multiplejson_empty(self):
		self.assertEqual(multiple_json(""), None, "Se requiere un fichero de entrada")

class Testelastic(unittest.TestCase):
	def test_concept_extraction_none1(self):
		es=None
		list_keywords=["prueba"]
		mode=0
		model=0
		reach=0
		self.assertEqual(concept_extraction(es,list_keywords,mode,model,reach), None, "Error con el servidor de elasticsearch")
	def test_concept_extraction_none2(self):
		es=es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
		list_keywords=None
		mode=0
		model=0
		reach=0
		self.assertEqual(concept_extraction(es,list_keywords,mode,model,reach), None, "Error de lectura del litado de palabras")
	def test_concept_extraction_none3(self):
		es=es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
		list_keywords=["prueba"]
		mode=None
		model=0
		reach=0
		self.assertEqual(concept_extraction(es,list_keywords,mode,model,reach), None, "Error con el modo de procesamiento")
	def test_concept_extraction_none4(self):
		es=es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
		list_keywords=["prueba"]
		mode=0
		model=None
		reach=0
		self.assertEqual(concept_extraction(es,list_keywords,mode,model,reach), None, "Error con el modelo de procesamiento")
	def test_concept_extraction_none5(self):
		es=es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
		list_keywords=["prueba"]
		mode=0
		model=0
		reach=None
		self.assertEqual(concept_extraction(es,list_keywords,mode,model,reach), None, "Error con el alcance definido")
	def test_extract_list_none1(self):
		es=None
		list_keywords=["prueba"]
		mode=0
		model=0
		reach=0
		self.assertEqual(extract_list(es,list_keywords,mode,model,reach), None, "Error con el servidor de elasticsearch")
	def test_extract_list_none2(self):
		es=es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
		list_keywords=None
		mode=0
		model=0
		reach=0
		self.assertEqual(extract_list(es,list_keywords,mode,model,reach), None, "Error de lectura del litado de palabras")
	def test_extract_list_none3(self):
		es=es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
		list_keywords=["prueba"]
		mode=None
		model=0
		reach=0
		self.assertEqual(extract_list(es,list_keywords,mode,model,reach), None, "Error con el modo de procesamiento")
	def test_extract_list_none4(self):
		es=es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
		list_keywords=["prueba"]
		mode=0
		model=None
		reach=0
		self.assertEqual(extract_list(es,list_keywords,mode,model,reach), None, "Error con el modelo de procesamiento")
	def test_extract_list_none5(self):
		es=es = Elasticsearch(hosts = [{'host': 'localhost', 'port': 9200}])
		list_keywords=["prueba"]
		mode=0
		model=0
		reach=None
		self.assertEqual(extract_list(es,list_keywords,mode,model,reach), None, "Error con el alcance definido")
	def test_search_results_none(self):
		self.assertEqual(search_results(None,"prueba.txt"), None, "Error con el servidor de elasticsearch")
	def test_search_results_none2(self):
		self.assertEqual(search_results("es",None), None, "Error con el archivo a buscar")
	
	def test_insert_concept_results_none(self):
		self.assertEqual(insert_concept_results(None,"prueba.txt","concepts","dato"), None, "Error con el servidor de elasticsearch")
	def test_insert_concept_results_none2(self):
		self.assertEqual(insert_concept_results("es",None,"concepts","dato"), None, "Error de lectura del archivo")
	def test_insert_concept_results_none3(self):
		self.assertEqual(insert_concept_results("es","prueba.txt",None,"dato"), None, "Error con el indice proporcionado")
	def test_insert_concept_results_none4(self):
		self.assertEqual(insert_concept_results("es","prueba.txt","concepts","None"), None, "Error con el dato a insertar")
	def test_insert_list_results_none(self):
		self.assertEqual(insert_list_results(None,"prueba.txt","concepts","dato"), None, "Error con el servidor de elasticsearch")
	def test_insert_list_results_none2(self):
		self.assertEqual(insert_list_results("es",None,"concepts","dato"), None, "Error de lectura del archivo")
	def test_insert_list_results_none3(self):
		self.assertEqual(insert_list_results("es","prueba.txt",None,"dato"), None, "Error con el indice proporcionado")
	def test_insert_list_results_none4(self):
		self.assertEqual(insert_list_results("es","prueba.txt","concepts","None"), None, "Error con el dato a insertar")
if __name__ == '__main__':
    unittest.main()

