#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import time
import operator 
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from operator import itemgetter
from itertools import *

def debug(input):
	return sys.stdout.write(str(input)+"\n")

def erase_spaces(text):
	""" CLEANING RULE
	This function will take every word whose letters are seperated by a single space
	"""
	counter=0
	list_index=[]
	# search all the index of words which length is equal at 1, meaning a single character
	for word in text:
		if len(word)==1:
			list_index.append(counter)
		counter+=1
	# search for consecutive characters
	result=[]
	liste=[]
	counter=0
	while counter < len(list_index)-1:
		if list_index[counter+1] - list_index[counter]==1:
			liste=liste+[list_index[counter]]
			counter+=1
		else:
			liste.append(list_index[counter])
			result.append(liste)
			liste=[]
			counter+=1
	liste.append(list_index[counter])
	result.append(liste)

	# search for consecutive characteurs which is bigger than 4 characters
	# and insert it in the text which is going to be analyzed
	for word in result:
		if len(word)>4:
			new_word=""
			for i in word:
				new_word=new_word+str(text[i])
			#text.pop(word[:-1])
			text.insert(word[0], new_word)
			for i in range(len(word)):
				text.pop(word[0]+1)

def 

if __name__ == '__main__':
	path='./db.json'
	A=['RÉFÉRÉ', 'du', ':', '2', 'NOVEMBRE', '2016', 'ORDONNANCE', 'No', '74/', '2016', 'No', 'RG', ':', '16/', '03216', 'Monsieur', 'Ahmed', 'X', '...', 'C/', 'Madame', 'Jihane', 'Y', '...', 'divorcée', 'X', '...', 'Expéditions', 'le', ':', '2', 'NOVEMBRE', '2016', 'Me', 'Véronique', 'PIOUX', 'SELARL', 'DUPLANTIER-MALLET', 'GIRY-ROUICHI', 'T.', 'I.', 'ORLÉANS', 'CHAMBRE', 'COMMERCIALE', 'O', 'R', 'D', 'O', 'N', 'N', 'A', 'N', 'C', 'E', 'LE', 'DEUX', 'NOVEMBRE', 'DEUX', 'MILLE', 'SEIZE', 'Nous']
	erase_spaces(A)
	time.sleep(20)

	with open(path, 'r', encoding='utf-8') as f:
		db_json=json.load(f)
		for case in db_json:
			"""
			# First test to display the JSON
			debug(case['content'][0]['section'])
			debug(case['content'][0]['content'])
			time.sleep(3)
			debug("\n\n")
			"""

			#First statistics with word counter
			count_all = Counter()
			terms_all = [term for term in word_tokenize(case['content'][0]['content'])]
			debug(terms_all)
			# Update the counter
			count_all.update(terms_all)
			# Print the first 5 most frequent words
			debug("\n")
			debug(count_all.most_common(5))
			debug("\n")


