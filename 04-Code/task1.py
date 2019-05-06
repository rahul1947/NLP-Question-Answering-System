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
import pandas as pd
import pysolr
 
'''
from GenerateTFIDF import computeTF
from GenerateTFIDF import computeIDF
from GenerateTFIDF import computeTFIDF
'''


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


# Task 1 deliverables
def processAllArticles():
 
    nlp = spacy.load("en_core_web_sm")

    wikipediaArticles = os.listdir("../02-Project-Data/WikipediaArticles/")
    #print(wikipediaArticles)
    
    #nltk.download('wordnet')
    nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')

    dependCMap = dict()
    headsMap =  dict()
    namedEntityMap = dict()
    sentenceMap= dict()
    
    
    for article in wikipediaArticles:
        filepath = '../02-Project-Data/WikipediaArticles/'+article
        print('Now Reading File...............',article)        
        corpus = read_data(filepath)
        doc = nlp(corpus)
        #print(doc)        
        tokens = tokennize(doc)                

        lemmasMap = dict()
        posMap = dict()
        tagsMap = dict()
         
        synsetsMap = dict()
        hypernymsMap = dict()
        hyponymsMap = dict()
        partMeronymsMap = dict()
        substanceMeronymsMap = dict()
        holonymsMap = dict()
         
        #Traverse every token and extract synsets and create dictionaries 
        #for t in tokens:        
            #token = nlp(t)[0]
            #print(t," ", token)
            
        for token in doc:
            #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)     
            
            lemmasMap[token] = token.lemma_
            posMap[token] = token.pos_
            tagsMap[token] = token.tag_
                    
            synsetsMap[token] = getSynsets(token)
            hypernymsMap[token] = getHypernyms(token)
            hyponymsMap[token] = getHyponyms(token)
            partMeronymsMap[token] = getPartMeronyms(token)
            substanceMeronymsMap[token] = getSubstanceMeronyms(token)
            holonymsMap[token] = getHolonyms(token)
         
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
        
        dependCMap[article], headsMap[article] = synParsing(doc)
        #print(dependCMap)
        #print(headsMap)
        
        namedEntityMap[article] = getNamedEntities(doc)
        #print(namedEntityMap)
        
        sentenceMap[article] = sentenceTokennize(doc)

    return tokens, lemmasMap, posMap, tagsMap, dependCMap, headsMap, namedEntityMap, synsetsMap, hypernymsMap, hyponymsMap, partMeronymsMap, substanceMeronymsMap, holonymsMap, sentenceMap
    


def findTop10CandidateSentences(question, sentences):
    
    candidates = collections.Counter()
    
    for sentence in sentences:
        sentenceWords = tokennize(nlp(sentence))
        wordmatches = set(filter(set(tokennize(nlp(question))).__contains__, sentenceWords))
        candidates[sentence] = len(wordmatches)
    #print(dictionary)   
    #print(candidates.most_common(10))    
    return candidates.most_common(10)
    

def findCandidateSentences(question, sentences):
    
    questionTokens = tokennize(nlp(question))
    candidateSentences = []
    
    for questionToken in questionTokens:
        for sentence in sentences:
            
            if questionToken in sentence:
                    candidateSentences.append(sentence)
                    
    return candidateSentences                
        

def generateTFIDF():

    nlp = spacy.load("en_core_web_sm")

    wikipediaArticles = os.listdir("../02-Project-Data/WikipediaArticles/")
    #print(wikipediaArticles)

    wordSets = set()    
        
    for article in wikipediaArticles:
        filepath = '../02-Project-Data/WikipediaArticles/'+article
        print('Now Reading File...............',article)        
        corpus = read_data(filepath)
        doc = nlp(corpus)
        #print(doc)        
        tokens = tokennize(doc)                
        wordSets = wordSets.union(set(tokens))

        
    # Generatting TF IDF
    articlesDict = list()
    articlesTFDict = list()
    articlesTFIDFDict = list()
        
    for article in wikipediaArticles:
        filepath = '../02-Project-Data/WikipediaArticles/'+article
        print('Now Processing File...............',article)        
        corpus = read_data(filepath)
        doc = nlp(corpus)
        #print(doc)        
        tokens = tokennize(doc)
                        
        wordDict = dict()
        TFDict = dict()
        TFIDFDict = dict()
        
        wordDict = dict.fromkeys(wordSets, 0)        
        for token in tokens:
            wordDict[token] += 1
        #print('................',len(wordDict),'...................')
        
        #creating list of dictionaries of word counts of every article    
        articlesDict.append(wordDict)
        
        #creating list of dictionaries of TF of every article    
        TFDict = computeTF(wordDict, tokens)
        articlesTFDict.append(TFDict)
        
        idfs = computeIDF(articlesDict)        
        
        TFIDFDict = computeTFIDF(TFDict, idfs)
        #print("TFIDFDict ",TFIDFDict)
        print("...................")
        articlesTFIDFDict.append(TFIDFDict)    
        
    print(articlesTFIDFDict)
    
    return articlesTFIDFDict, wikipediaArticles

    #printing list of dictionaries
    #for i in range(0,len(articlesDict)):
    #    print('At index', i)    
    #    print(articlesDict[i])
    #    print()
    
    
    
    
def findBestArticle(articlesTFIDFDict, question, wikipediaArticles):
    
    questionTokens = tokennize(nlp(question))
    questionDict = dict()
    scoreDict = dict()
    
    articleId = 0
    maxScore = 0
    for token in questionTokens:
        print("Checking token ", token)
        articleId = 0
        maxScore = -sys.maxsize -1
        #maxScore = sys.maxsize
        
        for article in articlesTFIDFDict:
            if token in article:
                score = article[token]
                print(score)
                print("In article ", articleId, " name ",  wikipediaArticles[articleId], "score ", score, " for token ", token)
                
                if score > maxScore:
                #if score < maxScore:
                     maxScore = score
                     scoreDict[token] = articleId
                articleId += 1
    
    #print(scoreDict)     
    
    #for score in scoreDict:
        #print(wikipediaArticles[scoreDict[score]])
        
    
    
        
# Main function
if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")
    
    tokens, lemmasMap, posMap, tagsMap, dependCMap, headsMap, namedEntityMap, synsetsMap, hypernymsMap, hyponymsMap, partMeronymsMap, substanceMeronymsMap, holonymsMap, sentenceMap = processAllArticles()
    
    #print(namedEntityMap)
    
    #Process question    
    #question = "Lincoln ?"
    #question = "Who founded Apple Inc."
    
    #runSolr()
    
    '''
    dependC, heads = synParsing(nlp(question))
    namedEntityQuestion = getNamedEntities(nlp(question))
    
    #Compute TFIDF and find the best article
    articlesTFIDFDict, wikipediaArticles = generateTFIDF()
    bestArticle = findBestArticle(articlesTFIDFDict, question, wikipediaArticles)    
    print(bestArticle)
    '''

    #Naive way of finding the candidate sentences  
    #candidateSentences = findTop10CandidateSentences(question, sentences)
    #print(candidateSentences)

    #Naive way of finding the candidate sentences
    '''
    print("Head is ", heads)
    print("NM is ", namedEntityQuestion)
    print("NM is ", namedEntityQuestion[0][0])
    
    candidateSentences = findCandidateSentences(namedEntityQuestion[0][0], sentences)
    #print(candidateSentences)
    
    done = True
    for (sentence, matches) in candidateSentences:
        
        if questionType(question) == "PERSON":
            for (text, label) in getNamedEntities(nlp(sentence)):    
                if "PERSON" == label:
                    answer = text
                    print("Found!!! ", answer)
                    done = True
                elif done:
                    break
    '''    
                    
    
#The-End