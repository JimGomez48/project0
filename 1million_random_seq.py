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
baseFile = open("ref_genome1.txt", "w")

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
baseFile.close()

# Open file for getting reads
baseFile = open("ref_genome1.txt", "r")

baseFileList = baseFile.readline()

ID = hash(baseFileList[:100])
baseAnswerFile = open("ans_genome1.txt", "w")
baseAnswerFile.write(">ID: \n")
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
            copyLen.append(copyLen[copyLoop])
            copyIndex.append(temp)
    
    baseFileList=copyToStr(baseFileList,copyIndex,copyLen[copyLoop])
    baseAnswerFile.write(">Copy Num: \n")
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
    
    for i in range(0,len(copyIndex)):
        if(temp+invLen > copyIndex[i] and temp<copyIndex[i]+copyLen[i]):
            write=0
            break
    if(write==1):
        actualInv+=1
        invIndex.append(temp)
        baseFileList=invertStr (baseFileList, invIndex[actualInv-1], invLen)
        
baseAnswerFile.write(">Inv Num: \n")
baseAnswerFile.write((str) (invIndex))
baseAnswerFile.write("\n")

#INS/DELS

# Lists of indices at which deletions and inserts were made
insList = []
delList = []

# Insertions/Deletions, split into sections of 2,000 (0.1% ins/del)
# 500 below comes from Sequence length / (Seq. length * 0.1% * 2) = 1 / (0.1% * 2)
sectionLen = int(stringLen * 0.001 * 2)
for i in range(0, int(0.0005 * stringLen)):
    # Get range of the indices of the subsection
    indicesList = range((i*sectionLen), ((i+1)*sectionLen) )
    
    # Make deletion in i-th section
    # Get index to delete from
    delIndex = random.randint(i*sectionLen, ((i+1)*sectionLen) - 1)
    # Delete the nucleotide at the index
    baseFileList = removeFrmStr(baseFileList, delIndex)
    delList.append(delIndex)
    
    # Make insertion in i-th section
    # Get index to insert at
    insIndex = random.randint(i*sectionLen, ((i+1)*sectionLen) - 2)
    # Insert a random nucleotide at the index
    baseFileList = insertToStr(baseFileList, insIndex, str(random.choice(nucleobaseList)))
    insList.append(insIndex)
       
# Write insert and delete indices to answer key file
baseAnswerFile.write(">Inserts:\n")
baseAnswerFile.write(str(insList))
baseAnswerFile.write("\n")
baseAnswerFile.write(">Deletes:\n")
baseAnswerFile.write(str(delList))
baseAnswerFile.write("\n")

# END INSERTS AND DELETIONS

#SNPS
baseAnswerFile.write(">SNP: \n")
baseAnswerFile.write((str)(generateSnps(baseFileList)))
baseAnswerFile.write("\n")

baseAnswerFile.close()

#READS
# File to hold reads from 1 million char sequence
readsFile = open("reads_genome1.txt", "w")

for i in range(0, (int)(stringLen*0.15)):
    # First read
    startIndexPart1 = (int(random.random()*(stringLen - 210) ))
    randomGap = random.randint(90, 110)
    # Second read
    startIndexPart2 = startIndexPart1 + randomGap + 1
    readList = baseFileList[startIndexPart1:startIndexPart1+210]
    
    # 1% error in reads 10% reads are garbage
    # Get value between 0 and 1
    randomReadCondition = random.random()
    
    #Throw in an error in 1% of the read length 200
    errors= (int) (0.01*200)
    
    for i in range(0,errors):
        #pick an index
        randomIndex = random.randint(0, 99)
        if(randomIndex < 50): pass
        else: randomIndex += randomGap - 50
        
        randomReadError = random.choice(nucleobaseList)
        while (randomReadError == readList[randomIndex]):
            randomReadError = random.choice(nucleobaseList)        
    
    #Full Garbage Read
    if(randomReadCondition>0.01 and randomReadCondition<0.11):
        readList=""
        for i in range(0,50):
            readList+=(random.choice(nucleobaseList) )   
        for i in range(0,randomGap):
            readList+='-'
        for i in range(50,99):
            readList+=random.choice(nucleobaseList)              
    

    readsFile.write((str) (readList[:50]))
    readsFile.write(',')
    readsFile.write((str) ( readList[50+randomGap:])) 
    readsFile.write("\n")
    
readsFile.close()    
