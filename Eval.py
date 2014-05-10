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
        total+=len(key[tmp].split(','))-2
        keynums+=1
        tmp+=1

    #Find student copy numbers
    while (m < len(stud)-1 and stud[m][0]!='>'):
        studTot+=len(stud[m].split(','))-2
        copynums+=1
        m+=1

    #for p in range(0,keynums-1):
    ansTemp=key[ans].split(',')
    ans2=ans
    while (ans2 < len(key) and key[ans2][0]!='>'):
        done=0
        ansTemp=key[ans2].split(',')
        ans2+=1

        for i in range(2,len(ansTemp)):
            studTemp=[0]*1000 #make a temp list
            for j in range(index, index+keynums):
                studTemp=stud[j].split(',')
                if(ansTemp[0]==studTemp[0] and ansTemp[1]==studTemp[1]):
                    for k in range(2, len(studTemp)):
                        if(int(ansTemp[i]) >= int(studTemp[k])-5 and int(ansTemp[i]) <= int(studTemp[k])+5):
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
    i=index
    while (i < len(stud) and stud[i][0]!='>'):
        studTot+=1
        i+=1
    ans+=1

    # Sort Inversions
    sortStud = []
    # Split each line into 3 parts
    for k in range(index, index+studTot):
        tempSort = stud[k].split(',')
        tempSort[2] = int(tempSort[2])
        sortStud.append(tempSort)

    # Sort by increasing index (the third part of each line)
    sortStud = sorted(sortStud,key= lambda sortStud:(sortStud[:][0],sortStud[:][2]))

    # After sorting, combine the parts together again into one string line
    for k in range(0, len(sortStud)):
        sortStud[k] = sortStud[k][0] + "," + sortStud[k][1] + "," + str(sortStud[k][2])

    # Copy the sorted section back into the student answer array
    stud[index:index+studTot] = sortStud
    tmpIndex=index-1
    while (ans < len(key) and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        index=tmpIndex+1


        if(index<len(stud)):
            studTemp = stud[index].split(',')

        while(studTemp[0][0]!='>' and int(studTemp[2])<=int(ansTemp[2]) and index<len(stud) and studTemp[0] == ansTemp[0]):
            if(int(ansTemp[0])==int(studTemp[0]) and ansTemp[1]==studTemp[1] and int(ansTemp[2]) >= int(studTemp[2])-5 and int(ansTemp[2]) <= int(studTemp[2])+5):
                correct+=1
                tmpIndex=index
                break
            tmpIndex=index
            index += 1
            if(index<len(stud)):
                studTemp = stud[index].split(',')

    return grade(studTot, correct, total)

#criteria to grade the insertion portion
def INSgrade ( stud, key, index):
    ans=findIndex(key,">INSERT")
    correct=0
    total=0
    studTot=0
    i=index
    while (i < len(stud) and stud[i][0]!='>'):
        studTot+=1
        i+=1
    ans+=1

    # Sort Insertions
    sortStud = []
    # Split each line into 3 parts
    for k in range(index, index+studTot):
        tempSort = stud[k].split(',')
        tempSort[2] = int(tempSort[2])
        sortStud.append(tempSort)

    # Sort by increasing index (the second part of each line)
    sortStud = sorted(sortStud,key= lambda sortStud:(sortStud[:][0],sortStud[:][2]))

    # After sorting, combine the parts together again into one string line
    for k in range(0, len(sortStud)):
        sortStud[k] = sortStud[k][0] + "," + sortStud[k][1] + "," + str(sortStud[k][2])

    # Copy the sorted section back into the student answer array
    stud[index:index+studTot] = sortStud

    tmpIndex=index-1
    while (ans < len(key) and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        index=tmpIndex+1
        if(index<len(stud)):
            studTemp = stud[index].split(',')
        while(studTemp[0][0]!='>' and int(studTemp[2])<=int(ansTemp[2]) and index<len(stud) and studTemp[0] == ansTemp[0]):
            if(int(ansTemp[0])==int(studTemp[0]) and ansTemp[1]==studTemp[1] and int(ansTemp[2]) >= int(studTemp[2])-5 and int(ansTemp[2]) <= int(studTemp[2])+5):
                correct+=1
                tmpIndex=index
                break
            tmpIndex=index
            index += 1
            if(index<len(stud)):
                studTemp = stud[index].split(',')

    return grade(studTot, correct, total)

#criteria to grade the deletion portion
def DELgrade ( stud, key, index):
    ans=findIndex(key,">DELETE")
    correct=0
    total=0
    studTot=0
    i=index
    while (i < len(stud) and stud[i][0]!='>'):
        studTot+=1
        i+=1
    ans+=1

    # Sort Insertions
    sortStud = []
    # Split each line into 3 parts
    for k in range(index, index+studTot):
        tempSort = stud[k].split(',')
        tempSort[2] = int(tempSort[2])
        sortStud.append(tempSort)

    # Sort by increasing index (the second part of each line)
    sortStud = sorted(sortStud,key= lambda sortStud:(sortStud[:][0],sortStud[:][2]))

    # After sorting, combine the parts together again into one string line
    for k in range(0, len(sortStud)):
        sortStud[k] = sortStud[k][0] + "," + sortStud[k][1] + "," + str(sortStud[k][2])

    # Copy the sorted section back into the student answer array
    stud[index:index+studTot] = sortStud

    tmpIndex=index-1
    while (ans < len(key) and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        index=tmpIndex+1

        if(index<len(stud)):
            studTemp = stud[index].split(',')
        while(studTemp[0][0]!='>' and int(studTemp[2])<=int(ansTemp[2]) and index<len(stud) and studTemp[0] == ansTemp[0]):
            if(int(ansTemp[0])==int(studTemp[0]) and ansTemp[1]==studTemp[1] and int(ansTemp[2]) >= int(studTemp[2])-5 and int(ansTemp[2]) <= int(studTemp[2])+5):
                correct+=1
                tmpIndex=index
                break
            tmpIndex=index
            index += 1
            if(index<len(stud)):
                studTemp = stud[index].split(',')

    return grade(studTot, correct, total)

#criteria to grade the SNP portion
def SNPgrade ( stud, key, index):
    ans=findIndex(key,">SNP")
    correct=0
    total=0
    studTot=0
    i=index
    while (i < len(stud) and stud[i][0]!='>'):
        studTot+=1
        i+=1
    ans+=1
    # Sort SNPs
    sortStud = []
    # Split each line into 3 parts
    for k in range(index, index+studTot):
        tempSort = stud[k].split(',')
        tempSort[3] = int(tempSort[3])
        sortStud.append(tempSort)

    # Sort by increasing index (the second part of each line)
    sortStud = sorted(sortStud,key= lambda sortStud:(sortStud[:][0],sortStud[:][3]))

    # After sorting, combine the parts together again into one string line
    for k in range(0, len(sortStud)):
        sortStud[k] = sortStud[k][0] + "," + sortStud[k][1] + "," + sortStud[k][2] + "," + str(sortStud[k][3])

    # Copy the sorted section back into the student answer array
    stud[index:index+studTot] = sortStud

    tmpIndex=index-1
    while (ans < len(key) and key[ans][0]!='>'):
        total+=1
        ansTemp=key[ans].split(',')
        ans+=1
        index=tmpIndex+1
        if(index<len(stud)):
            studTemp = stud[index].split(',')
        while(studTemp[0][0]!='>' and int(studTemp[3])<=int(ansTemp[3]) and index<len(stud) and studTemp[0] == ansTemp[0]):
            studTemp = stud[index].split(',')
            if(int(ansTemp[0])==int(studTemp[0]) and ansTemp[1]==studTemp[1] and ansTemp[2]==studTemp[2] and int(ansTemp[3]) >= int(studTemp[3])-5 and int(ansTemp[3]) <= int(studTemp[3])+5):
                correct+=1
                tmpIndex=index
                break
            tmpIndex=index
            index += 1
            if(index<len(stud)):
                studTemp = stud[index].split(',')
    return grade(studTot, correct, total)
    #calculate false positives

def needleman_wunsch(n, m):
    rows = len(n) + 1
    cols = len(m) + 1
    matrix = []
    for row in range(rows):
        matrix.append(list())
        for col in range(cols):
            matrix[row].append(0)
    for row in range(rows):
        for col in range(cols):
            top = matrix[row-1][col]
            topleft = matrix[row-1][col-1]
            left = matrix[row][col-1]
            if n[row-1] == m[col-1]:
                charscore = 1
            else:
                charscore = -1
            max_val = max(top-1, topleft+charscore, left-1)
            matrix[row][col] = max_val
    return matrix[rows-1][cols-1]

def STRgrade(stud, key, stud_index):
    print 'in STRgrade'
    keyIndex = findIndex(key,">STR:")
    keyIndex += 1 # index of first answer
    # find end of answers in key
    i = keyIndex
    while (i < len(key) and key[i][0] != '>'):
        i += 1
    key_answers = []
    for ans in key[keyIndex:i]:
        split_ans = ans.split(',')
        key_answers.append(split_ans)
    i = stud_index
    # find end of student answers
    while (i < len(stud) and stud[i][0]!='>'):
        i += 1
    student_answers = []
    for ans in stud[stud_index:i]:
        student_answers.append(ans.split(','))
    score = 0
    for key_ans in key_answers:
        for student_ans in student_answers:
            print str(student_ans)
            if int(student_ans[3]) >= int(key_ans[3])-20 and \
               int(student_ans[3]) <= int(key_ans[3])+20:
                score += 0.5
                ans_sequence = ""
                student_sequence = ""
                for rpt in range(0,int(key_ans[2])):
                    ans_sequence += key_ans[1]
                for rpt in range(0,int(student_ans[2])):
                    student_sequence += key_ans[1]
                max_align_score = len(ans_sequence)
                align_score = needleman_wunsch(ans_sequence, student_sequence)
                if align_score < 0:
                  align_score = 0
                score += (float(align_score)/(2*max_align_score))
                break;
    return grade(len(student_answers), score, len(key_answers))

def Eval(answerKey, studentAns):

    # Open up student answers
    #studentAns = open(sys.argv[1], "r")
    studAns = studentAns.readlines()
    studentAns.close()
    copyGrade=0
    invGrade=0
    insertGrade=0
    deleteGrade=0
    snpGrade=0
    strGrade=0

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
            print "COPY grade: " + str(copyGrade)
        if (studAns[i][0:10]==">INVERSION"):
            invGrade=INVgrade(studAns,ansKey,i+1)
            print "INVERSIONS grade: "+ str(invGrade)
        if (studAns[i][0:7]==">INSERT"):
            insertGrade =INSgrade(studAns,ansKey,i+1)
            print "INSERTIONS grade: "+ str(insertGrade)
        if (studAns[i][0:7]==">DELETE"):
            deleteGrade=DELgrade(studAns,ansKey,i+1)
            print "DELETIONS grade: "+ str(deleteGrade)
        if (studAns[i][0:4]==">SNP"):
            snpGrade=SNPgrade(studAns,ansKey,i+1)
            print "SNP grade: "+ str(snpGrade)
        if (studAns[i][0:4]==">STR"):
            strGrade=STRgrade(studAns,ansKey,i+1)
            print "STR grade: "+ str(strGrade)

    grades = {'SNP': snpGrade,'INDEL':(insertGrade+deleteGrade)/2,'COPY': copyGrade, 'INV': invGrade, 'STR': strGrade}
    return grades

def main():
    studentAns = open("C:\Users\Kevin\Downloads\\ans_STRtest4.txt", "r")
    answerKey = open("C:\Users\Kevin\Downloads\\ans_STRtest4.txt", "r")
    test= Eval(answerKey,studentAns)

if __name__ == '__main__':
    main()
