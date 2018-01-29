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


class Clustering:
	def __init__(self, path):
		with open(path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)

		data=[]
		label_predicted=[]
		for case in dbjson:
			for k in range(len(case['content'])):
				if case['content'][k]['section']=='Entete':
					data.append(case['content'][k]['content'])
					label_predicted.append(0)
				if case['content'][k]['section']=="Expose_litige":
					data.append(case['content'][k]['content'])
					label_predicted.append(1)
				if case['content'][k]['section']=="Motif_de_la_decision":
					data.append(case['content'][k]['content'])
					label_predicted.append(2)
				if case['content'][k]['section']=="Dispositif":
					data.append(case['content'][k]['content'])
					label_predicted.append(3)
		np.set_printoptions(threshold=np.nan)

		data_trained = data[0:300]


		count_vect = CountVectorizer()
		X_token = count_vect.fit_transform(data_trained)
		debug("X = "+str(X_token))

		tfidf_transformer = TfidfTransformer()
		X_transformer = tfidf_transformer.fit_transform(X_token)

		clf = MultinomialNB().fit(X_transformer, label_predicted[0:300])
		"""
		test1=[" + 6ème Chambre A ORDONNANCE No 235 R. G : 16/ 05349 M. Emmanuel X... C/ M. Yves Marie X... Déclare la demande ou le recours irrecevable Copie exécutoire délivrée le : à : REPUBLIQUE FRANCAISE AU NOM DU PEUPLE FRANCAIS COUR D'APPEL DE RENNES ORDONNANCE MISE EN ETAT DU 24 NOVEMBRE 2016 Le vingt quatre Novembre deux mille seize, par mise à disposition au Greffe, après prorogation, Madame Catherine MICHELOD, Magistrat de la mise en état de la 6ème Chambre A, Assistée de Xavier LE COLLEN, faisant fonction de Greffier, Statuant, après réquisitions écrites de Monsieur TOURET de COUCY, substitut général, dans la procédure opposant : DEMANDEUR A L'INCIDENT : Monsieur Emmanuel X... ... 00000 DIRE DA WA (ETHIOPIE) Représenté par Me Corinne DEMIDOFF de la SELARL EFFICIA, Plaidant, avocat au barreau de RENNES Représenté par Me Eric DEMIDOFF de la SCP SCP GAUVAIN-DEMIDOFF, Postulant, avocat au barreau de RENNES INTIME à DÉFENDEUR A L'INCIDENT : Monsieur Yves Marie X... ... 35240 MARCILLE ROBERT Représenté par Me Anne DAUGAN de la SELARL MARLOT/ DAUGAN/ LE QUERE, avocat au barreau de RENNES APPELANT","SUR CE, L'appel est régulier en la forme et recevable. En vertu de l'article L. 3212-1 du code de la santé publique, une personne atteinte de troubles mentaux ne peut faire l'objet de soins psychiatriques sur la décision du directeur d'un établissement mentionné à l'article L. 3222-1 du même code que lorsque les deux conditions suivantes sont réunies : 1- ses troubles mentaux rendent impossible son consentement, 2- son état mental impose des soins immédiats assortis soit d'une surveillance médicale constante justifiant une hospitalisation complète, soit d'une surveillance médicale régulière justifiant une prise en charge sous la forme mentionnée au 2 de l'article L. 3211-2-1. Madame Aurélie X... a été hospitalisée le 5 octobre 2016 au Centre Hospitalier Georges Mazurelle à LA ROCHE SUR YON, le Docteur Yvette Z..., médecin exerçant dans cette même ville, ayant établi le même jour à 9 heures un certificat médical faisant état d'une décompensation suite à l'arrêt par la patiente de son traitement neuroleptique. Le Docteur Olivier A..., praticien hospitalier ayant examiné Madame Aurélie X... le 6 octobre 2016 à 9h53, a constaté la conviction délirante et l'incohérence des propos de celle-ci ainsi que son absence d'adhésion aux soins psychiatriques. Le Docteur Florence B... et le Docteur Stéphane C..., psychiatres exerçant au sein de l'établissement hospitalier, qui ont successivement examiné Madame Aurélie X... dans les 24 heures et les 72 heures de son admission, ont conclu à la poursuite des soins psychiatriques en hospitalisation complète, la patiente n'ayant pas conscience de ses troubles délirants et son adhésion aux soins étant très fragile. Par décision en date du 8 octobre 2016, Monsieur le Directeur du Centre Hospitalier Georges MAZURELLE a maintenu Madame Aurélie X... en soins psychiatriques sous la forme d'une hospitalisation complète. L'avis médical motivé établi le 10 octobre 2016 par le Docteur Florence B... confirme notamment que Madame Aurélie X... présente des troubles délirants persistants et ne consent pas aux soins. L'avis médical motivé établi le 10 octobre 2016 par le Docteur Florence B... précise que le consentement aux soins n'est toujours pas installé mais que l'apaisement semble s'installer doucement. A l'audience, Madame Aurélie X... reconnaît qu'elle a besoin de soins et accepte d'être suivie, mais en ambulatoire ; elle conteste toutefois le diagnostic des médecins sur l'existence de troubles délirants et explique que le traitement qui lui est prescrit n'est pas adapté. Il ressort des éléments médicaux et des déclarations de Madame Aurélie X... que l'hospitalisation à la demande d'un tiers est intervenue le lendemain du jour où celle-ci s'est présentée volontairement au Centre Hospitalier Georges Mazurelle après l'arrêt d'un traitement neuroleptique considéré par elle comme incompatible avec son état de grossesse présumé ; que l'hospitalisation de Madame Aurélie X... à la demande d'un tiers, justifiée par le refus de celle-ci de poursuivre son traitement et l'aggravation des troubles en résultant, a permis la reprise de soins adaptés et l'amélioration progressive de l'état de santé mental de la patiente, l'adhésion de cette dernière n'étant cependant pas encore acquise. Il est ainsi établi que l'état mental de Madame Aurélie X... rend impossible son consentement et impose des soins immédiats assortis d'une surveillance médicale constante justifiant une hospitalisation complète. L'ordonnance déférée sera, en conséquence, confirmée.",]
		test2 = ["PAR CES MOTIFS La cour, Confirme le jugement rendu par la section agriculture du conseil de prud'hommes de Montpellier le 4 juin 2009 ; Ajoutant : Déboute Mme Carole X... de sa demande tendant à voir incorporer à son contrat de travail 5 jours de congés supplémentaires à titre d'avantage individuel acquis et de ses demandes indemnitaires subséquentes ; Condamne Mme Carole X... aux dépens de la procédure d'appel Dit n'y avoir lieu à condamnation sur le fondement de l'article 700 du code de procédure civile. LE GREFFIER, LE PRÉSIDENT, Cet arrêt fait l'objet d'un pourvoi en cassation formé par la Caisse MSA Languedoc. Il résulte des dispositions de l'article L2261-14 du code du travail que lorsqu'une convention ou un accord n'a pas été remplacé par une nouvelle convention ou un nouvel accord dans les délais précisés au premier alinéa, seuls les avantages individuels acquis résultant de l'accord remis en cause s'incorporent aux contrats de travail. Constitue notamment un avantage collectif, et non un avantage individuel acquis, celui dont le maintien est incompatible avec le respect par l'ensemble des salariés concernés de l'organisation collective du temps de travail qui leur est désormais applicable. Dès lors que l'avantage consistant en 5 jours de congés supplémentaires concernait les conditions de travail de l'ensemble du personnel, son maintien était incompatible avec le respect par les salariés de l'organisation collective applicable puisque cela les conduisait à travailler moins de 35 heures par semaine constituant la durée légale du temps de travail au sein de cette entreprise. Il ne s'agit donc pas d'un avantage individuel acquis par le salarié."]
		test = ["ARRET Cour d'appel de Paris, 24 février 2017, 15/02984 2017-02-24 Cour d'appel de Paris Infirme partiellement, réforme ou modifie certaines dispositions de la décision déférée 15/02984 Pôle 4- Chambre 1 PARIS Grosses délivrées RÉPUBLIQUE FRANÇAISE aux parties le : AU NOM DU PEUPLE FRANÇAIS COUR D'APPEL DE PARIS Pôle 4- Chambre 1 ARRÊT DU 24 FÉVRIER 2017 (no, 7 pages) Numéro d'inscription au répertoire général : 15/ 02984 Décision déférée à la Cour : Arrêt Arrêt Jugement du 24 Septembre 2014- Cour de Cassation de PARIS-RG no A13-21. 005 APPELANT Monsieur Jean-Michel, Gérard X...Affaire renvoyée à la Cour d'Appel de Paris après cassation partielle né le 26 Avril 1965 à LIBOURNE (33500) demeurant ... Représenté par Me Anne DEGRÂCES, avocat au barreau de PARIS, toque : E0893 Assisté sur l'audience par Me Béatrice DU PAYRAT, avocat au barreau de VERSAILLES INTIMÉE Madame Y... divorcée X... née le 25 Août 1965 à PARIS (75014) demeurant .../ FRANCE Représentée par Me Aude LACROIX, avocat au barreau de PARIS, toque : P0483 Assistée sur l'audience par Me Nathalie LE NORMAND, avocat au barreau de VERSAILLES COMPOSITION DE LA COUR : L'affaire a été débattue le 26 Janvier 2017, en audience publique, devant la Cour composée de : Madame Dominique DOS REIS, Présidente de chambre Mme Christine BARBEROT, Conseillère M. Dominique GILLES, Conseiller qui en ont délibéré Madame Dominique DOS REIS a été entendu en son rapport Greffier lors des débats : Monsieur Christophe DECAIX ARRÊT : CONTRADICTOIRE -rendu par mise à disposition de l'arrêt de la Cour, les parties en ayant été préalablement avisées dans les conditions prévues au deuxième alinéa de l'article 450 du code de procédure civile.  signé par Madame Dominique DOS REIS, Présidente et par Monsieur Christophe DECAIX, greffier auquel la minute de la décision à été remise par le magistrat signataire. "]
		"""
		test=data[301:len(data)]
		X_new_count= count_vect.transform(test)
		X_new_tfidf = tfidf_transformer.transform(X_new_count)

		predicted = clf.predict(X_new_tfidf)

		debug("Predicted : "+ str(predicted))
		debug("Theorical : "+ str(label_predicted[301:len(data)]))
		debug("NP MEAN : "+ str(np.mean(predicted==label_predicted[301:len(data)])))


class Clustering_delimiter:
	"""docstring for Clustering_delimiter"""
	def __init__(self, path):
		with open(path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)

		data=[]
		label_predicted=[]
		for case in dbjson:
			for k in range(len(case['content'])):
				if case['content'][k]['section']=='Entete':
					data.append(case['content'][k]['content'])
					label_predicted.append(0)
				if case['content'][k]['section']=="Expose_litige":
					data.append(case['content'][k]['content'])
					label_predicted.append(1)
				if case['content'][k]['section']=="Motif_de_la_decision":
					data.append(case['content'][k]['content'])
					label_predicted.append(2)
				if case['content'][k]['section']=="Dispositif":
					data.append(case['content'][k]['content'])
					label_predicted.append(3)


class Clustering_kmean:
	def __init__(self, path):
		with open(path, 'r', encoding='utf-8') as f:
			dbjson=json.load(f)

		list_index=[e for e in range(len(dbjson))]
		data_trained=[]
		label_predicted=[]
		for case in dbjson:
			for k in range(len(case['content'])):
				if case['content'][k]['section']=='Entete':
					data_trained.append(case['content'][k]['content'])
					label_predicted.append(0)
				if case['content'][k]['section']=="Expose_litige":
					data_trained.append(case['content'][k]['content'])
					label_predicted.append(1)
				if case['content'][k]['section']=="Motif_de_la_decision":
					data_trained.append(case['content'][k]['content'])
					label_predicted.append(2)
				if case['content'][k]['section']=="Dispositif":
					data_trained.append(case['content'][k]['content'])
					label_predicted.append(3)
		np.set_printoptions(threshold=np.nan)


		debug(str(label_predicted))

		vectorizer=CountVectorizer()
		X2=vectorizer.fit_transform(data_trained)
		debug(str(X2.toarray))

		vectorizer = TfidfVectorizer()
		X=vectorizer.fit_transform(data_trained)
		debug(str(X.toarray))

		svd=TruncatedSVD()
		normalizer = Normalizer()
		lsa=make_pipeline(svd, normalizer)
		X2=lsa.fit_transform(X2)

		true_k=4
		km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100000, n_init=1)

		km.fit(X2)

		
		debug("Homogeneity: %0.3f" % metrics.homogeneity_score(label_predicted, km.labels_))
		debug("Completeness: %0.3f" % metrics.completeness_score(label_predicted, km.labels_))
		debug("V-measure: %0.3f" % metrics.v_measure_score(label_predicted, km.labels_))
		debug("Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(label_predicted, km.labels_))
		debug("Silhouette Coefficient: %0.3f"% metrics.silhouette_score(X2, km.labels_, sample_size=1000))

		
		np.set_printoptions(threshold=np.nan)

		debug("KM LABELS : "+str(km.labels_))
		debug("NP MEAN = "+str(np.mean(km.labels_==label_predicted)))

