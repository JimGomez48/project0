'''
Created on Apr 22, 2014

@author: Jorge Munoz
'''

import sys

# ########################
#
# To run: python Eval.py studentAnswers.txt
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
    ans=findIndex(key,">COPY")+1
    tmp=ans
    correct=0
    total=0
    copynums=0
    m=index
    keynums=0
    studTot=0
    #Count key copy numbers
    while (key[tmp][0]!='>'): 
        total+=len(key[tmp].split(','))-1
        keynums+=1
        tmp+=1
        
    #Find student copy numbers
    while (m < len(stud)-1 and stud[m][0]!='>'): 
        studTot+=len(stud[m].split(','))-1
        copynums+=1
        m+=1
    
    #for p in range(0,keynums-1):
    ansTemp=key[ans].split(',')
    ans2=ans
    while (ans2 < len(key)-1 and key[ans2][0]!='>'):
        done=0
        ansTemp=key[ans2].split(',')
        ans2+=1
        
        for i in range(1,len(ansTemp)):  
            studTemp=[0]*1000 #make a temp list
            for j in range(index, index+len(studTemp)+1):
                studTemp=stud[j].split(',')
                if(ansTemp[0]==studTemp[0]):
                    for k in range(1, len(studTemp)):
                        if(int(ansTemp[i]) >int(studTemp[k])-5 and int(ansTemp[i]) <int(studTemp[k])+5):
                            correct+=1
                            done=1
                            break
                    if(done==1):break
    
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

def Eval( answerKey, studentAns):
    # Open up student answers
    #studentAns = open(sys.argv[1], "r")
    studAns = studentAns.readlines()
    studentAns.close()
    copyGrade=0
    invGrade=0
    insertGrade=0
    deleteGrade=0
    snpGrade=0
    
    for i in range(0,len(studAns)-1):
        #if (studAns[i][0:3]==">ID"):
        if (studAns[i][0]==">"):
            filename = studAns[i+1]
            filename=filename.translate(None,'\n>')
    #answerKey = open("ans_"+filename+".txt", "r")
    ansKey = answerKey.readlines()
    answerKey.close()
    
    for i in range(0,len(studAns)-1):
        if (studAns[i][0:5]==">COPY"):
            copyGrade=COPYgrade(studAns,ansKey,i+1)
            #print "COPY grade: " + str(copyGrade)
        if (studAns[i][0:10]==">INVERSION"):
            invGrade=INVgrade(studAns,ansKey,i+1)
            #print "INVERSIONS grade: "+ str(invGrade)       
        if (studAns[i][0:7]==">INSERT"):
            insertGrade =INSgrade(studAns,ansKey,i+1)
            #print "INSERTIONS grade: "+ str(insertGrade) 
        if (studAns[i][0:7]==">DELETE"):
            deleteGrade=DELgrade(studAns,ansKey,i+1)
            #print "DELETIONS grade: "+ str(deleteGrade)         
        if (studAns[i][0:4]==">SNP"):
            snpGrade=SNPgrade(studAns,ansKey,i)
            #print "SNP grade: "+ str(snpGrade)
            
    grades = {'SNP': snpGrade,'INDEL':(insertGrade+deleteGrade)/2,'COPY': copyGrade, 'INV': invGrade}
    return grades
