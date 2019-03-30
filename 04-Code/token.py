#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:45:43 2019

@author: Rahul Nalawade
"""
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a text")

tokens = [token.text for token in doc]

print(tokens)
