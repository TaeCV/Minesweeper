"""
This file represents the board minesweeper and get the action from the user
Coded by Chayakorn Vongbunsin
Made on 27/12/2020
"""

from os import path
import pygame as pg
import random
import MinesweeperEngine
import numpy as np

"""
Basic option. In the fututre add more option to add the width,height of the board and more functions
"""

#Given width, height, and FPS
Width, Height = 600, 700
FPS = 60

#Set up basic option
row = col = 15
SQ_size = Width//row
StartRow = 100
StartCol = 0
NumsBomb = 30
Images = {}

def LoadImages():    
    filepath = path.dirname(__file__)
    sourcepath = path.join(filepath, "Source")
    Img = ["bomb", "flag", "cross", "block"]
    for i in range (len(Img)):
        Images[Img[i]] = pg.transform.scale(pg.image.load(path.join(sourcepath, Img[i] +".png")).convert_alpha(), (SQ_size, SQ_size))

def main():
    pg.init()
    screen = pg.display.set_mode((Width,Height))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    LoadImages() # Loading Images
    running = True #Boolean for the statement of the game
    GameState = MinesweeperEngine.GameState(row, col, NumsBomb) # Set up a new board
    TimeStart = pg.time.get_ticks()
    Pause = False
    TimeOver =0
    addition_time = 0

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                if (not GameState.ClickBomb or GameState.Win) and not Pause:                
                    position = pg.mouse.get_pos()
                    if position[1] >= StartRow:            
                        x = (position[1]-100) // SQ_size
                        y = position[0] // SQ_size
                        if e.button == 1 and not GameState.FlagCheck[x][y]: # Left mouse click and not flaged
                            GameState.CheckOnBoard(x, y)
                        elif e.button == 3: # Right mouse click
                            GameState.FlagCheck[x][y] = not GameState.FlagCheck[x][y]
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_r: # Reset the game
                    GameState = MinesweeperEngine.GameState(row, col, NumsBomb) # Set up a new board
                    TimeStart = pg.time.get_ticks()
                    TimeOver = 0
                    Pause = False
                elif e.key == pg.K_SPACE:
                    Pause = not Pause
                    if not Pause:
                        TimeOver += pg.time.get_ticks()-addition_time
                        addition_time = 0
        screen.fill(pg.Color("white"))
        drawBoardandLine(screen, GameState.board, GameState.FlagCheck, GameState.ShowingBoard, GameState.ScoreBoard)
        if not Pause:
            counting_time = pg.time.get_ticks() - TimeStart - TimeOver
            # Change from millisecond to seconds and minutes
            countingMinute = str(counting_time//60000).zfill(2)
            countingSecond = str((counting_time % 60000) //1000).zfill(2)
            countingString = "%s:%s" % (countingMinute,countingSecond)
            font = pg.font.SysFont(None, 32)
            counting_text = font.render(countingString, 0, pg.Color("black"))
            counting_rect = counting_text.get_rect(center = (Width - 50, 50))
        elif addition_time == 0:
            addition_time = pg.time.get_ticks()
        pg.draw.rect(screen, pg.Color("grey"), pg.Rect(Width-counting_text.get_width()//2-60, 25, counting_text.get_width()+20, counting_text.get_height()+25))
        screen.blit(counting_text, counting_rect)
        if GameState.ClickBomb:
            ClickOnTheBomb(screen, GameState.board, (x,y), GameState.FlagCheck)
            LossText(screen)
            Pause = True
        if GameState.Win:
            WinnerText(screen)
            Pause = True
        clock.tick(FPS)
        pg.display.flip()

def drawBoardandLine(screen, board, FlagCheck, ShowingBoard, ScoreBoard):
    """
    This function draws a board and line on the screen by calling other functions
    """
    drawBoard(screen,board, FlagCheck, ShowingBoard, ScoreBoard)
    drawLine(screen,board)

def drawBoard(screen, board, FlagCheck, ShowingBoard, ScoreBoard):
    """
    This function draws a box on the board and also draw a flag if it is flagged 
    """
    Colors = ['', pg.Color("blue"), pg.Color("green"), pg.Color("red"), pg.Color("purple"),
                pg.Color("maroon"), pg.Color("turquoise"), pg.Color("black"), pg.Color("gray")]
    pg.draw.rect(screen, pg.Color("pink"), pg.Rect(0,0, Width, StartRow))
    for r in range (row):
        for c in range (col):
            screen.blit(Images["block"], pg.Rect(StartCol + c * SQ_size, StartRow + r * SQ_size, SQ_size, SQ_size))
            if FlagCheck[r][c]:
                screen.blit(Images["flag"], pg.Rect(StartCol + c * SQ_size, StartRow + r * SQ_size, SQ_size, SQ_size))
            if ShowingBoard[r][c]:
                pg.draw.rect(screen, pg.Color("gray"), pg.Rect(StartCol + SQ_size*c, StartRow + SQ_size*r, SQ_size, SQ_size))
                if ScoreBoard[r][c]:
                    font = pg.font.SysFont("Helvitca", SQ_size*3//4, True, False)
                    Text = font.render(str(ScoreBoard[r][c]), 0, Colors[ScoreBoard[r][c]])
                    TextLocation = Text.get_rect(center = (StartCol + SQ_size*c + SQ_size//2, StartRow + SQ_size*r + SQ_size//2))
                    screen.blit(Text, TextLocation)

def drawLine(screen, board): 
    """
    This function draws a line on the board
    """
    pg.draw.line(screen, pg.Color("black"), (0, 0), (Width, 0), 4)
    pg.draw.line(screen, pg.Color("black"), (0, StartRow-2), (Width, StartRow-2), 4)
    pg.draw.line(screen, pg.Color("black"), (0, 0), (0, StartRow), 4)
    pg.draw.line(screen, pg.Color("black"), (Width-2, 0), (Width-2, StartRow), 4)
    for r in range (row):
        pg.draw.line(screen, pg.Color("gainsboro"), (StartCol, StartRow + r*SQ_size), (StartCol + Width, StartRow + r*SQ_size))
        for c in range (col):
            pg.draw.line(screen, pg.Color("gainsboro"), (StartCol + c*SQ_size, StartRow), (StartCol + c*SQ_size, StartRow + Width))    
    pg.draw.line(screen, pg.Color("gainsboro"), (StartCol, Height), (StartCol + Width, Height))


def ClickOnTheBomb(screen, board, pos, FlagCheck):
    """
    This function will work if we click on the bomb.
    It will highlight that square with red color and show other bombs on the board
    If we flag wrong square, it will show a crossing bomb on the board
    """
    x,y = pos
    s = pg.Surface((SQ_size, SQ_size))
    s.fill(pg.Color("red"))
    for r in range (row):
        for c in range (col):
            if board[r][c] == "*" and not FlagCheck[r][c]:
                pg.draw.rect(screen, pg.Color("gray"), pg.Rect(StartCol + SQ_size*c, StartRow + SQ_size*r, SQ_size, SQ_size))
                if r == x and c == y:
                    screen.blit(s, (y*SQ_size, StartRow + x*SQ_size))
                screen.blit(Images["bomb"], pg.Rect(StartCol + c * SQ_size, StartRow + r * SQ_size, SQ_size, SQ_size))
            elif board[r][c] != "*" and FlagCheck[r][c]:
                pg.draw.rect(screen, pg.Color("gray"), pg.Rect(StartCol + SQ_size*c, StartRow + SQ_size*r, SQ_size, SQ_size))
                screen.blit(Images["bomb"], pg.Rect(StartCol + c * SQ_size, StartRow + r * SQ_size, SQ_size, SQ_size))
                screen.blit(Images["cross"], pg.Rect(StartCol + c * SQ_size, StartRow + r * SQ_size, SQ_size, SQ_size))

def WinnerText(screen):
    text = "Congratulation, you are the winner !!"
    font = pg.font.SysFont("Helvitca", 28, True, False)
    Text = font.render(text, 0, pg.Color("black"))
    Textbox = pg.Surface((Width//2 + 150, Width//2))
    Textbox.set_alpha(150)
    Textbox.fill(pg.Color("green"))
    screen.blit(Textbox, (Width//4 -75 ,StartRow//2 + Width//4))
    Text_rect = Text.get_rect(center = (Width//2, Height//2))
    screen.blit(Text, Text_rect)

def LossText(screen):
    text = "Unlucky, you lost! :("
    font = pg.font.SysFont("Helvitca", 28, True, False)
    Text = font.render(text, 0, pg.Color("black"))
    Textbox = pg.Surface((Width//2 + 150, Width//2))
    Textbox.set_alpha(150)
    Textbox.fill(pg.Color("green"))
    screen.blit(Textbox, (Width//4 -75 ,StartRow//2 + Width//4))
    Text_rect = Text.get_rect(center = (Width//2, Height//2))
    screen.blit(Text, Text_rect)

if __name__ == "__main__":
    main()
