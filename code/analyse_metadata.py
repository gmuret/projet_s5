#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import string

from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords

# CAUTION
# This program may not work on Windows or MacOS platform. It requires a specific class for Linux system
# This python program was tested on Ubuntu.

def debug(input):
	return sys.stdout.write(str(input)+"\n")

# This function detects all sections of a decision
def detect_section(path):


def text_cleaning(path):
	file = open(path, 'r')

	# First step : tokenisation 
	tokenized_reports = [word_tokenize(report) for report in file]
	debug(tokenized_reports)

	# Step 2 : delete ponctuation
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	tokenized_reports_no_punctuation = []
	for review in tokenized_reports:
		new_review = []
		for token in review: 
			new_token = regex.sub(u'', token)
			if not new_token == u'':
				new_review.append(new_token)
		tokenized_reports_no_punctuation.append(new_review)

	debug(tokenized_reports_no_punctuation)

	# Step 3 : delete filler words
	tokenized_reports_no_stopwords = []
	for report in tokenized_reports_no_punctuation:
		new_term_vector = []
		for word in report:
			if not word in stopwords.words('english'):
				new_term_vector.append(word)
		tokenized_reports_no_stopwords.append(new_term_vector)

	debug(tokenized_reports_no_stopwords)

if __name__ == '__main__':
	path="../test_environment/JURITEXT000034094700.xml"
	tokenization(path)