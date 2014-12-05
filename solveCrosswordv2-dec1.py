import sys
import numpy as np
import csv
import random
import string
import json

  
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
    cluesToWords = {}
    wordFreqs = {}
    answerToClueWords = {}
    for line in file_lines:
        line_info = (line.strip()).split('\t')
        if len(line_info) == 4:
            clue = line_info[0]
            answer = line_info[1]
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
 
            # here we create a dictionary of possible fill answer to the various words that appear in a particular
            # clue associated with that answer
            if answer not in answerToClueWords: 
                answerToClueWords[answer] = set([])
            # eliminate punctuation
            clueNoPunctuation = clue.translate(string.maketrans("",""), string.punctuation)


            wordsInClue = clueNoPunctuation.split()
            clueWords = answerToClueWords[answer]

            for word in wordsInClue:
                clueWords.add(word.lower())
            answerToClueWords[answer] = clueWords

 
 
    return wordsToClues, cluesToWords, wordFreqs, answerToClueWords
  
def englishWordsToLength(englishWordsData):
    wordsToLength = {}
    lengthToWords = {}
    for word in englishWordsData:
        wordsToLength[word] = len(word)
        if len(word) in lengthToWords:
            lengthToWords[len(word)].append(word)
        else:
            lengthToWords[len(word)] = [word]
  
  
    return wordsToLength, lengthToWords
  
  
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
    wordsInClue = clue.split()
    semanticScore = 0
    for word in wordsInClue:
        if word in answerMap[answer]:
            semanticScore += 1
    # Normalize
    return float(semanticScore)/len(wordsInClue)
 
     
 # Feature vector = "[freq, semantic analysis num, 
def generateFeatureVector(clue, answer, lengthToWords, wordFreqs, answerMap):
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
 


  
 # Todo: 
 # - abbrev mentioned with abbrev 
 # - capitalization in word/clue
 
def main():
  
    clues_filename = sys.argv[1]
    english_words_filename = sys.argv[2]
    cluesData = parseCluesFile(clues_filename)
    englishWordsData = parseEnglishWordsFile(english_words_filename)
  
  
    wordsToClues, cluesToWords, wordFreqs, answerToClueWords = analyzeCluesInput(cluesData)
    wordsToLength, lengthToWords = englishWordsToLength(englishWordsData) 
    # print answerToClueWords
 
    
    # now to test things, let's see what list we get of potential word fills
    # print getPotentialFills = 
  
    # print len(cluesToWords)
    # print len(wordsToLength)
  
  
  
  
  
  
  
if __name__=='__main__':
    main()