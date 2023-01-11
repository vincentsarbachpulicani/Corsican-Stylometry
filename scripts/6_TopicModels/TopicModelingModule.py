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

from wordcloud import WordCloud

from gensim.models import LdaModel

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import collections

from tqdm.notebook import tqdm
from gensim.corpora import Dictionary


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
        Allows to choose a subset of the original classification of entropies ans weights.
        
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

    

class GensimTopicModeling:
    """
    Initiate the topic modeling processing process using the Gensim library. The only parameter need is a corpus of tokenized documents. The differents methods existing are here to refine the results of the TM.
    
    Input -> Tokenized corpus of documents (List of documents tokenized)
    Output -> DataFrame, TSV files or wordclouds
    """
    
    def __init__(self, corpus):
        corpus = [[token for token in doc if not token.isnumeric()] for doc in corpus]
        corpus = [[token for token in doc if len(token) > 1] for doc in corpus]
        self.corpus = corpus
        self.dictionary = None
        self.model = None
        self.co = None
        self.num_topics = None
    
    def compute_bigrams(self, n, mini):
        """
        Allows to compute ngrams of tokens in order to take into account most frequent ngrams in the analysis.
        
        Parameters :
        
        n -> int : ngram type
        mini -> int : minimum of occurences of the ngrams
        """
        for idx in range(len(self.corpus)):
            ngrams = nltk.ngrams(self.corpus[idx], n)
            result = dict(collections.Counter(ngrams))
            new_result = {i for i in result if result[i]>=mini}
            for gram in new_result:
                self.corpus[idx].append('_'.join(gram))
                
    def vocabulary_from_corpus(self, no_below=5, no_above=0.5):
        """
        Selection of the vocabulary directly from the corpus using the filter_extremes() function from Gensim.
        
        Parameters :
        
        no_above -> int : more than no_above documents
        no_below -> int :less than no_below documents (absolute number)
        """
        dictionary = Dictionary(self.corpus)
        dictionary.filter_extremes(no_below=no_below, no_above=no_above)
        print(f"The generated dictionary contains {len(dictionary)} unique tokens.")
        self.dictionary = dictionary
    
    def vocabulary_from_filters(self, index_words):
        """
        Selection of the vocabulary according to a list of words WE DON'T WANT to be in, using the filter_tokens() function from Gensim.
        
        Parameter :
        
        index_words -> list : it's a list of words that we want to be removed from the dictionnary. The words must be in the dictionnary to work
        """
        index_words = [word for word in index_words if not word.isnumeric()]
        index_words = [word for word in index_words if len(word) > 1]
        
        dictionary = Dictionary(self.corpus)

        for word in tqdm(index_words):
            dictionary.filter_tokens(bad_ids=[dictionary.token2id[word]])
        print(f"The generated dictionary contains {len(dictionary)} unique tokens.")
        self.dictionary = dictionary
        
    def vocabulary_from_specific_list(self, vocab):
        """
        Selection of the vocabulary according to a specific list of words.
        
        Parameter :
        
        vocab -> list : list of words 
        """
        print(f"The generated dictionary contains {len(vocab)} unique tokens.")
        self.dictionary = vocab
        
    def model_training(self, num_topics, chunksize = 1500, passes = 20, iterations = 400, eval_every = None):
        """
        Method to train a model from our corpus and data defined previously. 
        
        Parameters :
        
        num_topics -> int : choose the number of topics
        chunksize -> int : number of documents to be used in each training chunk
        passes -> int : number of passes through the corpus during training
        iterations -> int : maximum number of iterations through the corpus when inferring the topic distribution of a corpus
        eval_every -> int : log perplexity is estimated every that many updates. Setting this to one slows down training by ~2x
        """
        
        self.num_topics = num_topics
        
        co = [self.dictionary.doc2bow(doc) for doc in self.corpus]
        
        
        print('Number of unique tokens: %d' % len(self.dictionary))
        print('Number of documents: %d' % len(co))
    
        # Set training parameters.
        num_topics = num_topics
        chunksize = chunksize
        passes = passes
        iterations = iterations
        eval_every = eval_every

        # Make an index to word dictionary.
        temp = self.dictionary[0]  # This is only to "load" the dictionary.
        id2word = self.dictionary.id2token

        model = LdaModel(
            corpus=co,
            id2word=id2word,
            chunksize=chunksize,
            alpha='auto',
            eta='auto',
            iterations=iterations,
            num_topics=num_topics,
            passes=passes,
            eval_every=eval_every
        )
        
        self.model = model
        self.co = co
        print("The model has been trained successfully.")

    def top_topics_and_coherence(self, mfw):
        """
        Print a table that shows all the topics generated by the model including their coherence and the most frequent words. return a dataframe.
        
        Parameter :
        
        mfw -> int : most frequent words
        """
        top_topics = self.model.top_topics(self.co)

        # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
        avg_topic_coherence = sum([t[1] for t in top_topics]) / self.num_topics
        print('Average topic coherence: %.4f.' % avg_topic_coherence)
        n = 0
        dic_co = {}
        for topic in top_topics:
            print()
            top_ = [topic[1]]
            l_ = [w[1] for w in topic[0]]
            print (topic[1], [w[1] for w in topic[0]])
            top_.extend(l_)
            dic_co[f"Topic {n}"] = top_
            n += 1
        
        col_names = ['Topic coherence']

        for i in range(mfw):
            col_names.append(f'Word {i + 1}')
        
        df_coherence = pd.DataFrame(data=dic_co, index=col_names)
        
        return df_coherence
    
    
    def draw_word_clouds(self, y, x, figsize=(20,10), dpi=150):
        """
        Method to visualize the topics through wordclouds. Return one plot with all the wordclouds in subplots.
        
        Parameters :
        
        y -> int : number of rows on the plot
        x -> int : number of columns on the plot
        figsize -> tuple of 2 integers : set the dimension of the image
        dpi -> int : set the resolution of the image
        """
        fig = plt.figure(figsize=figsize, dpi=dpi)
        
        for i in range(self.model.num_topics):
            ax = fig.add_subplot(y, x ,i+1)
            wordcloud = WordCloud(width=600, height=600, background_color='white').fit_words(dict(self.model.show_topic(i, 30)))

            titre = f"Topic {i}"
            ax.imshow(wordcloud)
            ax.axis('off')
            ax.set_title(titre, fontsize=18)
         
        return fig
    
    def visualisation_pyldavis(self, html=False):
        """
        Method to vusualize the date with the library pyLDAvis. Return the interactive notebook of the library. Can also have an output in HTML to save the notebook.
        
        Parameter :
        
        html -> bool : save the notebook in a HTML file or no
        """
        
        pyLDAvis.enable_notebook()
        
        p = gensimvis.prepare(self.model, self.co, self.dictionary)
        
        if html is True:
            pyLDAvis.save_html(p, 'lda.html')
        
        return p
        
