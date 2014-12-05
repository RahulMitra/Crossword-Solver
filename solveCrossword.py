import sys
import numpy as np
import csv
import random

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
	return wordsToClues, cluesToWords

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



def main():

	clues_filename = sys.argv[1]
	english_words_filename = sys.argv[2]
	cluesData = parseCluesFile(clues_filename)
	englishWordsData = parseEnglishWordsFile(english_words_filename)


	wordsToClues, cluesToWords = analyzeCluesInput(cluesData)
	wordsToLength, lengthToWords = englishWordsToLength(englishWordsData) 

	print len(cluesToWords)
	print len(wordsToLength)







if __name__=='__main__':
	main()