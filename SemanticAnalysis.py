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


	# Basic Latin-based languages are sometimes used in clues. 
	# These are typically articles of French, Spanish and German. 
	# clue: Man on the Spanish foot (4)
	# answer: HEEL. HE = man. EL = the in Spanish. HE + EL = HEEL (foot).
    def languageClue(self, clue):
    	possWords = []


	# An unusual type of word-play where the whole clue is both the definition and the word-play. 
	# “& lit.” clues are normally indicated by an exclamation mark.  
	# This type of clue is normally only found in challenging puzzles
	# example: Field entered by sportsmen ultimately!
	# answer: Answer: ARENA. AREA = field. N = sportsmen ultimately (last letter). 
	# AREA ‘entered by’ N = ARENA. (Whole clue is the definition)
    def andLitClue(self, clue):
    	possWords = []


	# Take letters out of clue to provide solution. 
	# Indicators: “heartlessly”, “loses”, “curtailed”, “dropped”, “gives up”
	# example: Parker loses a bed
	# answer: MAN. COAT = Parker. COAT loses “A” for COT (a bed)
    def deletionClue(self, clue):
    	possWords = []


    # Take the odd or even letters to form the solution. 
    # Indicated by “odd”, “even”, “regularly” or “every second”
    # example: Observe odd characters in scene
    # answer: SEE. Odd letters of SCENE
    # idea for implementation: construct words of providing length by constructing various combinations of 
    # words from the letters in the clue, as long as they are in order, can give higher weight to those
    # that come after trigger words like 'in', or can take out those words
    def oddEvenClue(self, clue):
    	possWords = []


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



    def mostProbableWord(self, fillLength, clue, type):
    	typeClue = self.typeOfClue(clue)
    	possWords = []
    	for t in typeClue:

    		if t == "question":
    			self.questionPresent(clue, fillLength) # need to figure out how to append possible words based on this type of clue

    		elif t == "exclamation":
    			self.andLitClue(clue)

    		elif t == "palindrome":
    			self.palindromeClue(clue, fillLength)

    		elif t == "hidden":
    			self.hiddenClue(clue)

    		elif t == "reverse":
    			self.reversalPresent(clue)

    		elif t == "homophone":
    			self.homophoneClue(clue)

    		elif t == "oddEven":
    			self.oddEvenClue(clue)

    		elif t == "deletion":
    			self.deletionClue(clue)

    		elif t == "container":
    			self.containerClue(clue)

    		elif t == "anagram":
    			self.anagramClue(clue)

    		elif t == "initialist":
    			self.initialismClue(clue)

    		elif t == "endalist":
    			self.endalismClue(clue)

    		elif t == "language":
    			self.languageClue(clue)







def main():
	sa = SemanticAnalysis()
	sa.trainCluesData("cluesFormatted.txt")

	sa.trainCrosswordsWords("crossWordiest.txt", "crossWordiest")
	sa.trainCrosswordsWords("most_common.txt", "mostCommon")


	clue = "Sketcher went up to get reward"
	mostProbableWord = sa.mostProbableWord(6, clue, "across")





if __name__=='__main__':
    main()