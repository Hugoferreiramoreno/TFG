"""
.. module:: keywords
   :platform: Unix, Windows
   :synopsis: Documentation for the keywords extraction module, in charge of the keywords extraction.

.. moduleauthor:: Hugo Ferreira Moreno <hugo.ferreira@estudiante.uam.es>

"""
import sys
import os
import re
import spacy
from spacy.tokenizer import Tokenizer
from spacy.attrs import ORTH, LEMMA, POS
import igraph
import numpy
from ws import Grampal

global SYNTACTIC_GROUP
SYNTACTIC_GROUP = ["N", "NOUN", "PROPN", "NPR", "ADJ"]
global MODEL
MODEL = "es_core_news_sm"
global CONNECTORS
CONNECTORS = ["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre", "hasta", "hacia", "para", "por", "según", "sin", "so", "sobre", "tras", "y"]
global EXCLUSIONS
EXCLUSIONS = ["AÑO", "NUEVO", "UNO", "1", "DOS", "2", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "LA", "MILLÓN", "ESTE", "VEZ", "GRACIA", "MISMO", "–"]

class OrderedDict(dict):
	"""``OrderectDict class``\n
	Creates a new Dictionnary data structure that allows multiple append on the same key.

	Args:
		Dict :The data structure Dictionnary.

	"""
	def __setitem__(self, key, value):
		"""Redefine the append on a Dictionnary.

		Args:
			self : The dictionnary.\n
			key (:obj:`str`): The key where whe want to append.\n
			value (:obj:`str`):The value that we append.

		Raises:
			KeyError: When errors with the key.

		"""
		try:
			self[key]
		except KeyError:
			super(OrderedDict, self).__setitem__(key, [])
		self[key].append(value)

def create_graph_grampal(text, k=2):
	"""Create a graph with the keywords and their links using grampal as service.

	Args:
		text (:obj:`str`): The text of origin. \n
		k (:obj:`int`): The correlation value ,by default = 2.

	Returns:
		graph (`igraph`): The graph generated.

	"""
	if text is None:
		print("Error text: The text cannot be void")
		return None
	if k <= 0:
		print("Error k: The correlation value has to be > 0")
		return -1
	graph = igraph.Graph()
	ginstance = Grampal()
	counter = 0
	values = []
	values2 = []
	values3 = []
	uniq = OrderedDict()
	uniq2 = OrderedDict()
	uniq3 = OrderedDict()
	for sentence in text.sents:
		response = ginstance.analiza(sentence.text)
		if response.status_code != 200:
			continue
		lines = response.text.splitlines()
		for i in range(len(lines)):
			if lines[i] != "":
				if ginstance.info_syntactic(lines[i])in SYNTACTIC_GROUP:
					if ginstance.info_lemma(lines[i]) != "UNKN" and ginstance.info_lemma(lines[i]) not in EXCLUSIONS:
						values.append((ginstance.info_lemma(lines[i]), counter))
						values2.append((ginstance.info_lemma(lines[i]), ginstance.info_orig(lines[i])))
						values3.append((ginstance.info_lemma(lines[i]), ginstance.info_syntactic(lines[i])))
				counter += 1

	for node in values:
		uniq[node[0]] = node[1]
	for node in values2:
		uniq2[node[0]] = node[1]
	for node in values3:
		uniq3[node[0]] = node[1]
	for key, value in uniq.items():
		graph.add_vertices(1)
		graph.vs[graph.vcount()-1]["lema"] = key
		graph.vs[graph.vcount()-1]["pos"] = value
		graph.vs[graph.vcount()-1]["orig"] = uniq2.get(key)
		graph.vs[graph.vcount()-1]["occur"] = len(value)
		graph.vs[graph.vcount()-1]["fr"] = round(len(value)/len(uniq), 4)
		graph.vs[graph.vcount()-1]["syntactic"] = uniq3.get(key)[0]
	l_aux = list(uniq.keys())
	for counter in range(0, len(values)):
		for i in range(1, k+1):
			if counter +i < len(values):
				current = values[counter][0]
				jump = values[counter+i][0]
				if current != jump:
					try:
						if graph.get_eid(l_aux.index(current), l_aux.index(jump)):
							pass
					except:
						graph.add_edge(l_aux.index(current), l_aux.index(jump))
	return graph

def create_graph_spacy(text, k=2):
	"""Create a graph with the keywords and their links using spacy as service.

	Args:
		text (:obj:`str`): The text of origin.\n
		k (:obj:`int`): The correlation value ,by default = 2.

	Returns:
		graph (`igraph`): The graph generated.

	"""
	if text is None:
		print("Error text: The length of the text must be len > 0")
		return None
	if k <= 0:
		print("Error k: The correlation value has to be > 0")
		return -1
	graph = igraph.Graph()
	values = []
	values2 = []
	values3 = []
	for sentence in text.sents:
		for token in sentence:
			if token.pos_ in SYNTACTIC_GROUP:
				if token.lemma_.upper() not in EXCLUSIONS:
					values.append((token.lemma_.lower(), token.i))
					values2.append((token.lemma_.lower(), token.text))
					values3.append((token.lemma_.lower(), token.pos_))
	uniq = OrderedDict()
	uniq2 = OrderedDict()
	uniq3 = OrderedDict()
	for node in values:
		uniq[node[0]] = node[1]
	for node in values2:
		uniq2[node[0]] = node[1]
	for node in values3:
		uniq3[node[0]] = node[1]
	for key, value in uniq.items():
		graph.add_vertices(1)
		graph.vs[graph.vcount()-1]["lema"] = key
		graph.vs[graph.vcount()-1]["pos"] = value
		graph.vs[graph.vcount()-1]["orig"] = uniq2.get(key)
		graph.vs[graph.vcount()-1]["occur"] = len(value)
		graph.vs[graph.vcount()-1]["fr"] = round(len(value)/len(uniq), 4)
		graph.vs[graph.vcount()-1]["syntactic"] = uniq3.get(key)[0]
	l_aux = list(uniq.keys())
	for counter in range(0, len(values)):
		for i in range(1, k+1):
			if counter +i < len(values):
				current = values[counter][0]
				jump = values[counter+i][0]
				if current != jump:
					try:
						if graph.get_eid(l_aux.index(current), l_aux.index(jump)):
							pass
					except:
						graph.add_edge(l_aux.index(current), l_aux.index(jump))
	return graph

def pagerank(graph):
	"""Use the Google's pagerank algorithm  to set a value for each node.

	Args:
		graph (`igraph`): Graph to be analyse.

	Returns:
		values (:obj:`list`): The list of values generated.

	"""
	if graph is None:
		print("Error graph: Empty graph")
		return None
	values = graph.pagerank()
	if len(values) <=0:
		print("Error pagerank: No values")
		return -1
	for counter in range(0, len(values)):
		graph.vs[counter]["value"] = round(values[counter], 4)
	return values

def topnodes(graph, top):
	"""Extract the Top nodes with higher values.

	Args:
		graph (`igraph`): Graph to be analyse.\n
		Top (:obj:`int`): Number of nodes we want to get from the top.

	Returns:
		nodes (:obj:`list`): The list of nodes generated.

	"""
	if graph is None:
		print("Error graph: Empty graph")
		return None
	if top < 1:
		print("Error Top: The number of nodes to extract must be > 0")
		return -1
	array = graph.vs["value"]
	nodes = numpy.argsort(array)[-top:][::-1]
	return nodes

def sort_values(graph):
	"""Get an array of the nodes sorted_by_occur by value.

	Args:
		graph (`igraph`): Graph to be analyse.

	Returns:
		nodes (:obj:`list`): The list of nodes generated.

	"""
	if graph is None:
		print("Error graph: Empty graph")
		return None
	array = graph.vs["value"]
	nodes = numpy.argsort(array)[-(len(array)-1):][::-1]
	return nodes

def sort_occurences(graph):
	"""Get an array of the nodes sorted_by_occur by occurence.

	Args:
		graph (`igraph`): Graph to be analyse.

	Returns:
		nodes (:obj:`list`): The list of nodes generated.

	"""
	if graph is None:
		print("Error graph: Empty graph")
		return None
	array = graph.vs["occur"]
	nodes = numpy.argsort(array)[-(len(array)-1):][::-1]
	return nodes

def concatenate_candidates_spacy(graph, nodes, text):
	"""Get the multiwords from the top nodes of the graph using spacy as service.

	Args:
		graph (`igraph`): Graph to be analyse.\n
		nodes (:obj:`list`): The list of top nodes.\n
		text (:obj:`str`): Text of origin.

	Returns:
		nodes (:obj:`list`): The list of the multiwords.

	"""
	if graph is None:
		print("Error graph: Empty graph")
		return None
	if nodes is None:
		print("Error nodes: Top nodes is empty")
		return None
	if  text is None:
		print("Error text: The length of the text must be len > 0")
		return None
	multiword = OrderedDict()
	for node in nodes:
		positions = graph.vs[node]["pos"]
		for pos in positions:
			control = 0
			if pos+1 >= len(text):
				continue
			for node2 in nodes:
				if control == 1:
					break
				elif graph.vs[node]["lema"] == graph.vs[node2]["lema"]:
					continue
				elif pos+1 in graph.vs[node2]["pos"]:
					lema_aux = graph.vs[node]["lema"]+" "+graph.vs[node2]["lema"]
					if lema_aux in multiword:
						multiword[lema_aux] = pos
						control = 1
						break
					else:
						for connector in CONNECTORS:
							lema_aux = graph.vs[node]["lema"]+" "+str(connector)+" "+graph.vs[node2]["lema"]
							if lema_aux in multiword:
								multiword[lema_aux] = pos
								control = 1
								break
						if control == 0:
							lema_aux = graph.vs[node]["lema"]+" "+graph.vs[node2]["lema"]
							multiword[lema_aux] = graph.vs[node]["value"]+graph.vs[node2]["value"]
							multiword[lema_aux] = graph.vs[node]["occur"]+graph.vs[node2]["occur"]
							multiword[lema_aux] = graph.vs[node]["fr"]+graph.vs[node2]["fr"]
							multiword[lema_aux] = (graph.vs[node]["orig"], graph.vs[node2]["orig"])
							multiword[lema_aux] = (graph.vs[node]["syntactic"], graph.vs[node2]["syntactic"])
							multiword[lema_aux] = pos
							control = 1
							break
				elif text[pos+1].text.lower() in CONNECTORS:
					if pos+2 in graph.vs[node2]["pos"]:
						lema_aux = graph.vs[node]["lema"]+" "+text[pos+1].text.lower()+" "+graph.vs[node2]["lema"]
						if lema_aux in multiword:
							multiword[lema_aux] = pos
							control = 1
							break
						else:
							for connector in CONNECTORS:
								lema_aux = graph.vs[node]["lema"]+" "+str(connector)+" "+graph.vs[node2]["lema"]
								if lema_aux in multiword:
									multiword[lema_aux] = pos
									control = 1
									break
							if control == 0:
								lema_aux = graph.vs[node]["lema"]+" "+text[pos+1].text.lower()+" "+graph.vs[node2]["lema"]
								multiword[lema_aux] = graph.vs[node]["value"]+graph.vs[node2]["value"]
								multiword[lema_aux] = graph.vs[node]["occur"]+graph.vs[node2]["occur"]
								multiword[lema_aux] = graph.vs[node]["fr"]+graph.vs[node2]["fr"]
								multiword[lema_aux] = (graph.vs[node]["orig"], graph.vs[node2]["orig"])
								multiword[lema_aux] = (graph.vs[node]["syntactic"], graph.vs[node2]["syntactic"])
								multiword[lema_aux] = pos
								control = 1
								break
	return multiword

def concatenate_candidates_grampal(graph, nodes, text):
	"""Get the multiwords from the top nodes of the graph using spacy as service.

	Args:
		graph (`igraph`): Graph to be analyse.\n
		nodes (:obj:`list`): The list of top nodes.\n
		text (:obj:`str`): Text of origin.

	Returns:
		nodes (:obj:`list`): The list of the multiwords.

	"""
	if graph is None:
		print("Error graph: Empty graph")
		return None
	if nodes is None:
		print("Error nodes: Top nodes is empty")
		return None
	if text is None:
		print("Error text: The length of the text must be len > 0")
		return None
	ginstance = Grampal()
	pos = 0
	control = 0
	multiword = OrderedDict()

	for sentence in text.sents:
		response = ginstance.analiza(sentence.text)
		if response.status_code != 200:
			continue
		lines = response.text.splitlines()
		for i in range(len(lines)):
			control = 0
			if lines[i] != "":
				if i < len(lines)-1:
					for node in nodes:
						if pos in graph.vs[node]["pos"]:
							if control == 1:
								break
							for node2 in nodes:
								if pos+1 in graph.vs[node2]["pos"]:
									lema_aux = graph.vs[node]["lema"]+" "+graph.vs[node2]["lema"]
									multiword[lema_aux] = graph.vs[node]["value"]+graph.vs[node2]["value"]
									multiword[lema_aux] = graph.vs[node]["occur"]+graph.vs[node2]["occur"]
									multiword[lema_aux] = graph.vs[node]["fr"]+graph.vs[node2]["fr"]
									multiword[lema_aux] = (graph.vs[node]["orig"], graph.vs[node2]["orig"])
									multiword[lema_aux] = (graph.vs[node]["syntactic"], graph.vs[node2]["syntactic"])
									multiword[lema_aux] = pos
									control = 1
									break
							if lines[i+1] != "" and control == 0:
								if ginstance.info_lemma(lines[i+1]).lower() in CONNECTORS:
									if i < len(lines)-2:
										for node2 in nodes:
											if pos+2 in graph.vs[node2]["pos"]:
												lema_aux = graph.vs[node]["lema"]+" "+ginstance.info_lemma(lines[i+1]).lower()+" "+graph.vs[node2]["lema"]
												multiword[lema_aux] = graph.vs[node]["value"]+graph.vs[node2]["value"]
												multiword[lema_aux] = graph.vs[node]["occur"]+graph.vs[node2]["occur"]
												multiword[lema_aux] = graph.vs[node]["fr"]+graph.vs[node2]["fr"]
												multiword[lema_aux] = (graph.vs[node]["orig"], graph.vs[node2]["orig"])
												multiword[lema_aux] = (graph.vs[node]["syntactic"], graph.vs[node2]["syntactic"])
												multiword[lema_aux] = pos
												control = 1
				pos += 1
	return multiword

def custom_tokenizer(nlp):
	"""Redefine the custom tokenizer of spacy .

	Args:
		nlp (`nlp`): The tokenizer from spacy.

	Returns:
		nlp (`nlp`): The new custom tokenizer.

	"""
	if nlp is None:
		print("Error nlp: nlp can't be null ")
		return None
	prefix_re = re.compile(r'''^[–—•\[\("']''')
	suffix_re = re.compile(r'''[—•,.\]\)"']$''')
	infix_re = re.compile(r'''[•~]''')
	simple_url_re = re.compile(r'''^https?://''')
	return Tokenizer(nlp.vocab, prefix_search=prefix_re.search, suffix_search=suffix_re.search, infix_finditer=infix_re.finditer, token_match=simple_url_re.match)

def print_graph(graph, path):
	"""Print the graph generated, it was used for validation on small graph, currently unused .

	Args:
		graph (`igraph`): The graph to be printed.\n
		path (:obj:`str`): The path.

	"""
	if graph is None:
		print("Error graph: Empty graph")
		return None
	if path is None:
		print("Error path: Empty path")
		return None
	graph.vs["label"] = graph.vs["lema"]
	igraph.plot(graph, path)

def main(arguments):
	"""Main function of the keywords module.

	Kwargs:
		graph (`igraph`): The graph to be printed.\n
		path (:obj:`str`): The path.

	"""
	ori = arguments[1]
	occurence = int(arguments[2])
	n_nodes = int(arguments[3])
	service = arguments[4]
	directory = os.path.join(os.path.dirname(os.getcwd()), "data", ori+".txt")
	text = open(directory, encoding="utf8").read() # open a document
	file_name = ori+"-"+"keywords"+"-"+service+".txt"
	directory = os.path.join(os.path.dirname(os.getcwd()), "result", "keywords_list", file_name)
	file_to_open = open(directory, "w", encoding="utf8")
	nlp = spacy.load(MODEL)
	nlp.tokenizer = custom_tokenizer(nlp)
	special_case = [{ORTH: '•', LEMMA: '•', POS: 'PUNCT'}]
	nlp.tokenizer.add_special_case('•', special_case)
	special_case2 = [{ORTH: '—', LEMMA: '—', POS: 'PUNCT'}]
	nlp.tokenizer.add_special_case('—', special_case2)
	doc = nlp(text)
	if service == "grampal":
		graph = create_graph_grampal(doc, occurence)
	elif service == "spacy":
		graph = create_graph_spacy(doc, occurence)
	else:
		print("service has to be grampal or spacy")
		sys.exit(1)
	pagerank(graph)
	if len(arguments) == 6 and int(arguments[5]) == 1:
		sorted_by_occur = sort_occurences(graph)
		file_name = ori+"-"+"frequencies"+"-"+service+".txt"
		directory = os.path.join(os.path.dirname(os.getcwd()), "result", "frequencies_list", file_name)
		file_to_open = open(directory, "w", encoding="utf8")
	else:
		sorted_by_occur = sort_values(graph)
	tnodes = topnodes(graph, n_nodes)
	if service == "spacy":
		multi = concatenate_candidates_spacy(graph, tnodes, doc)
	elif service == "grampal":
		multi = concatenate_candidates_grampal(graph, tnodes, doc)
	for key, values in multi.items():
		print(key+"\t"+str(values[0])+"\t"+str(values[1])+"\t"+str(values[2])+"\t"+str(values[3])+"\t"+str(values[4])+"\t"+str(values[5]), file=file_to_open)
	print("", file=file_to_open)
	for node in sorted_by_occur:
		print(str(graph.vs[node]["lema"])+"\t"+str(graph.vs[node]["value"])+"\t"+str(graph.vs[node]["occur"])+"\t"+str(graph.vs[node]["fr"])+"\t"+str(graph.vs[node]["orig"])+"\t"+graph.vs[node]["syntactic"], file=file_to_open) 
if __name__ == "__main__":
	if len(sys.argv) != 5 and len(sys.argv) != 6:
		print("Usage: python keywords.py file co-occurencia topnodes service frequency_flag(optional) \n Service can be grampal or spacy , if frequency_flag =1 the results will be sorted_by_occur by frequency ignoring pagerank values \n Example:python keywords.py 1-BancoSantander_2014 2 5 spacy")
		sys.exit(1)
	main(sys.argv)
