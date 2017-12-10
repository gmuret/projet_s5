#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

# CAUTION
# This program may not work on Windows or MacOS platform. It requires a specific class for Linux system
# This python program was tested on Ubuntu.

def write(input):
	return sys.stdout.write(str(input)+"\n")

# This function tranforms a xml file in a simple text file.
if __name__ == '__main__':
	#os.system("sed -e 's/<[^>]*>//g' ./JURITEXT000034222787.xml > output")
	#os.system("subl output")
	PATH = "../database_xml"
	for path, dirs, files in os.walk(PATH):
		for filename in files:
			fullpath = os.path.join(path, filename)
			file_xml = open(fullpath, "r")
			file_txt = open("../database_txt/"+str(filename), "w")
			for line in file_xml:
				p=re.sub(r'\<.*?\>\ *', '', line)
				#write(p)
				file_txt.write(p)
			file_xml.close()
			file_txt.close()

# L'information est disponible dans le paragraphe MOTIF
# On va regarder directement lee texte de LIEGIFRANCE
# MOTIF > paragraphe > FAITS PROCEDURES = on zone localement le paragraphe
# on applique des algorithmes de text mining