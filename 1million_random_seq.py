'''
Created on Apr 14, 2014

@author: Gabe and Jorge Munoz
'''

import random
import sys

def removeFrmStr (arr, index):
    arr1 = arr[0:index]
    arr2 = arr[index+1:]
    return arr1+arr2


def insertToStr (arr, index, char):
    arr1 = arr[0:index]
    arr2 = arr[index:]
    return arr1+char+arr2

# Generate random genetic sequence of length 1 million
nucleobaseList = ["C","T","G","A"]

# This is the true file without error introduced
baseFile = open("1_million_random_seq.txt", "w")

# This is the true file with error introduced
baseErrorFile = open("1_million_random_seq_error.txt", "w")
counter = 0

stringLen=100000000

for i in range(0, stringLen):
    randomBase = random.choice(nucleobaseList)

    
    baseFile.write(randomBase)
    
    # Insert error bases (1% error) into an error file
    # Get value between 0 and 1
    randomCondition = random.random()
    if (randomCondition <= 0.01):
        randomBaseError = random.choice(nucleobaseList)
        while (randomBaseError == randomBase):
            randomBaseError = random.choice(nucleobaseList)
            
        baseErrorFile.write(randomBaseError)
        counter = counter + 1
        #print(str(counter) + "    " + str(randomBase) + "    " + str(randomBaseError))
        #if (randomBase == randomBaseError):
        #    print("ERROR")
    else:
        baseErrorFile.write(randomBase)
        
baseFile.close()
baseErrorFile.close()

# Open file for getting reads
baseErrorFile = open("1_million_random_seq_error.txt", "r")
baseFileList = baseErrorFile.readlines()

# File to hold reads from 1 million char sequence
readsFile = open("1_million_random_seq_error_reads.txt", "w")

for i in range(0, (int)(stringLen*0.15)):
    # First read
    startIndexPart1 = (int(random.random()*(stringLen - 210) ))
    randomGap = random.randint(90, 110)
    # Second read
    startIndexPart2 = startIndexPart1 + randomGap + 1
    
    # Insertion/deletions percentage (0.1% error) 
    # Get value between 0 and 1
    randomInDelCondition = random.random()
    
    # DELETIONS CASE
    if (randomInDelCondition > 0.005 and randomInDelCondition <= 0.01):
        tempA=0
        tempB=0
        delList = baseFileList[0][startIndexPart1:startIndexPart1+210]
        
        randomIndex = random.randint(0, 99)
        
        if(randomIndex < 50): tempA=-1
        else: 
            randomIndex += randomGap - 50
            tempB=-1
        
        delList=removeFrmStr(delList, randomIndex)
        
        readsFile.write(delList[0:50+tempA])
        readsFile.write(randomGap*'-')
        readsFile.write(delList[50+tempA+randomGap:100+tempA+randomGap+tempB])
        readsFile.write("\n")
        
    # INSERTIONS CASE    
    elif (randomInDelCondition <= 0.005):
        tempA=0
        tempB=0
        insList = baseFileList[0][startIndexPart1:startIndexPart1+210]
    
        randomIndex = random.randint(0, 99)
        
        if(randomIndex < 50): tempA=1
        else: 
            randomIndex += randomGap - 50
            tempB=1
            
        insList = insertToStr(insList, randomIndex, random.choice(nucleobaseList))
            
        readsFile.write(insList[0:50+tempA])
        readsFile.write(randomGap*'-')
        readsFile.write(insList[50+tempA+randomGap:100+tempA+randomGap+tempB])
        readsFile.write("\n")
        
    else:
        readsFile.write(baseFileList[0][startIndexPart1:startIndexPart1+50])
        readsFile.write(randomGap*'-')
        readsFile.write(baseFileList[0][startIndexPart2:startIndexPart2+50]) 
        readsFile.write("\n")
    
baseErrorFile.close()
readsFile.close()    
    