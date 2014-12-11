import string




def main():

	inputF = open("homophones.txt")
	outputF = open("homophones_formatted", "w")

	lines = inputF.readlines()
	outputStr = ''

	for line in lines:
		# noPunct = 
		noPunct = line.replace(",", " ")
		noPunct = noPunct.replace("\t", "")
		noPunct = noPunct.replace("array(", "")
		noPunct = noPunct.translate(string.maketrans("",""), string.punctuation)
		noPunct = noPunct.strip()
		print noPunct
		noPunct = noPunct.strip()
		outputStr += noPunct + '\n'


    		
	outputF.write(outputStr)
	outputF.close()



if __name__=='__main__':
    main()