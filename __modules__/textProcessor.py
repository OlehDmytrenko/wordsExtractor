# -*- coding: utf-8 -*-
"""

@author: Олег Дмитренко

"""
from __modules__ import packagesInstaller
packages = ['fasttext', 'nltk']
packagesInstaller.setup_packeges(packages)

import fasttext
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from __modules__ import defaultModelsLoader, defaultSWsLoader

def stanza_built_words(sent, NWords, stopWords):
    WordsTags = []
    for word in sent.words:
        try:
            nword = (word.lemma).lower()
            tag = word.upos
        except:
            continue
        if tag == 'PROPN':
            tag = 'NOUN'
        WordsTags.append((nword,tag))
        if (nword not in stopWords) and (tag == 'NOUN'): 
            NWords.append(nword)
    return WordsTags, NWords

def stanza_nlp(text, nlpModel, stopWords):
    NWords = []
    doc = nlpModel(text)
    sents = doc.sentences
    for sent in sents:
        WordsTags, NWords = stanza_built_words(sent, NWords, stopWords)
    return NWords

def pymorphy2_built_words(sent, NWords, nlpModel, stopWords):
    WordsTags = []
    words = word_tokenize(sent)
    for word in words:
        try:
            nword = str(nlpModel.normal_forms(word)[0]).lower()
            tag = str((nlpModel.parse(word)[0]).tag.POS)
        except:
            continue
        if tag == 'PROPN':
            tag = 'NOUN'
        WordsTags.append((nword,tag))
        if (nword not in stopWords) and (tag == 'NOUN'): 
            NWords.append(nword)
    return WordsTags, NWords


def pymorphy2_nlp(text, nlpModel, stopWords):
    NWords = []
    sents = sent_tokenize(text)
    for sent in sents:
        WordsTags, NWords = pymorphy2_built_words(sent, NWords, nlpModel, stopWords)
    return NWords

def append_lang(defaultLangs, lang, package):
    try:
        defaultLangs[lang] = package
        #with open(dir_below()+"/config.json", "w") as configFile:
        #    try:
        #    except:
        #        pass
        #    configFile.close()
    except:
        print ('Unexpected Error while adding new languade to default list <defaultLangs>!')
    return defaultLangs

def lang_detect(message, defaultLangs, nlpModels, stopWords):
    lidModel = fasttext.load_model('lid.176.ftz')
    message = message.replace("\n", " ")
    #Check if all the characters in the text are whitespaces
    if message.isspace():
        return 'uk'
    else:
        try:
            # get first item of the prediction tuple, then split by "__label__" and return only language code
            lang = lidModel.predict(message)[0][0].split("__label__")[1]
        except:
            return "uk"
    if (lang not in defaultLangs):
        try:
            nlpModels = defaultModelsLoader.stanza_model_loader(defaultLangs, nlpModels, lang)
        except:
            return "uk"
        defaultSWsLoader.load_stop_words(defaultLangs, stopWords, lang)
    return lang
