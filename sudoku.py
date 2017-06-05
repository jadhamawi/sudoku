### Imports
from __future__ import print_function
import random

### Solver class
class Board:
    def __init__(self):
        # future: adjustable board size
        self.board = self.create_board()

    def create_board(self):

        # the grids are stored in lists of length 81
        # each element in the list represents the value (b/w 1 and 9) at the square
        # 0 index is top left, 8 is top right, 72 is bottom left, 80 is bottom right
        self.soln = []
        self.puzzle = []

        # let's prefill all squares with a zero
        # after this, we will stop appending
        # due to mutability of list data structure
        for i in range(0,81):
            self.soln.append(0)

        ### backtracking algorithm

        # idx will be our iterator through the eventual solution grid
        idx = 0

        # let's seed the first row randomly
        # there are 9 digits to permute, therefore 9! permutations
        # almost 360k permutations

        # seeding first row with unique values between 1 and 9
        for j in range(0,9):
            seed = random.randint(1,9)
            while not(self.check_row(self.soln, j, seed)):
                seed = random.randint(1,9)
            self.soln[j] = seed

        # to fill in the rest of the solution grid, idx must start at second row

        idx = 9

        while 0 in self.soln:
            if self.soln[idx] < 9:
                digit = self.soln[idx] + 1
            else:
                self.soln[idx] = 0
                idx = idx-1
                digit = 0
            while digit!=0 and not(self.check_sudoku_conditions(self.soln, idx,digit)):
                digit = digit + 1
                if digit > 9:
                    digit = 0
                    self.soln[idx] = 0
                    idx = idx-1
                    break

            if digit!=0:
                self.soln[idx] = digit
                idx = idx + 1

        ### end back tracking algorithm

        print('the solution to the Sudoku puzzle is: ')
        self.print_board(self.soln)

        # make a copy of the soln grid
        self.puzzle = self.soln[:]

        ### now let's remove values from puzzle grid at random
        # k is a counter variable, is the number of pairs we are removing
        k = 0
        maxPairs = 15 # arbitrary - related to difficulty level of puzzle

        # loops ensures that if we get stuck in an infinite loop, we'll be able to break
        loops = 0
        maxLoops = 1000

        while k < maxPairs:

            loops = loops + 1
            if loops > maxLoops:
                print('maxLoops exceeded')
                break

            # choose random row and column
            r = random.randint(1,9)
            c = random.randint(1,9)

            # ensure that the chosen square has not already had its value removed
            while self.get_square(self.puzzle, r, c) == 0:
                r = random.randint(1,9)
                c = random.randint(1,9)

            # set the value at the random location to zero
            # also set the value of the opposite square to zero for symmetry
            self.set_square(self.puzzle, r, c, 0)
            self.set_square(self.puzzle, c, r, 0)

            #if board has puzzle solution is unique
            #if self.unique_soln(self.puzzle):
            if self.solve_board(self.puzzle[:]) == self.soln:
                k = k + 1
            else:
                # revert the removal
                self.set_square(self.puzzle, r, c, self.get_square(self.soln, r, c))
                self.set_square(self.puzzle, c, r, self.get_square(self.soln, c, r))

        print('the Sudoku puzzle is: ')
        self.print_board(self.puzzle)

    def solve_board(self, grid):
        # input: puzzle
        # output: solved board
        # the algorithm tries to solve the puzzle by first looking for solutions
        #   that do not use the same numbers as in the original solution
        # if the only solution the solver can find is self.soln, then self.soln
        #   is unique

        digit = 0
        idx = 0

        while 0 in grid:
            if grid[idx] == 0:
                digit = grid[idx] + 1
                while digit!=0 and not(self.check_sudoku_conditions(grid, idx, digit)):
                    digit = digit + 1
                    if digit == self.soln[idx]:
                        digit = digit + 1
                    if digit > 9:
                        digit = 0
                        grid[idx] = self.soln[idx]
                        idx = idx - 1
                        break
                    #print(idx)
            else:
                idx = idx+1

            if digit != 0:
                grid[idx] = digit
                idx = idx + 1
                digit = 0

        #print('solve_board yields: ')
        #self.print_board(grid)

        return grid

    def unique_soln(self, grid):
    ### this method is not used
    # input: puzzle
    # output: True if the only solution to grid is self.soln
    # output: False if another solution to grid exists

        # keeps track of the uniqueness of the value at each square
        uniques = []

        # assume that values are uniques
        # if non-unique value found, then set element to False
        for i in range(0,81):
            uniques.append(True)

        # index with which we traverse through grid
        idx = 0

        # traverse through entire grid
        while idx < 81:
            if grid[idx] == 0: # only concerned with empty squares
                digit = grid[idx] + 1
                while digit!=0 and not(self.check_sudoku_conditions(grid, idx,digit)):
                    digit = digit + 1
                    if digit == self.soln[idx]: # not interested to see if the original soln works
                        digit = digit + 1
                    if digit > 9:
                        #print('unique value at square')
                        uniques[idx] = True
                        break
                    # new solution found
                    #print('new soln found')
                    uniques[idx] = False

            idx = idx + 1

        if False in uniques:
            return False
        else:
            return True

    def check_sudoku_conditions(self, grid, i, digit):
    # returns True if the digit is not already contained in the row, col, or block
        row_condition = self.check_row(grid, i, digit)
        col_condition = self.check_col(grid, i, digit)
        block_condition = self.check_block(grid, i, digit)
        if row_condition and col_condition and block_condition:
            return True
        else:
            return False

    def check_row(self, grid, i, digit):
    #returns True if the digit is not already contained in the row
        row = i/9 + 1

        for col in range(1,10):
            if self.get_square(grid, row, col) == digit:
                return False

        return True

    def check_col(self, grid, i, digit):
    #returns True if the digit is not already contained in the column
        col = i%9 + 1

        for row in range(1,10):
            if self.get_square(grid, row,col) == digit:
                return False

        return True

    def check_block(self, grid, i, digit):
    #returns True if the digit is not already contained in the block
        #an x value of 0 denotes left, 1 is middle, 2 is right
        x = i%27%9/3
        #y value of 0 represents top, 1 is middle, 2 is bottom
        y = i/27

        for j in range(0,81):
            if j%27%9/3 == x and j/27 == y:
            #i.e. if j is in the same block as i
                if grid[j] == digit:
                    return False

        return True

    def get_square(self, grid, row, col):
        #ensure row and col are appropriate
        if self.validate_value(row) == False:
            print('get - invalid row')
        if self.validate_value(col) == False:
            print('get - invalid column')

        #return the value in the grid
        idx = (row - 1) * 9 + (col - 1)
        return grid[idx]

    def set_square(self, grid, row, col, val):
        #ensure row and col are appropriate
        if self.validate_value(row) == False:
            print('set - invalid row')
        if self.validate_value(col) == False:
            print('set - invalid column')

        #ensure value is appropriate
        if self.validate_value(val) == False:
            print('invalid value')
        else:
            idx = (row - 1) * 9 + (col - 1)
            grid[idx] = val

    def print_board(self, grid):

        print('---------------------')

        for i in range(0,81):
            if i%3 == 0 and i!=0 and i%9!=0:
                print('|',end=' ')
            if (i%9 == 0 and i!=0) and i%27!=0:
                print('')
            if i%27 == 0 and i!=0:
                print('')
                print('---------------------')
            if grid[i] != 0:
                print(grid[i],end=' ')
            else:
                print(' ',end=' ')

        print('')
        print('---------------------')

    def validate_value(self, val):
        if not(val >= 0 and val <= 9):
            return False
        else:
            return True
