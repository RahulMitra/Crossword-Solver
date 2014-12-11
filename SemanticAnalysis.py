import SolverUtil
import string


''' abbreviations: http://en.wikipedia.org/wiki/Crossword_abbreviations '''
''' more info on cryptic crosswords: http://en.wikipedia.org/wiki/Cryptic_crossword ''' 
''' importing synonyms: http://stackoverflow.com/questions/2667057/english-dictionary-as-txt-or-xml-file-with-support-of-synonyms '''

class SemanticAnalysis:
    def __init__(self):

    	self.wordsToClues = {}
    	self.cluesToWords = {}
    	self.wordFreqs = {}
    	self.answerMap = {}
    	self.crossWordiest = {}
    	self.mostCommonWords = {}
    	self.synonyms = {} # a dictionary mapping each word to its list of synonyms, the list will include the word itself

    	''' can also create a dict of all indicators to the type of clue that they indicate '''

    	self.reverseIndicatorsDown = ['back', 'reflected', 'turned', 'going up'] 
    	self.reverseIndicatorsAcross = ['west', 'left']
    	self.hiddenClueIndicators = ['in part', 'partially', 'in', 'within', 'hides', 'conceals', 'some', 'held by']
    	self.palindromeIndicators = ['either way', 'going side to side', 'up and down', 'read both ways']
    	self.containerIndicators = ['within', 'in', 'around', 'about', 'contained', 'held', 'inside', 'retain', 'keeps', 'into']
    	self.homophoneIndicators = ['heard', 'sounds like', 'audibly', 'noisily', 'out loud', 'say', 'spoken']
    	self.initialismIndicators = ['first', 'prime', 'lead', 'head', 'top']
    	self.endalismIndicators = ['last', 'ultimate', 'final']
    	self.oddEvenIndicators = ['odd', 'even', 'regularly', 'every second']
    	self.deletionIndicators = ['heartlessly', 'loses', 'curtailed', 'dropped', 'gives up']
    	self.languageIndicators = ['French', 'Spanish', 'German']



    	''' there are hundreds of these and they are the most common clue type -- see if there's an anagram dict '''
    	''' most often they are words signaling 'to make change' '''
    	self.anagramIndicators = ['transfer', 'switch', 'cook', 'kill', 'reborn', 'mixed', 'turned', 'out', 'off', 'warped', 'lost', 'moved']


    def trainSynonyms(self, synonyms_filename):
    	# the file is formatted such that each line contains a set of synonyms
    	# need to map each word on each line to all other words on the line

		inputF = open("synonyms_en.txt")
		lines = inputF.readlines()

		synonyms = []
		allSynonyms = {}

		for line in lines:
			lineNoPunct = line.translate(string.maketrans("",""), string.punctuation) # ignore all punctuation
			line = lineNoPunct.strip()
			line = line.lower() # ignore all capitalization
			synonymsPresent = line.split()
			synonyms.append(synonymsPresent)

		for i in range(len(synonyms)):
			for j in range(len(synonyms[i])):

				allSynonyms[synonyms[i][j]] = synonyms[i]

		self.synonyms = allSynonyms




    def trainCluesData(self, clues_filename):
    	cluesData = SolverUtil.parseCluesFile(clues_filename)
    	self.wordsToClues, self.cluesToWords, self.wordFreqs, self.answerMap = SolverUtil.analyzeCluesInput(cluesData) 

    	for clue in self.cluesToWords:
    		print self.cluesToWords[clue]

    def trainCrosswordsWords(self, filename, typeWords):
    	inputF = open(filename)
    	lines = inputF.readlines()

    	if typeWords == "crossWordiest":
    		for line in lines:
    			lineElems = line.split()
    			self.crossWordiest[lineElems[0].lower()] = float(lineElems[1].strip())

    	elif typeWords == "mostCommon":
    		for line in lines:
    			lineElems = line.split()
    			self.mostCommonWords[lineElems[0].lower()] = int(lineElems[1].strip())




    	print self.mostCommonWords
    	print self.crossWordiest


    ''' to define if there is time '''
    # def datePresent(self, clue):
    # def pronounPresent(self, clue):
    # def otherCluesPresent(self, clue):
    # def abbrevPresent(self, clue):


    ''' skip but do naturally '''
	# Clues with more than one type of word-play are extremely common
	# clue: Joint in which two knights tuck into beer (5)
	# answer: ANKLE. NK = two different abbreviations of knight. ALE = beer. NK inside ALE = ANKLE (a joint).
	# clue2: Journey in the heart of Austria accompanied by composer (6)
	# answer: TRAVEL. T = heart of Aus(t)ria. RAVEL = composer. T +RAVEL = TRAVEL (to journey)
	# def combinationClue(self, clue):




    ''' skip, can't infer letters from 'objects' '''
	# Occasionally objects that look like letters may be used in a clue.
	# clue: Rookie wears glasses to the toilet (3)
	# answer: LOO. L = rookie (learner). OO looks like glasses. L + OO = LOO.
    # def visualClue(self, clue):


    ''' need to set domains of common foreign language words used in clue answers '''
	# Basic Latin-based languages are sometimes used in clues. 
	# These are typically articles of French, Spanish and German. 
	# clue: Man on the Spanish foot (4)
	# answer: HEEL. HE = man. EL = the in Spanish. HE + EL = HEEL (foot).
    def languageClue(self, clue):
    	possWords = []
    	return possWords


    ''' this one is tough as it combines several clue types '''
	# An unusual type of word-play where the whole clue is both the definition and the word-play. 
	# “& lit.” clues are normally indicated by an exclamation mark.  
	# This type of clue is normally only found in challenging puzzles
	# example: Field entered by sportsmen ultimately!
	# answer: Answer: ARENA. AREA = field. N = sportsmen ultimately (last letter). 
	# AREA ‘entered by’ N = ARENA. (Whole clue is the definition)
    def andLitClue(self, clue, fillLength):
    	possWords = []
    	clue = clue.lower()
    	clueNoPunct = clue.translate(string.maketrans("",""), string.punctuation)
    	clueWords = clueNoPunct.strip()

    	# this for loop doesn't exactly due this type of clue justice, it's just the beginning
    	for word in clueWords:
    		wordSyns = self.synonyms[word]:
    		for syn in wordSyns:
    			if len(syn) == fillLength:
    				possWords.append(syn)

    	return possWords


	# Take letters out of clue to provide solution. 
	# Indicators: “heartlessly”, “loses”, “curtailed”, “dropped”, “gives up”
	# example: Parker loses a bed
	# answer: MAN. COAT = Parker. COAT loses “A” for COT (a bed)
    def deletionClue(self, clue, fillLength):
    	possWords = []
    	clue = clue.lower()
    	clueNoPunct = clue.translate(string.maketrans("",""), string.punctuation)
    	clueWords = clueNoPunct.strip()
    	lossyWordIndex = -1
    	if 'heartlessly' in clueNoPunct:
    		lossyWordIndex = clueWords.index('heartlessly')

    	elif 'loses' in clueNoPunct:
    		lossyWordIndex = clueWords.index('loses')

    	elif 'curtailed' in clueNoPunct:
    		lossyWordIndex = clueWords.index('curtailed')

    	elif 'dropped' in clueNoPunct:
    		lossyWordIndex = clueWords.index('dropped')

    	elif 'gives up' in clueNoPunct:
    		lossyWordIndex = clueWords.index('up')

    	# make the assumption that the letter drops comes after deletion indicator
    	letterToDrop = clueWords[lossyWordIndex+1] 

    	for word in clueWords:
    		wordSyns = self.synonyms[word]
    		for syn in wordSyns:
    			if len(syn) == fillLength+1:
    				if letterToDrop in syn:
    					letterIndex = syn.index(letterToDrop)
    					if letterIndex < len(syn)-1
    						possWord = syn[:letterIndex] + syn[letterIndex+1:len(syn)]
    					else:
    						possWord = syn[:letterIndex]
    					possWords.append(possWord)


    	return possWords


    # Take the odd or even letters to form the solution. 
    # Indicated by “odd”, “even”, “regularly” or “every second”
    # example: Observe odd characters in scene
    # answer: SEE. Odd letters of SCENE
    # idea for implementation: construct words of providing length by constructing various combinations of 
    # words from the letters in the clue, as long as they are in order, can give higher weight to those
    # that come after trigger words like 'in', or can take out those words
    def oddEvenClue(self, clue, fillLength):
    	possWords = []
    	clue = clue.lower()
    	clueNoPunct = clue.translate(string.maketrans("",""), string.punctuation)
    	clueWords = clueNoPunct.strip()
    	odd = False
    	even = False
    	# if we are searching for odd or even fill
    	if 'even' in clueNoPunct:
    		even = True
    	elif 'odd' in clueNoPunct:
    		odd = True
    	# we have to generate both odd and even letters to form possible solutions if neither even or odd are present
    	if not odd and not even:
    		even = True
    		odd = True


    	for word in clueWords:

    		if odd:
    		# can generate a fill word taking odd letters from the word
    			if len(word) >= fillLength*2 - 1:
    				wordIndex = 0
    				newPossWord = ""
    				for i in range(fillLength):
    					newPossWord += word[wordIndex]
    					wordIndex += 2

    				possWords.append(newPossWord)

    		if even:
    			# can generate a fill word taking even letters from the word
    			if len(word) >= fillLength*2:
    				wordIndex = 1
    				newPossWord = ""
    				for i in range(fillLength):
    					newPossWord += newPossWord[wordIndex]
    					wordIndex += 2

    				possWords.append(newPossWord)


    	return possWords


    	




    # First letter or letters provide the solution. 
    # Indicated by “first”, “prime”, “lead”, “head”, “top”. 
    # Note similarly “last”, “ultimate”, “final” can refer to the last letter.
    # example: First class pile is really just tacky
    # answer: CHEAP. C = First class. HEAP = pile. C + HEAP = CHEAP (tacky)
    # example2: Starts to run around pointlessly in a bind 
    # answer: TRAP. First letters of To Run Around Pointlessly.
    # idea for implementation: if you see 'first' just try to make combinations of words from the first
    # letters of the clues following
    def initialismClue(self, clue):
    	possWords = []
    def endalismClue(self, clue):
    	possWords = []


    ''' skipped '''
    # Instead of wordplay clues can have two definitions side by side to give the same solution
    # example: Gone too far into no man’s land?
    # answer: OVER THE TOP. 1. Exceeded bounds. 2. Historical slang for charging from war trenches into “no man’s land”.
    def doubleDefinitionClue(self, clue):
    	possWords = []

   
   	# Homophones can be indicated by “heard”, “sounds like”, “audibly”, “noisily”, 
   	# “out loud”, “say”, “spoken”
   	# example: Not even one sister heard (4)
	# answer: NONE. Is a homophone of NUN (sister)
	# idea for implementation: is there a homophone dictionary to import?
    def homophoneClue(self, clue):
    	possWords = []


    # Anagrams are the most common clue-type. 
    # Indicated by potentially hundreds of words that loosely mean modify or change. 
    # Some examples: “transfer”, “switch”, “cook”, “kill”, “reborn”, “mixed”, “turned”, 
    # “out”, “off”, “warped”, “lost”, “moved”. Always consider potential anagram 
    # indicators when solving any clue. Fodder (the letters to be jumbled) will 
    # always appear before or after indicator. Multiple whole words can be used as 
    # fodder however the number of letters must match the solution.
    # example: Dress suiting a saint
    # answer: IGNATIUS. “Dress” indicates anagram. Letters of “a suiting” provide IGNATIUS (a saint). Note the importance of the article “a”.
    def anagramClue(self, clue):
    	possWords = []


    # Letters or words are placed inside other words. 
    # Indicators: “within”, “in”, “around”, “about”, “contained”, “held”, 
    # “inside”, “retain”, “keeps”, “into”.
    # example: Superman retains interest in Painter
    # answer: TITIAN. TITAN = Superman. I = interest. Put I into TITAN gives the painter TITIAN.
    def containerClue(self, clue):
    	possWords = []


    ''' skipped '''
    # Charade clues are formed by joining individual clues together to create the solution. 
    # Indicators not necessary but joining words like “with”, “follows”, “behind”, “after” 
    # are likely. More complex cryptic crosswords will often combine charade clues with other 
    # types of word-play. The use of abbreviations in charade clues is very common.
    # example: Place on bottom of sack
    # answer: PLUNDER. PL = Place (street name abbrev). UNDER = on bottom. PL + UNDER = PLUNDER (to sack).
    def charadeClue(self, clue):
    	possWords = []


	# Palindromes may be indicated by phases such as “either way”, 
	# “going side to side”, “up and down”, ”read both ways”
	# example: Advance in either direction
	# answer: PUT UP. A palindrome meaning advance. 
	# note for implementation: often the first word of a clue signals the most meaning
    def palindromeClue(self, clue):
    	possWords = []


    # The word is hidden within the letters of the wordplay. 
    # Indicators of a hidden clue are “in part”, “partially”, “in”, “within”, “hides”, 
    # “conceals”, “some”, and “held by”
    # example: Delia’s pickle contains jelly (5)
	# Answer: ASPIC
	# idea for implementation: basically create proper length combinations of all words in the string
	# of the desired length of the fill word
    def hiddenClue(self, clue, fillLength):
		clueNoPunct = clue.translate(string.maketrans("",""), string.punctuation)
		clueWords = clueNoPunct.split()
		clueStr = ''
		for word in clueWords:
			clueStr += word
		possWords = []
		for i in range(len(clueStr)-fillLength):
			possWords.append(clueStr[i:i+fillLength])




    # Reversals
	# The reverse of part of the clue provides the definition. 
	# Indicators: “back”, “reflected”, “turned” “going up” (in a down clue), 
	# “west” or “left” (in an across clue).
	# example: Sketcher went up to get reward
	# answer: drawer
	# another example: Go no further putting the crockery up
	# answer: Answer: STOP. Crockery = POTS. Reversed gives STOP.
	# idea for implementation: add words to the domain in reverse order of the words present in the clue
	# idea #2 for implementation: reference synonyms of words present in the clue
    def reversalPresent(self, clue, fillLength):
    	clueNoPunct = clue.translate(string.maketrans("",""), string.punctuation)
    	clueWords = clueNoPunct.split()
    	possWords = []

    	# we need to also include all definitions of words in the clue
    	# need to import dictionary for this to happen
    	for word in clueWords:
    		if len(word) == fillLength:
    			possWords.append(word[::-1]) # this reverses the word





    # In this type of clue the whole clue is usually the definition in an unusual context. 
   	# They are sometimes indicated by ending with a question mark.
   	# example clue: Hair style with comb in it? (7)
	# example answer: BEEHIVE
	# idea for solving: choose words that aren't common from clue such as 'hair' and 'comb'
	# what combos of words can we come up with that match the designated length ?
    def questionPresent(self, clue, fillLength):
    	clueNoPunct = clue.translate(string.maketrans("",""), string.punctuation)
    	clueWords = clueNoPunct.split()
    	possWords = []

    	# will want synonyms of each word and potentially their combos
    	for word in clueWords:
    		for synonym in self.synonyms[word]: ''' self.synonyms doesn't exist yet '''
    			possWords.append(synonym)

    	# now filter by word length in poss words and combinations of words in poss lengths
    	# that form the accurate length word





    # figure out what type of clue it is based on the words present in the clue and call that function
    def typeOfClue(self, clue, fillType):
    	typeClue = [] # make a list of the type clue that a clue can be so that it can be a combo
    	# first check for question mark or exclamation before parsing the clue
    	if '?' in clue:
    		typeClue.append("question")
    	elif '!' in clue:
    		typeClue.append("exlamation")
    	clueNoPunct = clue.translate(string.maketrans("",""), string.punctuation)
    	clueWords = clueNoPunct.split()


    	for palindromeIndicator in self.palindromeIndicators:
    		if palindromeIndicator in clueNoPunct:
    			typeClue.append("palindrome")

    	for hiddenClueIndicator in self.hiddenClueIndicators:
    		if hiddenClueIndicator in clueNoPunct:
    			typeClue.append("hidden")

    	if fillType == "across":
    		for reverseIndicator in self.reverseIndicatorsAcross:
    			if reverseIndicator in clueNoPunct:
    				typeClue.append("reverse")
    	else:
    		for reverseIndicator in self.reverseIndicatorsDown:
    			if reverseIndicator in clueNoPunct:
    				typeClue.append("reverse")

    	for homophoneIndic in self.homophoneIndicators:
    		if homophoneIndic in clueNoPunct:
    			typeClue.append("homophone")

    	for oddEvenIndicator in self.oddEvenIndicators:
    		if oddEvenIndicator in clueNoPunct:
    			typeClue.append("oddEven")

    	for deletionIndicator in self.deletionIndicators:
    		if deletionIndicator in clueNoPunct:
    			typeClue.append("deletion")


    	for word in clueWords:

    		if word in self.containerIndicators:
    			typeClue.append("container")

    		if word in self.anagramIndicators:
    			typeClue.append("anagram")

    		if word in self.initialismIndicators:
    			typeClue.append("initialist")

    		elif word in self.endalismIndicators:
    			typeClue.append("endalist")

    		if word in self.languageIndicators:
    			typeClue.append("language")



    def mostProbableWords(self, fillLength, clue, type):
    	typeClue = self.typeOfClue(clue)
    	possWords = []
    	for t in typeClue:

    		if t == "question":
    			newPossWords = self.questionPresent(clue, fillLength) # need to figure out how to append possible words based on this type of clue
    			possWords.extend(newPossWords)

    		elif t == "exclamation":
    			newPossWords = self.andLitClue(clue, fillLength)
    			possWords.extend(newPossWords)

    		elif t == "palindrome":
    			newPossWords = self.palindromeClue(clue, fillLength)
    			possWords.extend(newPossWords)

    		elif t == "hidden":
    			newPossWords = self.hiddenClue(clue)
    			possWords.extend(newPossWords)

    		elif t == "reverse":
    			newPossWords = self.reversalPresent(clue)
    			possWords.extend(newPossWords)

    		elif t == "homophone":
    			newPossWords = self.homophoneClue(clue)
    			possWords.extend(newPossWords)

    		elif t == "oddEven":
    			newPossWords = self.oddEvenClue(clue, fillLength)
    			possWords.extend(newPossWords)

    		elif t == "deletion":
    			newPossWords = self.deletionClue(clue, fillLength)
    			possWords.extend(newPossWords)

    		elif t == "container":
    			newPossWords = self.containerClue(clue)
    			possWords.extend(newPossWords)

    		elif t == "anagram":
    			newPossWords = self.anagramClue(clue)
    			possWords.extend(newPossWords)

    		elif t == "initialist":
    			newPossWords = self.initialismClue(clue)
    			possWords.extend(newPossWords)

    		elif t == "endalist":
    			newPossWords = self.endalismClue(clue)
    			possWords.extend(newPossWords)

    		elif t == "language":
    			newPossWords = self.languageClue(clue)
    			possWords.extend(newPossWords)







def main():
	sa = SemanticAnalysis()
	sa.trainCluesData("cluesFormatted.txt")
	sa.trainSynonyms("synonyms_en.txt")

	sa.trainCrosswordsWords("crossWordiest.txt", "crossWordiest")
	sa.trainCrosswordsWords("most_common.txt", "mostCommon")


	clue = "Sketcher went up to get reward"
	mostProbWords = sa.mostProbableWords(6, clue, "across")
	print mostProbWords





if __name__=='__main__':
    main()