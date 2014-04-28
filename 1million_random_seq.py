'''
Created on Apr 14, 2014

@author: Jorge Munoz, Gabriel Alsheikh, and James Gomez
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


sys.argv[1:]
if(len(sys.argv)==1):
    print "The program requires 1 input in the following format: \n"
    print "python chromosomes.py genomeID \n"
    
    sys.exit()
filename=sys.argv[1]

chromosomes =1
stringLen=1000000

# This is the true file without mutations introduced
#This is done only for random string outputs
#For the human genome, this part can be left out completely
baseFile = open("ref_"+filename+".txt", "w")   
print "Generating the reference GENOME..."
for i in range(1, chromosomes*stringLen+1):
    randomBase = random.choice(nucleobaseList)
    baseFile.write(randomBase)
    if(i%stringLen==0): baseFile.write("\n")
baseFile.close()
print "Reference genome COMPLETE"

#filename="genome1"

baseAnswerFile = open("ans_"+filename+".txt", "w")
baseAnswerFile.write(">")
baseAnswerFile.write(str(filename))
baseAnswerFile.write("\n")

readsFile = open("reads_"+filename+".txt", "w")

fullCOPYseq=[]
fullCOPY=[]
fullINVseq=[]
fullINV=[]
fullINS=[]
fullDEL=[]
fullSNP=[]

# Open file for getting reads
baseFile = open("ref_"+filename+".txt", "r")

for chrome in range(1,chromosomes+1):
    counter = 0
    
    #This is where we will store the answer key, which includes:
    #ID
    #Copy numbers
    #Ins/Del
    
    print "Generating mutations in chromosome: "+str(chrome)
    baseFileList = baseFile.readline()
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
        fullCOPY.append(copyIndex)
        fullCOPYseq.append((str)(baseFileList[copyIndex[0]:copyIndex[0]+copyLen[copyLoop]]))
        baseFileList=copyToStr(baseFileList,copyIndex,copyLen[copyLoop])
    
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
    
    fullINV.append(invIndex)
    
    #INS/DELS
    
    # Lists of indices at which deletions and inserts were made
    insList = []
    delList = []
    
    # Insertions/Deletions, split into sections of 2,000 (0.1% ins/del)
    # 500 below comes from Sequence length / (Seq. length * 0.1% * 2) = 1 / (0.1% * 2)
    sectionLen = int(stringLen * 0.001 * 2)
    for i in range(0, int(stringLen/sectionLen)):
        
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
             
    fullINS.append(insList) 
    fullDEL.append(delList)
    
    # END INSERTS AND DELETIONS
    
    #SNPS
    snps = (generateSnps(baseFileList))
    
    # Sort SNPs by increasing index
    snps = sorted(snps, key=lambda snps: snps[:][2])
    fullSNP.append(snps)
    
    #READS
    # File to hold reads from 1 million char sequence
    
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
        
        readsFile.write(str(chrome)+",")
        readsFile.write((str) (readList[:50]))
        readsFile.write(',')
        readsFile.write((str) ( readList[50+randomGap:])) 
        readsFile.write("\n")

#copys
baseAnswerFile.write(">COPY: \n")
for i in range(0,chromosomes):
    baseAnswerFile.write(str(i+1)+","+str(fullCOPYseq[i]))
    for j in range(len(fullCOPY[i])):
        baseAnswerFile.write(","+str(fullCOPY[i][j]))
    baseAnswerFile.write("\n")
    
#inversions
baseAnswerFile.write(">INVERSION: \n")
for i in range(0,chromosomes):
    for j in range(0,len(fullINV[i])):
        baseAnswerFile.write(str(i+1)+","+str(fullINV[i][j][0]) + "," + (str)(fullINV[i][j][1]) + "\n")


#inserts
baseAnswerFile.write(">INSERT:\n")
for i in range(0,chromosomes):
    for j in range(0, len(fullINS[i])):
        baseAnswerFile.write(str(i+1)+","+str(fullINS[i][j][0]) + "," + str(fullINS[i][j][1]))
        baseAnswerFile.write("\n")    
#deletes
baseAnswerFile.write(">DELETE:\n")
for i in range(0,chromosomes):
    for j in range(0, len(fullDEL[i])):
        baseAnswerFile.write(str(i+1)+","+str(fullDEL[i][j][0]) + "," + str(fullDEL[i][j][1]))
        baseAnswerFile.write("\n")    
        
#snps
baseAnswerFile.write(">SNP")
for i in range(0,chromosomes):
    for j in range(0, len(fullSNP[i])):
            baseAnswerFile.write("\n" + str(i+1)+","+(str)(fullSNP[i][j][0])+',')
            baseAnswerFile.write((str)(fullSNP[i][j][1])+',')
            baseAnswerFile.write((str)(fullSNP[i][j][2]))    
            
baseAnswerFile.close()
readsFile.close()
print "Program Complete"
