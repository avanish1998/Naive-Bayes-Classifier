#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
np.set_printoptions(precision=4)
import string
from nltk.tokenize import word_tokenize 
import re
import nltk



cnt = 0
tcor = 0
accuracy=[0,0,0,0,0]
tp=0
fp=0
fn=0
for k in range(0,5):
    file = open('a1_d3.txt','r')
    file2 = open('good.txt','w')
    file3 = open('bad.txt','w')
    file4 = open('test.txt','w')
    countb=0
    countg=0
    cnt=0
    while True:
        line = file.readline()
        if not line:
            break
        cnt += 1
        line = re.sub('[!.(,:$%^/*;?#)-]','',line)
        line = line + ' '
        temp=""
        words = word_tokenize(line) 
        for w in words: 
            w=w.lower()
            w=w.replace("'","")
            w=w.replace("`","")
            temp=temp+w;
            temp=temp+' ';
        if cnt>200*k and cnt<=200*(k+1):
            file4.writelines(temp.strip())
            file4.write("\n")
        else:
            length = len(temp)
            if temp[-2]=='1':
                countg += 1
                new_str = temp[:length-2]
                new_str = new_str+' '
                file2.writelines(new_str)
            elif temp[-2]=='0':
                countb += 1
                new_str = temp[:length-2] 
                new_str = new_str+' '
                file3.writelines(new_str)
    file5 = open('good.txt','r')
    line=file5.readline()
    wordlist = line.split()
    wordfreq = [wordlist.count(p) for p in wordlist]
    freq_good = dict(list(zip(wordlist,wordfreq)))
    file6 = open('bad.txt','r')
    line=file6.readline()
    wordlist = line.split()
    wordfreq = [wordlist.count(p) for p in wordlist]
    freq_bad = dict(list(zip(wordlist,wordfreq)))
    good2 = sum(freq_good.values())
    bad2 = sum(freq_bad.values())
    file7 = open('test.txt','r')
    correct = 0
    tc=0
    while True:
        test_query = file7.readline()
        if not test_query:
            break
        tc += 1
        length = len(test_query)
        senti = test_query[(length-2)]
        query = test_query[:length-2]
        wordlist = word_tokenize(query)
        good1 = len(wordlist)
        bad1 = len(wordlist)
        pro_bad=1
        pro_good=1
        for i in wordlist:
            word = i
            word=word.lower()
            word=word.replace("'","")
            word=word.replace("`","")
            if word in freq_good:
                count_good = freq_good[word]
            else:
                count_good=0
            if word in freq_bad:
                count_bad = freq_bad[word]
            else:
                count_bad=0
            prob_good = (count_good + 1)/(good1+good2)
            prob_bad = (count_bad + 1)/(bad1+bad2)
            pro_bad *= prob_bad
            pro_good *= prob_good
        result=0
        pro_bad *= countb/800
        pro_good *= countg/800
        if pro_bad*1000>pro_good*1000:
            result=0
        else:
            result=1
        if result==(ord(senti)-48):
            correct += 1
            tcor += 1
        if(result==1 and (ord(senti)-48)==1):
            tp += 1
        if(result==1 and (ord(senti)-48)==0):
            fp += 1
        if(result==0 and (ord(senti)-48)==1):
            fn += 1
    acc = (correct/tc)
    accuracy[k]=acc
print("Accuracy for each fold : ")
for k in range(0,5):
    print("Fold "+str(k+1)+" : "+str(accuracy[k]))
    



mean = sum(accuracy) / len(accuracy) 
variance = sum([((x - mean) ** 2) for x in accuracy]) / len(accuracy) 
dev = variance ** 0.5
mean = round(mean,3)
dev = round(dev,3)
print("Accuracy : ",mean," +/- ",dev)
precision = tp/(tp + fp)
recall = tp/(tp + fn)
print("Precision : ",precision)
print("Recall : ",recall)
f = 2*precision*recall/(precision+recall)
print("F-Score : ",f)





