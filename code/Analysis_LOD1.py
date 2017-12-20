#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import csv
import time
import json

import re
import string

from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from collections import Counter


# CAUTION
# This program may not work on Windows or MacOS platform. It requires a specific class for Linux system
# This python program was tested on Ubuntu 16.03 with Python3.

def debug(input):
	"""
	This simple function is useful for debuging any variable in the program
	:param input: must contain a variable the user want to display
	:type input: any
	:return: shows the content of a variable. Please be careful not to print the adress in memory
	:rtype: string
	"""
	return sys.stdout.write(str(input)+"\n")

class Analyse_LOD1:
	def __init__(self, db):
		self.cour_appel=self._id_cour_appel(db)
		self.rg=self._id_rg(db)
		self._json()

	def _id_cour_appel(self, db):
		class Cour_appel():
			def __init__(self, terms):
				self.cour_appel=[]
				self.city=""

				self._detect_cour_appel(terms)

			def _detect_cour_appel(self, terms):
				cour="cour"
				appel="appel"
				for k in range(len(terms)-2):
					word=terms[k]
					word_after=terms[k+1]
					if (cour in word) and (len(word) < len(cour)+2) and (appel in word_after):
						self.cour_appel=[word, word_after, terms[k+2]]
						self.city=terms[k+2]
						debug(self.city)
						break
				
			def get_cour_appel(self):
				return self.cour_appel
			def get_city(self):
				return self.city
		result=[]
		for case in db:
			for k in range(len(case['content'])):
				if case['content'][k]['section']=="Entete":
					result.append([Cour_appel(case['content'][k]['content']).get_city(), case['id_case']])
		debug(len(result))
		return result

	def _id_rg(self, db):
		class Rg():
			"""
			This class will detect the RG code.
			First pattern : "12/", "1234" which leads to RG=12/1234
			Second pattern : "12/1234"
			These patterns are detected if the words surrounded it containes "r", "g", "no", "rg"
			"""
			def __init__(self, terms):
				self.rg=""
				self._detect_rg(terms)
				self._clean_rg()
			def _detect_rg(self, terms):
				r=["r.", "r"]
				g=["g", ".g"]
				rg="rg"
				no="no"

				for k in range(2, len(terms)-2):
					if ("/" in terms[k]) and (len(terms[k])>=2):
						nb="0123456789/"
						alphabet=["r", "r.", "g", ".g", "rg", "no"]
						if ([e for e in alphabet if e==terms[k-1]] != []) and ([e for e in nb if e in terms[k+1]] != []):
							self.rg=terms[k]+terms[k+1]
							break
						elif ([e for e in alphabet if e==terms[k-1]] != []) and not([e for e in nb if e in terms[k+1]] != []):
							self.rg=terms[k]
						elif ([e for e in nb if e in terms[k+1]] != []) and (len(terms[k+1])>=3):
							self.rg=terms[k]+terms[k+1]

			def _clean_rg(self):
				for index, k in enumerate(self.rg):
					alphabet="0123456789/"
					if k not in alphabet:
						self.rg=self.rg.replace(k, "")

			def get_rg(self):
				return self.rg

		result=[]
		for case in db:
			debug("\n")
			debug("ID : "+case['id_case'])
			for k in range(len(case['content'])):
				if case['content'][k]['section']=="Entete":
					result.append([Rg(case['content'][k]['content']).get_rg(), case['id_case']])
			counter=0
		for k in result:
			if k!="":
				counter+=1
		debug("SUCCESS : "+str(counter)+"/"+str(len(result)))
		return result

	def _json(self):
		db=[]
		for content in self.cour_appel:
			dic={}
			dic['id_case']=content[1]
			dic['metadata']={}
			dic['metadata']['cour_appel'] = content[0]
			db.append(dic)
		for content in self.rg:
			for case in db:
				if case['id_case']==content[1]:
					case['metadata']['rg'] = content[0]

		with open('metadata_lod1.json', 'w', encoding='utf-8') as f:
			json.dump(db, f, indent=4, ensure_ascii=False)


