import json

# this is the word fill class that encapsulates the essentials of a word fill object 
# will be used in the csp
class Fill:

	def __init__(self):
		self.clue_index = 0 	# index of the clue associated with the word fill
		self.clue_type = "" 	# across or down
		self.fill_length = 0 	# length of fill
		self.coordinates = []	# list of coordinate pairs
		self.intersections = {} # dictionary: fill word intersection index => (clue index, clue type, intersection index)

	def getLength(self):
		return self.fill_length

	def getIntersections(self):
		return self.intersections

	def getType(self):
		return self.clue_type

# Crossword Puzzle Class
class Crossword:

	def __init__(self):
		self.clues = {} 		# map of (clue index, clue type) : clue
		self.acrossClues = [] 	# each clue has associated number, such as 1-across, 6-across, stores the possible number
		self.downClues = [] 	# same as across clues
		self.fills = [] 		# list of fill objects
		self.data = {}			# JSON representation of crossword puzzle
		self.formattedCW = [] 	# 2D matrix representing the crossword puzzle

	def getClues(self):
		return self.clues

	def getFills(self):
		return self.fills

	def populateClues(self):
		clues = {}
		acrossClues = self.data["clues"]["across"]
		# need to grab the index of the "." in order to get the number of the clue
		for clue in acrossClues:
			periodIndex = clue.index('.')
			numClue = int(clue[:periodIndex])
			clueStr = str(clue[periodIndex+2:])
			clues[(numClue, "across")] = clueStr
			self.acrossClues.append(int(clue[:periodIndex]))

		downClues = self.data["clues"]["down"]
		for clue in downClues:
			periodIndex = clue.index('.')
			numClue = int(clue[:periodIndex])
			clueStr = str(clue[periodIndex+2:])
			clues[(numClue, "down")] = clueStr
			self.downClues.append(int(clue[:periodIndex]))

		self.clues = clues
		self.acrossClues.sort()
		self.downClues.sort()

	def formatCrossword(self):
		gridnums = list(self.data["gridnums"])
		answerLetters = list(self.data["grid"])
		numRows = int(self.data["size"]["rows"])
		numCols = int(self.data["size"]["cols"])
		formattedCW = [[0] * numCols for x in range(numRows)]

		for i in range(numRows):
			for j in range(numCols):

				gridNumIndex = j + i * numCols

				if answerLetters[gridNumIndex] == ".":
					formattedCW[i][j] = -1
				else:
					formattedCW[i][j] = int(self.data["gridnums"][gridNumIndex])

		self.formattedCW = formattedCW
	
	def generateAcrossFills(self):
		fills = []
		numRows = int(self.data["size"]["rows"])
		numCols = int(self.data["size"]["cols"])

		counter = 0
		numCells = numRows * numCols

		while counter < numCells:
			# Extract row and col data from counter
			col = counter % numRows
			row = counter / numRows

			clue_num = self.formattedCW[row][col]
			if clue_num in self.acrossClues:
				starting_row = row
				starting_col = col
	
				num_fill = 1
				num_black = 0
				col = col + 1
				while True:

					# If we are the last row, update fill or black box
					# count and move to next column.
					if col == numCols - 1:
						if self.formattedCW[row][col] == -1:
							num_black = num_black + 1
						else:
							num_fill = num_fill + 1
						break
					# Otherwise do the usual checks
					else:
						if self.formattedCW[row][col] == -1:
							col = col + 1
							num_black = num_black + 1
						elif self.formattedCW[row][col] in self.acrossClues:
							break
						else:
							col = col + 1
							num_fill = num_fill + 1

				# Make new fill
				newFill = Fill()
				newFill.clue_index = clue_num
				newFill.clue_type = "across"
				newFill.fill_length = num_fill

				# get coordinates that this fill resides on
				for i in range(newFill.fill_length):
					newFill.coordinates.append((starting_row, starting_col + i))

				fills.append(newFill)

				counter = counter + num_fill + num_black
			else:
				counter = counter + 1

		for fill in fills:
			self.fills.append(fill)

	def generateDownFills(self):
		fills = []
		numRows = int(self.data["size"]["rows"])
		numCols = int(self.data["size"]["cols"])

		counter = 0
		numCells = numRows * numCols

		while counter < numCells:
			# Extract row and col data from counter
			row = counter % numRows
			col = counter / numRows

			clue_num = self.formattedCW[row][col]
			if clue_num in self.downClues:
				starting_row = row
				starting_col = col

				num_fill = 1
				num_black = 0
				row = row + 1
				while True:

					# If we are the last row, update fill or black box
					# count and move to next column.
					if row == numRows - 1:
						if self.formattedCW[row][col] == -1:
							num_black = num_black + 1
						else:
							num_fill = num_fill + 1
						break
					# Otherwise do the usual checks
					else:
						if self.formattedCW[row][col] == -1:
							row = row + 1
							num_black = num_black + 1
						elif self.formattedCW[row][col] in self.downClues:
							break
						else:
							row = row + 1
							num_fill = num_fill + 1

				# Make new fill
				newFill = Fill()
				newFill.clue_index = clue_num
				newFill.clue_type = "down"
				newFill.fill_length = num_fill

				# get coordinates that this fill resides on
				for i in range(newFill.fill_length):
					newFill.coordinates.append((starting_row + i, starting_col))

				fills.append(newFill)

				counter = counter + num_fill + num_black
			else:
				counter = counter + 1

		for fill in fills:
			self.fills.append(fill)

	
	def generateFillIntersections(self):
		numRows = int(self.data["size"]["rows"])
		numCols = int(self.data["size"]["cols"])
	
		for row in range(numRows):
			for col in range(numCols):
				intersecting_fills = [fill for fill in self.fills if (row, col) in fill.coordinates]
				if len(intersecting_fills) > 1:
					if (intersecting_fills[0].clue_type == "down"):
						down_fill =  intersecting_fills[0]
						across_fill = intersecting_fills[1]
					else:
						across_fill =  intersecting_fills[0]
						down_fill = intersecting_fills[1]

					initial_row = down_fill.coordinates[0][0]
					initial_col = across_fill.coordinates[0][1]
					down_fill_intersection_index = row - initial_row
					across_fill_intersection_index = col - initial_col
					
					# dictionary: fill word intersection index => ("other" fill word, "other" fill word's intersecting index)
					down_fill.intersections[str(down_fill_intersection_index)] = (across_fill, across_fill_intersection_index)
					across_fill.intersections[str(across_fill_intersection_index)] = (down_fill, down_fill_intersection_index)

	def load(self, crossword_file):
		# Reset all internal variables
		self.clues = {} 		
		self.acrossClues = []
		self.downClues = [] 
		self.fills = []
		self.data = JSONParser().parseJSON(crossword_file)
		self.formattedCW = []

		self.populateClues()
		self.formatCrossword()
		self.generateAcrossFills()
		self.generateDownFills()
		self.generateFillIntersections()

	def printFills(self):
		for fill in self.fills:
			info_str = "Fill: [" + str(fill.clue_index) + " " + str(fill.clue_type) \
						+ "] length " + str(fill.fill_length)
			print info_str
			for key in fill.intersections:
				intersecting_fill = fill.intersections[key][0]
				intersecting_index = fill.intersections[key][1]
				info_str = "[" + str(fill.clue_index) + " " + str(fill.clue_type) + "] char " + key \
							+ " intersects with [" + str(intersecting_fill.clue_index) + " " \
							+ str(intersecting_fill.clue_type) + "] char " + str(intersecting_index)
				print info_str
			print ""

class JSONParser:

	def __init__(self):
		self.data = {}

	def parseJSON(self, json_file):
		json_data=open(json_file)
		data = json.load(json_data)
		json_data.close()
		return data