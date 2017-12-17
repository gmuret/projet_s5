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

	if len(list_index)-1>0:
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
			debug("The new word is : "+str(new_word))
			text.insert(word[0], new_word)
			for i in range(len(word)):
				text.pop(word[0]+1)
			return True
		return False

class DatabaseCSV:
	def __init__(self, file):
		csvfile=open(file, 'r')
		self.reader = csv.DictReader(csvfile, dialect='excel')
		self.create_database()
		csvfile.close()
	
	def create_database(self):
		class Line:
			"""
			This class selects relevant information in one line of the CSV-database
			It works with a normalized csv database only, which is defined as followed:
			Column A: ID
			Column B: Number of line
			Column C: type
			Column D: Content
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
				self.set_types(row['types_macro'])
				# we extract the content of the section line[3]
				self.set_content(row['text'])
				self.set_id(row['file'])
				self.set_numline(row['line_num'])

		class ParseCases(Line):
			# TODO : ignore the n_a
			# TODO : find a better solution for giving a name / id for each case
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
				return sections
			def conv_json(self, db):
				with open('db.json', 'w', encoding='utf-8') as f:
					json.dump(db, f, indent=4, ensure_ascii=False)

		no = ParseSections(self.reader)

if __name__ == '__main__':
	file='../database_csv/annotations-clean.csv'
	csvfile=DatabaseCSV(file)

	path='./db.json'
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
		debug("Looking at "+str(case['id_case']))
		# FIRST CLEANING : SPACES BETWEEN LETTERSE WITHIN A WORD
		for k in range(len(case['content'])):
			count_all = Counter()
			terms_all = [term for term in word_tokenize(case['content'][k]['content'])]
			# Update the counter
			count_all.update(terms_all)
			if erase_spaces(terms_all):
				debug(case['id_case']+"\n")

#214 et 145