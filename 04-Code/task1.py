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

    tokens = [word.text for word in doc]
    return tokens

def sentenceTokennize(doc):
    
    sentences = [sent.string.strip() for sent in doc.sents]
    return sentences

# Lemmatizes corpus to extract lemmas as features
def lemmatize(doc):
    
    lemmas = [word.lemma_ for word in doc]
    return lemmas

# Gives Part-Of-Speech tags for each word in corpus.
def getPOS(doc):
    
    # Coarse grained part-of-speech tags
    pos = [word.pos_ for word in doc]
    
    # Fine grained part-of-speech tags
    tag = [word.tag_ for word in doc]
    
    return pos, tag

# Provides Syntactic Dependencies 
def synParsing(doc):
    
    # Dependency Labels
    dependC = [word.dep_ for word in doc]
    
    # Syntactic head token (governor)
    heads = [word.head.text for word in doc]
    
    return dependC, heads

# Extracting Named Entity feature
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
   
    sentences = sentenceTokennize(doc)
    #print(sentences)
    
    lemmas = lemmatize(doc)
    #print(lemmas)
    
    #posTags = getPOS(doc)
    #print(posTags)
    pos, tags = getPOS(doc)
    #print(pos)
    #print(tags)
    
    dependC, heads = synParsing(doc)
    #print(dependC)
    #print(heads)
    
    namedEntity = getNamedEntities(doc)
    #print(namedEntity)
    
    from spacy_wordnet.wordnet_annotator import WordnetAnnotator 
    #import nltk
    #nltk.download('wordnet')
    
    nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')
    #token = nlp('assassination')
    #print(type(tokens))        
    #print(token._.wordnet.synsets())

    synsetsMap = dict()
    hypernymsMap = dict()
    hyponymsMap = dict()
    partMeronymsMap = dict()
    substanceMeronymsMap = dict()
    holonymsMap = dict()
    
    #Traverse every token and extract synsets and create dictionaries 
    for t in tokens:        
        token = nlp(t)[0]
        #print(token._.wordnet.hypernyms())
        
        synsets = token._.wordnet.synsets()
        #print(t , " ", synsets)
        for syn in synsets:
            
            #Creating map for synonyms
            if not t in synsetsMap:
                synsetsMap[t] = set()
                synsetsMap[t].add(syn)
            else:
                synsetsMap[t].add(syn)
            #print("Synsets Map ", synsetsMap)
            
            hypernyms = syn.hypernyms()
            #print(syn , " hypernyms ", hypernyms)
            
            for hyper in hypernyms:
                #Creating map for hypernyms
                if not t in hypernymsMap:
                    hypernymsMap[t] = set()
                    hypernymsMap[t].add(hyper)
                else:
                    hypernymsMap[t].add(hyper)
            #print("Hypernyms Map ", hypernymsMap)
            
            hyponyms = syn.hyponyms()
            #print(syn , " hyponyms ", hyponyms)
            
            for hypo in hyponyms:
                #Creating map for hyponyms
                if not t in hyponymsMap:
                    hyponymsMap[t] = set()
                    hyponymsMap[t].add(hypo)
                else:
                    hyponymsMap[t].add(hypo)
            #print("Hyponyms Map ", hyponymsMap)
            
            partMeronyms = syn.part_meronyms()
            #print(syn , " part meronyms ", partMeronyms)
            
            for partMero in partMeronyms:
                #Creating map for partMeronyms
                if not t in partMeronymsMap:
                    partMeronymsMap[t] = set()
                    partMeronymsMap[t].add(partMero)
                else:
                    partMeronymsMap[t].add(partMero)
            #print("partMeronyms Map ", partMeronymsMap)
            

            substanceMeronyms = syn.substance_meronyms()
            #print(syn , " substance meronyms ", substanceMeronyms)

            for substanceMero in substanceMeronyms:
                #Creating map for partMeronyms
                if not t in substanceMeronymsMap:
                    substanceMeronymsMap[t] = set()
                    substanceMeronymsMap[t].add(substanceMero)
                else:
                    substanceMeronymsMap[t].add(substanceMero)
            #print("substanceMeronyms Map ", substanceMeronymsMap)

            holonyms = syn.member_holonyms()
            #print(syn , " member holonyms ", holonyms)

            for holo in holonyms:
                #Creating map for partMeronyms
                if not t in holonymsMap:
                    holonymsMap[t] = set()
                    holonymsMap[t].add(holo)
                else:
                    holonymsMap[t].add(holo)
            #print("substanceMeronyms Map ", substanceMeronymsMap)

    #print(synsetsMap)
    #print(hypernymsMap)
    #print(hyponymsMap)
    #print(partMeronymsMap)
    #print(substanceMeronymsMap)
    #print(holonymsMap)
        
    
    
        
    
            
    
#The-End