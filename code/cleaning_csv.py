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
						debug(row['filename;line_num;types;text'][counter_before:counter_after])
						line.append(row['filename;line_num;types;text'][counter_before:counter_after])
						counter_before=counter_after
				line.append(row['filename;line_num;types;text'][counter_before:len(row['filename;line_num;types;text'])])
				# then, we extract the name of the section the line belongs. This info is in the line[2]
				self.set_types(line[2])
				# we extract the content of the section line[3]
				self.set_content(line[3])
				debug(line)
				time.sleep(1)

		several_lines=[]
		for row in self.reader:
			#debug(str(Line(row).get_content()))
			several_lines.append(Line(row))


if __name__ == '__main__':
	file='../database_csv/annotations-full.csv'
	csvfile=CasesLibrary(file)