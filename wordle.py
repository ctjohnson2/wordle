#!/usr/bin/python3



from numpy import *
import numpy as np


import math
import sys
import re
import os
from os import system

import subprocess

import xml.etree.ElementTree as ET



def getgreys(dictionary,dictionaryscores,greyss):

    if len(greys)!=0:
       newlist = []
       newlistscores = []
       d=0
       for word in dictionary:

           c = 0
           for grey in greyss:

               if word.count(grey)!=0:

                  c+=1
           if c == 0:

              newlist.append(word)
              newlistscores.append(dictionaryscores[d])
           d+=1
       return newlist,newlistscores
    else:
       return dictionary,dictionaryscores

def getyellows(dictionary,dictionaryscores,yellowss,yc):

    if yc!=0:
       newlist = []
       newlistscores=[]
       d=0
       for word in dictionary:
           c=0
           r=0
      #     print(word)
           for i in range(len(yellowss)):

               if word.count(yellows[i]) > 0:

                  c+=1
               if word[i]==yellows[i]:
                  r+=1
     #      print(c,r)
           if c == yc and r==0:

              newlist.append(word)
              newlistscores.append(dictionaryscores[d])
           d+=1
       return newlist,newlistscores
    else:
        return dictionary,dictionaryscores

def getgreens(dictionary,dictionaryscores,greenss,gc):

    if gc!=0:
       newlist = []
       newlistscores=[]
       d=0
       for word in dictionary:
           c=0

           for i in range(len(greenss)):

               if greenss[i]==word[i]:

                  c+=1
    #       print(word,c,gc)
           if c == gc:

              newlist.append(word)
              newlistscores.append(dictionaryscores[d])
           d+=1
       return newlist,newlistscores
    else:
        return dictionary,dictionaryscores


def reorderdictionary(dictionary,dictionaryscores):
    newlist=[]

    newlistscores=[]
    
    c=0
    d=0

    N = len(dictionary)

    while d!=(N):
          topdog=0
          
          for i in range(len(dictionary)):

              if float(dictionaryscores[i]) > topdog:

                 topdog = dictionaryscores[i]
                 c=i
          
          newlist.append(dictionary[c])
          newlistscores.append(dictionaryscores[c])
          dictionary.pop(c)
          dictionaryscores.pop(c)
          d+=1
 
    return newlist,newlistscores
## get 5 letter words
fiveletdic = []
f=open("en_US.dic","r")

lines = f.readlines()

for line in lines:
    noslash = line.find("/")
    nopost = line.find("'")
    upper = (line.strip()).isupper()
    if nopost < 0 and upper == False and len(line.split('/')[0].strip())==5:
       fiveletdic.append(line.split('/')[0].strip()) 

f.close()


#### want to find optimal first word

Numwords = len(fiveletdic)
#### first find how many times each letter occurrs
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
#fiveletdic=["oases"]
### but first get rid of words with same letter
fiveletdicnodups = []
for word in fiveletdic:
    c = 0
    for letter in alphabet:
        if word.count(letter)==1:
           c+=word.count(letter)
          # print(letter,word.count(letter))
    
    if c== 5:

       fiveletdicnodups.append(word)



lettcount = []

for letter in alphabet:

    c=0
    for word in fiveletdicnodups:
   
        if word.count(letter) == 1:
           c+=1
    lettcount.append(c)

#### get word with highest lettcount sum

bestword=""
bestwordcount=0

for word in fiveletdicnodups:

    total = 0

    for i in range(0,5):

        for j in range(len(alphabet)):

            if word[i] == alphabet[j]:

               total+=lettcount[j]
               

    if bestwordcount < total:

        bestwordcount = total

        bestword = word



wordscores=[]
for word in fiveletdic:

    total = 0

    for i in range(0,5):

        for j in range(len(alphabet)):

            if word[i] == alphabet[j]:

               total+=lettcount[j]

    wordscores.append(total)



weights = [[] for i in range(0,5)]


for letter in alphabet:
    d0=0
    d1=0
    d2=0
    d3=0
    d4=0
    for word in fiveletdic:
        d0+= word[0].count(letter)
        d1+=word[1].count(letter)
        d2+=word[2].count(letter)
        d3+=word[3].count(letter)
        d4+=word[4].count(letter)
    weights[0].append(d0/Numwords)
    weights[1].append(d1/Numwords)
    weights[2].append(d2/Numwords)
    weights[3].append(d3/Numwords)
    weights[4].append(d4/Numwords)


for i in range(len(alphabet)):
    tots = weights[0][i]+weights[1][i]+weights[2][i]+weights[3][i]+weights[4][i]
    print(alphabet[i]+" = "+str(weights[0][i])+" "+str(weights[1][i])+" "+str(weights[2][i])+" "+str(weights[3][i])+" "+str(weights[4][i])+" "+str(tots/5))
newwordscores=[]
c=0
for word in fiveletdic:
    score = 0
    for i in range(0,5):
        for j in range(len(alphabet)):

            if word[i].count(alphabet[j])==1:
               score+=weights[i][j]
    newwordscores.append(score+wordscores[c]/Numwords)
    c+=1


#tmp = reorderdictionary(fiveletdic,newwordscores)

#print(tmp[0])
#print(tmp[1])





firstwordchoice = input("The optimal word is "+bestword+" , would you like to use this word? If so type: sure\n")

firstword=""


if firstwordchoice == "sure":
   print("Hell of a choice!")
   firstword = bestword


else:

    firstword = input("you fucking hate "+bestword+" ... fine, type your five letter word here:\n")

if len(firstword) != 5:

    print("If you hate resat so much you have to at least pick a 5 letter word")
    exit(1)


##### round 1 ###################################################


greylets = input("ROUND 1!!! EXCITING!!! I BET THE ANSWER IS RESAT!!!\n Can you tell me what letters sucked (grey)? Type the letters in no spaces, if none were grey just press Enter\n")

yellowlets = input("Any yellows ??? If yes type them with letter-order, for ex: for e,c in space type in: ???ce. If no green just press Enter\n")

greenlets = input("Any greens ???? If yes type them with letter-order, for ex: for e,c in space type in: ???ce. If no green just press Enter\n")


### grey stage #######################

greys = []

for i in range(len(greylets)):

    greys.append(greylets[i])

yellows = []

yellowcount=0
for i in range(len(yellowlets)):

    yellows.append(yellowlets[i])
    if yellowlets[i]!="?":

        yellowcount+=1

greens = []
greencount =0
for i in range(len(greenlets)):

    greens.append(greenlets[i])
    if greenlets[i]!="?":

        greencount+=1



print(yellowcount,greencount)
newlistgrey = getgreys(fiveletdic,wordscores,greys)
print("got greys")
newlistyellow=getyellows(newlistgrey[0],newlistgrey[1],yellows,yellowcount)    
print("got yellows")
newlistgreentmp = getgreens(newlistyellow[0],newlistyellow[1],greens,greencount)
print("got greens")

newlistgreen=reorderdictionary(newlistgreentmp[0],newlistgreentmp[1])
print("reordered")
for i in range(0,4):

    print(newlistgreen[0])
    print(newlistgreen[1])


    greylets = input("ROUND "+str(i+2)+"!!! Tell me the greys\n")

    yellowlets = input("Any yellows ??? If yes type them with letter-order, for ex: for e,c in space type in: ???ce. If no green just press Enter\n")

    greenlets = input("Any greens ???? If yes type them with letter-order, for ex: for e,c in space type in: ???ce. If no green just press Enter\n")


    greys = []

    for i in range(len(greylets)):

        greys.append(greylets[i])

    yellows = []
    yellowcount=0
    for i in range(len(yellowlets)):

        yellows.append(yellowlets[i])

    
        if yellowlets[i]!="?":

           yellowcount+=1

    greens = []
    greencount =0
    for i in range(len(greenlets)):

        greens.append(greenlets[i])
        if greenlets[i]!="?":

           greencount+=1

    newlistgrey = getgreys(newlistgreen[0],newlistgreen[1],greys)
    print("got greys")
    newlistyellow=getyellows(newlistgrey[0],newlistgrey[1],yellows,yellowcount)
    print("got yellows")
    newlistgreentmp = getgreens(newlistyellow[0],newlistyellow[1],greens,greencount)
    print("got greens")
    newlistgreen = reorderdictionary(newlistgreentmp[0],newlistgreentmp[1])
    print("reordered")

