"""
Ulta socho maine sidha socha to garbar bohot hua solution apna dimag aur tarika ulta karne par hi aya
"""

import numpy as np
import random


def generator():
    bo = np.array([0 for _ in range(81)])
    bo = bo.reshape((9, 9))
    numbers = random.randrange(16, 26)
    for i in range(numbers):
        pos_x, pos_y = random.randrange(0, 9), random.randrange(0, 9)
        rand_num = random.randrange(1, 10)
        check = validity(bo, rand_num, (pos_x, pos_y))
        if check is True:
            bo[pos_x, pos_y] = rand_num
    return bo


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, column = find

    for i in range(1, 10):
        if validity(bo, i, (row, column)):
            bo[row][column] = i
            if solve(bo):  # It runs the def again and a new row column is made actually which if not satisfied
                return True
            else:  # becomes next here i.e. backtracking
                bo[row][column] = bo[row][column]+1
    return False


def validity(bo, num, pos):
    # checking rows
    check_row = True
    if num in bo[pos[0]]:
            check_row = False
    # checking columns
    check_column = True
    for i in range(len(bo)):
        if bo[i][pos[1]] == num:
            check_column = False
    # checking boxes
    box_y = pos[0] // 3
    box_x = pos[1] // 3
    check_box = True
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num:
                check_box = False
    if check_row is False or check_column is False or check_box is False:
        check = False
    else:
        check = True
    return check


def print_board(bo):
    row = 0
    for i in range(len(bo)):
        if i == 0:
            print('-' * 25)
        for j in range(len(bo[0])):
            if j == 0:
                print('|', end=' ')
            print(bo[i][j], end=' ')
            if (j + 1) % 3 == 0 and j != 0:
                print('|', end=' ')
        print()
        row += 1
        if row % 3 == 0:
            print('-' * 25)


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo)):
            if bo[i][j] == 0:
                return i, j
    return None

if __name__ == '__main__':

    bo = generator()
    
    print_board(bo)
    solve(bo)
    print_board(bo)
