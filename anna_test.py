import string




def main():

	clue = "Delia's pickle contains jelly"
	fillLength = 5
	clueNoPunct = clue.translate(string.maketrans("",""), string.punctuation)
	print clueNoPunct
	clueWords = clueNoPunct.split()
	clueStr = ''
	for word in clueWords:
		clueStr += word
	print clueStr
	possWords = []
	for i in range(len(clueStr)-fillLength):
		# possWord = clueStr[i:i+fillLength]
		possWords.append(clueStr[i:i+fillLength])

	print possWords



if __name__=='__main__':
    main()