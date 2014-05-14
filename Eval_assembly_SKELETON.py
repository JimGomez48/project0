'''
Created on May 14, 2014

@author: Gabe
THIS IS A SKELETON. It's not fully fleshed out and checked yet.
'''

def grade(studTot, corr, tot):
    p= float(corr)/max(studTot,tot)
    r= float(corr)/tot

    if(corr==0):
        return 0
    return 2*p*r/(p+r)


def ASSEMBLYgrade(answerGenome, studentAns, index):
    
    studTot = 0 # Number of chunks taken from student's submission
    total = 0 # Number of total chunks from answer key 
    correct = 0
    
    k=index
    while (k < len(studentAns) and studentAns[k][0]!='>'):
        studTot+=1
        k+=1
    
    
    
    
    #studentAns.readline()
    
    #studentGenome = studentAns.readline()
    chunk_len = 100
    #studentAnsChunks = [studentGenome[i:i+chunk_len] for i in range(0, len(studentGenome), chunk_len)]   
    
    # Read the answer genome into a list
    # Skip the first line 
    # THIS IS ASSUMING THERE IS ONLY ONE HEADER LINE
    answerGenome.readLine()
    
    # Read lines of answer genome into 
    answerGenomeLines = answerGenome.readLines()
    
    # Concatenate genome into one string
    answerGenomeString = answerGenomeLines.replace('\n', '')
    answerGenomeString = answerGenomeString.replace('\r', '')
    total = len(answerGenomeString)/chunk_len # total number of chunks present in answer genome
    print len(answerGenomeString)
    
    inorder_vector = [] # Vector for starting indexes of mapped chunks to answer genome
    # Grade for mapping
    for i in range(0, len(studentAns)):
        index_of_mapping = answerGenomeString.find(studentAns[i])
        if (index_of_mapping != -1):
            # GIVE POINTS FOR EXISTING CHUNK HERE #
            inorder_vector.append(index_of_mapping) # Hold where chunk was mapped to in genome, and also which chunk it is; to be compared for in-orderness
        
    # TEST FOR ORDER    
    # NEEDS FIXING FOR LOGIC; (rushed while in class)
    # Make sure each chunk before subsequent chunks in the answer genome
    # This may need fixing to accommodate subset of correct inorder stuff??
    for i in range(0, len(inorder_vector)):
        for j in range(i+1, len(inorder_vector)): # NOTICE THE INNER LOOP STARTS AT i+1: chunks at i should come before chunks after i  
            if (inorder_vector[i] < inorder_vector[j]): # CHECK THAT A CHUNK COMES BEFORE ALL THE OTHER CHUNKS; ADD POINTS ACCORDINGLY
                print "k"
                
        

        
     
    # TEST FOR COVERAGE
        
        
    # RETURN GRADES DOWN HERE
            

def Eval(answerKey, studentAns):

    # Open up student answers
    #studentAns = open(sys.argv[1], "r")
    studAns = studentAns.readlines()
    studentAns.close()
    
    for i in range(0,len(studAns)-1):
        #if (studAns[i][0:3]==">ID"):
        if (studAns[i][0]==">"):
            filename = studAns[i+1]
            filename=filename.translate(None,'\n>')
    #answerKey = open("ans_"+filename+".txt", "r")
    ansKey = answerKey.readlines()
    answerKey.close()

    for i in range(0,len(studAns)-1):    
        if (studAns[i][0:9]==">ASSEMBLY"):
            assemblyGrade=ASSEMBLYgrade(studAns,ansKey,i+1)

    grades = {'ASSEMBLY': assemblyGrade}
    return grades



studentAns = open("C:\Users\Gabe!!\Documents\Gabes Papers\Homework Documents\UCLA\CS 229\Project 0\Project 0\InitialGenome\\private_genomeE1.txt", "r")
answerGenome = open("C:\Users\Gabe!!\Documents\Gabes Papers\Homework Documents\UCLA\CS 229\Project 0\Project 0\InitialGenome\\private_genomeE1.txt", "r")

grade = ASSEMBLYgrade(answerGenome, studentAns)
