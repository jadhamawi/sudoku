### Imports
from __future__ import print_function
import random

### Solver class
class Board:
    def __init__(self):
        #board size
        self.board = self.create_board()
        self.print_board()

    def create_board(self):
        self.grid = []

        # let's prefill all squares with a zero
        # after this, we will stop appending
        # due to mutability of list data structure
        for i in range(0,81):
            self.grid.append(0)

        #let's try a backtracking approach
        idx = 0

        while 0 in self.grid:
            if self.grid[idx] < 9:
                digit = self.grid[idx] + 1
            else:
                self.grid[idx] = 0
                idx = idx-1
                digit = 0
            while digit!=0 and not(self.check_sudoku_conditions(idx,digit)):
                digit = digit + 1
                if digit > 9:
                    digit = 0
                    self.grid[idx] = 0
                    idx = idx-1
                    break

            if digit!=0:
                self.grid[idx] = digit
                idx = idx + 1

    def check_sudoku_conditions(self, i, digit):
        a = self.check_row(i, digit)
        b = self.check_col(i, digit)
        c = self.check_block(i, digit)
        if a and b and c:
            #print('meets sudoku conditions')
            return True
        else:
            #print('uh-oh')
            return False

    def check_row(self, i, digit):
    #returns True if the digit is not already contained in the row
        row = i/9 + 1

        for col in range(1,10):
            if self.get_square(row,col) == digit:
                return False

        return True

    def check_col(self, i, digit):
    #returns True if the digit is not already contained in the column
        col = i%9 + 1

        for row in range(1,10):
            if self.get_square(row,col) == digit:
                return False

        return True

    def check_block(self,i, digit):
    #returns True if the digit is not already contained in the block
        #an x value of 0 denotes left, 1 is middle, 2 is right
        x = i%27%9/3
        #y value of 0 represents top, 1 is middle, 2 is bottom
        y = i/27

        for j in range(0,81):
            if j%27%9/3 == x and j/27 == y:
            #i.e. if j is in the same block as i
                if self.grid[j] == digit:
                    return False

        return True

    def get_square(self, row, col):
        #ensure row and col are appropriate
        if self.validate_value(row) == False:
            print('get - invalid row')
        if self.validate_value(col) == False:
            print('get - invalid column')

        #return the value in the grid
        idx = (row - 1) * 9 + (col - 1)
        return self.grid[idx]

    def set_square(self, row, col, val):
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
            self.grid[idx] = val

    def print_board(self):
        grid = self.grid

        print('---------------------')

        for i in range(0,81):
            if i%3 == 0 and i!=0 and i%9!=0:
                print('|',end=' ')
            if (i%9 == 0 and i!=0) and i%27!=0:
                print('')
            if i%27 == 0 and i!=0:
                print('')
                print('---------------------')
            print(grid[i],end=' ')

        print('')
        print('---------------------')

    def validate_value(self, val):
        if not(val > 0 and val < 10):
            return False
        else:
            return True
