import re
import lxml
from lxml import etree
import xml.etree.ElementTree as ET
import string
from spellchecker import SpellChecker
import unidecode
import shutil

def clean_text_COS(filename, acc=True, pun=True, low=True):
    '''
    Fonction qui nettoye les rubriques de la revue en corse.

    Entrée : XML
    Sortie : XML

    Paramètres :acc = bool, enlever les accents
                pun = bool, enlever la ponctuation
                low = bool, mettre la casse en minuscule
    '''
    tree = etree.parse(filename)
    ETtree = ET.parse(filename)
    root = ETtree.getroot()
    punc = ['!','+','=','“','”','(',')','-','`','[',']','°','©','{','}',';',':','«','»','"','\\',',','<','>','.','/','?','@','#','%','^','&','*','_','~','—', '–']
    for balise in tree.xpath('//rubrique[@lan="co"]/texte'):
        x = balise.text
        y = x
        if pun is True:
            for character in punc:
                y = y.replace(character, ' ')
        if low is True:
            y = y.lower()
        y = re.sub(r"’", r"'", y)
        y = re.sub(r" 1' ", r" l' ", y)
        y = re.sub(r"'", r" ", y)
        y = re.sub(r"‘", r" ", y)

        y = re.sub(r" altr (\w*u\b)", r" altru \1", y)
        y = re.sub(r" altr (\w*a\b)", r" altra \1", y)
        y = re.sub(r" altr (\w*à\b)", r" altra \1", y)
        y = re.sub(r" altr (\w*e\b)", r" altre \1", y)
        y = re.sub(r" altr (\w*i\b)", r" altri \1", y)
        y = re.sub(r" altr (\w*j\b)", r" altri \1", y)
        y = re.sub(r" altr un ", r" altru un ", y)
        
        y = re.sub(r" l (\w*u\b)", r" lu \1", y)
        y = re.sub(r" l (\w*a\b)", r" la \1", y)
        y = re.sub(r" l (\w*à\b)", r" la \1", y)
        y = re.sub(r" l (\w*e\b)", r" le \1", y)
        y = re.sub(r" l (\w*i\b)", r" li \1", y)
        y = re.sub(r" l (\w*j\b)", r" li \1", y)
        
        y = re.sub(r" quell (\w*u\b)", r" quellu \1", y)
        y = re.sub(r" quell (\w*a\b)", r" quella \1", y)
        y = re.sub(r" quell (\w*à\b)", r" quella \1", y)
        y = re.sub(r" quell (\w*e\b)", r" quelle \1", y)
        y = re.sub(r" quell (\w*i\b)", r" quelli \1", y)
        y = re.sub(r" quell (\w*j\b)", r" quelli \1", y)
        
        y = re.sub(r" ell (\w*i\b)", r" elli \1", y)
        y = re.sub(r" ell (\w*u\b)", r" ellu \1", y)
        y = re.sub(r" ell (\w*a\b)", r" ella \1", y)
        y = re.sub(r" ell (\w*à\b)", r" ella \1", y)
        y = re.sub(r" ell (\w*e\b)", r" elle \1", y)
        y = re.sub(r" ell (\w*j\b)", r" elli \1", y)
        y = re.sub(r" ell un ", r" ellu un ", y)
        
        y = re.sub(r" sott ", r" sottu ", y)
        y = re.sub(r" sopr ", r" sopra ", y)
        
        y = re.sub(r" bon (\w*u\b)", r" bonu \1", y)
        y = re.sub(r" bon (\w*a\b)", r" bona \1", y)
        y = re.sub(r" bon (\w*à\b)", r" bona \1", y)
        y = re.sub(r" bon (\w*e\b)", r" bone \1", y)
        y = re.sub(r" bon (\w*i\b)", r" boni \1", y)
        y = re.sub(r" bon (\w*j\b)", r" boni \1", y)

        
        y = re.sub(r" vostr (\w*u\b)", r" vostru \1", y)
        y = re.sub(r" vostr (\w*a\b)", r" vostra \1", y)
        y = re.sub(r" vostr (\w*i\b)", r" vostri \1", y)
        y = re.sub(r" vostr (\w*e\b)", r" vostre \1", y)
        y = re.sub(r" vostr (\w*à\b)", r" vostra \1", y)
        y = re.sub(r" vostr (\w*j\b)", r" vostri \1", y)
                
        y = re.sub(r" nostr (\w*u\b)", r" nostru \1", y)
        y = re.sub(r" nostr (\w*a\b)", r" nostra \1", y)
        y = re.sub(r" nostr (\w*i\b)", r" nostri \1", y)
        y = re.sub(r" nostr (\w*e\b)", r" nostre \1", y)
        y = re.sub(r" nostr (\w*à\b)", r" nostra \1", y)
        y = re.sub(r" nostr (\w*j\b)", r" nostri \1", y)
        
        y = re.sub(r"€", r"e", y)
        y = re.sub(r"$", r"s", y)
        y = re.sub(r"corsiea", r"corsica", y)
        y = re.sub(r"tl", r"tt", y)
        y = re.sub(r"0", r"o", y)
        y = re.sub(r"\|", r"", y)
        y = re.sub(r"cb", r"ch", y)
        
        y = re.sub(r" dia ", r" di a ", y)
        y = re.sub(r" dii ", r" di i ", y)
        y = re.sub(r" die ", r" di e ", y)
        
        y = re.sub(r"ae ", r"a e ", y)
        y = re.sub(r"au ", r"a u ", y)
        y = re.sub(r" ai ", r" a i ", y)
        y = re.sub(r"aa ", r"e a ", y)
        
        y = re.sub(r"ee ", r"e e ", y)
        y = re.sub(r"eu ", r"e u ", y)
        y = re.sub(r" ei ", r" e i ", y)
        y = re.sub(r" ea ", r" e a ", y)
        
        y = re.sub(r"eun ", r"e un ", y)
        y = re.sub(r"aun ", r"a un ", y)
        y = re.sub(r"auna ", r"a una ", y)
        y = re.sub(r"euna ", r"e una ", y)
        y = re.sub(r"iun ", r"i un ", y)
        y = re.sub(r"uun ", r"u un ", y)
        
        y = re.sub(r" ch ", r" chi ", y)
        y = re.sub(r" c ", r" ci ", y)
        y = re.sub(r" m ", r" mi ", y)
        y = re.sub(r" s ", r" si ", y)
        y = re.sub(r" t ", r" ti ", y)
        y = re.sub(r" d ", r" di ", y)
        y = re.sub(r" n ", r" ne ", y)
        if acc is True:
            y = unidecode.unidecode(y)
        for element in root.findall(".//rubrique"):
            if element.find('texte').text == x :
                element.find('texte').text = y
    ETtree.write(filename,encoding='UTF-8',xml_declaration=True)

def clean_text_ITA(filename, acc=True, pun=True, low=True):
    '''
    Fonction qui nettoye les rubriques de la revue en italien.

    Entrée : XML
    Sortie : XML

    Paramètres :acc = bool, enlever les accents
                pun = bool, enlever la ponctuation
                low = bool, mettre la casse en minuscule
    '''
    tree = etree.parse(filename)
    ETtree = ET.parse(filename)
    root = ETtree.getroot()
    punc = ['!','+','=','“','”','(',')','-','`','[',']','{','}','°',';','©',':','«','»','"','\\',',','<','>','.','/','?','@','#','$','%','^','&','*','_','~','—', '–']
    for balise in tree.xpath('//rubrique[@lan="it"]/texte'):
        x = balise.text
        y = x
        if pun is True:
            for character in punc:
                y = y.replace(character, ' ')
        y = re.sub(r"’", r"'", y)
        y = re.sub(r" 1' ", r" l' ", y)
        y = re.sub(r"'", r" ", y)
        y = re.sub(r"‘", r" ", y)
        y = re.sub(r"cb", r"ch", y)
        
        y = re.sub(r" ch ", r" chi ", y)
        y = re.sub(r" c ", r" ci ", y)
        y = re.sub(r" m ", r" mi ", y)
        y = re.sub(r" s ", r" si ", y)
        y = re.sub(r" t ", r" ti ", y)
        y = re.sub(r" d ", r" di ", y)
        y = re.sub(r" n ", r" ne ", y)
        
        y = re.sub(r" delia ", r" della ", y)
        y = re.sub(r" delie ", r" delle ", y)
        y = re.sub(r" dalia ", r" dalla ", y)
        y = re.sub(r" deli ", r" dell ", y)
        y = re.sub(r" dell (\w*a\b)", r" della \1 ", y)
        y = re.sub(r" dell (\w*e\b)", r" delle \1 ", y)
        y = re.sub(r" dall (\w*a\b)", r" dalla \1 ", y)
        y = re.sub(r" dall (\w*e\b)", r" dalle \1 ", y)
        
        y = re.sub(r" l (\w*o\b)", r" lo \1", y)
        y = re.sub(r" l (\w*a\b)", r" la \1", y)
        y = re.sub(r" l (\w*à\b)", r" la \1", y)
        y = re.sub(r" l (\w*e\b)", r" le \1", y)
        y = re.sub(r" l (\w*i\b)", r" li \1", y)
        y = re.sub(r" gl ", r" gli ", y)
        
        y = re.sub(r" quell (\w*o\b)", r" quello \1", y)
        y = re.sub(r" quell (\w*a\b)", r" quella \1", y)
        y = re.sub(r" quell (\w*à\b)", r" quella \1", y)
        y = re.sub(r" quell (\w*e\b)", r" quelle \1", y)
        y = re.sub(r" quell (\w*i\b)", r" quelli \1", y)
        
        y = re.sub(r"€", r"e", y)
        y = re.sub(r"$", r"s", y)
        y = re.sub(r"corsiea", r"corsica", y)
        y = re.sub(r"tl", r"tt", y)
        y = re.sub(r"0", r"o", y)
        y = re.sub(r"\|", r"", y)
        
        if low is True:
            y = y.lower()
        if acc is True:
            y = unidecode.unidecode(y)
        for element in root.findall(".//rubrique"):
            if element.find('texte').text == x :
                element.find('texte').text = y
    ETtree.write(filename,encoding='UTF-8',xml_declaration=True)

def clean_text_FRA(filename, acc=True, pun=True, low=True, co=True):
    '''
    Fonction qui nettoye les rubriques de la revue en français.

    Entrée : XML
    Sortie : XML

    Paramètres :acc = bool, enlever les accents
                pun = bool, enlever la ponctuation
                low = bool, mettre la casse en minuscule
                co = bool, appliquer une correction automatique du texte (disponible seulement pour le français)
    '''
    tree = etree.parse(filename)
    ETtree = ET.parse(filename)
    root = ETtree.getroot()
    punc = ['!','+','=','|','“','”','(',')','-','`','[',']','{','}',';',':','°','«','©','»','"','\\',',','<','>','.','/','?','@','#','$','%','^','&','*','_','~','—', '–']
    for balise in tree.xpath('//rubrique[@lan="fr"]/texte'):
        x = balise.text
        y = x
        if pun is True:
            for character in punc:
                y = y.replace(character, ' ')
        if low is True:
            y = y.lower()
        y = re.sub(r"‘", " ", y)
        y = re.sub(r"'", " ", y)
        y = re.sub(r"  ", r" ", y)
        #if co is True:
            #spell = SpellChecker(language='fr')
            #mis = y.split()
            #spell.unknown(mis)
            #corr = []
            #for word in mis :
                #corr.append(spell.correction(word))
            #y = ' '.join(corr)
        if acc is True:
            y = unidecode.unidecode(y)
        for element in root.findall(".//rubrique"):
            if element.find('texte').text == x :
                element.find('texte').text = y
    ETtree.write(filename,encoding='UTF-8',xml_declaration=True)

def cleanXML(file, cors = True, ital = True, fran = True, acc=True, pun=True, low=True, co=True):
    '''
    Fonction permettant de nettoyer l'intégralité fichier XML d'un numéro de revue.

    Entrée : XML
    Sortie : XML

    Paramètres : cors = bool, nettoyer le corse
                ital = bool, nettoyer l'italien
                fran = bool, nettoyer le français
                acc = bool, enlever les accents
                pun = bool, enlever la ponctuation
                low = bool, mettre la casse en minuscule
                co = bool, appliquer une correction automatique du texte (disponible seulement pour le français)
    '''
    print("File -> " + file)
    shutil.copy(file, "./out/" + file)
    if cors is True:
        clean_text_COS(file, acc=acc, pun=pun, low=low)
        print("Cleaning on Corsican done")
    if ital is True:
        clean_text_ITA(file, acc=acc, pun=pun, low=low)
        print("Cleaning on Italian done.")
    if fran is True:
        clean_text_FRA(file, acc=acc, pun=pun, low=low, co=co)
        print("Cleaning on French done.")
