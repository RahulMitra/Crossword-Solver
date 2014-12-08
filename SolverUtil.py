import sys
import numpy as np
import csv
import random
import collections
import operator 
import string


 
''' so far in order to run this file type the following into the command line:
    python solveCrossword.py cluesData.txt englishWords.txt '''
 
def parseCluesFile(filename):
    d = np.loadtxt(filename, delimiter="\r", dtype=str)
    return d
 
def parseEnglishWordsFile(filename):
    d = np.loadtxt(filename, dtype=str)
    return d
 
 
def analyzeCluesInput(file_lines):
    wordsToClues = {}
    cluesToWords = collections.Counter()
    wordFreqs = {}
    answerMap = {}
    for line in file_lines:
        line_info = (line.strip()).split('\t')
        if len(line_info) == 4:
            clue = line_info[0].lower()
            answer = line_info[1].lower()
            year = int(line_info[2])
            month = int(line_info[3])
 
            if answer not in wordsToClues:
                wordsToClues[answer] = [clue]
            else:
                if clue != wordsToClues[answer]:
                    wordsToClues[answer].append(clue)
 
            if clue not in cluesToWords:
                cluesToWords[clue] = [answer]
            else:
                if answer != cluesToWords[clue]:
                    cluesToWords[clue].append(answer)

            # Word Freq
            if answer in wordFreqs:
                wordFreqs[answer] += 1
            else:
                wordFreqs[answer] = 0

            # Answer map
            if answer not in answerMap: 
                answerMap[answer] = set([])
            clueNoPunctuation = clue.translate(string.maketrans("",""), string.punctuation)
            wordsInClue = clueNoPunctuation.split()
            answerSet = answerMap[answer]
            for word in wordsInClue: 
                if word not in answerSet:
                    answerSet.add(word)
            answerMap[answer] = answerSet




    return wordsToClues, cluesToWords, wordFreqs, answerMap
 
def englishWordsToLength(englishWordsData):
    wordsToLength = {}
    lengthToWords = {}
    for word in englishWordsData:
        wordsToLength[word] = len(word)
        if len(word) in lengthToWords:
            lengthToWords[len(word)].append(word)
        else:
            lengthToWords[len(word)] = [word]
 
 
    return wordsToLength
 
 
''' this is the baseline algorithm which will take in the length of the empty word, 
    the clue associated with that word, the dictionary of clues to words that we have from 
    our data set and the lengthToWords dictionary that maps various english word lengths
    to possible english words and returns a word that is already associated with a clue in 
    the database or picks a random word that meets the length criteria'''
def baseline(empty_word_length, clue, cluesToWords, lengthToWords):
    if clue in cluesToWords:
        possWords = cluesToWords[clue]
        # account for the correct length
        lenPossWords = []
        for word in possWords:
            if len(word) == empty_word_length:
                lenPossWords.append(word)
        return random.choice(lenPossWords)
 
    return random.choice(lengthToWords[empty_word_length])
 
 

# Takes a clue, answer pair and using answerMap, returns a score
# Note: can only do semantic analysis on answers in the answer map
# Have to do something somewhere else if answer is not there, as
# semanticAnalyis assumes that answer is in answerMap
# Note: The higher the score, the better
def semanticAnalysis(clue, answer, answerMap):

    if answer not in answerMap:
        print answer, "not in answer map"
        return 0.0

    print answer, "found in answer map"
    wordsInClue = clue.split()
    semanticScore = 0
    for word in wordsInClue:
        if word in answerMap[answer]:
            semanticScore += 1
    # Normalize
    return float(semanticScore)/len(wordsInClue)
    
 # Feature vector = "[freq, semantic analysis num, 
 # Returns the vector
def generateFeatureVector(clue, answer, wordFreqs, answerMap):
    features = []

    # FEATURE 1: Frequency of word in other crossword puzzles
    if answer not in wordFreqs:
        freq = 0
    else:
        freq = wordFreqs[answer]
    features.append(freq)

    # FEATURE 2: Semantic Analysis
    semantic = semanticAnalysis(clue, answer, answerMap)
    features.append(semantic)

    return features


# Variable ordering portion of backtracking 
# Given a variable and its domains 
# Returns a sorted list of domains
def orderValues(clue, domains, cluesToWords, wordFreqs, answerMap): 
    # Remove Punctuation TODO: is this right?
    clue = clue.translate(string.maketrans("",""), string.punctuation)

    answerToScore = {} ## dict mapping answer to value, which is what we will order by

    # First, check to see if clue has appeared before. These answers get the highest weight
    # if clue in cluesToWords:
    #     possibleAnswers = cluesToWords[clue]
    #     for answer in possibleAnswers: 
    #         answerToScore[answer] = 10000000000.0 * possibleAnswers[answer]

    # Then, go through all words of the approp. length and assign them a score
    for myTuple in domains:
        print myTuple
        # Compute score
        answer = myTuple[0]
        answerNum = myTuple[1]
        features = generateFeatureVector(clue, answer, wordFreqs, answerMap)
        weights = [.3, .7] ## Dummy weights for now, could potentially change it later
        score  = (features[0] * weights[0]) + (features[1] * weights[1])
        if answerNum not in answerToScore:
            answerToScore[answerNum] = score


    sortedTuples = sorted(answerToScore.items(), key=operator.itemgetter(1), reverse = True)
    sortedDomains = []
    for myTuple in sortedTuples: 
        sortedDomains.append(myTuple[1])
    return sortedDomains






 # Todo: 
 # - abbrev mentioned with abbrev 
 # - capitalization in word/clue

def main():
 
    clues_filename = sys.argv[1]
    english_words_filename = sys.argv[2]
    cluesData = parseCluesFile(clues_filename)
    englishWordsData = parseEnglishWordsFile(english_words_filename)
 
 
    wordsToClues, cluesToWords, wordFreqs, answerMap = analyzeCluesInput(cluesData)
    wordsToLength, lengthToWords = englishWordsToLength(englishWordsData) 

    # testClue = "Halloween animal sonar"
    # testAnswer = "Bat"



 
    print len(cluesToWords)
    print len(wordsToLength)
 
 
 
 
 
 
 
if __name__=='__main__':
    main()