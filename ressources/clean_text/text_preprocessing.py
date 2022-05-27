import re
import lxml
from lxml import etree
import xml.etree.ElementTree as ET
import string
from spellchecker import SpellChecker
import unidecode
import shutil
from nltk.corpus import stopwords
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from spacy.lang.it.stop_words import STOP_WORDS as it_stop
from stop_cos import co_stops
import pandas as pd

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
    punc = ['!','+','=','|','“','”','(',')','-','`','[',']','°','{','}',';',':','«','»','"','\\',',','<','>','.','/','?','@','#','$','%','^','&','*','_','~','—', '–']
    for balise in tree.xpath('//langue[@lan="cos"]/following-sibling::texte'):
        x = balise.text
        y = x
        if pun is True:
            for character in punc:
                y = y.replace(character, '')
        if low is True:
            y = y.lower()
        y = re.sub(r"’", r"'", y)
        y = re.sub(r" 1 ", r" li ", y)
        y = re.sub(r"l'(\w*u\b)", r"u \1", y)
        y = re.sub(r"l'(\w*a\b)", r"a \1", y)
        y = re.sub(r"l'(\w*à\b)", r"a \1", y)
        y = re.sub(r"l'(\w*e\b)", r"le \1", y)
        y = re.sub(r"l'(\w*i\b)", r"li \1", y)
        y = re.sub(r" lu ", r" u ", y)
        y = re.sub(r" la ", r" a ", y)
        y = re.sub(r" i ", r" li ", y)
        y = re.sub(r"d'", r"di ", y)
        y = re.sub(r"ch'", r"chi  ", y)
        y = re.sub(r"s'", r"si ", y)
        y = re.sub(r"quell'(\w*u\b)", r"quellu \1", y)
        y = re.sub(r"quell'(\w*a\b)", r"quella \1", y)
        y = re.sub(r"quell'(\w*à\b)", r"quella \1", y)
        y = re.sub(r"quell'(\w*e\b)", r"quelle \1", y)
        y = re.sub(r"quell'(\w*i\b)", r"quelli \1", y)
        y = re.sub(r"ell’", r"ellu ", y)
        y = re.sub(r"sott’", r"sottu", y)
        y = re.sub(r"sopr'", r"sopra ", y)
        y = re.sub(r"bon'(\w*u\b)", r"bonu \1", y)
        y = re.sub(r"bon'(\w*a\b)", r"bona \1", y)
        y = re.sub(r"bon'(\w*à\b)", r"bona \1", y)
        y = re.sub(r"bon'(\w*e\b)", r"bone \1", y)
        y = re.sub(r"bon'(\w*i\b)", r"boni \1", y)
        y = re.sub(r"bon'", r"bonu ", y)
        y = re.sub(r"vostr'(\w*u\b)", r"vostru \1", y)
        y = re.sub(r"vostr'(\w*a\b)", r"vostra \1", y)
        y = re.sub(r"vostr'(\w*i\b)", r"vostri \1", y)
        y = re.sub(r"vostr'(\w*e\b)", r"vostre \1", y)
        y = re.sub(r"vostr'(\w*à\b)", r"vostra \1", y)
        y = re.sub(r"c'", r"ci ", y)
        y = re.sub(r"n'", r"ne ", y)
        y = re.sub(r"t'", r"ti ", y)
        y = re.sub(r"nostr'(\w*u\b)", r"nostru \1", y)
        y = re.sub(r"nostr'(\w*a\b)", r"nostra \1", y)
        y = re.sub(r"nostr'(\w*i\b)", r"nostri \1", y)
        y = re.sub(r"nostr'(\w*e\b)", r"nostre \1", y)
        y = re.sub(r"nostr'(\w*à\b)", r"nostra \1", y)
        y = re.sub(r"'", r" ", y)
        y = re.sub(r"‘", r" ", y)
        y = re.sub(r" è ", r" hè ", y)
        y = re.sub(r"  ", r" ", y)
        y = re.sub(r" 1 ", r" i ", y)
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
                sw = bool, suppression des mots outils
    '''
    tree = etree.parse(filename)
    ETtree = ET.parse(filename)
    root = ETtree.getroot()
    punc = ['!','+','=','|','“','”','(',')','-','`','[',']','{','}','°',';',':','«','»','"','\\',',','<','>','.','/','?','@','#','$','%','^','&','*','_','~','—', '–']
    for balise in tree.xpath('//langue[@lan="ita"]/following-sibling::texte'):
        x = balise.text
        y = x
        if pun is True:
            for character in punc:
                y = y.replace(character, '')
        if low is True:
            y = y.lower()
        if acc is True:
            y = unidecode.unidecode(y)
        for element in root.findall(".//rubrique"):
            if element.find('texte').text == x :
                element.find('texte').text = y
    ETtree.write(filename,encoding='UTF-8',xml_declaration=True)

def clean_text_FRA(filename, acc=True, pun=True, low=True, co=True, sw=True):
    '''
    Fonction qui nettoye les rubriques de la revue en français.
    
    Entrée : XML
    Sortie : XML
    
    Paramètres :acc = bool, enlever les accents
                pun = bool, enlever la ponctuation
                low = bool, mettre la casse en minuscule
                co = bool, appliquer une correction automatique du texte (disponible seulement pour le français)
                sw = bool, suppression des mots outils
    '''
    tree = etree.parse(filename)
    ETtree = ET.parse(filename)
    root = ETtree.getroot()
    punc = ['!','+','=','|','“','”','(',')','-','`','[',']','{','}',';',':','°','«','»','"','\\',',','<','>','.','/','?','@','#','$','%','^','&','*','_','~','—', '–']
    for balise in tree.xpath('//langue[@lan="fra"]/following-sibling::texte'):
        x = balise.text
        y = x
        if pun is True:
            for character in punc:
                y = y.replace(character, '')
        if low is True:
            y = y.lower()
        y = re.sub(r"‘", " ", y)
        y = re.sub(r"'", " ", y)
        if co is True:
            spell = SpellChecker(language='fr')
            mis = y.split()
            spell.unknown(mis)
            corr = []
            for word in mis :
                corr.append(spell.correction(word))
            y = ' '.join(corr)
        if acc is True:
            y = unidecode.unidecode(y)
        for element in root.findall(".//rubrique"):
            if element.find('texte').text == x :
                element.find('texte').text = y
    ETtree.write(filename,encoding='UTF-8',xml_declaration=True)

def clean_XML(file, cors = True, ital = True, fran = True, acc=True, pun=True, low=True, co=True):
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
    filename = "output_" + file
    shutil.copyfile(file, filename)
    if cors is True:
        clean_text_COS(filename, acc=acc, pun=pun, low=low, sw=sw)
        print("Corsican done.")
    if ital is True:
        clean_text_ITA(filename, acc=acc, pun=pun, low=low, sw=sw)
        print("Italian done.")
    if fran is True:
        clean_text_FRA(filename, acc=acc, pun=pun, low=low, co=co, sw=sw)
        print("French done.")

def delete_stopwords_from_dataframe(table):
    '''
    Fonction supprimant les mots outils du texte des rubriques. 
    Si l'entrée est un fichier CSV, alors la fonction renvoie en output un nouveau fichier CSV.
    Si l'entrée est une dataframe, alors la fontion renvoie également une dataframe.
    
    Entrée : CSV ou dataframe
    sortie : CSV ou dataframe
    '''
    if isinstance(table, pd.DataFrame):
        print("Object -> dataframe.")
        data = table
        final_list = list(it_stop) + co_stops + list(fr_stop)
        data["Texte"] = data["Texte"].apply(lambda x : x.split())
        data["Texte"] = data["Texte"].apply(lambda x: [token for token in x if token not in final_list])
        data["Texte"] = data["Texte"].apply(lambda x : (" ").join(x))
        print("Done.")
        return data
    elif table.endswith('.csv'):
        print("Object -> CSV file.")
        data = pd.read_csv(table)
        final_list = list(it_stop) + co_stops + list(fr_stop)
        data["Texte"] = data["Texte"].apply(lambda x : x.split())
        data["Texte"] = data["Texte"].apply(lambda x: [token for token in x if token not in final_list])
        data["Texte"] = data["Texte"].apply(lambda x : (" ").join(x))
        data.to_csv("output_" + table)
        print("Done.")
        