"""
.. module:: ws
   :platform: Unix, Windows
   :synopsis: This module contains the functions related with Grampal ws

.. moduleauthor:: Hugo Ferreira Moreno <hugo.ferreira@estudiante.uam.es>

"""
# -*- coding: utf-8 -*-
import requests

class Grampal:
	"""``Grampal service class``\n
	This class implements all the functionality of the Grampal ws, allowing the tokenize and analyse of a phrase
	"""
	service_in = 'http://leptis.lllf.uam.es/api/grampal/general/'
	def __init__(self, service=None):
		"""Initialise the Grampal service 

		Args:
			service (:obj:`str`): The url of the service

		"""
		if service is not None:
			self.service_in = service

	def analiza_post(self, phrase):
		"""POST function of the Grampal service 

		Args:
			phrase (:obj:`str`): The phrase to be analyse.

		Returns:
			Object: The request object if successful, `None` otherwise.

			The status_code of the response can be checked:
				{
					'200': 'success',\
					'404: 'not found' \
				}

		"""
		if phrase is None:
			print("Error: phrase cannot have a null value")
		return requests.get(self.service_in+phrase)

	def analiza_get(self, phrase):
		"""GET function of the Grampal service 

		Args:
			phrase (:obj:`str`): The phrase to be analyse.

		Returns:
			Object: The request object if successful, `None` otherwise.

			The status_code of the response can be checked:
				{
					'200': 'success', \
					'404': 'not found' \n
				}

		"""
		if phrase is None:
			print("Error: phrase cannot have a null value")
		return requests.post(self.service_in, data={'texto': phrase})

	def analiza(self, phrase):
		"""Analyse a phrase using Grampal's service 

		Args:
			phrase (:obj:`str`): The phrase to be analyse.

		Returns:
			Object: The request object if successful, `None` otherwise.

			The status_code of the response can be checked:
				{
					'200': 'success', \
					'404': 'not found' \n
				}

		"""
		if phrase is None:
			print("Error in analiza function: phrase cannot have a null value")
			return None
		if phrase is "":
			print("Error in analiza function : phrase cannot have an empty value")
			return None
		return self.analiza_get(phrase)

	def info_syntactic(self, phrase):
		"""Parse the response from the Grampal ws extracting the syntactic information

		Args:
			phrase: Phrase to be analyse

		Returns:
			String: The syntactic information if successful, `None` otherwise.

		"""
		if phrase is None:
			print("Error in info_syntactic: phrase cannot have a null value")
			return None
		if phrase is "":
			print("Error in info_syntactic: phrase cannot have an empty value")
			return None
		token = phrase.split("/")
		sin = len(token)
		if token[sin-1].count(",") > 0:
			aux = token[sin-1].split(",")
			info_syntactic = aux[0]
		else:
			info_syntactic = token[sin-1]
		return info_syntactic

	def info_lemma(self, phrase):
		"""Parse the response from the Grampal ws extracting the lemma information

		Args:
			phrase: Phrase to be analyse

		Returns:
			String: The lemma information if successful, `None` otherwise.
		"""
		if phrase is None:
			print("Error in info_lemma: phrase cannot have a null value")
			return None
		if phrase is "":
			print("Error in info_lemma: phrase cannot have an empty value")
			return None
		token = phrase.split("/")
		return token[1]

	def info_orig(self, phrase):
		"""Parse the response from the Grampal ws extracting the word of origin

		Args:
			phrase: Phrase to be analyse

		Returns:
			String: The word of origin of the token
		"""
		if phrase is None:
			print("Error in info_orig: phrase cannot have a null value")
			return None
		if phrase is "":
			print("Error in info_orig: phrase cannot have an empty value")
			return None
		token = phrase.split("/")
		return token[0]
