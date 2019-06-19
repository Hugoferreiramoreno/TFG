"""@package listar_keywords.py
Documentation for the listar_keywords module.
This module allows the creation of a list of unique keywords
"""
import os
import glob
import re

total= set()
for filename in glob.glob('*.txt'):
	archivo=open(filename,"r",encoding="utf-8")
	for linea in archivo:
		prueba=re.sub(r'[^\w+ -.]', '', linea)
		prueba=prueba.strip()
		total.add(prueba.lower())
f= open("todos.txt","w",encoding="utf8")
for cosa in total:
	print(cosa,file=f)
f.close()