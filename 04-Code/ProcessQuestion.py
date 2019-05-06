# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 17:07:29 2019

@author: Sunny Bangale
"""

import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 
import nltk
import sys
import os
import collections
import pandas as pd
import pysolr

from task1 import getNamedEntities

question = ""

#function to derive question type
def questionType(question):

    question = str.lower(question)
    questionTokens = set()
    questionTokens.update(question.split())
            
    if "who" in questionTokens or "whom" in questionTokens:
        tempSet = set()
        tempSet.update(["PERSON", "ORG", "NORP"])
        return tempSet
    elif "when" in questionTokens:
        tempSet = set()
        tempSet.update(["DATE", "TIME", "EVENT", "DATETIME"])
        return tempSet
    elif "where" in questionTokens:
        tempSet = set()
        tempSet.update(["LOC", "GPE", "FAC", "EVENT"])
        return tempSet
    else:
        tempSet = set()
        tempSet.update(["UNKOWN"])
        return tempSet
    
    
def getQuestion():
    return question

#funtion to searc answer in Solr
def searchAnswerInSolr(questionEntitiesList, questionType):
    
    #connect to solr Sentence Information core
    solrSentenceInformation = pysolr.Solr('http://localhost:8983/solr/SentenceInformationCore', always_commit = True, timeout=10)
    
    #iso-8859-1
    
    #conect to solr nlp core
    solrNLPCore = pysolr.Solr('http://localhost:8983/solr/NLPCore', always_commit = True, timeout=10)
    
    allCandidateSentences = list()
    
    #search candidate sentences
    for tuple in questionEntitiesList:
        results = solrNLPCore.search('Word:' + tuple[0])    
        #print("Saw {0} result(s).".format(len(results)))
        
        for result in results:
            #iterate all intermediate results
            for r in result['SentenceList']:
                allCandidateSentences.append(r)
        print()
            
    
    #print(allCandidateSentences)
    
    answerList = set()
    
    questionFilters = ""
    for i in questionType:
        questionFilters += i + ' OR ' 
    questionFilters = questionFilters[:-3]
    
    print(questionFilters)

    #search answer from candidate sentences
    for sentence in allCandidateSentences:
        results = solrSentenceInformation.search(q = 'Id:' + sentence , fq= 'NamedEntities:' + questionFilters )    
        print("Saw {0} result(s).".format(len(results)))
       
        for result in results:
            
            coreId = result['Id']
            sentence = result['Sentence']
            #file = open('testfile.txt','a',encoding='utf8')  
            #file.write(sentence[0]) 
            
            namedEntitiesSet = set()
            namedEntitiesSet.update(result['NamedEntities'])
            #print(coreId)
            print(sentence)
            #print(namedEntitiesSet)
            
            sentenceNamedEntities = getNamedEntities(nlp(sentence[0]))
            
            
            for entity in questionEntitiesList:
                for wordTags in sentenceNamedEntities:
                    if entity[1] == wordTags[1]:
                        answerList.add(wordTags[0])
            
        print()
        
        
        
    print(answerList)    
    print(len(answerList))        
        
    
    
    

# Main function
if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")
    
    #Process question    
    question = "Who founded Apple Inc. ?"
    
    #derive question type
    questionType = questionType(question)
    #print(questionType)
    
    questionEntitiesList = getNamedEntities(nlp(getQuestion()))
    #print(questionEntitiesList)
            
    searchAnswerInSolr(questionEntitiesList, questionType)
    
    












