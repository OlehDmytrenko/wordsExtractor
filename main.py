# -*- coding: utf-8 -*-
"""

@author: Олег Дмитренко

"""
import sys, os
from __modules__ import configLoader, modelsLoader, stopwordsLoader, textProcessor, wordsAssessment
from __modules__ import similarityMatrix, matrixClustering 

import time
t0 = time.time()

if __name__ == "__main__":
    inputFilePath = sys.argv[1]
    stdOutput = open("outlog.log", "w")
    sys.stderr = stdOutput
    sys.stdout = stdOutput

    defaultLangs = configLoader.load_default_languages(os.getcwd())
    defaultSWs = stopwordsLoader.load_default_stop_words(defaultLangs)
    nlpModels = modelsLoader.load_default_models(defaultLangs)
    
    with open(inputFilePath, "r", encoding="utf-8") as inputFlow:
        document = ""
        docs = []
        
        lines = (inputFlow.read()).splitlines()
        for line in lines:
            document += (line + '\n')
            
            if line == '***':
                document = document[:-4]
                if document:
                    document = document[0:configLoader.int_value(os.getcwd(), 'maxDocLength')].lower()  
                    lang = textProcessor.lang_detect(document, defaultLangs, nlpModels, defaultSWs)
                    # check if model for lang exist (if NOT then skip this document and CONTINUE)
                    if (not defaultLangs[lang]):
                        document = ""
                        continue
                    # extract words from document
                    if (defaultLangs[lang] == 'pymorphy2'):
                        words = textProcessor.pymorphy2_nlp(document, nlpModels[lang], defaultSWs[lang])    
                    elif (defaultLangs[lang] == 'stanza'):
                        words  = textProcessor.stanza_nlp(document, nlpModels[lang], defaultSWs[lang])    
                    elif (not defaultLangs[lang]):
                        words = textProcessor.pymorphy2_nlp(document, nlpModels['en'], defaultSWs['en'])    
                    # form array of documents (where each document presented as array of extracted words)
                    docs.append(words)
                document = ""
                
        inputFlow.close()
    
    # get set of all unique words from all docs
    #setWords = wordsAssessment.get_set_words(docs)
    
    # get vector of all unique words from all docs
    vectorWords = wordsAssessment.get_vector_words(docs)
    
    df = wordsAssessment.TFIDF_vector(docs, vectorWords)
    df = wordsAssessment.GTF_vector(docs, vectorWords)
    #termsRanker.tfidf(documents)
    
    df_euclidian = similarityMatrix.euclidianSimilyrity(df)
    similarityMatrix.vizualization(df_euclidian)
    #matrixClustering.KMeansMethod(df_euclidian)
    
    print (time.time() - t0)
    
