import csv
import os
import urllib3
from lxml import etree
import re
import sys
import json
import shutil
import requests




def create_csv_file(content, name, arg):
	'''Permet de créer des fichiers .csv'''
	with open(name, arg) as file:
		writer = csv.writer(file)
		writer.writerow(content)

def create_file(content, name, arg):
	'''Permet de lire des fichiers .xml'''
	file = open(name, arg)
	file.write(content)
	file.close()

def api_nameper():
	name_per = str(input("Enter the name of your periodic : "))  #Nom de la revue à définir
	http = urllib3.PoolManager() 
	request = http.request('GET', "https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&maximumRecods=10&startRecord=1&query=dc.title all" + '"' + name_per + '"')
	xml = request.data #Après requête sur l'API de Gallica, on en récupère les données qu'on print dans un nouveau fichier XML
	create_file(xml, "apicollection.xml", "wb") 
	tree = etree.parse("apicollection.xml")
	for record in tree.xpath(  #Phase de parsing où on récupère les métadonnées qui nous intéressent
            "//srw:record",
            namespaces={
              'srw': 'http://www.loc.gov/zing/srw/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
              'dc': 'http://purl.org/dc/elements/1.1/'
              }
    ):
		for dctype in record.xpath(
            ".//dc:type",
            namespaces={ 
              'srw': 'http://www.loc.gov/zing/srw/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
              'dc': 'http://purl.org/dc/elements/1.1/'
              }
        ):
			if bool(dctype.text == "publication en série imprimée") or bool(dctype.text ==  "printed serial"):
				for relation in dctype.xpath( 
                    ".//ancestor::srw:record//dc:relation",
                    namespaces={ 
                      'srw': 'http://www.loc.gov/zing/srw/',
                      'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
                      'dc': 'http://purl.org/dc/elements/1.1/'
                      }
                    ):
                    
						if relation.text != "": #dans la balise <dctype>, on isole l'identifiant ARK
							myre = "(cb\w{7,10})"
							if re.search(myre, relation.text): 
								print("Name of the periodic : ", name_per) 
								print(relation.text)
								content = re.search(myre, relation.text).group(1) + '\n'
								create_file(content, "arkper.csv", "w+")


def api_dates_per(arg): #Une fois qu'on a récupérer l'ARK de la collection, on récupère les années de publication
	'''Permet de récupérer les années de publications des per'''
	http = urllib3.PoolManager()
	request = http.request('GET', "https://gallica.bnf.fr/services/Issues?ark=ark:/12148/" + arg + "/date")
	xml = request.data
	create_file(xml, "apidates.xml", "wb")
	tree = etree.parse("apidates.xml")
	for ark in tree.xpath("//year") :
		year = ark.text
		if bool(year) == 1: 
			zere = "([0-9]{4})" 
			if re.search(zere, year): 
				content = re.search(zere, year).group(1)
				create_csv_file([arg, content], "datesper.csv", "a+")

def api_ark_issue(ark, date): #Enfin on récupère les identifiants ARK de chaque numéros, années après années
	http = urllib3.PoolManager()
	request = http.request('GET', "https://gallica.bnf.fr/services/Issues?ark=ark:/12148/" + ark + "/date&date=" + date)
	xml = request.data
	create_file(xml, "apiarkissue.xml", "wb")
	tree = etree.parse("apiarkissue.xml")
	for issue in tree.xpath("//issue/@ark"):
		with open('arkissue.tsv', 'a') as out_file:
			tsv_writer = csv.writer(out_file, delimiter='\t')
			tsv_writer.writerow([issue, 'gallica', '1', lastpage]) #Dans le fichier TSV créé, on écrit à chaque ligne l'ARk du numéro, 'gallica', "1" et la dernière page (choisie au préalable)
			print("Edition of the periodic treated :", issue)



api_nameper()
lastpage = str(input("Number of pages of periodic issues to download : "))
print("Ark identifier of the periodic collected")

csvfile = open('arkper.csv', newline='')
spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
create_csv_file("", "datesper.csv", "w+")
for a in spamreader:
		a = json.dumps (a)
		myre = "(cb\w{7,10})"
		if re.search(myre, a):
			a = re.search(myre, a).group(1)
			print ("Treated ark code :", a)
			api_dates_per(a)


filename = "datesper.csv"#Création d'un TSV permettant d'être lu par le script IIIF Crawler
csvfile = open(filename, newline='')
spamereader = csv.reader(csvfile, delimiter=' ', quotechar='|')

with open('arkissue.tsv', 'wt') as out_file:  
	tsv_writer = csv.writer(out_file, delimiter='\t')
	tsv_writer.writerow(['ID', 'source', 'start', 'end'])

with open(filename) as f:
	reader = csv.reader(f, delimiter = ',')
	for row in reader:
		if row:
			ark = row[0]
			date = row[1]
			if(ark):
			    api_ark_issue(ark, date)
print("The .tsv file has been created with success")

os.system('python3 iiifcrawler.py arkissue.tsv')
