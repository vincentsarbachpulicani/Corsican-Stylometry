import nltk
nltk.download('omw-1.4')

import spacy
import numpy as np
import pandas as pd
import math
import itertools
import operator as op
import matplotlib.pyplot as plt
import re

from nltk.tokenize import RegexpTokenizer

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from statistics import mean
from statistics import median
from statistics import stdev


class PreprocessingCorpus:
    """
    Allows, if necessary, to process the corpus with some basic functions. 
    
        Input -> List of strings (corpus)
        Output -> List of strings (corpus)
    """
    
    def __init__(self, corpus):
        self.corpus = corpus
    
    def lower_case(self):
        """
        Lower case function. Mandatory for analysis.
        """
        self.corpus = [doc.lower() for doc in self.corpus]
    
    def tokenization(self):
        """
        Tokenizes each documents of the corpus.
        """
        tokenizer = RegexpTokenizer(r'\w+')
        self.corpus = [tokenizer.tokenize(doc) for doc in self.corpus]
        print("Tokenization done.")

class EntropyAnalysis:
    """
    Class allowing to calculate the entropy (Susan T. Dumais, 1992) and the weight of words in a corpus of documents. Also allows to manipulate the data to have different results and to have as output a vocabulary of words sorted according to their entropy or weight.
    
    Input -> Tokenized corpus of documents (List of documents tokenized)
    Output -> Graphs, DataFrame, TSV files or vocabulary
    """
    
    def __init__(self, corpus, frequency=None, vocabulary=None, ndocs = None):
        self.corpus = corpus
        self.frequency = frequency
        self.vocabulary = vocabulary
        self.ndocs = ndocs 
        self.classification = None
        self.expl_statistics = None
        self.sorted_classification = None
    
    def frequency_calculation(self):
        """
        Calculation of the global frequency of terms within the corpus.
        """
        self.frequency = dict(nltk.FreqDist(list(itertools.chain.from_iterable(self.corpus))))
        print(f"The frequency of the unique tokens of this corpus has been done.")
    
    def vocabulary_set(self):
        """
        List of unique tokens in the corpus.
        """
        self.vocabulary = list(self.frequency.keys())
        print(f"The vocabulary contains {len(self.vocabulary)} unique tokens.")
    
    def set_ndocs(self):
        """
        Number of documents present in the corpus.
        """
        self.ndocs = len(self.corpus)
        print(f"The corpus is composed of {len(self.corpus)}.")
    
    def probability(self, word, document):
        """
        Probability calculation of the global frequency (gf_i) and the term frequency (tf_ij). Function used directly in the entropy calculation.
        """
        tf = op.countOf(document, word)
        gf = self.frequency[word]
        return tf/gf, gf
    
    def entropy_calculation(self, output="dataframe"):
        """
        Calculation of the entropy of each term in the corpus. Deletion of words whose entropy is equal to 0.  The output is an array which is materialized as a dataframe object or a TSV file.

        Parameter :
        
        output -> str : "dataframe" (default), "tsv" or "both".
        """
        dic_entropies = {}
        
        for word in self.vocabulary:
            probs = []

            for doc in self.corpus:
                prob, freq = self.probability(word, doc)
                probs.append(prob)

            count = [probs.index(x) for x in probs if x > 0]

            entropy = -sum([probs[i] * np.log2(probs[i]) for i in count])/np.log2(self.ndocs)

            if entropy == -0.0:
                entropy = 0

            weight = freq * entropy

            dic_entropies[word] = [entropy, weight]

        dic_entropies = {key:val for key, val in dic_entropies.items() if val != [0, 0]}

        classification = pd.DataFrame(data=dic_entropies, index=["Entropy", "Weight score"]).T
        self.classification = classification
        
        if output == "dataframe":
            return classification
        
        elif output == "tsv":
            classification.to_csv("entropy.tsv", "\t")
        
        elif output == "both":
            classification.to_csv("entropy.tsv", "\t")
            return classification
        
        else:
            raise ValueError('The "output" parameter is false. Must be "tsv", "dataframe" or "both".')
    
    def exploratory_statistics(self):
        """
        Basic statistics of the corpus : mean, max value, min value, median and standard deviation. Return a dataframe.
        """
        dic_stats = {}
        
        for col in ['Entropy', 'Weight score']:
            mean_ = mean(self.classification[col].tolist())
            median_ = median(self.classification[col].tolist())
            stdev_ = stdev(self.classification[col].tolist())
            max_ = max(self.classification[col].tolist())
            min_ = min(self.classification[col].tolist())

            dic_stats[col] = [max_, min_, mean_, median_, stdev_]
            
        expl_statistics = pd.DataFrame(data=dic_stats, index=["Max value", "Min value", "Mean", "Median", "Standard deviation"])
        self.expl_statistics = expl_statistics
        
        return expl_statistics
    
    def plot_scores(self, data):
        """
        Plot the evolution of the entropies and the weight scores of the tokens.
        
        Parameter :
        
        data -> dataframe: with "Entropy" and "Weight score" columns and the tokens in index.
        
        """
        fig, ax1 = plt.subplots()
        color = 'red'

        ax1.set_xlabel('Words rank')
        ax1.set_ylabel('Entropy', color=color)
        ax1.plot(sorted(data['Entropy'].tolist()), color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()

        color = 'blue'
        ax2.set_ylabel('Weight score', color=color)
        ax2.plot(sorted(data['Weight score'].tolist()), color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title("Evolution of the entropy and the weight score in the vocabulary")
        plt.show()
        
    def classification_sort(self, data, min_range, max_range, col_name="Entropy", between_values=True, inclusive=False, output="dataframe"):
        """
        Allows to choose a subset of the original classification of entropies and weights.
        
        Parameters :
        
        data -> dataframe: with "Entropy" and "Weight score" columns and the tokens in index.
        min_range -> int: minimum value of the interval.
        max_range -> int: maximum value of the interval.
        col_name -> str: "Entropy" (default) or "Weight score", choose the values to base the sort.
        between_values -> bool: True (default), keep the values inside (default) or outside the interval.
        inclusive -> bool: False (default), include or exclude (default) the minimum and maximum values chosen.
        """
        if between_values is True:
            sorted_classification = data.loc[data[col_name].between(min_range, max_range, inclusive=inclusive)]
        else:
            sorted_classification = data.loc[~data[col_name].between(min_range, max_range, inclusive=inclusive)]
        
        self.sorted_classification = sorted_classification
        
        if output == "dataframe":
            return sorted_classification
        
        elif output == "tsv":
            sorted_classification.to_csv("entropy_sorted.tsv", "\t")
        
        elif output == "both":
            sorted_classification.to_csv("entropy_sorted.tsv", "\t")
            return sorted_classification
        
        else:
            raise ValueError('The "output" parameter is false. Must be "tsv", "dataframe" or "both".')
    
    
    def return_vocabulary(self, data):
        """
        Return a vocabulaire in the form of a list, from a classification dataframe.
        
        Parameter :
        
        data -> dataframe: with "Entropy" and "Weight score" columns and the tokens in index.
        """
        return list(data.index.values)