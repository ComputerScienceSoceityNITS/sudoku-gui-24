from intro import Intro
from Sudoku_GUI import Board
import pygame
import sudoku
from tkinter import messagebox
import tkinter


class Main():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = sudoku.generator()

        # Intro
        intro = Intro(self.x, self.y)
        pygame.init()
        intro.run()

        # Sudoku game
        board = Board(self.x, self.y, self.grid)
        pygame.init()
        try:
            board.run()
        except:
            tkinter.Tk().withdraw()
            messagebox.showinfo('Error', 'I am extremely sorry there was an error please restart the game')
        quit()


main = Main(650, 550)
try:
    main
except:
    messagebox.showinfo('Error', 'I am extremely sorry there was an error please restart the game')