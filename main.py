import CrosswordUtil
import CSPUtil
import SolverUtil
import numpy as np

def parseEnglishWordsFile(filename):
    d = np.loadtxt(filename, dtype=str)
    return d

def englishWordsToLength(englishWordsData):
    wordsToLength = {}
    lengthToWords = {}
    for word in englishWordsData:
        wordsToLength[word] = len(word)
        if len(word) in lengthToWords:
            lengthToWords[len(word)].append(word)
        else:
            lengthToWords[len(word)] = [word]

    return lengthToWords

def main():
    print "Reading crossword puzzle JSON data and forming CSP..."
    #crossword_file = "crosswords/04-03-2014.json"
    crossword_file = "crosswords/4by4.json"
    cw = CrosswordUtil.Crossword()
    cw.load(crossword_file)
    # cw.printFills()

    englishWordsData = parseEnglishWordsFile("crosswords/4by4sol.txt")
    #englishWordsData = parseEnglishWordsFile("wordsEn.txt")
    domain = englishWordsToLength(englishWordsData) 

    csp = CSPUtil.CSP()

    print "Reading clue data and training feature vector..."
    cluesData = SolverUtil.parseCluesFile("nyt-crossword-master/clues.txt")
    csp.wordsToClues, csp.cluesToWords, csp.wordFreqs, csp.answerMap = SolverUtil.analyzeCluesInput(cluesData)    
    
    # Create CSP variable for each fill in the crossword puzzle
    for fill in cw.fills:
        csp.add_variable((fill.clue_index, fill.clue_type, fill.clue), domain[fill.fill_length])
        info_str = "Added CSP Variable: (" + str(fill.clue_index) + " " + str(fill.clue_type) \
            + ") with domain length " + str(fill.fill_length)
        print info_str

    # Loop through across fills and add binary potentials for each of their
    # intersections. Note that every character in an across fill intersects
    # with a character in a down fill.
    for across_fill in [fill for fill in cw.fills if fill.clue_type == "across"]:
        for key in across_fill.intersections:

            down_fill, down_intersecting_index, down_clue = across_fill.intersections[key][0], \
                across_fill.intersections[key][1], across_fill.intersections[key][0].clue
            across_intersecting_index = key

            def potential(across_str, down_str):
                return across_str[int(across_intersecting_index)] == down_str[int(down_intersecting_index)]

            across_fill_var = (across_fill.clue_index, across_fill.clue_type, across_fill.clue)
            down_fill_var = (down_fill.clue_index, down_fill.clue_type, down_clue)
            csp.add_binary_potential(across_fill_var, down_fill_var, potential)

            print "Added CSP Binary Potential between", across_fill_var, "and", down_fill_var, 
            info_str = "Added CSP Binary Potential:\n\t" \
                        + str(across_fill_var) + " char " + str(across_intersecting_index) \
                        + " intersects " + str(down_fill_var) + " char " + str(down_intersecting_index)
            print info_str

    search = CSPUtil.BacktrackingSearch()

    print "Solving..."
    search.solve(csp)


if __name__=='__main__':
    main()
