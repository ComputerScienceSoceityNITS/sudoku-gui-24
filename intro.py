import pygame


class Intro:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.win = pygame.display.set_mode((self.x, self.y))
        pygame.display.set_caption('Sudoku')
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

    def run(self):
        """
        runs the window
        :return: None
        """

        crashed = False
        while not crashed:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    crashed = True

                if event.type == pygame.QUIT:
                    crashed = True

            self.draw()
            self.win.fill(self.WHITE)

        pygame.quit()

    def draw(self):
        """
        Updates the game window
        :return: None
        """

        clock = pygame.time.Clock()

        # Instructions
        self.text_font('~  made by Samraj32', 20, (self.x-180, 10), (34, 121, 214))
        self.text_font('Instructions -  ', 60, (10, 10), self.BLACK)
        self.text_font('~  Fill the board with numbers such that none of the entered number is in the row ', 20, (10, 90), self.BLACK)
        self.text_font('    nor in the column nor in the box', 20, (10, 120), self.BLACK)
        self.text_font('~  To place a number enter any number from 1 to 9 in your keyboard', 20, (10, 150), self.BLACK)
        self.text_font('~  Press del on your keyboard to remove a number ', 20, (10, 180), self.BLACK)
        self.text_font('~  If a number is valid it will be placed and the box border will become green ', 20, (10, 210), self.BLACK)
        self.text_font('~  If unsure of a number you can pencil it by pressing the space bar and your', 20, (10, 240), self.BLACK)
        self.text_font('    desired number together', 20, (10, 270), self.BLACK)
        self.text_font('~  To delete a pencil number press the space bar again', 20, (10, 300), self.BLACK)
        self.text_font('~  As soon as you place a number the game starts and the timer appears', 20, (10, 330), self.BLACK)
        self.text_font('~  If you guess a number which is invalid it will not be placed, the box border', 20, (10, 360), self.BLACK)
        self.text_font('   will become red and the number of times you enter a invalid number it will be', 20, (10, 390), self.BLACK)
        self.text_font('   shown below', 20, (10, 420), self.BLACK)
        self.text_font('~  If you press Enter in the numpad then the computer will solve the game for you', 20, (10, 450), self.BLACK)
        self.text_font('           Press any key to continue                        ', 40, (10, 480), (100, 255, 255))

        pygame.display.update()
        clock.tick(30)

    def text_font(self, text, size, pos, color):
        """
        Draws a font on the screen
        :param size: int
        :param pos: tuple or list
        :param text: string
        :param color: tuple
        :return: None
        """
        font = pygame.font.SysFont('times new roman', size)
        my_font = font.render(str(text), True, color)
        self.win.blit(my_font, pos)


if __name__ == '__main__':
    intro = Intro(650, 550)
    pygame.init()
    intro.run()


