import pandas as pd
import os
import sys
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from spacy.lang.it.stop_words import STOP_WORDS as it_stop




def delete_stopwords_from_dataframe(table, col_name):  #Suppression des mots-outils à partir d'un tableau pour raisons pratiques : comme ça j'ai le choix de les concerver ou non sans impacter la phase de nettoyage
    '''
    Fonction supprimant les mots outils du texte des rubriques.
    Si l'entrée est un fichier CSV, alors la fonction renvoie en output un nouveau fichier CSV.
    Si l'entrée est une dataframe, alors la fontion renvoie également une dataframe.

    Entrée : CSV ou dataframe
    sortie : CSV ou dataframe
    '''

    co_stops = ["li","le","e","u","a","la","ancu","unn","ellu","elli","ella","elle","quellu","quelle","quelli","quella","so","aghju","aghiu","he","simu","avemu","site","hannu","hanu","pe","par","seraghiu","sera","sara","oramai","tuttu","chi","quessu","quessa","quesse","quessi","bellu","bonu","bona","bon","boni","bone","boni","be","benche","mo", "lu", "cu","incu","nostru","vostru",'cusi','cun','st','bi', 'micca', 'altru','to','avia', 'stu', 'quandu', 'dopu','ca', 'ava', 'sottu', 'pocu','tutt', 'ind', 'inde', 'unu', 'tantu', 'dui','oh', 'fattu', 'vo', 'eiu', 'gran', 'bella', 'eccu', 'cum','nun', 'caru','cara','cari']

    if isinstance(table, pd.DataFrame): #Si l'entrée est une dataframe
        print("Object -> dataframe.")
        data = table
        final_list = list(it_stop) + co_stops + list(fr_stop)
        data[col_name] = data[col_name].apply(lambda x : x.split()) #Les string contenues dans les cellules de la DF deviennent des listes
        data[col_name] = data[col_name].apply(lambda x: [token for token in x if token not in final_list]) #Pour chaque liste des cellules du tableau, suppression des stopwords
        data[col_name] = data[col_name].apply(lambda x : (" ").join(x))  #On fusionne en une string toutes les éléments des listes des cellules de la DF
        print("Done.")
        return data
    elif table.endswith('.csv'):  #Si l'entrée est un fichier CSV
        print("Object -> CSV file.")
        data = pd.read_csv(table)
        final_list = list(it_stop) + co_stops + list(fr_stop)
        data[col_name] = data[col_name].apply(lambda x : x.split())
        data[col_name] = data[col_name].apply(lambda x: [token for token in x if token not in final_list])
        data[col_name] = data[col_name].apply(lambda x : (" ").join(x))
        data.to_csv("output_" + table)
        print("Done.")
