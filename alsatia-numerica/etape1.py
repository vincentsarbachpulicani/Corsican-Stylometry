# -*- coding: utf-8 -*-

# Importation de toutes les bibliothèques nécessaires à la réalisation du script
import csv
import os
import urllib3
from lxml import etree
import re
import sys

# Fonction de lecture du fichier .csv en UTF-8

def unicode_csv_reader(utf8_data, dialect=csv.excel): # définition de la fonction
    csv_reader = csv.reader(utf8_data, dialect=dialect) # la variable "csv.reader" prend la valeur de la fonction "reader" (importée de la bibliothèque csv) qui lit le fichier .csv en UTF-8
    for row in csv_reader: # pour chaque ligne du fichier .csv
        yield [unicode(cell, 'utf-8') for cell in row] # on décrypte le code en UTF-8 pour chaque champs

# Fonction de création de fichier
def create_file(content, name, arg): # définition de la fonction avec 3 arguments : le contenu du fichier, le nom du fichier et sa répétition (w=création d'un nouveau à chaque fois / a=on ajoute le contenu au sein du fichier s'il existe déjà)
    file = open(name, arg) # la variable "file" prend la valeur de la fonction "open" (importée de la bibliothèque os) qui vise à ouvrir le fichier demandé
    file.write(str(content) # on demande à la fonction "write" d'écrire le contenu (content) au sein du fichier précédemment ouvert
    file.close() # on ferme le fichier

# Fonction qui interroge automatiquement l'API de Gallica
def fonction_API(url, arg): # définition de la fonction
    http = urllib3.PoolManager() # importation de la fonction permettant de faire des requêtes sur navigateur
    request = http.request('GET', url + '"' + arg + '"') # notre requête correspond à une requête "GET" (récupérer) sur l'url définit les informations d'une notice d'une revue (extraite du fichier .csv)
    xml = request.data # la variable "xml" prend la veleur des données récupérées grâce à notre requête
    create_file(xml, "apicollection.xml", "w+") # on appelle la fonction de création de fichier où on retranscrit la chaîne de caractère de la variable "xml" (content) au sein d'un fichier nommé "apicollection.xml" (name) qui se recréé au fur et à mesure (arg)
    tree = etree.parse("apicollection.xml") # la variable "tree" prend la valeur de la fonction "parse" (importée de la bibliothèque etree) dans le but d'analyser le fichier "apicollection.xml" sous format .xml
    for record in tree.xpath( # ainsi on demande à la fonction "xpath" de parcourir l'arboréscence des champs du fichier .xml à la rechere de la balise <dc:relation>, celle où est inscrit l'identifiant ark des revues
            "//srw:record",
            namespaces={ # permet d'identifier les préfixes pour que pyhton puisse les comprendre
              'srw': 'http://www.loc.gov/zing/srw/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
              'dc': 'http://purl.org/dc/elements/1.1/'
              }
    ):
        for dctype in record.xpath( # ainsi on demande à la fonction "xpath" de parcourir l'arboréscence des champs du fichier .xml à la rechere de la balise <dc:relation>, celle où est inscrit l'identifiant ark des revues
            ".//dc:type",
            namespaces={ # permet d'identifier les préfixes pour que pyhton puisse les comprendre
              'srw': 'http://www.loc.gov/zing/srw/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
              'dc': 'http://purl.org/dc/elements/1.1/'
              }
        ):
            if bool(dctype.text == "publication en série imprimée") or bool(dctype.text ==  "printed serial"):
                for relation in dctype.xpath( # ainsi on demande à la fonction "xpath" de parcourir l'arboréscence des champs du fichier .xml à la rechere de la balise <dc:relation>, celle où est inscrit l'identifiant ark des revues
                    ".//ancestor::srw:record//dc:relation",
                    namespaces={ # permet d'identifier les préfixes pour que pyhton puisse les comprendre
                      'srw': 'http://www.loc.gov/zing/srw/',
                      'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
                      'dc': 'http://purl.org/dc/elements/1.1/'
                      }
                    ):
                    
                    # la variable "relation" prend ainsi la valeur du texte compris entre les balises <dc:relation> que la fonction "xpath" à isoler durant l'étape précédente
                    if relation.text != "": # la fonction "bool" (boolean) permet de savoir si une expression ets vraie ou fausse, dance le cas présent si la variable "relation" contient oui ou non du texte. Ainsi, si c'est le cas...
                        myre = "(cb\w{7,10})" # ...la variable "myre" prend la valeur d'une expression régulière servant à isoler une série de caractère correspondant à l'identifiant ark. Sinon, passer à la suite.
                        if re.search(myre, relation.text): # Si l'existence d'une série de caractère correspondant à l'identifiant ark est avérée...
                            print(arg) # ...alors afficher sur la console le nom de la revue actuellement traitée (permet de voir si le script fonctionne).
                            print(relation.text)
                            content = re.search(myre, relation.text).group(1) + '\n' # puis la variable "content" prend la valeur du groupe isoler par l'expression régulière, ici l'identifiant ark.
                            create_file(content, "arkrevues.csv", "a+") # et enfin rappelle à nouveau la fonction "create_file"  pour retranscrire dans un fichier .csv nommé "arkrevues.csv" l'identifiant ark isolé, l'un après l'autre dans un seul et unique fichier grâce à l'argument "a" et séparés d'un saut à la ligne (\n)  



# Le script commence donc ici, avant cela servait à définir toutes nos fonctions
filename = 'revues2.csv' # la variable "filename" prend la valeur du fichier .csv que nous voulons analyser. Il s'agit ici du .csv exporter depuis Heurist contenant les noms des recues qui nous intéressent. 
reader = unicode_csv_reader(open(filename)) # la variable "reader" prend la valeur de la focntion "unicode_csv_reader", précédément définie et qu'on appelle en précisant qu'on veut ouvrir le fichier inclut dans la variable "filename"
create_file("", "arkrevues.csv", "w+")
for a, b in reader: # ouverture d'un boucle : pour chaque cellules du .csv analysé ...
    fonction_API("https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&maximumRecods=10&startRecord=1&query=dc.title all", b) # ...on appelle la fonction "fonction_api" en précisant l'url de la requête API que nous voulons faire, en ajoutant à chaque fois la valeur de la colonne "b" pour chaque ligne, correspondant dans le .csv aux noms des revues


print("Première étape réalisée avec succès") # A la fin, on affiche sur la conole ce message pour savoir si le script est arrivé au bout.