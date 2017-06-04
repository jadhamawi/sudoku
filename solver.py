### Imports
from __future__ import print_function
import random

### Solver class
class Board:
    def __init__(self):
        #future: adjustable board size
        self.board = self.create_board()
        #self.print_board(self.grid)

    def create_board(self):

        #this grid contains the solution, not the puzzle
        self.soln = []

        # let's prefill all squares with a zero
        # after this, we will stop appending
        # due to mutability of list data structure
        for i in range(0,81):
            self.soln.append(0)

        ### let's try a backtracking algorithm

        idx = 0

        # let's seed the first row randomly
        # there are 9 digits to permute, therefore 9! permutations
        # almost 360k permutations

        for j in range(0,9):
            seed = random.randint(1,9)
            while not(self.check_row(self.soln, j, seed)):
                seed = random.randint(1,9)
            self.soln[j] = seed

        # now must idx must refer to start of second row

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

        print('the solution to the board is: ')
        self.print_board(self.soln)

        self.puzzle = self.soln

        ### now let's remove values from squares at random
        k = 0

        while k < 20:   # arbitrary
            print(k)
            r = random.randint(1,9)
            c = random.randint(1,9)

            self.set_square(self.puzzle, r, c, 0)
            self.set_square(self.puzzle, c, r, 0)
            self.print_board(self.puzzle)
            if self.solve_board(self.puzzle):
                print('keeping the zero')
                self.print_board(self.puzzle)
                k = k + 1
            else:
                # revert the removal
                self.set_square(self.puzzle, r, c, get_square(self.soln, r, c))
                self.set_square(self.puzzle, c, r, get_square(self.soln, c, r))

        print('the puzzle looks like: ')
        self.print_board(self.puzzle)


    def solve_board(self, grid):
    # input: puzzle
    # output: all empty squares filled in with appropriate value
        
        #index with which we traverse through grid
        idx = 0

        while 0 in grid: # grid contains empty squares
            if grid[idx] == 0: # only fill in empty squares
                digit = grid[idx] + 1
                while digit!=0 and not(self.check_sudoku_conditions(grid, idx,digit)):
                    digit = digit + 1
                    if digit > 9:
                        print('no solution')
                        return False

                if digit!=0:
                    grid[idx] = digit

            idx = idx + 1

        # print('solved board:')
        # self.print_board(grid)

        return True

    def check_sudoku_conditions(self, grid, i, digit):
    # returns True if the digit is not already contained in the row, col, or block
        a = self.check_row(grid, i, digit)
        b = self.check_col(grid, i, digit)
        c = self.check_block(grid, i, digit)
        if a and b and c:
            #print('meets sudoku conditions')
            return True
        else:
            #print('uh-oh')
            return False

    def check_row(self, grid, i, digit):
    #returns True if the digit is not already contained in the row
        row = i/9 + 1

        for col in range(1,10):
            if self.get_square(grid, row,col) == digit:
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
