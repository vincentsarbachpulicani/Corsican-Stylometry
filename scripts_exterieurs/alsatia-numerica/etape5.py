import csv
import os
import urllib3
from lxml import etree
import re
import sys
import json

n = 0    # on définit 'n' à 0, cela nous servira à rentrer l'identifiant facilement
path = '/home/vincsarb/dev/test/records'  # ces prochaines lignes nous servent à rentrer dans un dossier définit et à lire tous les fichiers .xml qui s'y trouvent
for filename in os.listdir(path):   # donc pour chaque fichiers .xml présent dans le dossier, il faut effectuer le cript suivant
    if not filename.endswith('.xml'): continue
    fullname = os.path.join(path, filename)
    tree = etree.parse(fullname)

    for title in tree.xpath('//dc:title', namespaces={    # cette boucle va chercher le titre dans la balise <dc:title>
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'dc': "http://purl.org/dc/elements/1.1/"
    }
    ):
        title = title.text
        print(title)
    
    for creator in tree.xpath('//dc:creator', namespaces={   # cette boucle va chercher le la société d'histoire (auteure) dans la balise <dc:creator>
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'dc': "http://purl.org/dc/elements/1.1/"
    }
    ):
        creator = creator.text
        if bool(creator) == 1:   # pour éviter d'avoir des données en trop (du genre ". Auteur du texte"), on isole seulement la partie intéressante avec une expression régulière
            creatorre = "(.+)(\.)" 
            if re.search(creatorre, creator): 
                creator = re.search(creatorre, creator).group(1)
                print(creator)


    for date in tree.xpath('//dc:date', namespaces={  # cette boucle va chercher l'année dans la balise <dc:date>
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'dc': "http://purl.org/dc/elements/1.1/"
    }
    ):
        date = date.text
        if bool(date) == 1: 
            datere = "([0-9]{4})" # étant donné nos besoins pour la mapping avec heurist, on isole seulement l'année de publication
            if re.search(datere, date): 
                date = re.search(datere, date).group(1)
                print(date)

    for numero in tree.xpath('//dc:description', namespaces={ # cette boucle va chercher le numéro dans la balise <dc:description>
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'dc': "http://purl.org/dc/elements/1.1/"
    }
    ):
        numero = numero.text
        numerore = "(.+)(\((.+)\))(.+)"  # il existe plusieurs balises <dc:description>, on va donc prendre celle qui nous inétresse, où il y a le numéro de la revue
        if bool(numero) == 1 :
            if re.search(numerore, numero) :
                tome = re.search(numerore, numero).group(3)
                print(tome)

    for publi in tree.xpath('//dc:publisher', namespaces={   # cette boucle va chercher les informations sur l'éditeur dans la balise <dc:publisher>
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'dc': "http://purl.org/dc/elements/1.1/"
    }
    ):
        publi = publi.text
        if bool(publi) == 1: 
            publire = "(.+)(\((.+)\))" # dans une même balise, deux infos nous intéresse, on va donc créer des groupes avec une expression régulière pour isoler ces informations
            if re.search(publire, publi): 
                edi = re.search(publire, publi).group(1)  # le groupe 1 correspond à l'éditeur (si mentionné)
                print(edi)
                place = re.search(publire, publi).group(3)  # le groupe 3 correspond au lieu d'édition
                print(place)

    for url in tree.xpath('//dc:identifier', namespaces={   # cette boucle va chercher le lien hypertexte dans la balise <dc:identifier>
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'dc': "http://purl.org/dc/elements/1.1/"
    }
    ):
        url = url.text
        print(url)
        if bool(url) == 1: 
            heberre = "(gallica)" # on a l'url, on peut en profiter pour récupérer l'hébergeur. ce n'ets pas obligatoire mais c'est pour être sûr que ce soir toujours Gallica
            if re.search(heberre, url): 
                heber = re.search(heberre, url).group(1)
                print(heber)

    for source in tree.xpath('//dc:source', namespaces={   # cette boucle va chercher le dépositaire dans la balise <dc:source>
    'oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'dc': "http://purl.org/dc/elements/1.1/"
    }
    ):
        source = source.text
        if bool(source) == 1: 
            sourcere = "(.+)(,)" # seul le dépositaire nous intéresse, nous n'avons pas besoin de la côte du document, ce n'ets pas le but d'Alsatia Numerica
            if re.search(sourcere, source): 
                source = re.search(sourcere, source).group(1)
                print(source)

    if bool(title) == 1 :  # on reprend 'n', si la boucle recommence...
        n = n + 1   # ... alors on fait le calcul n + 1
    else :    # sinon, on force l'arrêt de la boucle (pas forcément nécessaire, mais c'est une sécurité pour éviter une boucle infinie)
        break

    content = (str(n) + ';' + title + ';' + creator + ';' + date + ';' + "Periodique"+ ';' + tome + ';' + edi + ';' + place + ';' + url + ';' + heber + ';' + source + ';' + date + '\n').encode('utf-8')
    print(content)   # la variable 'content' prend la valeur de toutes les données récupérées jusqu'à présent, on rajoutant les séparateurs et un retour à la ligne à la fin (format de la syntaxe en csv)

    file = open("heurist.csv", "a")  # ici on ouvre le fichier heurist.csv pré-définit manuellement
    file.write(content)  # et on va inscrire la variable 'content', pui fermer le fichier
    file.close()
    # une fois fait, on recommence cette boucle jusqu'à qu'il n'y ait plus aucun fichier à lire pour Python