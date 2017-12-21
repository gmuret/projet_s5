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


from collections import Counter

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from nltk import bigrams 
from nltk import ngrams

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	"""

	with open('db_base.json', 'r', encoding='utf-8') as f:
		db_json=json.load(f)
	#print(f)
	#print (db_json)
	#print(db_json[0])
	#print(db_json[0]["content"][0]["content"])
	#print(len(db_json)) # len de 0 à 463 len = 464
	count_all = Counter()
	punctuation = list(string.punctuation)
	stop = stopwords.words('french') + punctuation + ['...','--','de','la','De','La','DE','LA']
	
	for i in range(len(db_json)):
		## Case 1: text not cleant
		
		# Create a list with all the terms
		
		terms_all = [term for term in word_tokenize(db_json[i]["content"][0]["content"])]
		
			# Update the counter
		#count_all.update(terms_all)
		
		## Case 2: Text cleant
		terms_stop = [term.lower() for term in word_tokenize(db_json[i]["content"][0]["content"]) if term not in stop]
		
			# Update the counter
		#count_all.update(terms_stop)
		
		## Case 3: Bigram
		
		terms_bigram = bigrams(terms_stop)
		
			# Update the counter
		#count_all.update(terms_bigram)
		
		## Case 4: Trigram
		
		terms_trigram = ngrams(terms_stop,3)
		
			# Update the counter
		count_all.update(terms_trigram)
		
	
		
	#Print the first 30 most frequent words
	debug(count_all.most_common(30))


	# In[4]:

	mot = []
	frequency = []

	for i in range(len(count_all.most_common(50))):
		mot.append(count_all.most_common(50)[i][0])
		frequency.append(count_all.most_common(50)[i][1])


	indices = np.arange(len(count_all.most_common(50)))
	plt.bar(indices, frequency, color='r')
	plt.xticks(indices, mot, rotation='vertical')
	plt.tight_layout()
	plt.show()


	# In[7]:


	mot_degueu = []
	frequency_degueu = []

	for i in range(len(count_all.most_common(50))):
		mot_degueu.append(count_all.most_common(50)[i][0])
		frequency_degueu.append(count_all.most_common(50)[i][1])


	indices_degueux = np.arange(len(count_all.most_common(50)))
	plt.bar(indices_degueux, frequency_degueu, color='r')
	plt.xticks(indices_degueux, mot_degueu, rotation='vertical')
	plt.tight_layout()
	plt.show()


	# In[9]:


	mot_bigram = []
	frequency_bigram = []

	for i in range(len(count_all.most_common(20))):
		mot_bigram.append(count_all.most_common(20)[i][0])
		frequency_bigram.append(count_all.most_common(20)[i][1])


	indices_bigram = np.arange(len(count_all.most_common(20)))
	plt.bar(indices_bigram, frequency_bigram, color='r')
	plt.xticks(indices_bigram, mot_bigram, rotation='vertical')
	plt.tight_layout()
	#plt.savefig('bigram.png')
	plt.show()


	# In[11]:


	mot_trigram = []
	frequency_trigram = []

	for i in range(len(count_all.most_common(20))):
		mot_trigram.append(count_all.most_common(20)[i][0])
		frequency_trigram.append(count_all.most_common(20)[i][1])


	indices_trigram = np.arange(len(count_all.most_common(20)))
	plt.bar(indices_trigram, frequency_bigram, color='r')
	plt.xticks(indices_trigram, mot_trigram, rotation='vertical')
	plt.tight_layout()
	#plt.savefig('trigram.png')
	plt.show()
"""







	# Look at the cleant json
	with open('db_clean_for_lod1.json', 'r', encoding='utf-8') as f:
		db_json=json.load(f)
		rg_stats=[]
		rg_stats_before=[]
		rg_stats_after=[]
		for case in db_json:
			for k in range(len(case['content'])):
				if case['content'][k]['section']=="Entete":
					terms = case['content'][k]['content']
					for k in range(2, len(terms)-2):
						if ("/" in terms[k]) and (len(terms[k])>=2):
							rg_stats_before.append(terms[k-1])
							rg_stats.append(terms[k])
							rg_stats_after.append(terms[k+1])


		rg_=[rg_stats, rg_stats_after, rg_stats_before]
		for k in rg_:
			count=Counter()
			count.update(k)
			debug(count.most_common(20))



