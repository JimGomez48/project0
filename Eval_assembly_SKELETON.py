'''
Created on May 14, 2014

@author: Gabe
THIS IS A SKELETON. It's not fully fleshed out and checked yet.
'''

def gradeAssembly(answerGenome, studentAns):
    studentAns.readline()
    
    studentGenome = studentAns.readline()
    chunk_len = 100
    studentAnsChunks = [studentGenome[i:i+chunk_len] for i in range(0, len(studentGenome), chunk_len)]
    
    # Read the answer genome into a list
    # Skip the first 2 lines
    answerGenome.readLine()
    answerGenome.readLine()
    
    answerGenomeLines = answerGenome.readLines()
    studTot = len(answerGenomeLines)
    
    answerGenomeString = answerGenomeLines.replace('\n', '')
    answerGenomeString = answerGenomeString.replace('\r', '')
    print len(answerGenomeString)
    
    inorder_vector = [] # Vector for starting indexes of mapped chunks to answer genome
    # Grade for mapping
    for i in range(0, len(studentAnsChunks)):
        index_of_mapping = answerGenomeString.find(studentAnsChunks[i])
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
                
                
        
        
        
     
    # TEST FOR COVERAGE
        
        
    # RETURN GRADES DOWN HERE
            
    


studentAns = open("C:\Users\Gabe!!\Documents\Gabes Papers\Homework Documents\UCLA\CS 229\Project 0\Project 0\InitialGenome\\private_genomeE1.txt", "r")
answerGenome = open("C:\Users\Gabe!!\Documents\Gabes Papers\Homework Documents\UCLA\CS 229\Project 0\Project 0\InitialGenome\\private_genomeE1.txt", "r")

grade = gradeAssembly(answerGenome, studentAns)
