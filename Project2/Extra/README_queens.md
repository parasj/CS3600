# n-queens

## How to run
Run `python test-queens.py`.

This will step through each n-queens problem and generate a test case (stored in the temp directory) and then attempt to solve it. For interpreting the result, I print out a diagram of the chessboard.

The output I get is in nqueens.out

## Representation
- Each queen is in a particular row (queen 1 in row 1, etc.)
- Values represent the column

## Constraints
Each queen must not attack each other queen. This is implemented in the constraint QueenDoesNotAttack.

Attack is determined by:
1. Each queen must have not be on the same column
2. Each queen must have a value plus assignment that is different
	e.g. queen 1 on col 2, queen 2 on col 1, we have queen 1 with value 3 and queen 2 with value 3 so they attack each other
3. Each queen must have a value minus assignment that is different
	e.g. queen 1 on col 2, queen 2 on col 1, we have queen 1 with value 3 and queen 2 with value 3 so they attack each other

## Works cited
Tutorial: https://developers.google.com/optimization/puzzles/queens#constraints