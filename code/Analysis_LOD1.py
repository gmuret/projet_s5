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
		#self.city=self._id_city(db)
		self.cour_appel=self._id_cour_appel(db)

	def _id_cour_appel(self, db):
		class Cour_appel():
			def __init__(self, terms):
				self.cour_appel=[]
				self.city=""

				self._set_cour_appel(terms)

			def _set_cour_appel(self, terms):
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
					result.append(Cour_appel(case['content'][k]['content']).get_city())
		debug(len(result))
		return result

	def _id_rg(self, terms):