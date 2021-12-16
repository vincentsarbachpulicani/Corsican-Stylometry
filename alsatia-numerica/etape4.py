# -*- coding: utf-8 -*-
import csv
import os
import urllib3
from lxml import etree
import re
import sys
import json

def unicode_csv_reader(utf8_data, dialect=csv.excel):
    csv_reader = csv.reader(utf8_data, dialect=dialect)
    for row in csv_reader:
    	yield [unicode(cell, 'utf-8') for cell in row]

def create_xml_file(content, name, arg):
    path = '/home/vincsarb/dev/test/records'
    name = os.path.join(path, name)
    print(name)
    file = open(name, arg)
    file.write(content)
    file.close()


def fonction_API(url, ark):
	http = urllib3.PoolManager()
	request = http.request('GET', url + ark)
	xml = request.data
	create_xml_file(xml, ark + ".xml", "w+")

filename = 'arknumero.csv'
reader = unicode_csv_reader(open(filename))
with open(filename) as f:
	reader = csv.reader(f, delimiter = ',')
	for row in reader:
		coll = row[0]
		ark = row[1]
		if (coll):
			fonction_API("https://gallica.bnf.fr/services/OAIRecord?ark=", ark)

print ("Quatrième étape réalisée avec succès")