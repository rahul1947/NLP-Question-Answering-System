# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 17:07:29 2019

@author: Sunny
"""

def process(question):

    question = str.lower(question)
    questionTokens = question.split()
            
    if "who" in questionTokens or "whom" in questionTokens:
        return "PERSON"
    elif "when" in questionTokens:
        return "DATE"
    elif "where" in questionTokens:
        return "LOCATION"
    else:
        return "UNKOWN"
    


# Main function
if __name__ == '__main__':


    print(process("When is Apple ?"))













