# -*- coding: utf-8 -*-
"""
Created on Sun May  5 01:53:39 2019

@author: Sunny Bangale
"""

import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 
import nltk
import pysolr

from task1 import tokennize
from task1 import processAllArticles
from task1 import sentenceTokennize
from task1 import getNamedEntities
from ProcessQuestion import getQuestion


def runSolr():
    
    nlp = spacy.load("en_core_web_sm")
    
    #connect to solr Sentence Information core
    solrSentenceInformation = pysolr.Solr('http://localhost:8983/solr/SentenceInformationCore', always_commit = True, timeout=100)
    
    #conect to solr nlp core
    solrNLPCore = pysolr.Solr('http://localhost:8983/solr/NLPCore', always_commit = True, timeout = 100)

    
    candidateSentences = dict()
    sentenceIdList = list()
    bannedSet = dict()

    tokens, lemmasMap, posMap, tagsMap, dependCMap, headsMap, namedEntityMap, synsetsMap, hypernymsMap, hyponymsMap, partMeronymsMap, substanceMeronymsMap, holonymsMap, sentenceMap = processAllArticles()
    
    sentenceId = 1
    for article in sentenceMap:
        sentences = sentenceMap[article]
        
        for sentence in sentences:
            namedEntitiesList = getNamedEntities(nlp(sentence))
            
            namedEntitiesWordSet = set()
            namedEntitiesTagSet = set()
            bannedSet = set()
            
            #AbrahamLincoln.txt_584
            for ent in namedEntitiesList:
                
                namedEntitiesWordSet.add(ent[0])
                namedEntitiesTagSet.add(ent[1])
                
                #extra filter on unnecessary tags
                if(ent[1] == "PERCENT" or ent[1] == "MONEY" or ent[1] == "QUANTITY" or ent[1] == "ORDINAL" or ent[1] == "CARDINAL" ):
                    bannedSet.add(ent[0])

            coreId = article + "_" + str(sentenceId)
            #print(coreId)
            
            #'''
            #Adding indexes to Sentence Information Core
            solrSentenceInformation.add([
                {
                    "Id" : coreId,
                    "Sentence": sentence,
                    "NamedEntities": namedEntitiesTagSet
                }
            ])
            
            #'''
            #solrSentenceInformation.delete(q='*:*')
            
            sentenceId += 1
            
            #print(namedEntitiesWordSet)
            for word in namedEntitiesWordSet:
                
                if word == 'Lincoln': 
                    word = 'Abraham Lincoln'
                
                #filter unncessary words
                if(word not in bannedSet):                    
                    if word not in candidateSentences:
                        sentenceIdList = set()
                        sentenceIdList.add(coreId)
                        candidateSentences[word] = sentenceIdList
                    else:
                        sentenceIdList = candidateSentences[word]
                        sentenceIdList.add(coreId)
                        candidateSentences[word] = sentenceIdList
        
                        
    #print(candidateSentences)                                

    #'''
    
    for text in candidateSentences:
        #Adding indexes to NLP Core        
        solrNLPCore.add([
                    {
                        "Word" : text,
                        "SentenceList": candidateSentences[text]
                    }
                ])        
    #'''
    #solrNLPCore.delete(q='*:*')
    
    
    

# Main function
if __name__ == '__main__':

    
    runSolr()






