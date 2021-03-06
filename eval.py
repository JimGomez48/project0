'''
Created on Apr 22, 2014

@author: Jorge Munoz
'''

import sys
import argparse

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

def needleman_wunsch(n, m):
    rows = len(n) + 1
    cols = len(m) + 1
    matrix = []
    for row in range(rows):
        matrix.append(list())
        for col in range(cols):
            matrix[row].append(0)
    #initialize first column
    for row in range(rows):
      matrix[row][0] = -row
    #initalize first row
    for col in range(cols):
      matrix[0][col] = -col
    for row in range(1, rows):
        for col in range(1, cols):
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

#criteria to grade the copy portion
#stud contains the student answers
#key contains the answer key
# i is the index of the array for which the answers begin on
# These structs will determine the number of false positives and negatives and
# use the grade struct to determine an accurate ranking/grade


#
# TEST AGAIN FOR MULTIPLE COPIES
#

#SNP score function
def SNPgrade(stud, key, stud_index):
    keyIndex = findIndex(key,">SNP")
    keyIndex += 1 # index of first answer
    # find end of answers in key
    i = keyIndex
    while (i < len(key) and key[i][0] != '>'):
        i += 1
    key_answers = []
    for ans in key[keyIndex:i]:
        split_ans = ans.split(',')
        key_answers.append(split_ans)
    answer_key_length = len(key_answers)
    i = stud_index
    # find end of student answers
    while (i < len(stud) and stud[i][0]!='>'):
        i += 1
    new_i = i

    #if the student answer file has 400% the number of SNPs as really exists, just assign 0 and don't waste time scoring
    if (new_i - stud_index) > 4 * answer_key_length:
        return new_i, 0
    stud[stud_index:new_i] = sorted(stud[stud_index:new_i], key=lambda l: (int(l.split(',')[0]),int(l.split(',')[3])))

    score = 0
    max_posn_diff = 5
    for student_ans in stud[stud_index:new_i]:
        student_ans = student_ans.split(',')
        remove_list = []

        #loop through remaining answer key entries to find the best match, if any
        for key_ans in key_answers:
            #if this key has already been passed, then mark it for removal
            if int(student_ans[3]) > int(key_ans[3])+max_posn_diff:
                remove_list.append(key_ans)

            elif int(student_ans[3]) >= int(key_ans[3])-max_posn_diff and \
               int(student_ans[3]) <= int(key_ans[3])+max_posn_diff and \
                    student_ans[2] == key_ans[2]:
                score += 1
                remove_list.append(key_ans)
                break

            #once answers keys that are out of range are reached, then break the for loop
            elif int(student_ans[3]) < int(key_ans[3])-max_posn_diff:
                break

        #get rid of the unneeded answer key entries
        for old_key in remove_list:
            key_answers.remove(old_key)

    return new_i, grade(len(stud[stud_index:new_i]), score, answer_key_length)

def STRgrade(stud, key, stud_index):
    keyIndex = findIndex(key,">STR")
    keyIndex += 1 # index of first answer
    # find end of answers in key
    i = keyIndex
    while (i < len(key) and key[i][0] != '>'):
        i += 1
    key_answers = []
    for ans in key[keyIndex:i]:
        split_ans = ans.split(',')
        key_answers.append(split_ans)
    answer_key_length = len(key_answers)
    i = stud_index
    # find end of student answers
    while (i < len(stud) and stud[i][0]!='>'):
        i += 1
    new_i = i

    stud[stud_index:new_i] = sorted(stud[stud_index:new_i], key=lambda l: (int(l.split(',')[0]),int(l.split(',')[3])))

    score = 0
    max_posn_diff = 20
    for student_ans in stud[stud_index:new_i]:
        student_ans = student_ans.split(',')
        remove_list = []

        #loop through remaining answer key entries to find the best match, if any
        for key_ans in key_answers:
            #if this key has already been passed, then mark it for removal
            if int(student_ans[3]) > int(key_ans[3])+max_posn_diff:
                remove_list.append(key_ans)

            elif int(student_ans[3]) >= int(key_ans[3])-max_posn_diff and \
               int(student_ans[3]) <= int(key_ans[3])+max_posn_diff:
                score += 0.5
                ans_sequence = ""
                student_sequence = ""
                for rpt in range(0,int(key_ans[2])):
                    ans_sequence += key_ans[1]
                for rpt in range(0,int(student_ans[2])):
                    student_sequence += key_ans[1]
                max_align_score = max(len(ans_sequence), len(student_sequence)) #either sequence can be longer
                align_score = needleman_wunsch(ans_sequence, student_sequence)
                if align_score < 0:
                  align_score = 0
                adj_score = (float(align_score)/(max_align_score)) #normalize to 0 to 1
                adj_score = (adj_score**4) #since repeats only vary -2 to 2, its fairly easy to get close, so increasing penalty for error
                score += adj_score / 2
                remove_list.append(key_ans)
                break

            #once answers keys that are out of range are reached, then break the for loop
            elif int(student_ans[3]) < int(key_ans[3])-max_posn_diff:
                break

        #get rid of the unneeded answer key entries
        for old_key in remove_list:
            key_answers.remove(old_key)

    return new_i, grade(len(stud[stud_index:new_i]), score, answer_key_length)

#criteria to grade the inversion portion
def INVgrade ( stud, key, stud_index):
    keyIndex=findIndex(key,">INVERSION")
    keyIndex += 1 # index of first answer
    # find end of answers in key
    i = keyIndex
    while (i < len(key) and key[i][0] != '>'):
        i += 1
    key_answers = []
    for ans in key[keyIndex:i]:
        split_ans = ans.split(',')
        key_answers.append(split_ans)
    answer_key_length = len(key_answers)
    i = stud_index
    # find end of student answers
    while (i < len(stud) and stud[i][0]!='>'):
        i += 1
    new_i = i

    stud[stud_index:new_i] = sorted(stud[stud_index:new_i], key=lambda l: (int(l.split(',')[0]),int(l.split(',')[2])))

    score = 0
    max_posn_diff = 5
    for student_ans in stud[stud_index:new_i]:
        student_ans = student_ans.split(',')
        remove_list = []

        #loop through remaining answer key entries to find the best match, if any
        for key_ans in key_answers:
            #if this key has already been passed, then mark it for removal
            if int(student_ans[2]) > int(key_ans[2])+max_posn_diff:
                remove_list.append(key_ans)

            elif int(student_ans[2]) >= int(key_ans[2])-max_posn_diff and \
               int(student_ans[2]) <= int(key_ans[2])+max_posn_diff:
                score += 0.5
                ans_sequence = key_ans[1]
                student_sequence = student_ans[1]
                max_align_score = max(len(ans_sequence), len(student_sequence)) #either sequence can be longer
                align_score = needleman_wunsch(ans_sequence, student_sequence)
                if align_score < 0:
                  align_score = 0
                adj_score = (float(align_score)/(max_align_score)) #normalize to 0 to 1
                score += adj_score / 2
                remove_list.append(key_ans)
                break

            #once answers keys that are out of range are reached, then break the for loop
            elif int(student_ans[2]) < int(key_ans[2])-max_posn_diff:
                break

        #get rid of the unneeded answer key entries
        for old_key in remove_list:
            key_answers.remove(old_key)

    return new_i, grade(len(stud[stud_index:new_i]), score, answer_key_length)

#criteria to grade the insert portion
def INDELgrade ( stud, key, stud_index, insert_or_delete):
    keyIndex=findIndex(key,insert_or_delete)
    keyIndex += 1 # index of first answer
    # find end of answers in key
    i = keyIndex
    while (i < len(key) and key[i][0] != '>'):
        i += 1
    key_answers = []
    for ans in key[keyIndex:i]:
        split_ans = ans.split(',')
        key_answers.append(split_ans)
    answer_key_length = len(key_answers)
    i = stud_index
    # find end of student answers
    while (i < len(stud) and stud[i][0]!='>'):
        i += 1
    new_i = i

    stud[stud_index:new_i] = sorted(stud[stud_index:new_i], key=lambda l: (int(l.split(',')[0]),int(l.split(',')[2])))

    score = 0
    max_posn_diff = 5
    for student_ans in stud[stud_index:new_i]:
        student_ans = student_ans.split(',')
        remove_list = []

        #loop through remaining answer key entries to find the best match, if any
        for key_ans in key_answers:
            #if this key has already been passed, then mark it for removal
            if int(student_ans[2]) > int(key_ans[2])+max_posn_diff:
                remove_list.append(key_ans)

            elif int(student_ans[2]) >= int(key_ans[2])-max_posn_diff and \
               int(student_ans[2]) <= int(key_ans[2])+max_posn_diff:
                score += 0.5
                ans_sequence = key_ans[1]
                student_sequence = student_ans[1]
                max_align_score = max(len(ans_sequence), len(student_sequence)) #either sequence can be longer
                align_score = needleman_wunsch(ans_sequence, student_sequence)
                if align_score < 0:
                  align_score = 0
                adj_score = (float(align_score)/(max_align_score)) #normalize to 0 to 1
                score += adj_score / 2
                remove_list.append(key_ans)
                break

            #once answers keys that are out of range are reached, then break the for loop
            elif int(student_ans[2]) < int(key_ans[2])-max_posn_diff:
                break

        #get rid of the unneeded answer key entries
        for old_key in remove_list:
            key_answers.remove(old_key)

    return new_i, grade(len(stud[stud_index:new_i]), score, answer_key_length)

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
    new_i = m

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
                if ansTemp[0]==studTemp[0]:
                    for k in range(2, len(studTemp)):
                        if(int(ansTemp[i]) >= int(studTemp[k])-5 and int(ansTemp[i]) <= int(studTemp[k])+5):
                            correct += 0.5
                            ans_sequence = ansTemp[1]
                            student_sequence = studTemp[1]
                            max_align_score = max(len(ans_sequence), len(student_sequence)) #either sequence can be longer
                            align_score = needleman_wunsch(ans_sequence, student_sequence)
                            if align_score < 0:
                                align_score = 0
                            adj_score = (float(align_score)/(max_align_score)) #normalize to 0 to 1
                            correct += adj_score / 2
                            done=1
                            break
                if(done==1):
                    break

    return new_i, grade(studTot, correct, total)

def longest_increasing_subsequence(sequence):
    seq_len = len(sequence)
    M = []
    predecessor = []
    for i in xrange(seq_len):
        M.append(0)
        predecessor.append(0)
    M.append(0)
    M[0] = 0 # not really used
    longest_subseq_len = 0
    for i in xrange(0, seq_len):
        lo = 1
        hi = longest_subseq_len
        while lo <= hi:
          mid = (lo+hi)/2
          if sequence[M[mid]] < sequence[i]:
              lo = mid+1
          else:
            hi = mid-1
        newL = lo
        predecessor[i] = M[newL-1]
        if newL > longest_subseq_len:
            M[newL] = i
            longest_subseq_len = newL
        elif sequence[i] < sequence[M[newL]]:
            M[newL] = i
    subseq = []
    for i in xrange(longest_subseq_len):
      subseq.append(0)
    k = M[longest_subseq_len]
    for i in xrange(longest_subseq_len):
        subseq[longest_subseq_len-i-1] = sequence[k]
        k = predecessor[k]
    return subseq

def findCoverage( fullRange, length):
    newRange=list()
    count =1
    newRange.append(fullRange[0])
    overlap=0
    for i in range(1,len(fullRange)):
        if(newRange[count-1][1]>=fullRange[i][0] and newRange[count-1][1]<=fullRange[i][1]):
            #count+=1
            overlap+=newRange[count-1][1]-fullRange[i][0]
            newRange[count-1]=[newRange[count-1][0],fullRange[i][1]]

        else:
            newRange.append(fullRange[i])
            count+=1

    sums=0
    for i in range(len(newRange)):
        sums+=newRange[i][1]-newRange[i][0]+1
    return float(sums)/length, overlap



def ASSEMBLYgrade(stud, key, index):
    keyIndex=findIndex(key,">chr")+1
    i=keyIndex
    key_answers=[]
    while (i < len(key) and key[i][0] != '>'):
            i += 1

    key_answers=''

    for ans in key[keyIndex:i]:
        split_ans = ans.split(',')
        key_answers+=str(ans)

    answer_key_length = len(key_answers)
    i = index
    # find end of student answers
    while (i < len(stud) and stud[i][0]!='>'):
        i += 1
    new_i = i
    #student_answers = []
    #print stud
    #for ans in stud[index:i]:
    #    student_answers.append(ans.split(',')) # takes in every chunk

    studTot = 0 # Number of chunks taken from student's submission
    total = 0 # Number of total chunks from answer key
    correct = 0

    k=index
    while (k < len(stud)):
        studTot+=1
        k+=1

    # Sort by increasing index (the second part of each line)
    #student_answers.sort(key= lambda student_answers:(len(student_answers[0]),len(student_answers[0])), reverse=True)
    stud.sort(key= lambda stud:(len(stud),len(stud)), reverse=True)

    score = 0

    #GRADE:
    key_size=50

    index = {}

    for i in range(len(key_answers)):#50 is the 50-mer map
        if i + key_size <=  len(key_answers):
            key = key_answers[i:i+key_size]

            if index.has_key(key):
                index[key].append(i)
            else:
                index[key] = list()
                index[key].append(i)

    startPos=[]
    for i in range(studTot):
        templist=[]
        for j in range(len(stud[i])-key_size):
            key = stud[i][j:j+key_size]
            #print key
            if(index.has_key(key)):
                templist.append(min(index.get(key)))
            #else:
            #    print "Index not found"
        startPos.append(templist)

    fullRange=list()

    for i in range(len(startPos)):
        seq = longest_increasing_subsequence(startPos[i])
        #print seq
        count=0
        if len(seq)!=0:
            fullRange.append([seq[0],seq[-1]+50])

    listed=fullRange
    listed.sort(key= lambda listed:(int(listed[0])))

    covScore, overlap= findCoverage(listed, len(key_answers))

    return new_i, min(1, covScore) - 0.5*max(min(1,float(overlap)/len(key_answers)),0)
    '''

    fullRange.sort(key= lambda fullRange:(int(fullRange[1])-int(fullRange[0])), reverse=True)

    sums=0
    N50=0
    avgN50=0

    for i in range(len(fullRange)):
        N50=fullRange[i][1]-fullRange[i][0]+1
        sums+=N50
        avgN50=sums/i
        if(sums>=len(key_answers)/2):
            break

    score= min(avgN50/(len(key_answers)/4.0),1)*0.5'''

def Eval(answerKey, studentAns):

    studAns = [line.rstrip() for line in studentAns]
    studentAns.close()
    copyGrade=0
    invGrade=0
    insertGrade=0
    deleteGrade=0
    snpGrade=0
    strGrade=0
    aluGrade=0
    assGrade=0

    for i in range(0,len(studAns)-1):
        if (studAns[i][0]==">"):
            filename = studAns[i+1]
            filename=filename.translate(None,'\n>')
            break
    ansKey = [line.rstrip() for line in answerKey]
    answerKey.close()

    for i in range(0,len(studAns)-1):
        new_i = -1
        if (studAns[i][0:5]==">COPY"):
            new_i, copyGrade=COPYgrade(studAns,ansKey,i+1)
        if (studAns[i][0:10]==">INVERSION"):
            new_i, invGrade=INVgrade(studAns,ansKey,i+1)
        if (studAns[i][0:7]==">INSERT"):
            new_i, insertGrade =INDELgrade(studAns,ansKey,i+1, ">INSERT")
        if (studAns[i][0:7]==">DELETE"):
            new_i, deleteGrade=INDELgrade(studAns,ansKey,i+1, ">DELETE")
        if (studAns[i][0:4]==">SNP"):
            new_i, snpGrade=SNPgrade(studAns,ansKey,i+1)
        if (studAns[i][0:4]==">STR"):
            new_i, strGrade=STRgrade(studAns,ansKey,i+1)
        if (studAns[i][0:4]==">ALU"):
            new_i, aluGrade=INDELgrade(studAns,ansKey,i+1, ">ALU")
        if (studAns[i][0:9]==">ASSEMBLY"):
            new_i, assGrade=ASSEMBLYgrade(studAns,ansKey, i+1)

        #allows loop to skip over the portions that were already evaluated
        if new_i != -1:
            i = new_i - 1

    grades = {'SNP': snpGrade,'INDEL':(insertGrade+deleteGrade)/2,'COPY': copyGrade, 'INV': invGrade,
              'STR': strGrade, 'ALU': aluGrade, 'ASS':assGrade}
    return grades


def main():
    parser = argparse.ArgumentParser(
        description="This script evaluates an answer submission of donor-genome"
                    " mutations with respect to a reference-genome. It compares"
                    " the submission file against a true answer key and "
                    " generates scores for different mutation types."
    )
    parser.add_argument(
        "answer_key",
        type=str,
        help="The true answer key containing the mutations and their locations "
             "in the donor-genome with respect to its reference-genome"
    )
    parser.add_argument(
        "submission_file",
        type=str,
        help="The submitted file containing a set of mutations and locations. "
             "Tested against the true answer key"
    )
    args = parser.parse_args()
    answer_key = args.answer_key
    stud_ans = args.submission_file

    print "Evaluating..."
    test = Eval(answerKey=open(answer_key), studentAns=open(stud_ans))
    for key in test:
        print key + ' grade: ' + str(test[key])


if __name__ == '__main__':
    main()
