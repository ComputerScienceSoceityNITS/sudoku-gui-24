

import pygame
import sudoku
import time
import numpy as np
import tkinter as tk


class Board:

    def __init__(self, x, y, grid):
        pygame.display.set_caption('Sudoku_by_RAJ217')
        self.x = x
        self.y = y
        self.win = pygame.display.set_mode((self.x, self.y+70))
        pygame.display.set_caption('Sudoku')
        self.win.fill((255, 255, 255))
        self.grid = grid
        self.grid_fresh = grid
        self.ranges_horizontal = []
        self.ranges_vertical = []
        self.pos_orig_num = self.base_grid(self.grid)
        self.pos_num = self.pos_orig_num[:]
        self.po = []
        self.state = 0
        self.count = 0
        self.color = (0, 255, 255)
        self.wrong_guess = []
        self.right_guess = []
        self.guess_numbers = []
        self.wrong_num = []
        self.wrong_count = 0
        self.a = 0          # just a checker
        self.solved = False

    def run(self):
        """
        runs the sudoku game
        :return: whole program
        """
        crashed = False
        while not crashed:

            for event in pygame.event.get():

                if not self.solved:
                    if event.type == pygame.MOUSEBUTTONUP:
                        po = pygame.mouse.get_pos()
                        self.po.append(po)
                        self.color = (0, 255, 255)

                    # Taking guess input for sudoku
                    n = None
                    if event.type == pygame.KEYDOWN:
                        key = pygame.key.get_pressed()
                        if key[pygame.K_1]:
                            n = 1
                        elif key[pygame.K_2]:
                            n = 2
                        elif key[pygame.K_3]:
                            n = 3
                        elif key[pygame.K_4]:
                            n = 4
                        elif key[pygame.K_5]:
                            n = 5
                        elif key[pygame.K_6]:
                            n = 6
                        elif key[pygame.K_7]:
                            n = 7
                        elif key[pygame.K_8]:
                            n = 8
                        elif key[pygame.K_9]:
                            n = 9
                        elif key[pygame.K_DELETE]:
                            self.del_no(self.po[-1])
                            self.color = (0, 255, 255)
                            continue
                        elif key[pygame.K_KP_ENTER]:

                            self.solve_()
                            self.draw()

                            self.a = 1
                            temp = pygame.event.wait()
                            if temp.type == pygame.KEYDOWN:
                                crashed = True
                                break
                        else:
                            continue

                        if key[pygame.K_SPACE]:
                            new_key = pygame.key.get_pressed()
                            if new_key[pygame.K_1]:
                                n = 1
                            elif new_key[pygame.K_2]:
                                n = 2
                            elif new_key[pygame.K_3]:
                                n = 3
                            elif new_key[pygame.K_4]:
                                n = 4
                            elif new_key[pygame.K_5]:
                                n = 5
                            elif new_key[pygame.K_6]:
                                n = 6
                            elif new_key[pygame.K_7]:
                                n = 7
                            elif new_key[pygame.K_8]:
                                n = 8
                            elif new_key[pygame.K_9]:
                                n = 9
                            self.guess_numbers.append([self.po[-1], n])
                            self.assume_numbers()
                            continue

                        if self.a == 0:
                            # Check so that no numbers overlap
                            po = self.find_cube(self.po[-1])        # makes sure that user doesn't changes the question i.e. the main grid
                            for pos in self.pos_orig_num:
                                if len(pos) == 3:
                                    pos_cube = self.find_cube(pos[:2])
                                    if pos_cube == po:
                                        break
                            else:
                                po = self.find_cube_mid_pos(self.po[-1])
                                if list(po) not in [i[:2] for i in self.pos_num]:
                                    self.pos_num.append([po[0], po[1], n])

                                    self.state += 1

                                    self.check_update_no()

                                elif list(po) in [i[:2] for i in self.pos_num]:           # no overlap
                                    temp_l = [i[:2] for i in self.pos_num]
                                    index = temp_l.index(list(po))
                                    self.pos_num[index][-1] = n

                                    board_pos = self.find_cube(temp_l[index])
                                    self.check_update_no()

                                    if int(self.grid[board_pos[1]-1][board_pos[0]-1]) is 0:
                                        self.pos_num.pop(index)

                    else:
                        if 0 not in self.grid:
                            self.text('Solved', (250, self.y + 15), (100, 255, 255))
            self.horizontal_lines()
            self.vertical_lines()
            self.text('~  made by Samraj32', (160, self.y+45), (34, 121, 214))
            
            if self.state >= 1:
                if self.state == 1 and self.count == 0:
                    self.time = time.time()
                    self.count += 1
                self.timer()

            self.draw()
            self.win.fill((255, 255, 255))

        pygame.quit()

    def draw(self):
        """
        Updates the game
        :return: update the screen
        """

        clock = pygame.time.Clock()

        # place the numbers
        if self.a == 0:
            self.draw_numbers(self.grid)
        else:
            self.draw_numbers(self.grid_fresh)
            self.text('Solved', (250, self.y + 15), (100, 255, 255))

        if 0 not in self.grid:
            self.text('Solved', (250, self.y + 15),  (100, 255, 255))

        # place the assumed numbers that is on the top left
        self.assume_numbers()

        # select the cube
        if len(self.po) > 0:
            self.select_cube(self.find_cube(self.po[-1]), self.color)

        # count number of mistakes
        if self.wrong_count > 0:
            self.x_display()

        pygame.display.update()
        clock.tick(20)

    def horizontal_lines(self):
        """
        draws horizontal lines
        :return: Horizontal lines
        """

        gap = self.y/9
        for i in range(1, 10):
            if i % 3 == 0:
                thickness = 3
            else:
                thickness = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i*gap), (self.x, i*gap), thickness)

    def vertical_lines(self):
        """
        draws vertical lines
        :return: Vertical lines
        """

        gap = self.x/9
        for i in range(1, 9):
            if i % 3 == 0:
                thickness = 3
            else:
                thickness = 1
            pygame.draw.line(self.win, (0, 0, 0), (i*gap, 0), (i*gap, self.y), thickness)

    def assume_numbers_pos(self, pos):
        """
        This gives the position of the number in the top left part, not placing it
        :param pos: position of the box
        :return: displays the number in the top left part of the respective box
        """

        gap_vertical = self.y / 9
        gap_horizontal = self.x / 9
        pos_ = self.find_cube_mid_pos(pos)
        box = self.find_cube(pos)
        new_pos_x = (box[0] - 1) * gap_horizontal + (pos_[0] - (box[0] - 1) * gap_horizontal) / 2
        new_pos_y = (box[1] - 1) * gap_vertical + (pos_[1] - (box[1] - 1) * gap_vertical) / 2

        return new_pos_x, new_pos_y

    def assume_numbers(self):
        """
        It provide the necessary positions and numbers to the assume_num_pos method
        :return: pass the required value to assume_num_pos method
        """

        temp = [self.assume_numbers_pos(po[0]) for po in self.guess_numbers]
        for i in self.guess_numbers:
            pos = self.assume_numbers_pos(i[0])
            if temp.count(pos) <= 2:
                if i[-1] is not None:
                    font = pygame.font.SysFont('Sans Serif', 25)
                    my_font = font.render(str(i[-1]), True, (204, 148, 91))
                    self.win.blit(my_font, (pos[0], pos[1]))
            if temp.count(pos) > 1:
                index = self.guess_numbers.index(i)
                self.guess_numbers.pop(index)

    def find_cube_mid_pos(self, pos):
        """
        Gives the position of the block which is clicked
        :param pos: tuple or list
        :return: coordinate of mid of cube for numbers to placed
        """

        X = pos[0]
        Y = pos[1]
        gap_horizontal = self.x/9
        gap_vertical = self.y/9
        pos_x = 0
        pos_y = 0
        for i in range(1, 10):
            if X >= (i-1)*gap_horizontal and X <= i*gap_horizontal:
                pos_x = ((i-1)*gap_horizontal+i*gap_horizontal)/2-10
            if Y >= (i - 1) * gap_vertical and Y <= i * gap_vertical:
                pos_y = ((i-1)*gap_vertical+i*gap_vertical)/2-15

        return pos_x, pos_y

    def find_cube(self, pos):
        """
        Returns the cube location
        :param pos: tuple or list
        :return: coordinate of cube
        """

        X = pos[0]
        Y = pos[1]
        gap_horizontal = self.x / 9
        gap_vertical = self.y / 9
        pos_x = 0
        pos_y = 0
        for i in range(1, 10):
            if X >= ((i - 1) * gap_horizontal) and X <= (i * gap_horizontal):
                pos_x = i
            if Y >= ((i - 1) * gap_vertical) and Y <= (i * gap_vertical):
                pos_y = i

        return pos_x, pos_y

    def find_pos(self, pos):
        """
        gives location according to the position given in the non gui board form
        :param pos: tuple or list
        :return: location
        """

        X = pos[0]
        Y = pos[1]
        gap_horizontal = self.x / 9
        gap_vertical = self.y / 9
        pos_x = X * gap_horizontal
        pos_y = Y * gap_vertical

        loc = self.find_cube_mid_pos((pos_x, pos_y))

        return loc

    def draw_numbers(self, bo):
        """
        Draws the number in a given cube
        :param bo: The numpy array which has to be projected
        :return: updated screen(image created and then updated)
        """
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                num = bo[i][j]
                if num != 0:
                    loc = self.find_pos((j,  i))
                    font = pygame.font.SysFont('Sans Serif', 50)
                    myfont = font.render(str(num), True, (0, 0, 0))
                    self.win.blit(myfont, loc)

    def del_no(self, pos):
        pos = self.find_cube_mid_pos(pos)
        for positions in self.pos_orig_num:
            if len(positions) == 3:
                if positions[:2] == list(pos):
                    break
        else:
            for positions in self.pos_num:
                if len(positions) == 3:
                    loc = self.find_cube(pos)
                    loc_x, loc_y = loc[0] - 1, loc[1] - 1
                    if list(pos) == positions[:2] and int(self.grid[loc_y][loc_x]) is not 0:
                        self.pos_num.remove(positions)

                        # updating the non GUI part
                        self.grid[loc_y][loc_x] = 0

    def base_grid(self, arr):
        """
        This finds the coordiantes of the base that is the problem which the user has to solve
        :param arr: numpy array or 2d list
        :return: all positions with respective numbers
        """

        gap_horizontal = self.x / 9
        gap_vertical = self.y / 9
        positions = []
        for y in range(len(arr)):
            for x in range(len(arr[y])):
                no = int(arr[y][x])
                if no != 0:
                    pos_x = (x*gap_horizontal + (x + 1)*gap_horizontal)/2 - 10
                    pos_y = (y*gap_vertical + (y + 1)*gap_vertical)/2 - 15
                    positions.append([pos_x, pos_y, no])
                else:
                    positions.append([0])
        return positions

    def check_update_no(self):
        """
        Returns the color of the selected cube based on the validity, valid-green, invalid-red and update it
        :return: None, changes self.color and also updates the grid
        """
        pos = self.find_cube(self.pos_num[-1][:-1])
        pos = list(pos)
        pos[0], pos[1] = pos[1]-1, pos[0]-1

        no = self.pos_num[-1][-1]

        check = sudoku.validity(self.grid, no, pos)
        if check is False:
            self.color = (255, 0, 0)
            pos = self.pos_num[-1][:-1]
            self.wrong_count += 1
            board_pos = self.find_cube(pos)
            board_pos = list(map(lambda x: x-1, board_pos))
            self.grid[board_pos[1]][board_pos[0]] = 0

        else:
            self.color = (0, 255, 0)
            self.right_guess.append((pos, no))
            pos = self.pos_num[-1][:-1]
            board_pos = self.find_cube(pos)
            board_pos = list(map(lambda x: x - 1, board_pos))
            self.grid[board_pos[1]][board_pos[0]] = no

    def select_cube(self, box_pos, color):
        """
        Marks the cube which is slected as blue
        :param box_pos: position of the box the first box being (1, 1)
        :param color: it is the color of the selected box
        :return: colours the box border
        """
        box_x = box_pos[0]
        box_y = box_pos[1]

        for positions in self.pos_orig_num:
            if len(positions) == 3:
                positions = self.find_cube(positions[:2])
                check_box_x = positions[0]
                check_box_y = positions[1]
                if box_x == check_box_x and box_y == check_box_y:
                    break
        else:

            gap_horizontal = self.x / 9
            gap_vertical = self.y / 9
            for i in range(2):
                # horizontal lines
                pygame.draw.line(self.win, color, ((box_x-1)*gap_horizontal, (box_y-i)*gap_vertical), (box_x*gap_horizontal, (box_y-i)*gap_vertical), 3)
                # vertical lines
                pygame.draw.line(self.win, color, ((box_x - i) * gap_horizontal, (box_y - 1) * gap_vertical), ((box_x - i) * gap_horizontal, (box_y) * gap_vertical), 3)

    def x_display(self):
        """
        Shows the number of wrong attempts
        :return: red(X) x wrong count in image form
        """

        font = pygame.font.SysFont('Sans Serif', 40)
        X = font.render(str('X'), True, (255, 0, 0))
        self.win.blit(X, (160, self.y + 12))

        font = pygame.font.SysFont('Sans Serif', 30)
        text = font.render(str('Wrong Count :  '), True, (0, 0, 0))
        self.win.blit(text, (10, self.y+15))

        count = font.render(f'x {self.wrong_count}', True, (0, 0, 0))
        self.win.blit(count, (190, self.y + 17))

    def solve_(self):
        """
        Solve the sudoku using algorithm
        :return: solved sudoku
        """
        sudoku.solve(self.grid_fresh)
        sudoku.print_board(self.grid_fresh)

    def text(self, text, pos, color):
        """
        Show a text 'solving' so the user knows the computer is solving the game
        :param text: string
        :param pos: list or tuple
        :param color: tuple or list
        :return: text
        """

        font = pygame.font.SysFont('Sans Serif', 30)
        solving = font.render(f'{text}', True, color)
        self.win.blit(solving, pos)

    def timer(self):
        """
        returns the time which is used in the draw method to show the time
        :return: time image
        """
        c_time = int(str(time.time() - self.time).split('.')[0])
        sec = c_time%60
        t_min = c_time//60
        minute = t_min//60
        hour = t_min//60
        if sec < 10:
            sec = '0'+str(sec)
        if minute < 10:
            minute = '0'+str(minute)
        if hour < 10:
            hour = '0'+str(hour)
        current_time = f'Time : {hour}:{minute}:{sec}'

        font = pygame.font.SysFont('Sans Serif', 40)
        myfont = font.render(f'{current_time}', True, (0, 0, 0))
        self.win.blit(myfont, (self.x-220, self.y+12))


if __name__ == '__main__':

    base = sudoku.generator()
    sudoku.print_board(base)

    sudoku.print_board(base)
    board = Board(600, 500, base)
    pygame.init()
    board.run()
    quit()