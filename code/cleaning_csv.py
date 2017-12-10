#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import csv
import time

# CAUTION
# This program may not work on Windows or MacOS platform. It requires a specific class for Linux system
# This python program was tested on Ubuntu.

def debug(input):
	return sys.stdout.write(str(input)+"\n")

class CasesLibrary:
	def __init__(self, file):
		csvfile=open(file, 'r')
		self.reader = csv.DictReader(csvfile)
		self.create_database()
		csvfile.close()
	
	def create_database(self):
		class Line:
			"""
			This class selects relevant information in one line of the CSV-database
			 
			"""
			def __init__(self, row):
				self.types=""
				self.content=""
				self.create_line(row)

			def set_types(self, type):
				self.types=type

			def set_content(self, cont):
				self.content=cont

			def get_types(self):
				return self.types

			def get_content(self):
				return self.content

			def create_line(self, row):
				# we seperate all the fields seperated by a ';' in a line
				line = []
				counter_before = 0
				counter_after = 0
				for letters in row['filename;line_num;types;text']:
					counter_after+=1
					if letters == ';':
						line.append(row['filename;line_num;types;text'][counter_before:counter_after])
						counter_before=counter_after
				line.append(row['filename;line_num;types;text'][counter_before:len(row['filename;line_num;types;text'])])
				# then, we extract the name of the section the line belongs. This info is in the line[2]
				self.set_types(line[2])
				# we extract the content of the section line[3]
				self.set_content(line[3])

		class Sections(Line):
			# TODO : ignore the n_a
			def __init__(self, reader):
				self.sections={}
				lines=[]
				for row in reader:
					#debug(str(Line(row).get_content()))
					lines.append(Line(row))
				self.create_section(lines)

			def create_section(self, lines):
				actual_section=""
				contents=""
				for row in lines:
					if actual_section == row.get_types():
						contents=contents + " " + row.get_content()
					else:
						debug("Actual section : "+ str(actual_section))
						debug("contents : "+str(contents))
						debug("\n")
						self.sections[actual_section]=contents
						actual_section=row.get_types()
						contents=""
						contents=contents + " " + row.get_content()
						time.sleep(0.5)

		new_section = Sections(self.reader)

if __name__ == '__main__':
	file='../database_csv/annotations-full.csv'
	csvfile=CasesLibrary(file)