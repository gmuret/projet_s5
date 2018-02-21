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
import string
from nltk import bigrams 
from nltk import ngrams

import nltk

import operator 

"""
CAUTION
This program may not work on Windows or MacOS platform. It is highly recommended to use a Linux Distribution.
This python program was tested on Ubuntu 16.03 with Python3.

This program was designed in the context of Open Law's project "IA et Droit". 
The licence of this program is Open Source and was created students from IMT Atlantic engineering school.


 ####  #####  ##### ###   #     ##    ####### ##           ##
##	## ##  ## ##    ####  #     ##    ##   ##  ##         ##
#	 # #####  ###   ## ## #     ##    #######   ##   #   ##
##	## ##     ##    ##  ###     ##    ##   ##    ## ### ##
 ####  ##     ##### ##   ##     ##### ##   ##     ##   ##


"""

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
		"""
		This class gathers methods to extract the first level of information in a decision from a json database.
		The JSON database must be created with the class Cleaning_csv to avoid conflicts and incompatibility.
		This level of information is composed of indicators, quoted as followed :
		- Cour d'appel
		- numero RG
		- date où le jugement est rendu
		Each indicator is extracted with a method as followed :
		- Cour d'appel 							:		self._id_cour_appel
		- numero rg 							:		self._id_rg
		- date où le jugement est prononcé 		:		self._id_date
		"""
		debug("\n")
		debug("Identification de la cour d'appel..\n")
		self.cour_appel, self.cour_appel_success=self._id_cour_appel(db)
		debug("Identification du numero RG..\n")
		self.rg, self.rg_success=self._id_rg(db)
		debug("Identification de la date..\n")
		self.date, self.date_success=self._id_date(db)
		debug("Enregistrement dans la base de données..\n")
		self._json()
		debug("Done !")

	def _id_cour_appel(self, db):
		"""
		This method gathers 
		"""
		class Cour_appel():
			def __init__(self, terms):
				self.cour_appel=[]
				self.city=""
				self.succes=0
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
		counter=0
		for k in result:
			if k != "" and len(k)<30:
				counter+=1
		return result, counter/(len(result)+1)

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
			for k in range(len(case['content'])):
				if case['content'][k]['section']=="Entete":
					result.append([Rg(case['content'][k]['content']).get_rg(), case['id_case']])
		counter=0
		for k in result:
			if k[0]!="" and len(k[0])<10:
				counter+=1
		return result, counter/(len(result)+1)

	def _id_date(self, db):
		count_all = Counter()
		punctuation = list(string.punctuation)
		stop = stopwords.words('french') + punctuation + ['...','--','de','la','De','La','DE','LA']
		mois = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
		date = []
		manquant = []
		liste_compte = []
		## Generating all the "Entete" tokenized and cleant from all punctuation
		for case in db:
			for k in range(len(case['content'])):
				if case['content'][k]['section']=="Entete":
					terms_stop=case['content'][k]['content']
					for j in range (len(terms_stop[0:96])):
						new_date=[]
						if terms_stop[j] in mois:
							if terms_stop[j+1] == 'deux':
								new_date=[(terms_stop[j-1],terms_stop[j],terms_stop[j+1],terms_stop[j+2],terms_stop[j+3])]
							else:
								new_date=[(terms_stop[j-1],terms_stop[j],terms_stop[j+1])]
							date.append([new_date, case['id_case']])
		counter=0
		for word in date:
			if len(word[0])==2:
				if len(word[0][2])>=2:
					counter+=1
			else:
				counter+=1
		return date, counter/(len(date)+1)

	def _json(self):
		db=[]
		dbjson={}
		dbjson['rg_success']=self.rg_success
		dbjson['city_success']=self.cour_appel_success
		dbjson['date_success']=self.date_success
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
		for content in self.date:
			for case in db:
				if case['id_case']==content[1]:
					case['metadata']['date'] = content[0][0]
		dbjson['content']=db

		with open('./dataset/metadata_lod1.json', 'w', encoding='utf-8') as f:
			json.dump(dbjson, f, indent=4, ensure_ascii=False)
