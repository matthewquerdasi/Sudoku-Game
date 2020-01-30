#Matt Querdasi
#sudokuSolverGame.py

import pygame
import time
pygame.font.init()



#colors
teal = (0,128,160)
red = (255,50,50)
green = (0,200,0)
white = (255,255,255)
black = (0,0,0)
yellow = (255,215,0)


avenir_font = pygame.font.SysFont('Avenir TTC', 25)



class Grid:

    sample_board = [[0,0,2,4,0,5,8,0,0],
                    [0,4,1,8,0,0,0,2,0],
                    [6,0,0,0,7,0,0,3,9],
                    [2,0,0,0,3,0,0,9,6],
                    [0,0,9,6,0,7,1,0,0],
                    [1,7,0,0,5,0,0,0,3],
                    [9,6,0,0,8,0,0,0,1],
                    [0,2,0,0,0,9,5,6,0],
                    [0,0,8,3,0,6,9,0,0]]

    def __init__(self, rows, cols, width, height, window, top_spacing):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.selected = None
        self.window = window
        self.top_spacing = top_spacing
        self.cubes = [[Cube(self.sample_board[i][j], i, j, width, height, self.top_spacing) for j in range(0, cols)] for i in range(0, rows)]
        self.solution = None
        self.score = 0

    def drawLines(self):
        #Draws sudoku board lines
        top_spacing = self.top_spacing
        spacing = self.width/9

        for i in range(0,10):
            current = round(i*spacing)
            if i % 3 == 0:
                #draws vertical thick lines
                pygame.draw.line(self.window, white, (current, top_spacing), (current, self.height + top_spacing), 4)
                #draws horizontal thick lines
                pygame.draw.line(self.window, white, (0, current + top_spacing), (self.width, current + top_spacing), 4)
            else:
                #draws vertical thin lines
                pygame.draw.line(self.window, white, (current, 50), (current, self.height + top_spacing), 1)
                #draws horizontal thin lines
                pygame.draw.line(self.window, white, (0, current + top_spacing), (self.width, current + top_spacing), 1)

    def drawCubes(self):
        #Draws cube numbers on to board
        top_spacing = self.top_spacing
        spacing = self.width/9

        for i in range(self.rows):
            for j in range(self.cols):
                curr_cube = self.cubes[i][j]
                curr_cube.draw(self.window) #draws cube number

    def clickReset(self):
        #resets selected cube
        (row, col) = self.selected
        self.cubes[row][col].selected = False
        self.selected = None

    def mouseClick(self, position):
        #Takes input x,y from mouse click position
        (x,y) = position

        if 0 < x < self.width:
            if self.top_spacing < y < (self.height + self.top_spacing):

                #resets previously selected cube
                if self.selected is not None:
                    self.clickReset()

                row = int(x // (self.width/9))
                col = int((y - self.top_spacing) // (self.width/9))

                self.cubes[row][col].selected = True
                self.selected = (row, col)

    def keyPress(self, input):
        #Takes int input from user and changes cube value

        if self.selected is not None and input is not None:
            (row, col) = self.selected
            if self.cubes[row][col].value == 0:
                self.cubes[row][col].incorrect = False
                self.cubes[row][col].temp = input



    def solveBoard(self, board):
        """
        solves sudoku board
        board: list of ints
        return: bool
        """

        found = self.findEmpty(board)
        if found:
            (row, col) = found
        else:
            return True

        i = 1
        while i < 10:
            if self.isValid(board, (row, col), i):
                board[row][col] = i

                if self.solveBoard(board):
                    return True

                board[row][col] = 0

            i += 1

        return False

    def findEmpty(self, board):
        """
        finds first empty location on board
        board: list of ints
        return: (row, col)
        """

        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == 0:
                    return (i, j)

    def isValid(self, board, position, move):
        """
        checks whether move is valid
        board: list of ints
        position: (row, col)
        move: int
        return: bool
        """
        (row, col) = position

        #row
        for i in range(0, len(board[0])):
            if move == board[row][i]:
                return False
        #column
        for j in range(0, len(board[0])):
            if move == board[j][col]:
                return False
        #nonet 3x3
        x_box = col // 3
        y_box = row // 3

        for i in range(y_box*3, y_box*3 + 3):
            for j in range(x_box*3, x_box*3 + 3):
                if move == board[i][j]:
                    return False

        return True


    def checkMoves(self):

        #checks if board has been solved already and solves
        if self.solution is None:
            copy = self.sample_board
            self.solveBoard(copy)
            self.solution = copy

        #checks user moves and updates correct/incorrect moves lists
        for i in range(0, self.rows):
            for j in range(0, self.cols):

                user_temp_value = self.cubes[i][j].temp
                solution_value = self.solution[i][j]

                #Checks for correct user input
                if user_temp_value == solution_value:
                    self.cubes[i][j].value = user_temp_value #sets real value to user_temp_value
                    self.cubes[i][j].correct = True
                    user_temp_value = 0
                #Checks for incorrect user input
                if user_temp_value != solution_value and user_temp_value != 0 and self.cubes[i][j].incorrect != True:
                    self.cubes[i][j].incorrect = True
                    self.score += 1


    def updateBoard(self, time):
        #time
        time_font = pygame.font.SysFont("Arial", 40) #sets font to arial
        min = str(time//60)
        sec = str(time%60)
        if len(sec) == 1:
            sec = "0" + sec
        time_display = time_font.render(min + ":" + sec, 1, (black))
        self.window.blit(time_display, (400, 15))

        #Draws score on to board
        score_font = pygame.font.SysFont("Arial", 40) #sets font to arial
        score_number_display = score_font.render(str(self.score), 1, (red))
        score_text_display = score_font.render("Mistakes: ", 1, (black))
        self.window.blit(score_number_display, (160, 15))
        self.window.blit(score_text_display, (25, 15))

    def deleteMove(self):

        if self.selected is not None:
            (row, col) = self.selected
            if self.cubes[row][col].value == 0:
                self.cubes[row][col].temp = 0


class Cube:
    def __init__(self, value, row, col, width, height, top_spacing):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.correct = False
        self.incorrect = False
        self.top_spacing = top_spacing

    def draw(self, window):
        spacing = int(self.width/9)
        hor_adj = 18
        vert_adj = 12 + self.top_spacing
        number_font = pygame.font.SysFont("Arial", 50) #sets font to arial
        (x,y) = (int(self.row * spacing), int(self.col * spacing))

        #highlights correct cube
        if self.correct == True:
            pygame.draw.rect(window, (green), ((x + hor_adj - 14), (y + vert_adj - 10), spacing, spacing))

        if self.temp == 0 and self.value == 0:
            number = number_font.render(str(self.temp), 1, (teal))
            window.blit(number, (x + hor_adj, y + vert_adj))

        #highlights selected cube
        if self.selected == True and self.correct == False:
            pygame.draw.rect(window, (white), ((x + hor_adj - 14), (y + vert_adj - 10), spacing, spacing))

        #highlights incorrect cube
        if self.incorrect == True and self.temp != 0:
            number = number_font.render(str(self.temp), 1, (red))
            window.blit(number, (x + hor_adj, y + vert_adj))

        #draws all user values
        if self.temp != 0 and self.incorrect == False:
            number = number_font.render(str(self.temp), 1, (yellow))
            window.blit(number, (x + hor_adj, y + vert_adj))

        #draws all non absent correct numbers
        if self.value != 0:
            number = number_font.render(str(self.value), 1, (black))
            window.blit(number, (x + hor_adj, y + vert_adj))






def drawBoard(window, board, time):
    #wipes screen
    window.fill(teal)

    #draws grid lines
    board.drawLines()
    #draws cubes
    board.drawCubes()

    board.updateBoard(time)


def main():
    window = pygame.display.set_mode((500,550))
    pygame.display.set_caption("Sudoku Game")
    sudoku_board = Grid(9, 9, 500, 500, window, 50)
    input = None
    start_time = time.time()
    score = 0

    running = True
    while running:
        game_time = round(time.time() - start_time)

        #Checks for exit command
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT")
                running  = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                sudoku_board.mouseClick(position)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    input = 1
                if event.key == pygame.K_2:
                    input = 2
                if event.key == pygame.K_3:
                    input = 3
                if event.key == pygame.K_4:
                    input = 4
                if event.key == pygame.K_5:
                    input = 5
                if event.key == pygame.K_6:
                    input = 6
                if event.key == pygame.K_7:
                    input = 7
                if event.key == pygame.K_8:
                    input = 8
                if event.key == pygame.K_9:
                    input = 9
                if event.key == pygame.K_RETURN:
                    sudoku_board.checkMoves()
                if event.key == pygame.K_SPACE:
                    sudoku_board.deleteMove()

                sudoku_board.keyPress(input)
                input = None



        #drawing board

        drawBoard(window, sudoku_board, game_time)

        pygame.display.update()


main()
pygame.quit()











"""
    clock = str(round((pygame.time.get_ticks()/1000), 2)) #rounds timer to 2 decimal places and makes string
    clock_surface = avenir_font.render(clock, False, white) #creates new surface with text
    window.blit(clock_surface, (450,20)) #draws clock surface on screen
"""
