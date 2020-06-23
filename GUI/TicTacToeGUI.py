import pygame
import sys
import random
import time
from pygame.locals import *

# Set up the colors and dimensions.
BACKGROUNDCOLOR = (255, 255, 255)
LINECOLOR = (0, 0, 0)
WIDTH = 600
HEIGHT = 600
FONTSIZE = 70

# Set up the window.
pygame.init()
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("TicTacToe GUI")
mainClock = pygame.time.Clock()

# Set up the font.
mainFont = pygame.font.SysFont(None, FONTSIZE)

# Terminate the program.
def terminate():
    pygame.quit()
    sys.exit()

# Draw the table
def drawTable(board):
    # Draw the lines:
    windowSurface.fill(BACKGROUNDCOLOR)
    for i in (200, 400):
        pygame.draw.line(windowSurface, LINECOLOR, (i, 0), (i, HEIGHT), 2)
        pygame.draw.line(windowSurface, LINECOLOR, (0, i), (WIDTH, i), 2)
    # Display the 'X's and 'O's
    for i in range(9):
        if board[i] != ' ':
            drawText(board[i], mainFont, windowSurface, i %
                     3 * 200 + 100, i // 3 * 200 + 100)

    pygame.display.update()


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, LINECOLOR)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def waitForKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def isFullBoard(board):
    for i in range(9):
        if board[i] == ' ':
            return False
    return True


def isWinner(bo, le):
    # Given a board and a player's letter, this function return True if that player has won.
    # We use "bo" instead of  "board" and "le" instead of "letter" so we don't have to type as much
    return ((bo[0] == le and bo[1] == le and bo[2] == le) or  # Across the top
            (bo[3] == le and bo[4] == le and bo[5] == le) or  # Across the middle
            (bo[6] == le and bo[7] == le and bo[8] == le) or  # Across the bottom
            (bo[0] == le and bo[3] == le and bo[6] == le) or  # Down the left side
            (bo[1] == le and bo[4] == le and bo[7] == le) or  # Down the middle
            # Down the right side
            (bo[2] == le and bo[5] == le and bo[8] == le) or
            (bo[0] == le and bo[4] == le and bo[8] == le) or  # Diagonal
            (bo[2] == le and bo[4] == le and bo[6] == le))  # Diagonal


def getBoardCopy(board):
    # Make a copy of the board list and return it
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy


def chooseRandmMoveFromList(board, movesList):
    # Returns a valid move from the apssed list on the passed board
    # Return None if there is no valid move
    possibleMoves = []
    for i in movesList:
        if board[i] == ' ':
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is the algorithm for our Tic-Tac-Toe AI:
    # First, check if we can win in the next move
    for i in range(9):
        boardCopy = getBoardCopy(board)
        if boardCopy[i] == ' ':
            boardCopy[i] = 'O'
            if isWinner(boardCopy, 'O'):
                return i

    # Check if the player could win on their next move and block them
    for i in range(9):
        boardCopy = getBoardCopy(board)
        if board[i] == ' ':
            boardCopy[i] = 'X'
            if isWinner(boardCopy, 'X'):
                return i

    # Try to take one of the corners, if they are free
    move = chooseRandmMoveFromList(board, [0, 2, 6, 8])
    if move != None:
        return move

    # Try to take the center, if is free
    if board[4] == ' ':
        return 5

    # Move on one of the sides.
    return chooseRandmMoveFromList(board, [1, 3, 5, 7])

def redraw(board):
    drawTable(board)
    pygame.display.update()

def gameLoop():
    while True:
        board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText("Press any key to start.", mainFont,
                windowSurface, WIDTH//2, HEIGHT//2)
        pygame.display.update()
        waitForKey()
        playerTurn = 1
        while True:
            if playerTurn:
                print(1)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        terminate()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            terminate()
                    if event.type == MOUSEBUTTONDOWN:
                        if board[event.pos[0] // 200 + event.pos[1] // 200 * 3] == ' ':
                            board[event.pos[0] // 200 +
                                event.pos[1] // 200 * 3] = 'X'
                            playerTurn = False
                if isWinner(board,'X'):
                    redraw(board)
                    time.sleep(1)
                    windowSurface.fill(BACKGROUNDCOLOR)
                    drawText("You won. Congratulations!",mainFont,windowSurface,WIDTH//2,HEIGHT//2)
                    break   
            else:
                print(0)
                move = getComputerMove(board,'O')
                board[move] = 'O'
                if isWinner(board,'O'):
                    redraw(board)
                    time.sleep(1)
                    windowSurface.fill(BACKGROUNDCOLOR)
                    drawText("You lost.",mainFont,windowSurface,WIDTH//2,HEIGHT//2)
                    break
                playerTurn = True
            if isFullBoard(board):
                
                windowSurface.fill(BACKGROUNDCOLOR)
                drawText("It is a tie.",mainFont,windowSurface,WIDTH//2,HEIGHT//2)
                break
            mainClock.tick(60)
            redraw(board)
        pygame.display.update()
        waitForKey()
gameLoop()        
            
