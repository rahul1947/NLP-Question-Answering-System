#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:45:43 2019

@author: Rahul Nalawade
         Sunny Bangale
"""
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 
import nltk
import sys
import os
import collections
import json


# Reads data from the given file directed as in filepath, and returns it.
def read_data(filepath):
    try:
        f = open(filepath, 'r', encoding="utf8")    
    except UnicodeDecodeError:
        f = open(filepath, 'r', encoding="iso-8859-1")
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
def lemmatize(token):
     
     doc = list(token)   
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

# Provides Synsets of a token 
def getSynsets(token):
    
    synsets = token._.wordnet.synsets()
    return synsets            

# Provides Hypernyms of a token 
def getHypernyms(token):
    
    allHypernyms = set()
    synsets = token._.wordnet.synsets()
    #print(token , " ", synsets)
    for syn in synsets:
        hypernyms = syn.hypernyms()
        allHypernyms.update(hypernyms)

    return allHypernyms            

# Provides Hyponyms of a token 
def getHyponyms(token):
    
    allHyponyms = set()
    synsets = token._.wordnet.synsets()
    #print(token , " ", synsets)
    for syn in synsets:
        hyponyms = syn.hyponyms()
        allHyponyms.update(hyponyms)

    return allHyponyms            


# Provides Part Meronyms of a token 
def getPartMeronyms(token):
    
    allPartMeronyms = set()
    synsets = token._.wordnet.synsets()
    #print(token , " ", synsets)
    for syn in synsets:
        partMeronyms = syn.part_meronyms()
        #print(syn , " hyponyms ", hyponyms)
        allPartMeronyms.update(partMeronyms)

    return allPartMeronyms            


# Provides Substance Meronyms of a token 
def getSubstanceMeronyms(token):
    
    allSubstanceMeronym = set()
    synsets = token._.wordnet.synsets()
    #print(token , " ", synsets)
    for syn in synsets:
        substanceMeronym = syn.substance_meronyms()
        #print(syn , " hyponyms ", hyponyms)
        allSubstanceMeronym.update(substanceMeronym)

    return allSubstanceMeronym   


# Provides Holonyms of a token 
def getHolonyms(token):

    allHolonyms = set()
    synsets = token._.wordnet.synsets()
    #print(token , " ", synsets)
    for syn in synsets:
        holonyms = syn.member_holonyms()
        allHolonyms.update(holonyms)

    return allHolonyms            

#function to get root of a sentence
def getRoot(doc):
    
    dependC, heads = synParsing(doc)
    for i in range(0, len(dependC)):
        if dependC[i] == 'ROOT':
            root = heads[i] 
            
    #root = [token for token in doc if token.head == token][0]
    return root            

#function to create word POS map
def getPosWordMap(doc):

    posWordMap = dict()
    
    for word in doc:
        if word.pos_ not in posWordMap:
            posList = set()
            posList.add(word.text)
            posWordMap[word.pos_] = posList
        else:
            posList = posWordMap[word.pos_]
            posList.add(word.text)
            posWordMap[word.pos_] = posList
    
    return posWordMap 

# Function to run the TASK 1 and the generate and print NLP features for a single file (first file) as the Wikipedia Article. 
# Precondition: 'directory' must constain at-least one wikipedia article. 
def processFirstArticle(directory, resultDirectory):

    #------------- SCANNING THE RELEVANT FILE -------------
    wikipediaArticles = os.listdir(directory)
    #print(wikipediaArticles)
    
    nlp = spacy.load("en_core_web_sm")
    
    #nltk.download('wordnet')
    nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')

    dependCMap = dict()
    headsMap =  dict()
    namedEntityMap = dict()
    sentenceMap= dict()
    
    firstArticle = wikipediaArticles[0]
    filepath = directory + firstArticle
    
    print('Now Reading File . . . . . . . ', firstArticle)        
    
    corpus = read_data(filepath)
    doc = nlp(corpus)

    #------------- EXTRACTING NLP FEATURES ----------------
    lemmasMap = dict()
    posMap = dict()
    tagsMap = dict()
     
    synsetsMap = dict()
    hypernymsMap = dict()
    hyponymsMap = dict()

    partMeronymsMap = dict()
    substanceMeronymsMap = dict()
    holonymsMap = dict()

    #1. TOKENIZATION
    tokens = tokennize(doc)                
    
    # For each token in the document, extracting features      
    for token in doc:
        
        lemmasMap[token] = token.lemma_ # 2. Lemmatization
        posMap[token] = token.pos_ # 3. POS tagging (coarse-grained)
        tagsMap[token] = token.tag_ # 4. POS tagging (fine-grained)
                
        synsetsMap[token] = getSynsets(token) # 5. SynSet of the token
        hypernymsMap[token] = getHypernyms(token) # 6. Hypernyms
        hyponymsMap[token] = getHyponyms(token) # 7. Hyponyms

        partMeronymsMap[token] = getPartMeronyms(token) # 8. Part Meronyms
        substanceMeronymsMap[token] = getSubstanceMeronyms(token) # 9. Substance Meronyms
        holonymsMap[token] = getHolonyms(token) # 10. Holonyms
    #endFor
    
    # 11. DEPENDENCY labels and 12. SYNTACTIC HEADS for each token in the doc
    dependCMap[firstArticle], headsMap[firstArticle] = synParsing(doc)
    
    # 13. NAMED ENTITIES
    namedEntityMap[firstArticle] = getNamedEntities(doc)

    # 14. SENTENCE TOKENIZATION
    sentenceMap[firstArticle] = sentenceTokennize(doc)

    #---------------- WRITING THE FEATURES ----------------

    with open(resultDirectory + 'D01-Tokens.txt', 'w', encoding='utf-8') as f01:
        json.dump(tokens, f01)
    
    f02 =  open(resultDirectory + 'D02-Lemmas.txt', 'w')
    f02.write(str(lemmasMap))
    f02.close()
    
    f03 =  open(resultDirectory + 'D03-POS.txt', 'w')
    f03.write(str(posMap))
    f03.close()
    
    f04 =  open(resultDirectory + 'D04-Tags.txt', 'w')
    f04.write(str(tagsMap))
    f04.close()
    
    f05 = open(resultDirectory + 'D05-Synsets.txt', 'w')
    f05.write(str(synsetsMap))
    f05.close()
    
    f06 = open(resultDirectory + 'D06-Hypernyms.txt', 'w')
    f06.write(str(hypernymsMap))
    f06.close()
    
    f07 = open(resultDirectory + 'D07-Hyponyms.txt', 'w')
    f07.write(str(hyponymsMap))
    f07.close()

    f08 = open(resultDirectory + 'D08-Meronyms-Part.txt', 'w')
    f08.write(str(partMeronymsMap))
    f08.close()

    f09 = open(resultDirectory + 'D09-Meronyms-Substance.txt', 'w')
    f09.write(str(substanceMeronymsMap))
    f09.close()

    f10 = open(resultDirectory + 'D10-Holonyms.txt', 'w')
    f10.write(str(holonymsMap))
    f10.close()

    f11 = open(resultDirectory + 'D11-Dependencies.txt', 'w')
    f11.write(str(dependCMap))
    f11.close()

    f12 = open(resultDirectory + 'D12-Syntactic-Heads.txt', 'w')
    f12.write(str(headsMap))
    f12.close()

    f13 = open(resultDirectory + 'D13-Named-Entities.txt', 'w')
    f13.write(str(namedEntityMap))
    f13.close()

    f14 = open(resultDirectory + 'D14-Tokenized-Sentences.txt', 'w')
    f14.write(str(sentenceMap))
    f14.close()
    
    #------------------------------------------------------


# Function to run the TASK 1 and the generate NLP features for all the files as Wikipedia Articles. 
# Precondition: 'directory' must constain at-least one wikipedia article. 
# Returns the 14 NLP features collected from the Wikipedia Articles.
def processAllArticles(directory):

    wikipediaArticles = os.listdir(directory)
    #print(wikipediaArticles)
    
    nlp = spacy.load("en_core_web_sm")
    
    #nltk.download('wordnet')
    nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')

    dependCMap = dict()
    headsMap =  dict()
    namedEntityMap = dict()
    sentenceMap= dict()
    
    # Process all the articles and find the respective NLP features
    for article in wikipediaArticles:
        
        #--------------- SCANNING THE ARTICLE -----------------
        filepath = directory + article
        print('Now Reading File . . . . . . . ', article)        
        
        corpus = read_data(filepath)
        doc = nlp(corpus)               

        #------------- EXTRACTING NLP FEATURES ----------------
        lemmasMap = dict()
        posMap = dict()
        tagsMap = dict()
         
        synsetsMap = dict()
        hypernymsMap = dict()
        hyponymsMap = dict()

        partMeronymsMap = dict()
        substanceMeronymsMap = dict()
        holonymsMap = dict()
        
        #1. TOKENIZATION
        tokens = tokennize(doc)

        for token in doc:
            #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)     
            
            lemmasMap[token] = token.lemma_ # 2. Lemmatization
            posMap[token] = token.pos_ # 3. POS tagging (coarse-grained)
            tagsMap[token] = token.tag_ # 4. POS tagging (fine-grained)
                    
            synsetsMap[token] = getSynsets(token) # 5. SynSet of the token
            hypernymsMap[token] = getHypernyms(token) # 6. Hypernyms
            hyponymsMap[token] = getHyponyms(token) # 7. Hyponyms

            partMeronymsMap[token] = getPartMeronyms(token) # 8. Part Meronyms
            substanceMeronymsMap[token] = getSubstanceMeronyms(token) # 9. Substance Meronyms
            holonymsMap[token] = getHolonyms(token) # 10. Holonyms
        #endFor
        
        # 11. DEPENDENCY labels and 12. SYNTACTIC HEADS for each token in the doc
        dependCMap[article], headsMap[article] = synParsing(doc)
        
        # 13. NAMED ENTITIES
        namedEntityMap[article] = getNamedEntities(doc)

        # 14. SENTENCE TOKENIZATION
        sentenceMap[article] = sentenceTokennize(doc)

    # Returning all the 14 NLP features collected FOR EVERY WIKIPEDIA ARTICLE
    return tokens, lemmasMap, posMap, tagsMap, dependCMap, headsMap, namedEntityMap, synsetsMap, hypernymsMap, hyponymsMap, partMeronymsMap, substanceMeronymsMap, holonymsMap, sentenceMap
   
        
# Main function
if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")

    # where wikipedia articles resides
    directory = '../02-Project-Data/WikipediaArticles-Test/'

    # where we intend to store the result (for an article) for demo
    resultDirectory = '../06-Results/Task-01/'
    
    # UNCOMMENT TO SHOW THE DEMO OF TASK 01. Make sure to remove files from 'resultDirectory'.
    #processFirstArticle(directory, resultDirectory)

    # Implementation of TASK 01 for all the files in the 'directory'
    tokens, lemmasMap, posMap, tagsMap, dependCMap, headsMap, namedEntityMap, synsetsMap, hypernymsMap, hyponymsMap, partMeronymsMap, substanceMeronymsMap, holonymsMap, sentenceMap = processAllArticles(directory) 
    
    #print(tokens)    
    #print(lemmasMap)    
    #print(posMap)    
    #print(tagsMap)    
    #print(synsetsMap)
    #print(hypernymsMap)
    #print(hyponymsMap)
    #print(partMeronymsMap)
    #print(substanceMeronymsMap)
    #print(holonymsMap)
    #print(dependCMap)
    #print(headsMap)
    #print(namedEntityMap)              
    
#The-End