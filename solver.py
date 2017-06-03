### Imports
from __future__ import print_function
import random

### Solver class
class Board:
    def __init__(self):
        #board size
        self.board = self.create_board()

    def create_board(self):
        self.grid = []

        # let's prefill all squares with a zero
        # after this, we will stop appending
        # due to mutability of list data structure
        for i in range(0,81):
            self.grid.append(0)

        # #temporary
        # for i in range(0,81):
        #     grid[i] = random.randint(0,9)

        #let's try to fill the first row

        #digits = range(1,10)

        for i in range(0,9):
            digit = random.randint(1,9)
            print(self.check_row(i,digit))
            while self.check_row(i,digit) == False:
                digit = random.randint(1,9)
            self.grid[i] = digit
            #check if col contains temp
            #check if block contains temp
            #if none of them contain temp:
                #set grid[i] to temp

    def check_row(self, i, digit):
        row = i/9 + 1

        for col in range(1,10):
            if self.get_square(row,col) == digit:
                return False

        return True

    def check_col(self, i, digit):
        col = i%9 + 1

        for row in range(1,10):
            if self.get_square(row,col) == digit:
                return False

        return True

    def get_square(self, row, col):
        #ensure row and col are appropriate
        #validate_value(row, col)

        #return the value in the grid
        idx = (row - 1) * 9 + (col - 1)
        return self.grid[idx]

    def set_square(self, row, col, val):
        #ensure row and col are appropriate
        #validate_value(row, col)

        #ensure value is appropriate
        if not(val > 0 and val < 10):
            #error
            print('inappropriate value')
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
                #print('_____________________')
            print(grid[i],end=' ')

        print('')
        print('---------------------')

    def validate_value(val):
        if not(val > 0 and val < 10):
            return False
        else:
            return True
