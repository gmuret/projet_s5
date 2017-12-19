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

class Line:
	"""
	This class selects relevant information in one line of the CSV-database
	It works with a specific structure of CSV-database
	Attributes
		:types(str):	the line belongs to a section which is defined in types
		:content(str):	the line has a content 
		:id(str):		the line belongs to a case, identified by an id
		:linenum(int):	it represents the line number
	
	Methods:
		:set_types
		:get_types
		:set_content
		:get_content
		:set_numline
		:get_numline
		:set_id
		:get_id
		:create_line
	"""
	def __init__(self, row):
		self.types=""
		self.content=""
		self.id=""
		self.linenum=0
		self.create_line(row)
	def set_types(self, type):
		self.types=type
	def set_content(self, cont):
		self.content=cont
	def set_numline(self, num):
		self.linenum
	def get_linenum(self):
		return self.linenum
	def set_id(self, new_id):
		self.id=new_id
	def get_id(self):
		return self.id
	def get_types(self):
		return self.types
	def get_content(self):
		return self.content
	def create_line(self, row):
		"""
		It creates the line object by filling in the attributes of the present object
		
		parameters
			:row(str): the row is the line taken from the CSV-database which will be treated by the present method
		"""
		self.set_types(row['types_macro'])
		# we extract the content of the section line[3]
		self.set_content(row['text'])
		self.set_id(row['file'])
		self.set_numline(row['line_num'])

class ParseCases(Line):
	"""
	
	"""
	def __init__(self, reader):
		self.cases={}
		id_before=""
		lines=[] #which contains all the lines of one case
		name="JURI0"
		counter=1
		for row in reader:
			line=Line(row)
			if id_before=="":
				id_before=line.get_id()
			if id_before == line.get_id():
				lines=lines+[line]
			else:
				counter+=1
				new_name=name+str(counter)
				self.cases[new_name]=lines
				lines=[line]
				id_before=line.get_id()
	def get_cases(self):
		return self.cases

class ParseSections(ParseCases):
	def __init__(self, reader):
		#self.db={'id_case':'', 'content' : {'section':'', 'nb_section':'', 'content':''}}
		cases = ParseCases(reader).get_cases()
		self.db=[]
		for case in cases:
			self.db.append({'id_case':case, 'content':self.create_section(cases[case])})
		self.conv_json(self.db)

	def create_section(self, lines):
		contents=""
		nb_section=0
		actual_section=lines[0].get_types()
		sections=[]
		for row in lines:
			if actual_section == row.get_types():
				contents=contents + " " + row.get_content()
			else:
				nb_section+=1
				sections.append({'section':actual_section, 'nb_section':nb_section, 'content':contents})
				contents=row.get_content()
				actual_section=row.get_types()
		sections.append({'section':actual_section, 'nb_section':nb_section, 'content':contents})
		return sections
	def conv_json(self, db):
		with open('db_base.json', 'w', encoding='utf-8') as f:
			json.dump(db, f, indent=4, ensure_ascii=False)

class DatabaseCSV:
	def __init__(self, file):

		# OPENS CSV AND TRANSFORMS THE DATABASE INTO A JSON FILE
		csvfile=open(file, 'r')
		self.reader = csv.DictReader(csvfile, dialect='excel')
		self._create_database()
		csvfile.close()

		# OPENS THE JSON FILE
		path="./db_base.json"
		with open(path, 'r', encoding='utf-8') as f:
			db_json=json.load(f)

		# STARTS THE CLEANING METHODS
		##
		# FIRST CLEANING : SPACES BETWEEN LETTERSE WITHIN A WORD AND ERASE THE PUNCTUATIONS
		for case in db_json:
			debug("Looking at "+str(case['id_case']))
			for k in range(len(case['content'])):
				count_all = Counter()
				# Update the counter

				terms_all = [term.lower() for term in word_tokenize(case['content'][k]['content'])]
				count_all.update(terms_all)
				self._erase_spaces(terms_all)
				terms_all=self._erase_punctuation(case['content'][k]['content'])
				case['content'][k]['content']=terms_all

		with open('db_clean_for_lod1.json', 'w', encoding='utf-8') as f:
			json.dump(db_json, f, indent=4, ensure_ascii=False)

	
	def _create_database(self):
		no = ParseSections(self.reader)
		
	def _erase_punctuation(self, text):
		punctuation = list(string.punctuation)
		stop = stopwords.words('french') + punctuation + ['...','--','de','la','De','La','DE','LA', 'du', 'au']
		terms_stop = [term.lower() for term in word_tokenize(text) if term.lower() not in stop]
		return terms_stop

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

		# Looking for consecutive characteurs which are bigger than 4 characters
		# And inserting them in the text