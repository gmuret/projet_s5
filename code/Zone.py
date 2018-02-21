#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import csv
import time
import json
from random import randint

import re
import string

from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from collections import Counter
import string
from nltk import bigrams 
from nltk import ngrams
from nltk.stem.snowball import SnowballStemmer

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

class Clustering_delimiter_first_idea:
	"""docstring for Clustering_delimiter"""

	def __init__(self, path):
		with open(path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)
		Clean_dataset_for_extraction(dbjson)
		path="./dataset/db_clean_for_zone.json"
		with open(path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)
		data=[]
		label=[]
		for case in dbjson:
			debug("Looking at "+str(case['id_case']))
			for k in range(len(case['content'])):
				if case['content'][k]['section']=='Entete':
					data.append(case['content'][k]['content'])
					label.append(0)
				if case['content'][k]['section']=="Expose_litige":
					data.append(case['content'][k]['content'])
					label.append(1)
				if case['content'][k]['section']=="Motif_de_la_decision":
					data.append(case['content'][k]['content'])
					label.append(2)
				if case['content'][k]['section']=="Dispositif":
					data.append(case['content'][k]['content'])
					label.append(3)
		np.set_printoptions(threshold=np.nan)

		data_trained = data[0:600]

		count_vect = CountVectorizer()
		X_token = count_vect.fit_transform(data_trained)

		tfidf_transformer = TfidfTransformer()
		X_transformer = tfidf_transformer.fit_transform(X_token)

		clf = MultinomialNB().fit(X_transformer, label[0:600])

		test=data[601:len(data)]
		X_new_count= count_vect.transform(test)
		X_new_tfidf = tfidf_transformer.transform(X_new_count)

		predicted = clf.predict(X_new_tfidf)

		debug("Predicted : "+ str(predicted))
		debug("Theorical : "+ str(label[601:len(data)]))
		debug("NP MEAN : "+ str(np.mean(predicted==label[601:len(data)])))

		"""
		path="../database_txt/JURITEXT000006939781.xml"
		Clean_new_decision(path)

		new_path="new_text.json"
		with open(new_path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)

		for key in dbjson.keys():
			for line in dbjson[key]:
				terms_all=[term.lower() for term in word_tokenize(line)]
				debug(str(terms_all))
		"""

class Clustering_delimiter_second_idea:
	"""docstring for Clustering_delimiter"""
	def __init__(self, path):

		################## TRAINING

		# je prend le json de base 
		"""
		with open(path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)

		Clean_dataset_for_extraction(dbjson)
		"""
		path="./dataset/db_clean_for_zone.json"
		self.data_for_training=[]
		self.keys=[]
		self.data_predicted=[]
		cursor_length=20
		stride=1
		self._build_dataset_for_training(path, cursor_length, stride)

		np.set_printoptions(threshold=np.nan)

		self._create_model(self.data_for_training, self.label)
		self._testing_trained_dataset(path)
		debug("NEW TEST\n")
		path="./dataset_for_prediction/JURITEXT000034284320.xml"
		self._new_file_for_prediction(path, cursor_length, stride)
		debug("NEW TEST\n")

		path="./dataset_for_prediction/JURITEXT000034284365.xml"
		self._new_file_for_prediction(path, cursor_length, stride)
		debug("NEW TEST\n")

		path="./dataset_for_prediction/JURITEXT000034284498.xml"
		self._new_file_for_prediction(path, cursor_length, stride)
		debug("NEW TEST\n")

		path="./dataset_for_prediction/JURITEXT000034284556.xml"
		self._new_file_for_prediction(path, cursor_length, stride)
		debug("NEW TEST\n")

		path="./dataset_for_prediction/JURITEXT000034284652.xml"
		self._new_file_for_prediction(path, cursor_length, stride)
		debug("NEW TEST\n")

		path="./dataset_for_prediction/JURITEXT000034284674.xml"
		self._new_file_for_prediction(path, cursor_length, stride)
		debug("NEW TEST\n")
		
		

		"""
		path="../database_txt/JURITEXT000006939781.xml"
		Clean_new_decision(path)

		new_path="new_text.json"
		with open(new_path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)

		for key in dbjson.keys():
			for line in dbjson[key]:
				terms_all=[term.lower() for term in word_tokenize(line)]
				debug(str(terms_all))
		"""

	def _build_dataset_for_training(self, path, cursor_length, stride):
		with open(path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)
		data=[]
		self.label=[]
		debug("PREAPRING DATASET FOR TRAINING\n")
		for case in dbjson:
			debug("Preparing "+str(case['id_case']))
			self.keys.append(case['id_case'])
			for k in range(len(case['content'])):
				temp=case['content'][k]['content']
				if case['content'][k]['section']=="Entete":
					if len(temp)-cursor_length>0:
						index=randint(0, len(temp)-cursor_length)
						data.append(self._list_to_string(temp[index:index+cursor_length]))
						self.label.append(0)
#					text_split=self._split_text(temp, cursor_length, stride)
					#new=[self._list_to_string(line) for line in self._split_text(temp, cursor_length, stride)]
#					new=text_split
#					data=data+new
					#for i in range(len(new)):
#					self.label.append(0)
				if case['content'][k]['section']=="Expose_litige":
					text_split=self._split_text(temp, cursor_length, stride)
					#data.append(self._list_to_string(text_split[0]))
					#self.label.append(1)
					#new=[self._list_to_string(line) for line in text_split]
					new=self._list_to_string(text_split)
					data.append(new)
					debug(new)
					#for i in range(len(new)):
					self.label.append(1)
				if case['content'][k]['section']=="Motif_de_la_decision":
					if len(temp)-cursor_length>0:
						index=randint(0, len(temp)-cursor_length)
						data.append(self._list_to_string(temp[index:index+cursor_length]))
						self.label.append(0)
#					text_split=self._split_text(temp, cursor_length, stride)
#					#data.append(self._list_to_string(text_split[0]))
#					#self.label.append(3)
#					#new=[self._list_to_string(line) for line in text_split]
#					new=text_split
#					data=data+new
#					#for i in range(len(new)):
#					self.label.append(4)
				if case['content'][k]['section']=="Dispositif":
					if len(temp)-cursor_length>0:
						index=randint(0, len(temp)-cursor_length)
						data.append(self._list_to_string(temp[index:index+cursor_length]))
						self.label.append(0)
#					text_split=self._split_text(temp, cursor_length, stride)
#					#data.append(self._list_to_string(text_split[0]))
#					#self.label.append(5)
#					#new=[self._list_to_string(line) for line in text_split]
#					new=text_split
#					data=data+new
#					#for i in range(len(new)):
#					self.label.append(6)
		self.data_for_training=data
		debug(len(data))
		debug(len(self.label))

	def _create_model(self, data_trained, label):
		debug("TRAINING STEP, please wait\n")
		self.count_vect = CountVectorizer()
		self.X_token = self.count_vect.fit_transform(data_trained)

		self.tfidf_transformer = TfidfTransformer()
		self.X_transformer = self.tfidf_transformer.fit_transform(self.X_token)

		self.clf = MultinomialNB().fit(self.X_transformer, label)
		debug("DONE!\n")


	def _new_file_for_prediction(self, path, cursor_length, stride):
		dbjson=Clean_new_decision(path).get_dbjson()

		text=dbjson['clean']
		text_to_predict=[]

		k=0

		while k<len(text)-cursor_length:
			text_to_predict.append(self._list_to_string(self._split_text(text[k:-1], cursor_length, stride)))
			k+=stride

		X_new_count = self.count_vect.transform(text_to_predict)
		X_new_tfidf = self.tfidf_transformer.transform(X_new_count)

		predicted = self.clf.predict(X_new_tfidf)
		debug(predicted)

	#def _matrix_predicted(self, predicted):
		


	def _testing_trained_dataset(self, path):

		debug("BEGINING TEST OF THE MODEL\n")
		with open(path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)
		

		X_new_count = self.count_vect.transform(self.data_for_training)
		X_new_tfidf = self.tfidf_transformer.transform(X_new_count)

		predicted = self.clf.predict(X_new_tfidf)
		debug("Rate error : "+ str(1-np.mean(predicted==self.label)))


	def _list_to_string(self, arr):
		text=""
		for word in arr:
			text=text+word+" "
		return text
	def _split_text(self, list_words, cursor_length, stride):
		"""
		if len(list_words)>cursor_length:
			index=0
			test=[]
			while index+cursor_length<len(list_words):
				test.append(list_words[index:index+10])
				index+=stride
			return test
		else:
			return list_words
		"""
		if len(list_words)>cursor_length:
			return list_words[0:cursor_length]
			debug(" LIST = " + str(list_words[0:cursor_length]))
		else:
			return list_words


class Clean_new_decision:
	def __init__(self, path):
		self.file=open(path, 'r')
		self.dbjson={}
		self.dbjson['initial']=self._initial_text()
		self.dbjson['clean']=self._clean_text()
		new_path='./new_text.json'
		with open(new_path, 'w', encoding='utf-8') as f:
			json.dump(self.dbjson, f, indent=4, ensure_ascii=False)
		self.file.close()

	def get_dbjson(self):
		return self.dbjson

	def _initial_text(self):
		content=[]
		for line in self.file:
			if line!="\n":
				content.append(line)
		oneline=""
		for line in content:
			oneline=oneline + " "+line
		return oneline

	def _clean_text(self):
		return Clean_text(self.dbjson['initial']).get_text()

class Clean_dataset_for_extraction:
	def __init__(self, dbjson):
		debug("CLEANING FOR ZONE SPLIT\n")
		for case in dbjson:
			debug("Looking at "+str(case['id_case']))
			for k in range(len(case['content'])):
				case['content'][k]['content']=Clean_text(case['content'][k]['content']).get_text()

		with open('./dataset/db_clean_for_zone.json', 'w', encoding='utf-8') as f:
			json.dump(dbjson, f, indent=4, ensure_ascii=False)

class Clean_text:
	def __init__(self, text):
		self.text=[term.lower() for term in word_tokenize(text)]
		self._erase_spaces(self.text)
		self._erase_punctuation(self.text)
		self._erase_little_words(self.text)

	def get_text(self):
		return self.text

	def _erase_punctuation(self, text):
		punctuation = list(string.punctuation)
		stop = stopwords.words('french') + punctuation + ['...','--','de','la','De','La','DE','LA', 'du', 'au', '*']
		self.text = [term.lower() for term in self.text if term.lower() not in stop]
		stemmer = SnowballStemmer("french")
		#self.text=[stemmer.stem(text) for text in self.text]

	def _erase_spaces(self, text):
		""" CLEANING RULE
		This function will take every word whose letters are seperated by a single space
		"""
		counter=0
		list_index=[]

		# Looking for all indexes of words whose lengths are equal at 1, meaning a single character
		for word in text:
			if len(word)==1:
				list_index.append(counter)
			counter+=1

		# Looking for consecutive characters
		word=[]
		counter=0
		while counter < len(list_index)-1:
			if list_index[counter+1] - list_index[counter]==1:
				word=word+[list_index[counter]]
				to_be_treated=False
				if counter+1==len(list_index)-1:
					to_be_treated=True
			else:
				word.append(list_index[counter])
				to_be_treated=True
			if to_be_treated:
				if len(word)>4:
					new_word=""
					for i in word:
						new_word=new_word+str(text[i])
					text.insert(word[0], new_word)
					for i in range(len(word)):
						text.pop(word[0]+1)
					for k in range(counter,len(list_index)):
						list_index[k]=list_index[k]-len(word)+1

				word=[]
			counter+=1
	def _erase_little_words(self, text):
		k=0
		while k<len(text):
			if len(text[k])<2:
				temp=text.pop(k)
			else:
				k+=1
