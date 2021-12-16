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

def fonction_API(url, ark, date):
	http = urllib3.PoolManager()
	request = http.request('GET', url + ark + "/date&date=" + date)
	xml = request.data
	create_xml_file(xml, "apiarknumero.xml", "w+")
	tree = etree.parse("apiarknumero.xml")
	for issue in tree.xpath("//issue/@ark"):
		print(issue)
		create_csv_file([ark,issue], "arknumero.csv", "a+")

filename = 'datesrevues.csv'
reader = unicode_csv_reader(open(filename))
create_csv_file("", "arknumero.csv", "w+")
with open(filename) as f:
	reader = csv.reader(f, delimiter = ',')
	for row in reader:
		if row:
			ark = row[0]
			date = row[1]
			if(ark):
			    fonction_API("https://gallica.bnf.fr/services/Issues?ark=ark:/12148/", ark, date)

print("Troisième étape réalisée avec succès")