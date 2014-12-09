import sys
import numpy as np

def parseCluesFile(filename):
	return np.loadtxt(filename, delimiter="\r", dtype=str)

def rewriteFile(data, outputFName):
	outputF = open(outputFName, "w")

	outputStr = ""
	for line in data:
		outputStr += line + "\n"
	outputF.write(outputStr)
	outputF.close()


def main():
	clues = parseCluesFile(sys.argv[1])
	outputF = sys.argv[2]
	rewriteFile(clues, outputF)

if __name__=='__main__':
    main()
	