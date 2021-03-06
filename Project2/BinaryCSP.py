from collections import deque

"""
	Base class for unary constraints
	Implement isSatisfied in subclass to use
"""
class UnaryConstraint:
	def __init__(self, var):
		self.var = var

	def isSatisfied(self, value):
		util.raiseNotDefined()

	def affects(self, var):
		return var == self.var


"""	
	Implementation of UnaryConstraint
	Satisfied if value does not match passed in paramater
"""
class BadValueConstraint(UnaryConstraint):
	def __init__(self, var, badValue):
		self.var = var
		self.badValue = badValue

	def isSatisfied(self, value):
		return not value == self.badValue

	def __repr__(self):
		return 'BadValueConstraint (%s) {badValue: %s}' % (str(self.var), str(self.badValue))


"""	
	Implementation of UnaryConstraint
	Satisfied if value matches passed in paramater
"""
class GoodValueConstraint(UnaryConstraint):
	def __init__(self, var, goodValue):
		self.var = var
		self.goodValue = goodValue

	def isSatisfied(self, value):
		return value == self.goodValue

	def __repr__(self):
		return 'GoodValueConstraint (%s) {goodValue: %s}' % (str(self.var), str(self.goodValue))


"""
	Base class for binary constraints
	Implement isSatisfied in subclass to use
"""
class BinaryConstraint:
	def __init__(self, var1, var2):
		self.var1 = var1
		self.var2 = var2

	def isSatisfied(self, value1, value2):
		util.raiseNotDefined()

	def affects(self, var):
		return var == self.var1 or var == self.var2

	def otherVariable(self, var):
		if var == self.var1:
			return self.var2
		return self.var1


"""
	Implementation of BinaryConstraint
	Satisfied if both values assigned are different
"""
class NotEqualConstraint(BinaryConstraint):
	def isSatisfied(self, value1, value2):
		if value1 == value2:
			return False
		return True

	def __repr__(self):
		return 'NotEqualConstraint (%s, %s)' % (str(self.var1), str(self.var2))

class ConstraintSatisfactionProblem:
	"""
	Structure of a constraint satisfaction problem.
	Variables and domains should be lists of equal length that have the same order.
	varDomains is a dictionary mapping variables to possible domains.

	Args:
		variables (list<string>): a list of variable names
		domains (list<set<value>>): a list of sets of domains for each variable
		binaryConstraints (list<BinaryConstraint>): a list of binary constraints to satisfy
		unaryConstraints (list<BinaryConstraint>): a list of unary constraints to satisfy
	"""
	def __init__(self, variables, domains, binaryConstraints = [], unaryConstraints = []):
		self.varDomains = {}
		for i in xrange(len(variables)):
			self.varDomains[variables[i]] = domains[i]
		self.binaryConstraints = binaryConstraints
		self.unaryConstraints = unaryConstraints

	def __repr__(self):
		return '---Variable Domains\n%s---Binary Constraints\n%s---Unary Constraints\n%s' % ( \
			''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
			''.join([str(e) + '\n' for e in self.binaryConstraints]), \
			''.join([str(e) + '\n' for e in self.binaryConstraints]))


class Assignment:
	"""
	Representation of a partial assignment.
	Has the same varDomains dictionary stucture as ConstraintSatisfactionProblem.
	Keeps a second dictionary from variables to assigned values, with None being no assignment.

	Args:
		csp (ConstraintSatisfactionProblem): the problem definition for this assignment
	"""
	def __init__(self, csp):
		self.varDomains = {}
		for var in csp.varDomains:
			self.varDomains[var] = set(csp.varDomains[var])
		self.assignedValues = { var: None for var in self.varDomains }

	"""
	Determines whether this variable has been assigned.

	Args:
		var (string): the variable to be checked if assigned
	Returns:
		boolean
		True if var is assigned, False otherwise
	"""
	def isAssigned(self, var):
		return self.assignedValues[var] != None

	"""
	Determines whether this problem has all variables assigned.

	Returns:
		boolean
		True if assignment is complete, False otherwise
	"""
	def isComplete(self):
		for var in self.assignedValues:
			if not self.isAssigned(var):
				return False
		return True

	"""
	Gets the solution in the form of a dictionary.

	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if not complete.
	"""
	def extractSolution(self):
		if not self.isComplete():
			return None
		return self.assignedValues

	def __repr__(self):
		return '---Variable Domains\n%s---Assigned Values\n%s' % ( \
			''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
			''.join([str(e) + ':' + str(self.assignedValues[e]) + '\n' for e in self.assignedValues]))



####################################################################################################


"""
	Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
	Do not assign value to var. Only check if this value would be consistent or not.
	If the other variable for a constraint is not assigned, then the new value is consistent with the constraint.

	Args:
		assignment (Assignment): the partial assignment
		csp (ConstraintSatisfactionProblem): the problem definition
		var (string): the variable that would be assigned
		value (value): the value that would be assigned to the variable
	Returns:
		boolean
		True if the value would be consistent with all currently assigned values, False otherwise
"""
def consistent(assignment, csp, var, value):
	"""Question 1"""
	us = [not uc.affects(var)
			or uc.isSatisfied(value)
				for uc in csp.unaryConstraints]
	bs = [not bc.affects(var)
			or not assignment.isAssigned(bc.otherVariable(var))
			or bc.isSatisfied(value, assignment.assignedValues[bc.otherVariable(var)])
				for bc in csp.binaryConstraints]
	return all(us) and all(bs)


"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.
	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.

	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic

	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
	Returns:
		Assignment
		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod):
	# if assignment.isComplete(): return assignment
	# var = selectVariableMethod(assignment, csp)
	# for value in orderValuesMethod(assignment, csp, var):
	# 	undo = assignment.assignedValues[var]
	# 	if consistent(assignment, csp, var, value):
	# 		assignment.assignedValues[var] = value
	# 		result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
	# 		if result:
	# 			return result
	# 	assignment.assignedValues[var] = undo
	# return None
	return recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, noInferences)


"""
	Uses unary constraints to eliminate values from an assignment.

	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
	Returns:
		Assignment
		An assignment with domains restricted by unary constraints. None if no solution exists.
"""
def eliminateUnaryConstraints(assignment, csp):
	domains = assignment.varDomains
	for var in domains:
		for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
			for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
				domains[var].remove(value)
				if len(domains[var]) == 0:
					# Failure due to invalid assignment
					return None
	return assignment


"""
	Trivial method for choosing the next variable to assign.
	Uses no heuristics.
"""
def chooseFirstVariable(assignment, csp):
	for var in csp.varDomains:
		if not assignment.isAssigned(var):
			return var


"""
	Selects the next variable to try to give a value to in an assignment.
	Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		the next variable to assign
"""
def minimumRemainingValuesHeuristic(assignment, csp):
	nextVar = None
	domains = assignment.varDomains

	def constraintCounter(assignment, csp, var):
		return len([const for const in csp.binaryConstraints
						if const.affects(var)
							and not assignment.isAssigned(const.otherVariable(var))])

	"""Question 2"""
	unassignedVars = [var for var in domains if not assignment.isAssigned(var)]
	lengths = [(len(domains[var]), var) for var in unassignedVars]
	minlengths = [length[1] for length in lengths if length[0] is min(lengths)[0]]

	if len(minlengths) is 0:
		nextVar = None
	elif len(minlengths) is 1 or len(csp.binaryConstraints) is 0:
		nextVar = minlengths[0]
	else:
		nextVar = max([(constraintCounter(assignment, csp, var), var) for var in minlengths])[1]

	return nextVar


"""
	Trivial method for ordering values to assign.
	Uses no heuristics.
"""
def orderValues(assignment, csp, var):
	return list(assignment.varDomains[var])


"""
	Creates an ordered list of the remaining values left for a given variable.
	Values should be attempted in the order returned.
	The least constraining value should be at the front of the list.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable to be assigned the values
	Returns:
		list<values>
		a list of the possible values ordered by the least constraining value heuristic
"""
def leastConstrainingValuesHeuristic(assignment, csp, var):
	deps = [const.otherVariable(var) for const in csp.binaryConstraints if const.affects(var)]
	return sorted(list(assignment.varDomains[var]),
		key=lambda val: len([dep for dep in deps if val in assignment.varDomains[dep]]))


"""
	Trivial method for making no inferences.
"""
def noInferences(assignment, csp, var, value):
	return set([])

def undoInferences(assignment, inferences):
	for infvar, infval in inferences:
		assignment.varDomains[infvar].add(infval)

"""
	Implements the forward checking algorithm.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def forwardChecking(assignment, csp, var, value):
	inferences = set([])
	domains = assignment.varDomains

	deps = [(const.otherVariable(var), const) for const in csp.binaryConstraints if const.affects(var) and assignment.assignedValues[const.otherVariable(var)] is None]
	inferences = set([(other, otherval) for other, const in deps for otherval in domains[other] if not const.isSatisfied(value, otherval)])
	
	for infvar, infval in inferences:
		domains[infvar].remove(infval)

	consistent = [domains[other] and len(domains[other]) > 0 for other, const in deps]
	if not all(consistent):
		undoInferences(assignment, inferences)
		return None

	return inferences

"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.

	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.


	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
	inferenceMethod: noInferences, maintainArcConsistency, forwardChecking


	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
		inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>): a function to specify what type of inferences to use
				Can be forwardChecking or maintainArcConsistency
	Returns:
		Assignment

		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
	if assignment.isComplete(): return assignment
	var = selectVariableMethod(assignment, csp)
	for value in orderValuesMethod(assignment, csp, var):
		undo = assignment.assignedValues.copy()
		if consistent(assignment, csp, var, value):
			assignment.assignedValues[var] = value
			inferences = inferenceMethod(assignment, csp, var, value)
			if inferences is not None:
				result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
				if result:
					return result
				else:
					assignment.assignedValues[var] = None
					undoInferences(assignment, inferences)
		assignment.assignedValues = undo
	return None



"""
	Helper funciton to maintainArcConsistency and AC3.
	Remove values from var2 domain if constraint cannot be satisfied.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var1 (string): the variable with consistent values
		var2 (string): the variable that should have inconsistent values removed
		constraint (BinaryConstraint): the constraint connecting var1 and var2
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""

def revise(assignment, csp, var1, var2, constraint):
	inferences = set([])

	i1 = [val for val in assignment.varDomains[var1] if not any([val2 for val2 in assignment.varDomains[var2] if constraint.isSatisfied(val2, val)])]
	assignment.varDomains[var1] = assignment.varDomains[var1].difference(i1)
	inferences = inferences.union([(var1, val) for val in i1])

	i2 = [val for val in assignment.varDomains[var2] if not any([val1 for val1 in assignment.varDomains[var1] if constraint.isSatisfied(val1, val)])]
	assignment.varDomains[var2] = assignment.varDomains[var2].difference(i2)
	inferences = inferences.union([(var2, val) for val in i2])
	
	if len(assignment.varDomains[var2]) < 1:
		undoInferences(assignment, inferences)
		return None

	return inferences

"""
	Implements the maintaining arc consistency algorithm.
	Inferences take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, and
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def maintainArcConsistency(assignment, csp, var, value):
	inferences = set([])
	domains = assignment.varDomains
	values = assignment.assignedValues

	q = deque([const for const in csp.binaryConstraints if const.affects(var)])
	while len(q) > 0:
		const = q.popleft()
		var1 = const.var1
		var2 = const.var2

		revisions = revise(assignment, csp, var1, var2, const)
		if revisions is None:
			undoInferences(assignment, inferences)
			return None
		elif len(revisions) > 0:
			inferences = inferences.union(revisions)
			q.extend([c for c in csp.binaryConstraints if c is not const and ((c.affects(var2) and not c.affects(var1)) or (c.affects(var1) and not c.affects(var2)))])

	return inferences

"""
	AC3 algorithm for constraint propogation. Used as a preprocessing step to reduce the problem
	before running recursive backtracking.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		Assignment
		the updated assignment after inferences are made or None if an inconsistent assignment
"""
def AC3(assignment, csp):
	inferences = set([])
	domains = assignment.varDomains
	values = assignment.assignedValues

	q = deque(csp.binaryConstraints)
	while len(q) > 0:
		const = q.popleft()
		var1 = const.var1
		var2 = const.var2

		revisions = revise(assignment, csp, var1, var2, const)
		if revisions is None:
			return None
		elif len(revisions) > 0:
			q.extend([c for c in csp.binaryConstraints if c is not const and  ((c.affects(var2) and not c.affects(var1)) or (c.affects(var1) and not c.affects(var2)))])

	return assignment


"""
	Solves a binary constraint satisfaction problem.

	Args:
		csp (ConstraintSatisfactionProblem): a CSP to be solved
		orderValuesMethod (function): a function to decide the next value to try
		selectVariableMethod (function): a function to decide which variable to assign next
		inferenceMethod (function): a function to specify what type of inferences to use
		useAC3 (boolean): specifies whether to use the AC3 preprocessing step or not
	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if no solution exists.
"""
def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic, selectVariableMethod=minimumRemainingValuesHeuristic, inferenceMethod=None, useAC3=True):
	assignment = Assignment(csp)

	assignment = eliminateUnaryConstraints(assignment, csp)
	if assignment == None:
		return assignment

	if useAC3:
		assignment = AC3(assignment, csp)
		if assignment == None:
			return assignment
	if inferenceMethod is None or inferenceMethod==noInferences:
		assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
	else:
		assignment = recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
	if assignment == None:
		return assignment

	return assignment.extractSolution()

class QueenDoesNotAttack(BinaryConstraint):
	def isSatisfied(self, value1, value2):
		def plusMinusDifferent(a, a1, b, b1):
			return ((a + a1 != b + b1) and (a - a1 != b - b1)) or ((a + b1 != b + a1) and (a - b1 != b - a1))

		if value1 is not value2 and plusMinusDifferent(int(self.var1), int(value1), int(self.var2), int(value2)):
			return True
		return False

	def __repr__(self):
		return 'QueenDoesNotAttack (%s, %s)' % (str(self.var1), str(self.var2))