# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 18:14:29 2020

@author: surendra_dattatrey
"""

import pandas as pd
import os

os.chdir(r'C:\\Users\\suredra_work')


replacement = pd.read_excel('Word for testing.xlsx',encoding = 'utf-8')
replacement = replacement.apply(lambda x: x.astype(str).str.lower())
replacement['Word'] = replacement['Word'].str.strip()
replacement['Replacement'] = replacement['Replacement'].str.strip()

control = pd.read_excel('Control for testing.xlsx',encoding = 'utf-8')
control = control.apply(lambda x: x.astype(str).str.lower())


sentence = pd.read_excel('Sentence for testing.xlsx',encoding = 'utf-8')
sentence = sentence.apply(lambda x: x.astype(str).str.lower())

#List of words
list_word = [str(word) for word in replacement['Word'].str.lower().tolist()]
#List of replecament words
list_replacement = [str(rep) for rep in replacement['Replacement'].str.lower().tolist()]

#List of control words
list_control = [str(word) for word in control['Word'].str.lower().tolist()]

#list of common elements
common_element = [element for element in list_word if element in list_control]

#Creating key-value pair for waods and replacement
dict_replace = {}
for i in replacement['Word'].unique():
    dict_replace[i] = [str(replacement['Replacement'][j]).lower() for j in replacement[replacement['Word']==i].index]
    

#Dictionary with common words and its replacement
newdict = {k: dict_replace[k] for k in common_element}

#Empty dataframe
df = pd.DataFrame(columns=['Sentence','Word','Replacement'])
df['Sentence'] = sentence['Sentence'].str.lower()


# Method to find the words from replacementfile that are present in the sentence 
def return_token(dataframe,list_):
    temp_list = []
    for i in range(len(dataframe)):    
        sent = dataframe['Sentence'][i]
        words = []
        for word in list_:
            if word in sent:            
                words.append(word)
        temp_list.append(words)
    return temp_list

word_list = return_token(df,dict_replace.keys())
   
#Method to remove uncommon words
def replace_uncommon(list_,dict_):
    temp_list = []
    for ele in list_:
        temp_ele = [i if i in dict_.keys() else str('') for i in ele ]
        temp_list.append(temp_ele)
    return temp_list

list_final = replace_uncommon(word_list,newdict)


# Method to do replacement 
def convert(l, d):
    return [convert(x, d) if isinstance(x, list) else d.get(x, x) for x in l]

replace_list = convert(list_final,newdict)

#Method to unlist the elements
def unlist(temp_list):
    _list = []
    for listElem in temp_list:
        dummy_list = []
        for ele in listElem:        
            if len(ele) == 1:
                dummy_list.append(ele[0])
            elif len(ele) == 0:
                dummy_list.append('')
            else:   
                dummy_list.append(list(ele))
        _list.append(dummy_list)       
    return _list
new_replace_list = unlist(replace_list)

df['Word'] = word_list
df['Replacement'] = new_replace_list


#dumping file to csv
df.to_csv('result.csv',index=False,encoding = 'utf-8')

