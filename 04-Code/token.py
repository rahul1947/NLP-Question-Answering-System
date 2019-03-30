#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:45:43 2019

@author: Rahul Nalawade
         Sunny Bangale
"""
import spacy

# Reads data from the given file directed as in filepath, and returns it.
def read_data(filepath):
    f = open(filepath, 'r')
    corpus = f.read()
    return corpus

# Creates an array of tokens for the given corpus.
def tokennize(doc):
    
    #[token.text for token in doc]
    tokens = [word.text for word in doc]
    return tokens

# Lemmatizes corpus to extract lemmas as features
def lemmatize(doc):
    
    lemmas = [word.lemma_ for word in doc]
    return lemmas

# Gives Part-Of-Speech tags for each word in corpus.
def getPOS(doc):
    
    pos_tags = [word.pos_ for word in doc]
    return pos_tags

# Provides Syntactic Dependencies 
def synParsing(doc):
    
    # Dependency Labels
    dependC = [word.dep_ for word in doc]
    
    # Syntactic head token (governor)
    heads = [word.head.text for word in doc]
    
    return dependC, heads

def getNamedEntities(doc):
    
    # Text and label of named entity span
    namedEntities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return namedEntities


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
    pos_tags = getPOS(doc)
    #print(pos_tags)
    
    dependC, heads = synParsing(doc)
    #print(dependC)
    #print(heads)
    
    namedEntity = getNamedEntities(doc)
    print(namedEntity)
    
#The-End