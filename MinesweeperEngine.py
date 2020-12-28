"""
This file will be about calculation the squares on board and others
Coded by Chayakorn Vongbunsin
Made on 27/12/2020
"""

import random

class GameState():
    def __init__(self, row, col, n):
        self.row = row
        self.col = col
        self.NumsBomb = n
        self.board = self.makeBoard(row, col, n)
        self.ShowingBoard = [[False for j in range (col)] for i in range (row)]
        self.FlagCheck = [[False for j in range (col)] for i in range (row)]
        self.ClickBomb = False
        self.ScoreBoard = self.MakingScoreBoard(row, col)
        self.BoxLeft = row*col
        self.Win = False 
        self.BombLeft = n

    def makeBoard(self, row, col, NumsBomb):
        """
        This function makes board fill with "-" and "*" which "-" is a blank and "*" is a bomb
        """
        board = [["-" for i in range (row)]for j in range (col)] # Make a blank board without bomb which "-" represents blank space
        BombCount = 0
        while BombCount < NumsBomb: # Fill in the bomb until the board has N bombs (N = NumsBomb)
            RandRow = random.randint(0, row-1)
            RandCol = random.randint(0, col-1)
            while board[RandRow][RandCol] == "*":  # Check is it already a bomb in that square if it is change a row and column        
                RandRow = random.randint(0, row-1)
                RandCol = random.randint(0, col-1)
            board[RandRow][RandCol] = "*"
            BombCount += 1
        
        return board

    def CheckOnBoard(self, row, col):
        """
        Check the square that you clicked and check neighbour box if its score equals to 0
        """
        if self.board[row][col] == "*":
            self.ClickBomb = True
        elif self.board[row][col] == "-":
            self.ShowingBoard[row][col] = True
            if self.FlagCheck[row][col]:
                self.FlagCheck[row][col] = False
                self.BombLeft += 1
            self.BoxLeft -= 1
            if self.BoxLeft <= self.NumsBomb:
                self.Win =True
            if self.ScoreBoard[row][col] == 0: # If that box scores is not zero, we don't need to search more
                self.CheckNearby(row, col)

    def CheckNearby(self, row, col):
        """
        This function is recursive function to check all of 4 sides near the square that we looking for
        """
        Direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for PosX, PosY in Direction:
            NewRow = row + PosX
            NewCol = col + PosY
            if 0 <= NewRow < self.row and 0 <= NewCol < self.col and self.board[NewRow][NewCol] == "-" and not self.ShowingBoard[NewRow][NewCol]:
                self.ShowingBoard[NewRow][NewCol] = True
                if self.FlagCheck[NewRow][NewCol]:
                    self.FlagCheck[NewRow][NewCol] = False
                    self.BombLeft += 1
                self.BoxLeft -= 1
                if self.BoxLeft <= self.NumsBomb:
                    self.Win =True
                if self.ScoreBoard[NewRow][NewCol] == 0: # If that box scores is not zero, we don't need to search more
                    self.CheckNearby(NewRow, NewCol)

    def MakingScoreBoard(self, row, col):
        """
        This function will calculate each score box
        """
        TempBoard = [[0 for j in range (col)] for i in range (row)]
        Direction = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for r in range (row):
            for c in range (col):
                if self.board[r][c] == "*":
                    for PosX, PosY in Direction:
                        NewRow = r + PosX
                        NewCol = c + PosY
                        if 0 <= NewRow < row and 0 <= NewCol < col and self.board[NewRow][NewCol] != "*":
                            TempBoard[NewRow][NewCol] += 1
        
        return TempBoard

    def OpenAroundIt(self, row, col):
        """
        Special function works when the focusing box has the number of flags arount it equals to its score
        """
        Direction = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        CountingFlag = 0
        ItsScore = self.ScoreBoard[row][col]
        for PosX, PosY in Direction:
            NewRow = row + PosX
            NewCol = col + PosY
            if 0 <= NewRow < self.row and 0 <= NewCol < self.col:
                if self.FlagCheck[NewRow][NewCol]: CountingFlag += 1
        if CountingFlag == ItsScore:
            for PosX, PosY in Direction:
                NewRow = row + PosX
                NewCol = col + PosY
                if 0 <= NewRow < self.row and 0 <= NewCol < self.col and not self.FlagCheck[NewRow][NewCol]:
                    self.CheckOnBoard(NewRow, NewCol)
