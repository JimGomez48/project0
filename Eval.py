'''
Created on Apr 22, 2014

@author: Jorge Munoz
'''

import sys

# ########################
#
# To run: python Eval.py studentAnswers.txt genomeX
#
# #####################

#Using F1-Score
def grade(studTot, corr, tot):
    p= float(corr)/max(studTot,tot)
    r= float(corr)/tot
    
    if(corr==0):
        return 0
    return 2*p*r/(p+r)

def findIndex(arr, temp):
    for i in range(0,len(arr)):
        if ( arr[i][0:len(temp)]==temp):
            return i      
        
#criteria to grade the copy portion
#stud contains the student answers
#key contains the answer key
# i is the index of the array for which the answers begin on
# These structs will determine the number of false positives and negatives and
# use the grade struct to determine an accurate ranking/grade


#
# TEST AGAIN FOR MULTIPLE COPIESSS
#

def COPYgrade ( stud, key, index):
    ans=findIndex(key,">COPY")
    correct=0
    total=0
    copynums=1
    i=index+1
    while (i < len(stud)-1 and stud[i][0]!='>'): 
        compynums+=1
        i+=1
    ans+=1
    ansTemp=key[ans].split(',')
    studTot=copynums*(len(ansTemp)-1)        
    while (ans < len(key)-1 and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        for j in range(index, index+studTot+1):
            studTemp=stud[j].split(',')
            if(ansTemp[0]==studTemp[0]):
                for i in range(1,len(ansTemp)):
                    for k in range(1, len(studTemp)):
                        if(int(ansTemp[i]) >int(studTemp[k])-5 and int(ansTemp[i]) <int(studTemp[k])+5):
                            correct+=1
                            break
    total=(len(ansTemp)-1)*copynums
    return grade(studTot, correct, total)    

#criteria to grade the inversion portion
def INVgrade ( stud, key, index):
    ans=findIndex(key,">INVERSION")
    correct=0
    total=0
    studTot=0
    i=index+1
    while (i < len(stud)-1 and stud[i][0]!='>'): 
        studTot+=1
        i+=1
    ans+=1
    while (ans < len(key)-1 and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        for j in range(index, index+studTot+1):
            studTemp=stud[j].split(',')
            
            if(ansTemp[0]==studTemp[0] and int(ansTemp[1]) >int(studTemp[1])-5 and int(ansTemp[1]) <int(studTemp[1])+5):
                correct+=1
                break
            
    return grade(studTot, correct, total)    

#criteria to grade the insertion portion
def INSgrade ( stud, key, index):
    ans=findIndex(key,">INSERT")
    correct=0
    total=0
    studTot=0
    i=index+1
    while (i < len(stud)-1 and stud[i][0]!='>'): 
        studTot+=1
        i+=1
    ans+=1
    while (ans < len(key)-1 and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        for j in range(index, index+studTot+1):
            studTemp=stud[j].split(',')
            
            if(ansTemp[0]==studTemp[0] and int(ansTemp[1]) >int(studTemp[1])-5 and int(ansTemp[1]) <int(studTemp[1])+5):
                correct+=1
                break
            
    return grade(studTot, correct, total)   

#criteria to grade the deletion portion
def DELgrade ( stud, key, index):
    ans=findIndex(key,">DELETE")
    correct=0
    total=0
    studTot=0
    i=index+1
    while (i < len(stud)-1 and stud[i][0]!='>'): 
        studTot+=1
        i+=1
    ans+=1
    while (ans < len(key)-1 and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        for j in range(index, index+studTot+1):
            studTemp=stud[j].split(',')
            
            if(ansTemp[0]==studTemp[0] and int(ansTemp[1]) >int(studTemp[1])-5 and int(ansTemp[1]) <int(studTemp[1])+5):
                correct+=1
                break
            
    return grade(studTot, correct, total)

#criteria to grade the SNP portion
def SNPgrade ( stud, key, index):
    ans=findIndex(key,">SNP")
    correct=0
    total=0
    studTot=0
    i=index+1
    while (i < len(stud)-1 and stud[i][0]!='>'): 
        studTot+=1
        i+=1
    ans+=1
    while (ans < len(key)-1 and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        for j in range(index, index+studTot+1):
            studTemp=stud[j].split(',')
            
            if(ansTemp[0]==studTemp[0] and ansTemp[1]==studTemp[1] and int(ansTemp[2]) >int(studTemp[2])-5 and int(ansTemp[2]) <int(studTemp[2])+5):
                correct+=1
                break
            
    return grade(studTot, correct, total)
    #calculate false positives

sys.argv[1:]

if(len(sys.argv)==1):
    print "The program requires 2 inputs in the following format: \n"
    print "python Eval.py studentAnswers.txt genomeX \n"
    
    sys.exit()

# Open up student answers
studentAns = open(sys.argv[1], "r")
studAns = studentAns.readlines()
studentAns.close()

answerKey = open("ans_"+sys.argv[2]+".txt", "r")
ansKey = answerKey.readlines()
answerKey.close()

for i in range(0,len(studAns)-1):
    if (studAns[i][0:5]==">COPY"):
        print "COPY grade: " + str(COPYgrade(studAns,ansKey,i+1))
    if (studAns[i][0:10]==">INVERSION"):
        print "INVERSIONS grade: "+ str(INVgrade(studAns,ansKey,i+1))       
    if (studAns[i][0:7]==">INSERT"):
        print "INSERTIONS grade: "+ str(INSgrade(studAns,ansKey,i+1)) 
    if (studAns[i][0:7]==">DELETE"):
        print "DELETIONS grade: "+ str(DELgrade(studAns,ansKey,i+1))         
    if (studAns[i][0:4]==">SNP"):
        print "SNP grade: "+ str(SNPgrade(studAns,ansKey,i))
        
