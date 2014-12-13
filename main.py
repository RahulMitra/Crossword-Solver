import CrosswordUtil
import CSPUtil
import SolverUtil
import numpy as np
import sys
from multiprocessing import Process, Manager
import string
import SemanticAnalysis

# -------------------------------------------------------------------------------------------------------------
# Clue Analysis Code
# -------------------------------------------------------------------------------------------------------------
def trainFeatureVector(csp, clues_training_data):
    print "Reading clue data and training feature vector..."
    cluesData = SolverUtil.parseCluesFile(clues_training_data)
    csp.wordsToClues, csp.cluesToWords, csp.wordFreqs, csp.answerMap = SolverUtil.analyzeCluesInput(cluesData)
    return csp.answerMap    

# will decrease the domain size based on the fill object's clue
def decreaseDomain(fill, currDomain, wordsToClues, cluesToWords, wordFreqs, answerMap, sa):
    clue = fill.clue.translate(string.maketrans("",""), string.punctuation)
    newDomain = []


    ''' this places most probable words at the beginning of the possible domain values, given a certain clue '''

    newDomain = sa.mostProbableWords(fill.fill_length, fill.clue, fill.clue_type) # this puts most probable words at beginning 
    newDomain.extend(currDomain)    



    ''' this will call order values based on words that have appeared before '''
    # tupleDomains = [(currDomain[i], i) for i in range(len(currDomain))]
    # sortedDomains = SolverUtil.orderValues(fill.clue, tupleDomains, cluesToWords, wordFreqs, answerMap)
    # sortedWordDomains = [currDomain[i] for i in range(len(sortedDomains))]
    # newDomain.extend(sortedWordDomains)

    if len(newDomain) > 500:
        return newDomain[:500]
    else:
        return newDomain


# -------------------------------------------------------------------------------------------------------------
# CSP Generation Code
# -------------------------------------------------------------------------------------------------------------
def createCSPVariables(csp, cw, domain, sa):
    # Create CSP variable for each fill in the crossword puzzle
    print "Adding CSP Variables..."
    for fill in cw.fills:

        fillDomain = decreaseDomain(fill, domain[fill.fill_length], csp.wordsToClues, csp.cluesToWords, csp.wordFreqs, csp.answerMap, sa)

        csp.add_variable((fill.clue_index, fill.clue_type, fill.clue), fillDomain)
        info_str = "Added CSP Variable: (" + str(fill.clue_index) + " " + str(fill.clue_type) \
            + ") with domain length " + str(fill.fill_length)
        print info_str
  
def generate_binary_potential_table(csp, across_fill_var, down_fill_var, across_intersecting_index, \
                                down_intersecting_index, potentials_tables):

    def potential(across_str, down_str):
        # print across_str, across_intersecting_index, "and", down_str, down_intersecting_index
        return across_str[int(across_intersecting_index)] == down_str[int(down_intersecting_index)]

    csp.add_binary_potential(across_fill_var, down_fill_var, potential, potentials_tables)
    print "Added CSP Binary Potential between", across_fill_var, "and", down_fill_var, 
    info_str = "Added CSP Binary Potential:\n\t" \
                + str(across_fill_var) + " char " + str(across_intersecting_index) \
                + " intersects " + str(down_fill_var) + " char " + str(down_intersecting_index)
    print info_str

def executeJobsMultithreaded(csp, jobs, potentials_tables, num_concurrent_jobs):
    num_jobs = len(jobs)
    job_size = num_concurrent_jobs
    num_batches = num_jobs / job_size
    
    job_indexes = []
    for i in range(num_batches):
        indexes = [i*job_size + x for x in range(job_size)]
        job_indexes.append(indexes)

        # If we are on the last batch, check % to see if there are any left
        if i == num_batches - 1:
            remaining_jobs = num_jobs % job_size
            if remaining_jobs > 0:
                indexes = [(i+1)*job_size + x for x in range(remaining_jobs)]
                job_indexes.append(indexes)

    # execute each job batch
    for job_list in job_indexes:

        print "Computing binary potentials ", job_list, "in parallel out of", (num_jobs-1), "total"
        # start all the jobs
        for index in job_list:
            jobs[index].start()

        # Wait for all jobs to be done,
        # we want to wait for all binary potential tables to be computed.
        for index in job_list:
            jobs[index].join()

    # Now set all the binary potential tables (do this synchronously, NOT multithreaded...)
    print "Done generating binary potential tables. Adding CSP Binary Potentials..."
    for bp in potentials_tables:
        csp.update_binary_potential_table(bp[0], bp[1], bp[2])


def createCSPBinaryPotentials(csp, cw, num_concurrent_jobs):
    # Loop through all the across fills and add binary potentials for each of their
    # intersections. Note that every character in an across fill intersects
    # with a character in a down fill.
    potentials_tables = Manager().list()

    jobs = []

    ''' approach: 
        note the across intersections and down intersections and 
    '''

    for across_fill in [fill for fill in cw.fills if fill.clue_type == "across"]:
        for key in across_fill.intersections:

            down_fill, down_intersecting_index, down_clue = across_fill.intersections[key][0], \
                across_fill.intersections[key][1], across_fill.intersections[key][0].clue
            across_intersecting_index = key

            across_fill_var = (across_fill.clue_index, across_fill.clue_type, across_fill.clue)
            down_fill_var = (down_fill.clue_index, down_fill.clue_type, down_clue)
            
            # Make a new process to generate each binary potential table
            p = Process(target=generate_binary_potential_table, \
                        args=(csp, across_fill_var, down_fill_var, across_intersecting_index, \
                            down_intersecting_index, potentials_tables))
            jobs.append(p)

    # execute jobs in parallel (multi-processing makes process for each one)
    executeJobsMultithreaded(csp, jobs, potentials_tables, num_concurrent_jobs)    

def chooseBest(allAssignments, answerMap):
    optimalSolution = None
    bestScore = 0
    for solution in allAssignments:
        # solution is a dictionary, where each key is a (clue number, clue type, clue) mapped to the answer
        clues = solution.keys()

        solutionScore = 0 
        for clue in clues:
            wordedClue = clue[2].lower()
            answer = solution[clue]
            wordedClue = wordedClue.translate(string.maketrans("",""), string.punctuation)
            # answer = answer.translate(string.maketrans("",""), string.punctuation)
            print "clue: ", clue
            print "answer: ", answer 
            pairScore = SolverUtil.semanticAnalysis(wordedClue, answer, answerMap)
            print pairScore, '\n'
            solutionScore += pairScore

        print "-------Solution Score: ", solutionScore, "---------------"
        if solutionScore > bestScore:
            bestScore = solutionScore
            optimalSolution = solution

    print "Best score = ", bestScore
    return optimalSolution

#Prints error rate stats
def errorRate(realAnswers, best):
    inCommon = 0.0
    for entry in best:
        print entry
        if entry[2] in realAnswers:
            inCommon += 1

    rate = float(inCommon)/len(realAnswers)
    print "Number words in common: ", inCommon
    print "Total words: ", len(realAnswers)
    print "Percent correct: ", rate



def main():
    print "Reading crossword puzzle JSON data and forming CSP..."
    
    # need this to clear out previous solutions file
    f = open("output_solutions.txt", 'w')
    f.close()

    # crossword_file = "crosswords/04-03-2014.json"
    # crossword_file = "crosswords/4by4.json"
    crossword_file = "crosswords/4by4v2.json"

    #english_words_file = "crosswords/4by4sol.txt"
    english_words_file = "wordsEnShort.txt"

    # create crossword puzzle object and load with data from JSON file
    cw = CrosswordUtil.Crossword()
    cw.load(crossword_file)
    # cw.printFills()
    englishWordsData = SolverUtil.parseEnglishWordsFile(english_words_file)
    domain = SolverUtil.englishLengthToWords(englishWordsData) 
    # print domain

    # create CSP, train data, create variables, and create binary potentials
    csp = CSPUtil.CSP()
    answerMap = trainFeatureVector(csp, "cluesFormatted.txt")


    #### THIS IS WRONG, NEED TO FIND A WAY TO GET REAL ANSWERS FROM JSON ---------------------------------
    # realAnswers = answerMap.keys()
    # 'List of answers = ', realAnswers
    realAnswers = cw.getAnswers()

    ''' create semantic analysis object to get a list of most probable words given a certain clue '''
    sa = SemanticAnalysis.SemanticAnalysis()
    sa.trainCluesData("cluesFormatted.txt")
    sa.trainSynonyms("synonyms_en.txt")
    sa.trainHomophones("homophones.txt")
    sa.trainCrosswordsWords("crossWordiest.txt", "crossWordiest")


    createCSPVariables(csp, cw, domain, sa)

    # Sets the number of jobs to execute in parallel when computing
    # the binary potentials, as this is an extremely computation heavy step
    num_concurrent_jobs = 5
    createCSPBinaryPotentials(csp, cw, num_concurrent_jobs)

    # Solve the CSP
    search = CSPUtil.BacktrackingSearch()
    print "Solving CSP..."
    allAssignments = search.solve(csp)
    best = chooseBest(allAssignments, answerMap)
    print best
    errorRate(realAnswers, best)




if __name__=='__main__':
    main()


# what anna did:
# 1. line 208, 209 say 'this is wrong, need to get answers from json' so within crossword util
# 2. note: for some reason even though the list of words is being printed out correctly for 'best answers',  
#  and the solution matches the set of best answers, it is saying that the accuracy is 0  
# 3. in semantic analysis, added code to take in 'cryptic-clues-testData.txt' to go through the cryptic types
# of clues and print out the lists of most probable words given a particular clue, clue type, and fill length
#       NOTE: anagram clue takes forever, this is something michael implemented.. so not sure if we want to take it out
# 4. integrated results into final draft paper, and wrote about semantic analysis in final draft 
