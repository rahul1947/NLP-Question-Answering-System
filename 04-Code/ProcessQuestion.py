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
import pysolr
import re

from task1 import getNamedEntities
from task1 import getRoot
from task1 import lemmatize
from task1 import getPosWordMap

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
def searchAnswerInSolr(questionEntitiesList, questionType, questionRoot, questionWordPosMap):
    
    nlp = spacy.load("en_core_web_sm")

    #connect to solr Sentence Information core
    solrSentenceInformation = pysolr.Solr('http://localhost:8983/solr/SentenceInformationCore', always_commit = True, timeout=10)
    
    #conect to solr nlp core
    solrNLPCore = pysolr.Solr('http://localhost:8983/solr/NLPCore', always_commit = True, timeout=10)
    
    allCandidateSentences = list()
    
    #search candidate sentences
    for tuple in questionEntitiesList:

        cleanedWord = re.sub(r'[^\w\s\'s]', ' ', tuple[0])
        results = solrNLPCore.search('Word:' + cleanedWord)    
        #print("Saw {0} result(s).".format(len(results)))
        
        for result in results:
            #iterate all intermediate results
            for r in result['SentenceList']:
                allCandidateSentences.append(r)
        #print()
         
    #print(allCandidateSentences)
    
    probableAnswerDocs = list()
    probableAnswerList = list()
    probableAnswerSentences = list()
    
    '''
    questionFilters = ""
    for i in questionType:
        questionFilters += i + ' OR ' 
    questionFilters = questionFilters[:-3]
    #print(questionFilters)
    '''
    #search answer from candidate sentences
    for sentence in allCandidateSentences:
        
        results = solrSentenceInformation.search('q = Id:' + sentence)
        #print("Saw {0} result(s).".format(len(results)))
       
        for result in results:
            
            coreId = result['Id']
            sentence = result['Sentence']    
            namedEntitiesSet = set()
            namedEntitiesSet.update(result['NamedEntities'])
            #print(coreId)
            #print(sentence)
            #print(namedEntitiesSet)
            
            ''''            
            intersectionNamedEntities = questionType.intersection(namedEntitiesSet)
            sentenceNamedEntities = getNamedEntities(nlp(sentence[0]))
            
            if len(intersectionNamedEntities) > 0:                
                for entity in intersectionNamedEntities:
                    for wordTags in sentenceNamedEntities:
                        if entity == wordTags[1]:
                            probableAnswerList.append(wordTags[0])
                            probableAnswerDocs.append(coreId[0])
                            probableAnswerSentences.append(sentence[0])
            '''
            if questionType.intersection(namedEntitiesSet):
                probableAnswerSentences.append(sentence[0])
                probableAnswerDocs.append(coreId[0])
                
    #print(probableAnswerList)    
    #print(probableAnswerDocs)
    #print(probableAnswerSentences)
    
    answerList = list()
    answerDocs= list()
    answerSentences = list()
    
    #Filter answers based on root, lemma and pos tags
    for i in range(len(probableAnswerSentences)):
        sentenceRoot = getRoot(nlp(probableAnswerSentences[i]))
        questionRootLemma = lemmatize(nlp(questionRoot))
        sentenceRootLemma = lemmatize(nlp(sentenceRoot))
        
        if questionRoot == sentenceRoot or questionRootLemma == sentenceRootLemma:
            answerSentences.append(probableAnswerSentences[i])
            answerDocs.append(probableAnswerDocs[i])
        else:
            sentencePosWordMap = getPosWordMap(nlp(probableAnswerSentences[i]))
            
            if 'NOUN' in sentencePosWordMap and 'NOUN' in questionPosWordMap and sentencePosWordMap['NOUN'].intersection(questionPosWordMap['NOUN']):
                answerSentences.append(probableAnswerSentences[i])
                answerDocs.append(probableAnswerDocs[i])
            if 'VERB' in sentencePosWordMap and 'VERB' in questionPosWordMap and sentencePosWordMap['VERB'].intersection(questionPosWordMap['VERB']):
                answerSentences.append(probableAnswerSentences[i])
                answerDocs.append(probableAnswerDocs[i])
            if 'PROPN' in sentencePosWordMap and 'PROPN' in questionPosWordMap and sentencePosWordMap['VERB'].intersection(questionPosWordMap['VERB']):
                answerSentences.append(probableAnswerSentences[i])
                answerDocs.append(probableAnswerDocs[i])
            if 'PRON' in sentencePosWordMap and 'PRON' in questionPosWordMap and sentencePosWordMap['VERB'].intersection(questionPosWordMap['VERB']):
                answerSentences.append(probableAnswerSentences[i])
                answerDocs.append(probableAnswerDocs[i])
                  
                        
    if len(answerSentences) > 0:
        print(answerSentences)
        print(answerDocs)
    else:
        print('No answer found!')        
        
    
    

# Main function
if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")
    
    #Process question    
    #question = "Who founded Apple Inc.?"
    #question = "When was Apple Inc. founded?"
    #question = "When did Abraham Lincoln die?"
    #question = "Who founded Apple Inc.?"
    #question = "Where is Apple’s headquarters?"
    #question = "Where did Thomas Lincoln purchase farms?"
    #question = "Where is the headquarters of AT&T?"
    #question = "When did Steve Jobs die?"
    #question = "Where is Apple’s headquarters?"
    #question = "Who supported Apple in creating a new computing platform?"
    #question = "Where did Thomas Lincoln purchase farms?"
    #question = "Who supported Apple in creating a new computing platform?"
    question = "Where was Melinda born?"
        
    #derive question type
    questionType = questionType(question)
    #print(questionType)
    
    questionEntitiesList = getNamedEntities(nlp(getQuestion()))
    #print("Question entities ", questionEntitiesList)
    
    questionPosWordMap = getPosWordMap(nlp(question))
    #print(questionPosWordMap)
    
    questionRoot = getRoot(nlp(question))
    #print(questionRoot)
    #questionRoot = 'founded'
        
    searchAnswerInSolr(questionEntitiesList, questionType, questionRoot, questionPosWordMap)
    
    












