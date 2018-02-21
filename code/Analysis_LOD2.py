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


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD

from sklearn import metrics
import numpy as np

from sklearn.naive_bayes import MultinomialNB

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

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

class Analyse_LOD2:
	def __init__(self, db):
		debug("\n")
		debug("Identification du fondement juridique..\n")
		self.fondement_juridique =self._id_fondement_juridique(db)
		debug("Enregistrement dans la base de données..\n")
		self._json()
		debug("Done !")

	def _id_fondement_juridique(self, db):
		class Fondement_juridique():
			"""docstring for Fondement_juridique"""
			def __init__(self, terms):
				self.fondement_juridique=[]
				k=0
				while k < len(terms)-4:
					detection_text_l=["l."]
					detection_text_r=["r."]
					detection_text_article = "article"
					figures="1234567890"
					if terms[k] in detection_text_l and terms[k+1][0] in figures:
						self.fondement_juridique.append("l." + terms[k+1])
					if terms[k] in detection_text_r and terms[k+1][0] in figures:
						self.fondement_juridique.append("r." + terms[k+1])
					if terms[k] in detection_text_r or terms[k] in detection_text_l:
						if terms[k][len(terms[k])-1] in figures:
							self.fondement_juridique.append(terms[k])
					if detection_text_article in terms[k] and terms[k+1][0] in figures:
						self.fondement_juridique.append("article "+ terms[k+1] + " " + terms[k+2]+ " " + terms[k+3] + " "+ terms[k+4])
					k+=1
			def get_fondement_juridique(self):
				return self.fondement_juridique

		result_expose_litige=[]
		result_motif_decision=[]
		result_dispositif=[]
		for case in db:
			for k in range(len(case['content'])):
				if case['content'][k]['section']=="Expose_litige":
					result_expose_litige.append([Fondement_juridique(case['content'][k]['content']).get_fondement_juridique(), case['id_case']])
				if case['content'][k]['section']=="Motif_de_la_decision":
					result_motif_decision.append([Fondement_juridique(case['content'][k]['content']).get_fondement_juridique(), case['id_case']])
				if case['content'][k]['section']=="Dispositif":
					result_dispositif.append([Fondement_juridique(case['content'][k]['content']).get_fondement_juridique(), case['id_case']])
		return result_expose_litige, result_motif_decision, result_dispositif

		
	def _json(self):
		db=[]
		dbjson={}
		for k in range(len(self.fondement_juridique[0])):
			content1=self.fondement_juridique[0][k]
			content2=self.fondement_juridique[1][k]
			content3=self.fondement_juridique[2][k]
			dic={}
			dic['id_case']=content1[1]
			dic['metadata']={}
			dic['metadata']['fondement_juridique_expose_litige'] = content1[0]
			dic['metadata']['fondement_juridique_motif_decision'] = content2[0]
			dic['metadata']['fondemennt_juridique_dispositif']=content3[0]
			db.append(dic)
		dbjson['content']=db

		with open('metadata_lod2.json', 'w', encoding='utf-8') as f:
			json.dump(dbjson, f, indent=4, ensure_ascii=False)
