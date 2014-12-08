import json, re
import copy
import SolverUtil

# General code for representing a weighted CSP (Constraint Satisfaction Problem).
# All variables are being referenced by their index instead of their original
# names.
class CSP:
    def __init__(self):
        # Total number of variables in the CSP.
        self.numVars = 0

        # The list of variable names in the same order as they are added. A
        # variable name can be any hashable objects, for example: int, str,
        # or any tuple with hashtable objects.
        self.varNames = []

        # Each entry is the list of domain values that its corresponding
        # variable can take on.
        # E.g. if B \in ['a', 'b'] is the second variable
        # then valNames[1] == ['a', 'b']
        self.valNames = []

        # Each entry is a unary potential table for the corresponding variable.
        # The potential table corresponds to the weight distribution of a variable
        # for all added unary potential functions. The table itself is a list
        # that has the same length as the variable's domain. If there's no
        # unary function, this table is stored as a None object.
        # E.g. if B \in ['a', 'b'] is the second variable, and we added two
        # unary potential functions f1, f2 for B,
        # then unaryPotentials[1][0] == f1('a') * f2('a')
        self.unaryPotentials = []

        # Each entry is a dictionary keyed by the index of the other variable
        # involved. The value is a binary potential table, where each table
        # stores the potential value for all possible combinations of
        # the domains of the two variables for all added binary potneital
        # functions. The table is represented as a 2D list, with size
        # dom(var) x dom(var2).
        #
        # As an example, if we only have two variables
        # A \in ['b', 'c'],  B \in ['a', 'b']
        # and we've added two binary functions f1(A,B) and f2(A,B) to the CSP,
        # then binaryPotentials[0][1][0][0] == f1('b','a') * f2('b','a').
        # binaryPotentials[0][0] should return a key error since a variable
        # shouldn't have a binary potential table with itself.
        #
        # One important thing to note here is that the indices in the potential
        # tables are indexed with respect to its variable's domain. Hence, 'b'
        # will have an index of 0 in A, but an index of 1 in B. Conversely, the
        # first value for A and B may not necessarily represent the same thing.
        # Beaware of the difference when implementing your CSP solver.
        self.binaryPotentials = []

        self.wordsToClues = {}
        self.cluesToWords = {}
        self.wordFreqs = {} 
        self.answerMap = {}

    def add_variable(self, varName, domain):
        """
        Add a new variable to the CSP.
        """
        if varName in self.varNames:
            raise Exception("Variable name already exists: %s" % str(varName))
        var = len(self.varNames)
        self.numVars += 1
        self.varNames.append(varName)
        self.valNames.append(domain)
        self.unaryPotentials.append(None)
        self.binaryPotentials.append(dict())

    def get_neighbor_vars(self, var):
        """
        Returns a list of indices of variables which are neighbors of
        the variable of indec |var|.
        """
        return self.binaryPotentials[var].keys()

    def add_unary_potential(self, varName, potentialFunc):
        """
        Add a unary potential function for a variable. Its potential
        value across the domain will be *merged* with any previously added
        unary potential functions through elementwise multiplication.

        How to get unary potential value given a variable index |var| and
        value index |val|?
        => csp.unaryPotentials[var][val]
        """
        try:
            var = self.varNames.index(varName)
        except ValueError:
            if isinstance(varName, int):
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                print '!! Tip:                                                                       !!'
                print '!! It seems you trying to add a unary potential with variable index...        !!'
                print '!! When adding a potential, you should use variable names.                    !!'
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            raise

        potential = [float(potentialFunc(val)) for val in self.valNames[var]]
        if self.unaryPotentials[var] is not None:
            assert len(self.unaryPotentials[var]) == len(potential)
            self.unaryPotentials[var] = [self.unaryPotentials[var][i] * \
                potential[i] for i in range(len(potential))]
        else:
            self.unaryPotentials[var] = potential

    def add_binary_potential(self, varName1, varName2, potential_func):
        """
        Takes two variable names and a binary potential function
        |potentialFunc|, add to binaryPotentials. If the two variables already
        had binaryPotentials added earlier, they will be *merged* through element
        wise multiplication.

        How to get binary potential value given a variable index |var1| with value
        index |val1| and variable index |var2| with value index |val2|?
        => csp.binaryPotentials[var1][var2][val1][val2]
        """
        try:
            var1 = self.varNames.index(varName1)
            var2 = self.varNames.index(varName2)
        except ValueError:
            if isinstance(varName1, int) or isinstance(varName2, int):
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                print '!! Tip:                                                                       !!'
                print '!! It seems you trying to add a binary potential with variable indices...     !!'
                print '!! When adding a potential, you should use variable names.                    !!'
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            raise

        self.update_binary_potential_table(var1, var2,
            [[float(potential_func(val1, val2)) \
                for val2 in self.valNames[var2]] for val1 in self.valNames[var1]])
        self.update_binary_potential_table(var2, var1, \
            [[float(potential_func(val1, val2)) \
                for val1 in self.valNames[var1]] for val2 in self.valNames[var2]])

    def update_binary_potential_table(self, var1, var2, table):
        """
        Private method you can skip for 0c, might be useful for 1c though.
        Update the binary potential table for binaryPotentials[var1][var2].
        If it exists, element-wise multiplications will be performed to merge
        them together.
        """
        if var2 not in self.binaryPotentials[var1]:
            self.binaryPotentials[var1][var2] = table
        else:
            currentTable = self.binaryPotentials[var1][var2]
            assert len(table) == len(currentTable)
            assert len(table[0]) == len(currentTable[0])
            for i in range(len(table)):
                for j in range(len(table[i])):
                    currentTable[i][j] *= table[i][j]


# A backtracking algorithm that solves weighted CSP.
# Usage:
#   search = BacktrackingSearch()
#   search.solve(csp)
class BacktrackingSearch():

    def reset_results(self):
        """
        This function resets the statistics of the different aspects of the
        CSP solver. We will be using the values here for grading, so please
        do not make any modification to these variables.
        """
        # Keep track of the best assignment and weight found.
        self.optimalAssignment = {}
        self.optimalWeight = 0

        # Keep track of the number of optimal assignments and assignments. These
        # two values should be identical when the CSP is unweighted or only has binary
        # weights.
        self.numOptimalAssignments = 0
        self.numAssignments = 0

        # Keep track of the number of times backtrack() gets called.
        self.numOperations = 0

        # Keep track of the number of operations to get to the very first successful
        # assignment (doesn't have to be optimal).
        self.firstAssignmentNumOperations = 0

        # List of all solutions found.
        self.allAssignments = []

    def print_stats(self):
        """
        Prints a message summarizing the outcome of the solver.
        """
        if self.optimalAssignment:
            print "Found %d optimal assignments with weight %f in %d operations" % \
                (self.numOptimalAssignments, self.optimalWeight, self.numOperations)
            print "First assignment took %d operations" % self.firstAssignmentNumOperations
        else:
            print "No solution was found."

        print self.optimalAssignment

    def get_delta_weight(self, assignment, var, val):
        """
        Given a CSP, a partial assignment, and a proposed new value for a variable,
        return the change of weights after assigning the variable with the proposed
        value.

        @param assignment: A list of current assignment. len(assignment) should
            equal to self.csp.numVars. Unassigned variables have None values, while an
            assigned variable has the index of the value with respect to its
            domain. e.g. if the domain of the first variable is [5,6], and 6
            was assigned to it, then assignment[0] == 1.
        @param var: Index of an unassigned variable.
        @param val: Index of the proposed value with respect to |var|'s domain.

        @return w: Change in weights as a result of the proposed assignment. This
            will be used as a multiplier on the current weight.
        """
        assert assignment[var] is None
        w = 1.0
        if self.csp.unaryPotentials[var]:
            w *= self.csp.unaryPotentials[var][val]
            if w == 0: return w
        for var2, potential in self.csp.binaryPotentials[var].iteritems():
            if assignment[var2] == None: continue  # Not assigned yet
            w *= potential[val][assignment[var2]]
            if w == 0: return w
        return w

    def solve(self, csp, mcv = True, lcv = True, mac = True):
        """
        Solves the given weighted CSP using heuristics as specified in the
        parameter. Note that unlike a typical unweighted CSP where the search
        terminates when one solution is found, we want this function to find
        all possible assignments. The results are stored in the variables
        described in reset_result().

        @param csp: A weighted CSP.
        @param mcv: When enabled, Most Constrained Variable heuristics is used.
        @param lcv: When enabled, Least Constraining Value heuristics is used.
        @param mac: When enabled, AC-3 will be used after each assignment of an
            variable is made.
        """
        # CSP to be solved.
        self.csp = csp

        # Set the search heuristics requested asked.
        self.mcv = mcv
        self.lcv = lcv
        self.mac = mac

        # Reset solutions from previous search.
        self.reset_results()

        # The list of domains of every variable in the CSP. Note that we only
        # use the indices of the values. That is, if the domain of a variable
        # A is [2,3,5], then here, it will be stored as [0,1,2]. Original domain
        # name/value can be obtained from self.csp.valNames[A]
        self.domains = [list(range(len(domain))) for domain in self.csp.valNames]

        # Perform backtracking search.
        self.backtrack([None] * self.csp.numVars, 0, 1)

        # Print summary of solutions.
        self.print_stats()

    def printOptimalAssignment(self):
        print "\nSOLUTION FOUND:"
        for key in self.optimalAssignment:
            clue_index = key[0]
            clue_type = key[1]
            info_str = str(clue_index) + " " + str(clue_type) + ": " + self.optimalAssignment[key]
            print info_str
        print ""

    def backtrack(self, assignment, numAssigned, weight):
        """
        Perform the back-tracking algorithms to find all possible solutions to
        the CSP.

        @param assignment: A list of current assignment. len(assignment) should
            equal to self.csp.numVars. Unassigned variables have None values, while an
            assigned variable has the index of the value with respect to its
            domain. e.g. if the domain of the first variable is [5,6], and 6
            was assigned to it, then assignment[0] == 1.
        @param numAssigned: Number of currently assigned variables
        @param weight: The weight of the current partial assignment.
        """

        info_str = "assigned " + str(numAssigned) + "/" + str(self.csp.numVars) + " variables"
        print info_str 

        self.numOperations += 1
        assert weight > 0
        if numAssigned == self.csp.numVars:
            # A satisfiable solution have been found. Update the statistics.
            self.numAssignments += 1
            newAssignment = {}
            for var in range(self.csp.numVars):
                newAssignment[self.csp.varNames[var]] = self.csp.valNames[var][assignment[var]]
            self.allAssignments.append(newAssignment)

            if len(self.optimalAssignment) == 0 or weight >= self.optimalWeight:
                if weight == self.optimalWeight:
                    self.numOptimalAssignments += 1
                else:
                    self.numOptimalAssignments = 1
                self.optimalWeight = weight

                self.optimalAssignment = newAssignment
                if self.firstAssignmentNumOperations == 0:
                    self.firstAssignmentNumOperations = self.numOperations

            # Function I wrote to simplify printing assignments so they are more readable.
            self.printOptimalAssignment()
            return

        # Select the index of the next variable to be assigned.
        var = self.get_unassigned_variable(assignment)

        # Least constrained value (LCV) is not used in this assignment

        # DOMAIN ORDERING CODE:
        # ----------------------------------------------------------------
        # previously, was: ordered_values = self.domains[var]
        
        # clue name is: (clue index, clue type, clue). We want the
        # actual clue, so get the third value in the tuple.
        clue = self.csp.varNames[var][2]

        # Generate domain pairs which are (word, index) since the CSP only
        # keeps track of indexes.
        domain_pairs = []
        for val in self.domains[var]:
            domain_pairs.append((self.csp.valNames[var][val], val))

        # ordered_values is the domain indexes re-ordered using the sentiment analysis
        ordered_values = SolverUtil.orderValues(clue, domain_pairs, self.csp.cluesToWords, \
            self.csp.wordFreqs, self.csp.answerMap)

        # Continue the backtracking recursion using |var| and |ordered_values|.
        if not self.mac:
            # When arc consistency check is not enabled.
            for val in ordered_values:
                deltaWeight = self.get_delta_weight(assignment, var, val)
                if deltaWeight > 0:
                    assignment[var] = val
                    self.backtrack(assignment, numAssigned + 1, weight * deltaWeight)
                    assignment[var] = None
        else:
            # Arc consistency check is enabled.
            # Problem 1c: skeleton code for AC-3
            # You need to implement arc_consistency_check().
            for val in ordered_values:
                deltaWeight = self.get_delta_weight(assignment, var, val)
                if deltaWeight > 0:
                    assignment[var] = val
                    # create a deep copy of domains as we are going to look
                    # ahead and change domain values
                    localCopy = copy.deepcopy(self.domains)
                    # fix value for the selected variable so that hopefully we
                    # can eliminate values for other variables
                    self.domains[var] = [val]

                    # enforce arc consistency
                    self.arc_consistency_check(var)

                    self.backtrack(assignment, numAssigned + 1, weight * deltaWeight)
                    # restore the previous domains
                    self.domains = localCopy
                    assignment[var] = None

    def get_unassigned_variable(self, assignment):
        """
        Given a partial assignment, return the index of a currently unassigned
        variable.

        @param assignment: A list of current assignment. This is the same as
            what you've seen so far.

        @return var: Index of a currently unassigned variable.
        """

        if not self.mcv:
            # Select a variable without any heuristics.
            for var in xrange(len(assignment)):
                if assignment[var] is None: return var
        else:
            # Problem 1b
            # Heuristic: most constrained variable (MCV)
            # Select a variable with the least number of remaining domain values.
            # Hint: remember to use indices: for var_idx in range(len(assignment)): ...
            # Hint: given var_idx, self.domains[var_idx] gives you all the possible values
            fewest_assignments = float('inf')
            fewest_index = 0
            for var_idx in range (len(assignment)):
              if assignment[var_idx] is None:
                num_assignments = 0
                for val in self.domains[var_idx]:
                  deltaWeight = self.get_delta_weight(assignment, var_idx, val)
                  if deltaWeight != 0: num_assignments += 1
                if num_assignments < fewest_assignments:
                  fewest_assignments = num_assignments
                  fewest_index = var_idx
            return fewest_index

    def arc_consistency_check(self, var):
        """
        Perform the AC-3 algorithm. The goal is to reduce the size of the
        domain values for the unassigned variables based on arc consistency.

        @param var: The index of variable whose value has just been set.
        """
        # Problem 1c
        # Hint: How to get indices of variables neighboring variable at index |var|?
        # => for var2 in self.csp.get_neighbor_vars(var):
        #       # use var2
        #
        # Hint: How to check if two values are inconsistent?
        # For unary potentials (var1 is the index, val1 is the value index):
        #   => self.csp.unaryPotentials[var1][val1] == 0
        #
        # For binary potentials (var1 and var2 are indices, val1 and val2 are value indices)::
        #   => self.csp.binaryPotentials[var1][var2][val1][val2] == 0
        #   (self.csp.binaryPotentials[var1][var2] returns a nested dict of all assignments)
       
        queue = list()
        queue.append(var)

        while (len(queue) != 0):
          # Pop Xj from queue
          var1 = queue.pop()
          
          # Iterate over all neighbors Xk
          for var2 in self.csp.get_neighbor_vars(var1):
            if var2 != var1:

              # Make a copy of the domain, and iterate over this copy, while
              # removing elements from the actual domain
              var2_domain = self.domains[var2]
              var2_domain_copy = copy.deepcopy(var2_domain)
              domain_changed = False
              
              # Unary Potential Check:
              # Iterate over all values in the domain of Xk. If any are
              # inconsistent, remove them from the domain
              for val2 in var2_domain_copy:
                unaryPotential = self.csp.unaryPotentials[var2]
                if unaryPotential is not None:
                  if (unaryPotential[val2] == 0):
                    if val2 in var2_domain:
                      var2_domain.remove(val2)
                      domain_changed = True

              # Binary Potential Check:
              # Iterate over all values in the domain of Xk
              for val2 in var2_domain_copy:
                # If every single value in the domain of Xj is inconsistent
                # with val2, then remove val2 from the domain of Xk. 
                remove_value = True 
                for val1 in self.domains[var1]:
                  binaryPotentials = self.csp.binaryPotentials[var1][var2]
                  if binaryPotentials is not None:
                    if (binaryPotentials[val1][val2] != 0):
                      remove_value = False
                if remove_value:
                  if val2 in var2_domain:
                    var2_domain.remove(val2)
                    domain_changed = True

              # Finally, if the domain of var2 has changed, then add 
              # it to the queue.
              if domain_changed:
                queue.append(var2)





