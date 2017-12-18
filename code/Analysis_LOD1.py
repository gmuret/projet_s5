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

import cleaning_csv

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

class Analyse_LOD:
	def __init__(self, db):
		self.

	def _id_city(self):
		for case in db_json:
		for k in range(len(case['content'])):
			if case['content'][k]['sectino']=="Entete":
				count_all = Counter()
				terms_all = [term.lower() for term in word_tokenize(case['content'][k]['content'])]


if __name__ == '__main__':
	os.system("python3 cleaning_csv.py")
	path='./db.json'
	with open(path, 'r', encoding='utf-8') as f:
		db_json=json.load(f)
	A=Analyse_LOD(db_json)