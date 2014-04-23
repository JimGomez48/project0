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

#criteria to grade the copy portion
def COPYgrade ( stud, key, i):
    pass

#criteria to grade the inversion portion
#stud contains the student answers
#key contains the answer key
# i is the index of the array for which the answers begin on
def INVgrade ( stud, key, i):
    pass

#criteria to grade the insertion portion
def INSgrade ( stud, key, i):
    pass

#criteria to grade the deletion portion
def DELgrade ( stud, key, i):
    pass

#criteria to grade the SNP portion
def SNPgrade ( stud, key, i):
    pass

sys.argv[1:]

# Open up student answers
studentAns = open(sys.argv[1], "r")
studAns = studentAns.readlines()
studentAns.close()

answerKey = open("ref_"+sys.argv[2]+".txt", "r")
ansKey = answerKey.readlines()
answerKey.close()

for i in range(0,len(studAns)-1):
    if (studAns[i][0:5]==">COPY"):
        COPYgrade(studAns,ansKey,i+1)
    if (studAns[i][0:10]==">INVERSION"):
        INVgrade(studAns,ansKey,i+1)        
    if (studAns[i][0:7]==">INSERT"):
        INSgrade(studAns,ansKey,i+1) 
    if (studAns[i][0:7]==">DELETE"):
        DELgrade(studAns,ansKey,i+1)         
    if (studAns[i][0:4]==">SNP"):
        SNPgrade(studAns,ansKey,i+1)
        
