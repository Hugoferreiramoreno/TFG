
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
from keywords import create_graph_grampal

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
		
	def test_concatenate_candidates_spacy_none(self):
		self.assertEqual(concatenate_candidates_spacy(None,2,"prueba"), None, "El grafo a analizar no puede estar a None")
	def test_concatenate_candidates_spacy_none(self):
		self.assertEqual(concatenate_candidates_spacy(igraph.Graph(),None,"prueba"), None, "Los nodos a analizar no puede estar a None")
	def test_concatenate_candidates_spacy_none(self):
		self.assertEqual(concatenate_candidates_spacy(igraph.Graph(),2,None), None, "El texto a analizar no puede estar a None")

	def test_concatenate_candidates_grampal_none(self):
		self.assertEqual(concatenate_candidates_grampal(None,2,"prueba"), None, "El grafo a analizar no puede estar a None")
	def test_concatenate_candidates_grampal_none(self):
		self.assertEqual(concatenate_candidates_grampal(igraph.Graph(),None,"prueba"), None, "Los nodos a analizar no puede estar a None")
	def test_concatenate_candidates_grampal_none(self):
		self.assertEqual(concatenate_candidates_grampal(igraph.Graph(),2,None), None, "El texto a analizar no puede estar a None")
	
	def test_custom_tokenizer_none(self):
		self.assertEqual(concatenate_candidates_grampal(igraph.Graph(),2,None), None, "El texto a analizar no puede estar a None")

if __name__ == '__main__':
    unittest.main()

