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

def create_csv_file(content, name, arg):
	with open(name, arg) as file:
		writer = csv.writer(file)
		writer.writerow(content)

def create_xml_file(content, name, arg):
    file = open(name, arg)
    file.write(content)
    file.close()

def fonction_API(url, arg):
    http = urllib3.PoolManager()
    request = http.request('GET', url + arg + "/date")
    xml = request.data
    create_xml_file(xml, "apidates.xml", "w+")
    tree = etree.parse("apidates.xml")
    for ark in tree.xpath("//year") :
    	year = ark.text
    	if bool(year) == 1: 
            zere = "([0-9]{4})" 
            if re.search(zere, year): 
                content = re.search(zere, year).group(1)
                create_csv_file([arg, content], "datesrevues.csv", "a+")


filename = 'arkrevues.csv'
reader = unicode_csv_reader(open(filename))
create_csv_file("", "datesrevues.csv", "w+")
for a in reader:
	a = json.dumps (a)
	myre = "(cb\w{7,10})"
	if re.search(myre, a):
	    a = re.search(myre, a).group(1)
	    print (a)
	    fonction_API("https://gallica.bnf.fr/services/Issues?ark=ark:/12148/", a)

print("Deuxième étape réalisée avec succès")

