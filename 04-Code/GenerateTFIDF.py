# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 23:47:54 2019

@author: Owner
"""
import math

def computeTF(wordDict, tokens):
    tfDict = {}
    tokenCount = len(tokens)
    
    for word, count in wordDict.items():
        tfDict[word] = count/ float(tokenCount)
    
    #print("tfDict ", tfDict)
    return tfDict
    

def computeIDF(articleList):
    
    idfDict = {}
    N = len(articleList)
    idfDict = dict.fromkeys(articleList[0].keys(), 0)
    
    for article in articleList:
        for word, val in article.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        #print("word ",word," val ",val)
        #something needs to be changed here
        #if val > 0:
        idfDict[word] = math.log10(N / (float(val) + 1.0))
    
    #print("idfDict ", idfDict)
    return idfDict            


def computeTFIDF(tfBows, idfs):
    tfidf = {}
    
    for word, val in tfBows.items():
        tfidf[word] =  val * idfs[word]
    
    return tfidf    

    
    
    
    
    
    
    