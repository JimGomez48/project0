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

def removeFrmStrM (arr, index, size):
    arr1 = arr[0:index]
    arr2 = arr[index+size:]
    return arr1+arr2

def insertToStr (arr, index, char):
    arr1 = arr[0:index]
    arr2 = arr[index:]
    return arr1+char+arr2

def copyToStr (arr, index, size):
    arr1=arr[index[0]:index[0]+size]
    #copy the substring into the array
    for i in range(1,len(index)):
        arr=insertToStr(arr,index[i], arr1)
    return arr

'''
Generates snps at random indeces in the array and returns a list
of the indeces of snps
'''
def generateSnps(arr):
    origLength = len(arr)
    count = 0.0
    snpIndeces = []

    while (count/len(arr)) < .003:
        index = random.randint(0, len(arr))
        snpIndeces.append(index)
        if arr[index] == "A":
            snp = random.choice(["C", "G", "T"])
        elif arr[index] == "C":
            snp = random.choice(["A", "G", "T"])
        elif arr[index] == "G":
            snp = random.choice(["A", "C", "T"])
        elif arr[index] == "T":
            snp = random.choice(["A", "C", "G"])

        removeFrmStr(arr, index)
        insertToStr(arr, index, snp)

        count += 1
        # print count
        # print index
        # print "orig: " + arr[index]
        # print "snp: " + snp

    # print snpIndeces
    return snpIndeces

def invertStr (arr, index, size):
    arr1= arr[index:index+size]
    arr=removeFrmStrM(arr,index, size)
    arr=insertToStr(arr,index, arr1[::-1])
    return arr
        
# Generate random genetic sequence of length 1 million
nucleobaseList = ["C","T","G","A"]

# This is the true file without error introduced
baseFile = open("1_million_random_seq.txt", "w")

counter = 0

#This is where we will store the answer key, which includes:
#ID
#Copy numbers
#Ins/Del
#
stringLen=1000000

#create original string and ID
#ID will be a hash of the first 100 characters

for i in range(0, stringLen):
    randomBase = random.choice(nucleobaseList)
    baseFile.write(randomBase)
    
    # Insert error bases (1% error) into an error file
    # Get value between 0 and 1
    '''randomCondition = random.random()
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
        baseErrorFile.write(randomBase)'''
baseFile.close()
#baseErrorFile.close()

# Open file for getting reads
baseFile = open("1_million_random_seq.txt", "r")

baseFileList = baseFile.readline()

ID = hash(baseFileList[:100])
baseAnswerFile = open("1_million_random_seq_error_ans_key.txt", "w")
baseAnswerFile.write("ID: ")
baseAnswerFile.write(str(ID))
baseAnswerFile.write("\n")

#Copy Numbers
#Sequence of random length between 20-50

copyIndex=[]
copyLen=[]
for copyLoop in range(0,1):
    copyLen.append(random.randint(20,50))
    copyIndex.append(int(random.random()*(stringLen - copyLen[copyLoop]) ))
    
    #0.001% of the time the string is copied
    for i in range (0,(int)(stringLen*0.00001)):
        temp=(int(random.random()*(stringLen - copyLen[copyLoop]) ))
        write=1
        for j in range (0,len(copyIndex)-1):
            if(temp>copyIndex[j] and temp<copyIndex[j]+copyLen[copyLoop]):
                write=0
                break;
        if(write==1):
            copyIndex.append(temp)
    
    baseFileList=copyToStr(baseFileList,copyIndex,copyLen[copyLoop])
    baseAnswerFile.write("Copy Num: \n")
    baseAnswerFile.write((str) (baseFileList[copyIndex[0]:copyIndex[0]+copyLen[copyLoop]]))
    baseAnswerFile.write("\n")
    baseAnswerFile.write((str) (copyIndex))
    baseAnswerFile.write("\n")

#Inversions
#0.001% of string is inverted
actualInv=0
invIndex=[]
for invLoop in range(0, (int)(0.00001*stringLen)):
    write =1
    temp=int(random.random()*(stringLen - copyLen[copyLoop]) )
    invLen = random.randint(20,50)
    
    #CopyLen[0] for now
    # UPDATE THIS WHEN POSSIBLE
    #
    
    for i in range(0,len(copyIndex)):
        if(temp+invLen > copyIndex[i] and temp<copyIndex[i]+copyLen[0]):
            write=0
            break
    if(write==1):
        actualInv+=1
        invIndex.append(temp)
        baseFileList=invertStr (baseFileList, invIndex[actualInv-1], invLen)
        
baseAnswerFile.write("Inv Num: \n")
baseAnswerFile.write((str) (invIndex))
baseAnswerFile.write("\n")

baseAnswerFile.close()

#sys.exit([0])

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
