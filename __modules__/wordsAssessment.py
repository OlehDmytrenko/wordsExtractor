# -*- coding: utf-8 -*-
"""

@author: Олег Дмитренко

"""      
import sys
from __modules__ import packagesInstaller
packages = ['nltk']
packagesInstaller.setup_packeges(packages)

import math
from nltk import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer 
import pandas as pd

stdOutput = open("outlog.log", "a")
sys.stderr = stdOutput
sys.stdout = stdOutput


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def most_freq(NTerms):
    fdist = FreqDist(word.lower() for word in NTerms)
    for (term, freq) in fdist.most_common():
        print (term, freq)
    return 


def tfidf(messages):
    # settings that you use for count vectorizer will go here 
    tfidf_vectorizer=TfidfVectorizer() 
    # just send in all your docs here 
    tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(messages)

    # get the first vector out (for the first document) 
    first_vector_tfidfvectorizer=tfidf_vectorizer_vectors[0] 
    # place tf-idf values in a pandas data frame 
    df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"]) 
    df = df.sort_values(by=["tfidf"],ascending=False)
    print (df)
    df.to_excel("output.xlsx")
    return

def GTF(docs):  
    quantity_all_elements = sum(len(doc) for doc in docs)
    for doc in docs:
        for word in doc:
            TF = 1.0*doc.count(word) / len(doc)
            IDF = math.log(1.0 * len(docs) / (sum(1 for doc in docs if word in doc)))
            TFIDF = TF*IDF
            #print (word, TFIDF)
    return

# get TF-IDF for all words in doc
# save ascending by tfidf dataframes in xlsx format (each doc on separate sheet)
def TFIDF(docs):  
    sheet = 0
    with pd.ExcelWriter('output.xlsx') as output:
        for doc in docs:
            words = []
            TFIDFs = []
            sheet = sheet + 1
            for word in doc:
                TF = 1.0*doc.count(word) / len(doc)
                IDF = math.log(1.0 * len(docs) / (sum(1 for doc in docs if word in doc)))
                TFIDF = TF*IDF
                words.append(word)
                TFIDFs.append(TFIDF)
                #print (word, TFIDF) 
            df = pd.DataFrame(TFIDFs, index=words, columns=["tfidf"]) 
            df = df.sort_values(by=["tfidf"],ascending=False)
            df.to_excel(output, sheet_name=str(sheet))
    return

# get vector of GTF that corresponds to vectorWords for each doc
def GTF_vector(docs, vectorWords):
    # create dataframe of TF-IDF where indeces are vectorWords and colomns are number of documents
    df = pd.DataFrame(index=[word for (word,freq) in vectorWords])
    column = 0
    # calculate number of all words in all documents
    norm = sum(len(doc) for doc in docs)
    
    with pd.ExcelWriter('GTF.xlsx') as output:
        for doc in docs:
            GTFs = []
            column += 1
            for (word, freq) in vectorWords:
                if word in doc:
                    GTFs.append(freq/norm)
                else:
                    GTFs.append(0)
            # add verctor of GTF to dataframe 
            df[str(column)] = GTFs
            #df2 = pd.DataFrame(GTFs, index=[word for (word,freq) in vectorWords], columns=["GTF"]) 
            #df2 = df2.sort_values(by=["GTF"],ascending=False)
            #df2.to_excel(output, sheet_name=str(column))
        
        df.to_excel(output, sheet_name='Matrix')
        df.to_csv('GTF.csv')
        print (df.to_numpy)
    return

# get vector of TF-IDF that corresponds to vectorWords for each doc
def TFIDF_vector(docs, vectorWords):
    # create dataframe of TF-IDF where indeces are vectorWords and colomns are number of documents
    df = pd.DataFrame(index=[word for (word,freq) in vectorWords])#, columns=list(range(1, len(docs))))
    column = 0
    
    for doc in docs:
        TFIDFs = []
        column += 1
        for (word, freq) in vectorWords:
            TF = 1.0*doc.count(word) / len(doc)
            IDF = math.log(1.0 * len(docs) / (sum(1 for doc in docs if word in doc)))
            TFIDF = TF*IDF
            TFIDFs.append(TFIDF)
        # add verctor of TF-IDF to dataframe 
        df[str(column)] = TFIDFs
        df.to_excel('TF-IDF.xlsx')
    return

def get_set_words(docs):
    words = []
    for doc in docs:
        words += doc
    return sorted(set(words))
    
def get_vector_words(docs):
    words = []
    for doc in docs:
        words += doc
    fdist = FreqDist(word for word in words)
    return fdist.most_common(100)