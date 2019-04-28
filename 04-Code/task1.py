#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:45:43 2019

@author: Rahul Nalawade
         Sunny Bangale
"""
import spacy
import sys
from GenerateTFIDF import computeTF
from GenerateTFIDF import computeIDF
from GenerateTFIDF import computeTFIDF

import os


# Reads data from the given file directed as in filepath, and returns it.
def read_data(filepath):
    f = open(filepath, 'r', encoding="utf8")
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


def getSynsets(token):
    
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

    return synsetsMap            


def getHypernyms(token):
    
    synsets = token._.wordnet.synsets()
        #print(t , " ", synsets)
    for syn in synsets:
        #Creating map for synonyms
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
        
    return hypernymsMap            


def getHyponyms(token):
    
    synsets = token._.wordnet.synsets()
        #print(t , " ", synsets)
    for syn in synsets:
        #Creating map for synonyms
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
        
    return hyponymsMap            


def getPartMeronyms(token):
    
    synsets = token._.wordnet.synsets()
        #print(t , " ", synsets)
    for syn in synsets:
        #Creating map for synonyms
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
        
    return partMeronymsMap            



def getSubstanceMeronyms(token):
    
    synsets = token._.wordnet.synsets()
        #print(t , " ", synsets)
    for syn in synsets:
        #Creating map for synonyms
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
        
    return substanceMeronymsMap            

def getHolonyms(token):
    
    synsets = token._.wordnet.synsets()
        #print(t , " ", synsets)
    for syn in synsets:
        #Creating map for synonyms
        holonyms = syn.member_holonyms()
        #print(syn , " member holonyms ", holonyms)

        for holo in holonyms:
            #Creating map for holonyms
            if not t in holonymsMap:
                holonymsMap[t] = set()
                holonymsMap[t].add(holo)
            else:
                holonymsMap[t].add(holo)
        #print("substanceMeronyms Map ", substanceMeronymsMap)
        
    return holonymsMap            



#Building a trie............................................
'''
class Node:
    PhraseId = -1
    #Dictionary<String, Node>
    Children = dict()
    
        
    def Node(id):
        PhraseId = id



def addPhrase(root, phrase, phraseId):

    # a pointer to traverse the trie without damaging the original reference
    node = Node()
    node = root

    # break phrase into words
    words = phrase.split();
    #print(words)
    
    # start traversal at root
    for i in range(0, len(words)):
        
        # if the current word does not exist as a child to current node, add it
        if (words[i] not in node.Children):
            node.Children[words[i]] = Node()
            #print("sarckha sarkha")
            #print(node.Children)
        else:    
            # move traversal pointer to current word
            node = node.Children[words[i]];
            #print("kadhi kadhi")

        # if current word is the last one, mark it with phrase Id
        if i == (len(words) - 1):
            node.PhraseId = phraseId;
            #print("ikde pan ala bagh")
            #print(node.Children)
            #print()


def findPhrases(root, textBody):
    # a pointer to traverse the trie without damaging the original reference
    node = Node()
    node = root
    #print(node.PhraseId)
    
    # a list of found ids
    foundPhrases = []

    # break text body into words
    words = textBody.split();
    print(words)
    
   # starting traversal at trie root and first word in text body
    i = 0
    while i < len(words):
        
        # if current node has current word as a child move both node and words pointer forward
        if (words[i] in node.Children):
            print("ithe ")
            #print("finding ",words[i],  " in ", node.Children)
            # move trie pointer forward
            node = node.Children[words[i]]
            
            # move words pointer forward
            i = i + 1
        else:
            print("ata ithe")
            # current node does not have current word in its children
            # if there is a phrase Id, then the previous sequence of words matched a phrase, add Id to found list
            if (node.PhraseId != -1):
                foundPhrases.append(node.PhraseId)

            if (node == root):
                # if trie pointer is already at root, increment words pointer
                i = i + 1
            else:
                # if not, leave words pointer at current word and return trie pointer to root
                node = root
            
    # one case remains, word pointer as reached the end and the loop is over but the trie pointer is pointing to a phrase Id
    #print(node.PhraseId)
    if (node.PhraseId != -1):
        foundPhrases.append(node.PhraseId)
        
    print("Candidate sentences ")    
    print(foundPhrases)

#...........................................................................
'''

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
    print(wikipediaArticles)

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

    '''
    #printing list of dictionaries
    for i in range(0,len(articlesDict)):
        print('At index', i)    
        print(articlesDict[i])
        print()
    '''
    
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
                print("In article ", articleId, " name ",  wikipediaArticles[articleId], "score ", score, " for token ", token)
                
                if score > maxScore:
                #if score < maxScore:
                     maxScore = score
                     scoreDict[token] = articleId
                articleId += 1
    
    #print(scoreDict)     
    
    for score in scoreDict:
        print(wikipediaArticles[scoreDict[score]])
        
    


# Main function
if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")
    
    #Process question    
    question = "Who shot Abraham Lincoln ?"
    #question = "Who founded Apple Inc."
    
    '''
    dependC, heads = synParsing(nlp(question))
    namedEntityQuestion = getNamedEntities(nlp(question))
    
    #Compute TFIDF and find the best article
    articlesTFIDFDict, wikipediaArticles = generateTFIDF()
    bestArticle = findBestArticle(articlesTFIDFDict, question, wikipediaArticles)    
    '''

    
    #AbrahamLincoln
    filepath = '../02-Project-Data/WikipediaArticles/A.txt'    
    corpus = read_data(filepath)
    doc = nlp(corpus)
    #print(corpus)
    
    
    #Task 1 processing
    
    tokens = tokennize(doc)
    #print(tokens)
   
    sentences = sentenceTokennize(doc)
    #print(sentences)
    
    lemmas = lemmatize(doc)
    #print(lemmas)
    
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
    
    
    '''
    trie = Node()
    pid = 0
    for sentence in sentences:
        #print(sentence)
        #print(pid)
        
        addPhrase(trie, sentence, pid)
        #print(trie.Children)
        #print()
        pid += 1
    
    
    findPhrases(trie, "Book")
    '''


        
    '''
    print("Head is ", heads)
    print("NM is ", namedEntityQuestion)
    print("NM is ", namedEntityQuestion[0][0])
    
    candidateSentences = findCandidateSentences(namedEntityQuestion[0][0], sentences)
    #print(candidateSentences)
    '''
    
    
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
        
        #synsetsMap = getSynsets(token)
        #hypernymsMap = getHypernyms(token)
        #hyponymsMap = getHyponyms(token)
        #partMeronymsMap = getPartMeronyms(token)
        #substanceMeronymsMap = getSubstanceMeronyms(token)
        holonymsMap = getHolonyms(token)
        
        
        '''
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
        '''
                
    print(synsetsMap)
    print(hypernymsMap)
    print(hyponymsMap)
    print(partMeronymsMap)
    print(substanceMeronymsMap)
    print(holonymsMap)
    


    
            
    
#The-End