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

def debug(input):
	return sys.stdout.write(str(input)+"\n")



if __name__ == '__main__':
	path='./db.json'
	with open(path, 'r', encoding='utf-8') as f:
		db_json=json.load(f)
		