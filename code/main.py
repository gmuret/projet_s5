#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Cleaning_csv
#import Analysis_LOD1

if __name__ == '__main__':
	file='../database_csv/annotations-clean.csv'
	json_db=Cleaning_csv.DatabaseCSV(file)

	path='./db.json'
