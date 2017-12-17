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
	A=['RÉFÉRÉ', 'du', ':', '2', 'NOVEMBRE', '2016', 'ORDONNANCE', 'No', '74/', '2016', 'No', 'RG', ':', '16/', '03216', 'Monsieur', 'Ahmed', 'X', '...', 'C/', 'Madame', 'Jihane', 'Y', '...', 'divorcée', 'X', '...', 'Expéditions', 'le', ':', '2', 'NOVEMBRE', '2016', 'Me', 'Véronique', 'PIOUX', 'SELARL', 'DUPLANTIER-MALLET', 'GIRY-ROUICHI', 'T.', 'I.', 'ORLÉANS', 'CHAMBRE', 'COMMERCIALE', 'O', 'R', 'D', 'O', 'N', 'N', 'A', 'N', 'C', 'E', 'LE', 'DEUX', 'NOVEMBRE', 'DEUX', 'MILLE', 'SEIZE', 'Nous']
	erase_spaces(A)
	time.sleep(20)

	with open(path, 'r', encoding='utf-8') as f:
		db_json=json.load(f)
