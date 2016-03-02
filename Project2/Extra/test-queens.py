import Testing
import BinaryCSP
import sys
import itertools


def build_nqueens(n):
	buf = []

	for i in range (1, n + 1):
		domain = " ".join([str(_) for _ in range(1, n + 1)])
		line = "%(i)s %(domain)s" % locals()
		buf.append(line)
	buf.append("0")

	for i, j in itertools.combinations(range(1, n + 1), 2):
		line = "QueenDoesNotAttack %(i)s %(j)s" % locals()
		buf.append(line)
	buf.append("0")

	return buf

def printBoard(sol, n):
	if sol is not None:
		for i in range(1, n + 1):
			sys.stdout.write(" _")
		sys.stdout.write("\n")

		for i in range(1, n + 1):
			sys.stdout.write("|")
			for j in range(1, n + 1):
				if sol[str(i)] is str(j):
					sys.stdout.write('Q')
				else:
					sys.stdout.write("_")
				sys.stdout.write("|")
			sys.stdout.write('\n')

def nqueen(n):
	print "Attempting solution for %(n)s queens" % locals()

	filename = "temp/%(n)s-queens.csps" % locals()

	testcase = build_nqueens(n)
	with open(filename, 'w') as f:
		f.write('\n'.join(testcase))
	# print "Constructed testcase %(testcase)s" % locals()

	problem = Testing.csp_parse(testcase)
	# print "Parsed problem %(problem)s" % locals()
	sol = BinaryCSP.solve(problem)
	print "Solution attempted %(sol)s" % locals()
	printBoard(sol, n)

	print "\n"

nqueen(3)
nqueen(4)
nqueen(5)
nqueen(6)
nqueen(7)
nqueen(8)
nqueen(9)