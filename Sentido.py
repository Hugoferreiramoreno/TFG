"""@package Sense.py
Documentation for the Sense.py module.
This module extract the sense of a given word through Babelnet web services 
"""
import requests
import json
import sys

class Babel:
	"""!@brief Babelnet service class.
	"""
	service_in = 'https://babelnet.io/v5/'

	def __init__(self, service=None):
		"""!@brief Initialise the Babelnet service .
		!@param self The webservice
		!@param service Set to none by default,  we can change the default route if needed.
		"""
		if service is not None:
			self.service_in = service

	def analiza_post(self, phrase):
		"""!@brief POST function of the Babelnet service .
		!@param self The webservice
		!@param phrase  Word to be analyse.
		"""
		return requests.get(self.service_in+phrase)

	def analiza_get(self, phrase):
		"""!@brief GET function of the Babelnet service .
		!@param self The webservice
		!@param phrase  Word to be analyse.
		"""
		return requests.post(self.service_in, data={'texto': phrase})

	def analiza(self, phrase):
		"""!@brief Retrieves the concepts of a word using Babelnet service .
		!@param self The webservice
		!@param phrase  Word to be analyse.
		"""
		return self.analiza_post(phrase)

if __name__ == "__main__":
	if len(sys.argv) != 2 :
		print ("Usage: python Sense.py word")
		sys.exit(1)
	BInstance= Babel()
	response=BInstance.analiza('getSenses?lemma='+sys.argv[1]+'&searchLang=ES&key=be008762-c570-43f8-9fea-b7656dc5c8c4')
	datos=json.loads(response.text)
	sentidos=set()
	for dato in datos:
		for clave,valor in dato.items():
			if clave == "properties":
				sentidos.add(valor['fullLemma'].lower())
	print(sentidos)