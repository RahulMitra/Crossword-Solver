import string




def main():

	inputF = open("synonyms_en.txt")
	lines = inputF.readlines()

	synonyms = []
	allSynonyms = {}

	for line in lines:
		lineNoPunct = line.translate(string.maketrans("",""), string.punctuation)
		line = lineNoPunct.strip()
		synonymsPresent = line.split()
		synonyms.append(synonymsPresent)

	for i in range(len(synonyms)):
		for j in range(len(synonyms[i])):

			allSynonyms[synonyms[i][j]] = synonyms[i]

    		
	print allSynonyms



if __name__=='__main__':
    main()