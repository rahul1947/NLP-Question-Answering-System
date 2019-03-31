#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:45:43 2019

@author: Rahul Nalawade
"""
import spacy
from spacy.lang.en import English
from spacy.pipeline import SentenceSegmenter



# Reads data from the given file directed as in filepath, and returns it.
def read_data(filepath):
    f = open(filepath, 'r')
    corpus = f.read()
    return corpus

# Creates an array of tokens for the given corpus.
def tokennize(doc):
    
    # segmenting text into words, punctuation, etc.
    tokens = [word.text for word in doc]
    return tokens

# Lemmatizes corpus to extract lemmas as features
def lemmatize(doc):
    
    # assigning base form of words
    lemmas = [word.lemma_ for word in doc]
    return lemmas

# Gives Part-Of-Speech tags for each word in corpus.
def getPOS(doc):
    
    # Coarse grained part-of-speech tags
    pos = [word.pos_ for word in doc]
    
    # Fine grained part-of-speech tags
    tag = [word.tag for word in doc]
    
    return pos, tag

# Provides Syntactic Dependencies 
def synParsing(doc):
    
    # Dependency Labels
    dependC = [word.dep_ for word in doc]
    
    # Syntactic head token (governor)
    heads = [word.head.text for word in doc]
    
    return dependC, heads

# Provides Named Entities
def getNamedEntity(doc):
    
    # Text and label of named entity span
    namedEntities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return namedEntities
#-----------------------------------------------------------------------------
def newlineSplit(doc):
    start = 0
    isNewline = False
    
    for word in doc:
        
        if (isNewline and not word.is_space):
            yield doc[start:word.i]
            start = word.i
            isNewline = False
        elif (word.text == '\n'):
            isNewline = True
        if (start < len(doc)):
            yield doc[start:len(doc)]
    #endFor


#-----------------------------------------------------------------------------
# Main function
if __name__ == '__main__':

    filepath = '../02-Project-Data/WikipediaArticles/AbrahamLincoln.txt'    
    corpus = read_data(filepath)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(corpus)
    #print(corpus)
    
    tokens = tokennize(doc)
    #print(tokens)
    lemmas = lemmatize(doc)
    #print(lemmas)
    pos, tags = getPOS(doc)
    #print(pos)
    #print(tags)
    
    dependC, heads = synParsing(doc)
    #print(dependC)
    #print(heads)
    
    namedEntity = getNamedEntity(doc)
    print(namedEntity)
    
    #-------------------------------------------------------------------------
    # SENTENCE SEGMENTATION
    # REFERENCE: https://www.youtube.com/watch?v=WbEKxcsO66U
    #nlp = English()
    #sbd = SentenceSegmenter(nlp.vocab, strategy = newlineSplit)
    #nlp.add_pipe(sbd)
    
    
#The-End