#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:41:34 2019

@author: Rahul Nalawade
"""
import io
import json

data = []

test_questions = ["this is question 1", "this is question 2", "this is question 3", "this is question 4"]


for question in test_questions:
    
    answers = {}
    answers['1'] = "first answer"
    answers['2'] = "second answer"
    
    sentences = {}
    sentences['1'] = "first sentence"
    sentences['2'] = "second sentence"
    
    documents = {}
    documents['1'] = "document1.txt"
    documents['2'] = "document2.txt"
    
    data.append({
        'question': question,
        'answers': answers,
        'sentences': sentences,
        'documents': documents
    })
#endFor

jstr = json.dumps(data, ensure_ascii=False, indent=4)

print(jstr)
    
with io.open('output.txt', 'w', encoding='utf-8') as f:
    f.write(jstr)

