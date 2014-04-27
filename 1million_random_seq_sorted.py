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
        arr=removeFrmStrM(arr,index[i],len(arr1))
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
        snpIndeces.append([arr[index],snp, index])

        count += 1

    return snpIndeces

def invertStr (arr, index, size):
    arr1= arr[index:index+size]
    arr=removeFrmStrM(arr,index, size)
    arr=insertToStr(arr,index, arr1[::-1])
    return arr1
        
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

print "Running..."
#create original string and ID
#ID will be a hash of the first 100 characters
for i in range(0, stringLen):
    randomBase = random.choice(nucleobaseList)
    baseFile.write(randomBase)
baseFile.close()

filename="genome1"

# Open file for getting reads
baseFile = open("ref_"+filename+".txt", "r")

baseFileList = baseFile.readline()

ID = hash(baseFileList[:100])
ID=filename
baseAnswerFile = open("ans_"+filename+".txt", "w")
baseAnswerFile.write(">ID \n")
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
    baseAnswerFile.write(">COPY\n")
    baseAnswerFile.write((str)(baseFileList[copyIndex[0]:copyIndex[0]+copyLen[copyLoop]]))
    for i in range(0, len(copyIndex)):
        baseAnswerFile.write("," + (str)(copyIndex[i]))
    baseAnswerFile.write("\n")

#Inversions
#0.001% of string is inverted
actualInv=0
invIndex=[]
orig = []
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
        # baseFileList=
        # orig =
        invIndex.append([0, temp])
        orig = invertStr(baseFileList, invIndex[actualInv-1][1], invLen)
        invIndex[invLoop][0] = orig

# Sort invIndex by the index of the inversion
invIndex = sorted(invIndex, key=lambda invIndex: invIndex[:][1])

baseAnswerFile.write(">INVERSION\n")
for i in range(0, len(invIndex)):
    baseAnswerFile.write(invIndex[i][0] + "," + (str)(invIndex[i][1]) + "\n")

#INS/DELS

# Lists of indices at which deletions and inserts were made
insList = []
delList = []

# Insertions/Deletions, split into sections of 2,000 (0.1% ins/del)
# 500 below comes from Sequence length / (Seq. length * 0.1% * 2) = 1 / (0.1% * 2)
sectionLen = int(stringLen * 0.001 * 2)
for i in range(0, int(0.0005 * stringLen)):
    
    # Make deletions in i-th section
    # Get index to delete from
    
    # Number of nucleotides to insert and delete
    numToInsDel = random.randint(1,5)
    
    # Sequence of nucleotides deleted
    delSeq = []
    delStartIndex = random.randint(i*sectionLen, ((i+1)*sectionLen) - numToInsDel)
    # Delete the nucleotides starting at the index
    for j in range(0, numToInsDel):
        nucleoDeleted = baseFileList[delStartIndex]
        baseFileList = removeFrmStr(baseFileList, delStartIndex)
        delSeq.append(nucleoDeleted)
    
    
    delList.append([str(''.join(delSeq)), str(delStartIndex)])
    #delList.append(''.join(delSeq) + "," + str(delStartIndex))
    
    # Make insertions in i-th section
    # Get index to insert at

    # Sequence of nucleotides inserted
    insSeq = []
    insStartIndex = random.randint(i*sectionLen, ((i+1)*sectionLen) - numToInsDel)
    # Insert the nucleotides starting at the index
    for j in range(0, numToInsDel):
        randomNucleo = random.choice(nucleobaseList)
        baseFileList = insertToStr(baseFileList, insStartIndex + j, str(randomNucleo))
        insSeq.append(randomNucleo)
    
    insList.append([str(''.join(insSeq)), str(insStartIndex)])    
    #insList.append(''.join(insSeq) + "," + str(insStartIndex))
            
# Write insert and delete sequences and indices to answer key file
baseAnswerFile.write(">INSERT:\n")
for i in range(0, len(insList)):
    baseAnswerFile.write(insList[i][0] + "," + (insList[i][1]))
    #baseAnswerFile.write(str(insList[i]))
    baseAnswerFile.write("\n")

baseAnswerFile.write(">DELETE:\n")
for i in range(0, len(delList)):
    baseAnswerFile.write(delList[i][0] + "," + (delList[i][1]))    
    #baseAnswerFile.write(str(delList[i]))
    baseAnswerFile.write("\n")

# END INSERTS AND DELETIONS

#SNPS
baseAnswerFile.write(">SNP")
snps = (generateSnps(baseFileList))

# Sort SNPs by increasing index
snps = sorted(snps, key=lambda snps: snps[:][2])

# baseAnswerFile.write((str)(generateSnps(baseFileList)))
for i in range(0, len(snps)):
    baseAnswerFile.write("\n" + (str)(snps[i][0])+',')
    baseAnswerFile.write((str)(snps[i][1])+',')
    baseAnswerFile.write((str)(snps[i][2]))
baseAnswerFile.close()

#READS
# File to hold reads from 1 million char sequence

readsFile = open("reads_"+filename+".txt", "w")

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
print "DONE"
