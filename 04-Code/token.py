#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:45:43 2019

@author: Rahul Nalawade
"""
import spacy

# Reads data from the given file directed as in filepath, and returns it.
def read_data(filepath):
    f = open(filepath, 'r')
    corpus = f.read()
    return corpus

# Creates an array of tokens for the given corpus.
def tokennize(corpus):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(corpus)
    
    [token.text for token in doc]
    tokens = [token.text for token in doc]
    return tokens

# Main function
if __name__ == '__main__':

    filepath = '../02-Project-Data/WikipediaArticles/AbrahamLincoln.txt'    
    corpus = read_data(filepath)
    #print(corpus)
    tokens = tokennize(corpus)
    print(tokens)

#The-End