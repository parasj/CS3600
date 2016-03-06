n-queens
========

n-queens is a problem of placing n queens on an n x n chessboard such that no two queens attack each other. See contraints and works cited for more information on the problem.


How to run
----------
- From the root of Project2, run `python autograder.py -t ExtraCredit/6queens.test`
- This will run the test for the extra credit that is 6-queens.
- For your convenience, a visualization of the chessboard is printed out to the console as well so you can visually verify the solution.


Representation
--------------
- Each queen is in a particular row (queen 1 in row 1, etc.)
- Values represent the column
- 6 was chosen for n as it has only 4 solutions which means I can specify them all by hand in the solution file to check if the assignment is valid.


Constraints
-----------
Each queen must not attack each other queen. This is implemented in the constraint QueenDoesNotAttack.

Attack is determined by:

1. Each queen must have not be on the same column
2. Each queen must have a value plus assignment that is different (e.g. queen 1 on col 2, queen 2 on col 1, we have queen 1 with value 3 and queen 2 with value 3 so they attack each other)
3. Each queen must have a value minus assignment that is different (e.g. queen 1 on col 2, queen 2 on col 1, we have queen 1 with value 3 and queen 2 with value 3 so they attack each other)

Works cited
-----------
Tutorial: https://developers.google.com/optimization/puzzles/queens#constraints