#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Cleaning_csv
import Analysis_LOD1
import Analysis_LOD2
import sys
import json

def debug(input):
	return sys.stdout.write(str(input)+"\n")

if __name__ == '__main__':
	"""
	file='../database_csv/annotations-clean.csv'
	debug("\n")
	debug("Projet Open Law IA & Droit")
	debug("Objectif du programme : Extraction des données d'un dataset et tests de précisions.")
	debug("FIRST STEP : CLEANING CSV AND WRITTING THE JSON DATABASE")
	debug("\n")
	json_db=Cleaning_csv.DatabaseCSV(file)
	path="./db_clean_for_lod1.json"
	with open(path, 'r', encoding='utf-8') as f:
		db_json=json.load(f)
	debug("\n")
	debug("#### LOD 1 ####")
	path='./db_clean_for_lod1.json'
	Analysis_LOD1.Analyse_LOD1(db_json)
	Analysis_LOD2.Analyse_LOD2(db_json)
	"""
	path="./db_base.json"
	Analysis_LOD2.Clustering(path)
