import CrosswordUtil
import CSPUtil
import SolverUtil
import numpy as np
import sys
from multiprocessing import Process, Manager
import string

# -------------------------------------------------------------------------------------------------------------
# Clue Analysis Code
# -------------------------------------------------------------------------------------------------------------
def trainFeatureVector(csp, clues_training_data):
    print "Reading clue data and training feature vector..."
    cluesData = SolverUtil.parseCluesFile(clues_training_data)
    csp.wordsToClues, csp.cluesToWords, csp.wordFreqs, csp.answerMap = SolverUtil.analyzeCluesInput(cluesData)    

# will decrease the domain size based on the fill object's clue
def decreaseDomain(fill, currDomain, wordsToClues, cluesToWords, wordFreqs, answerMap):
    clue = fill.clue.translate(string.maketrans("",""), string.punctuation)

    tupleDomains = [(currDomain[i], i) for i in range(len(currDomain))]
    sortedDomains = SolverUtil.orderValues(fill.clue, tupleDomains, cluesToWords, wordFreqs, answerMap)
    sortedWordDomains = [currDomain[i] for i in range(len(sortedDomains))]
    if len(sortedWordDomains) > 500:
        return sortedWordDomains[:500] # return just top 100 hits for the domain
    else:
        return sortedWordDomains


# -------------------------------------------------------------------------------------------------------------
# CSP Generation Code
# -------------------------------------------------------------------------------------------------------------
def createCSPVariables(csp, cw, domain):
    # Create CSP variable for each fill in the crossword puzzle
    print "Adding CSP Variables..."
    for fill in cw.fills:
        fillDomain = decreaseDomain(fill, domain[fill.fill_length], csp.wordsToClues, csp.cluesToWords, csp.wordFreqs, csp.answerMap)
        csp.add_variable((fill.clue_index, fill.clue_type, fill.clue), fillDomain)
        info_str = "Added CSP Variable: (" + str(fill.clue_index) + " " + str(fill.clue_type) \
            + ") with domain length " + str(fill.fill_length)
        print info_str
  
def generate_binary_potential_table(csp, across_fill_var, down_fill_var, across_intersecting_index, \
                                down_intersecting_index, potentials_tables):

    def potential(across_str, down_str):
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


def main():
    print "Reading crossword puzzle JSON data and forming CSP..."

    #crossword_file = "crosswords/04-03-2014.json"
    crossword_file = "crosswords/4by4.json"

    # english_words_file = "crosswords/4by4sol.txt"
    english_words_file = "wordsEn.txt"

    # create crossword puzzle object and load with data from JSON file
    cw = CrosswordUtil.Crossword()
    cw.load(crossword_file)
    englishWordsData = SolverUtil.parseEnglishWordsFile(english_words_file)
    domain = SolverUtil.englishLengthToWords(englishWordsData) 

    # create CSP, train data, create variables, and create binary potentials
    csp = CSPUtil.CSP()
    trainFeatureVector(csp, "cluesFormatted.txt")
    createCSPVariables(csp, cw, domain)

    # Sets the number of jobs to execute in parallel when computing
    # the binary potentials, as this is an extremely computation heavy step
    num_concurrent_jobs = 5
    createCSPBinaryPotentials(csp, cw, num_concurrent_jobs)

    # Solve the CSP
    search = CSPUtil.BacktrackingSearch()
    print "Solving CSP..."
    search.solve(csp)

if __name__=='__main__':
    main()