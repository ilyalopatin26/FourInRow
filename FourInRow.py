"""
Four in a row game test
"""

import numpy as np
from copy import deepcopy

from abstractGame import absGame

class Game(absGame):
    def __init__(self):
        super().__init__()
        self._board = [ [] for _ in range(7)  ] 
    
    class move:
        def __init__(self, col):
            self.col = col
        
        def toOneHot(self) -> np.array:
            return np.array( [ 1 if i == self.col else 0 for i in range(7) ] )

        def __hash__(self)->int :
            return self.col
        def __eq__(self, other) -> bool:
            return  self.col == other.col
        def __ne__(self, other) -> bool:
            return not self.__eq__(other)
        def __str__(self) -> str:
            return f"({self.col})"
        
    
    def checkValidMove(self, move) -> bool:
        return len(self._board[move.col]) < 6
    
    def getValidMoves(self) -> list:
        return [ self.move(j) for j in range(7) if self.checkValidMove( self.move(j) )  ]
    
    def _checkDraw(self) -> bool:
        return  len( self.getValidMoves()  ) < 1
    
    def _checkWinLastMove(self, move) -> bool:
        
        col = move.col
        h = len(self._board[col]) - 1
        
        l,r = h, h
        while l > 0 and self._board[col][l-1] == self._curPlayer:
            l -= 1
        while r < len(self._board[col])-1 and self._board[col][r+1] == self._curPlayer:
            r += 1
        if r - l + 1 >= 4:
            return True

        l,r = col, col
        while l > 0 and len(self._board[l-1]) > h and self._board[l-1][h] == self._curPlayer:
            l -= 1
        while r < 6 and len(self._board[r+1]) > h and self._board[r+1][h] == self._curPlayer:
            r += 1
        if r - l + 1 >= 4:
            return True
        
        l, r = 0, 0
        while col - l > 0 and h - l > 0 and len(self._board[col-l-1]) > h-l-1 and self._board[col-l-1][h-l-1] == self._curPlayer:
            l += 1
        while col + r < 6 and h + r < 5 and len(self._board[col+r+1]) > h+r+1 and self._board[col+r+1][h+r+1] == self._curPlayer:
            r += 1
        if r + l + 1 >= 4:
            return True

        l, r = 0, 0
        while col - l > 0 and h + l < 5 and len(self._board[col-l-1]) > h+l+1 and self._board[col-l-1][h+l+1] == self._curPlayer:
            l += 1
        while col + r < 6 and h - r > 0 and len(self._board[col+r+1]) > h-r-1 and self._board[col+r+1][h-r-1] == self._curPlayer:
            r += 1
        if r + l + 1 >= 4:
            return True
        
        return False
    
    
    def _makeMove(self, move):
        self._board[ move.col].append( self._curPlayer )
    
    def toNpArray(self) -> np.array:
        np_array = np.zeros( (6, 7) )
        for w in range(7):
            for h in range( len(self._board[w])  ):
                np_array[5-h ][w] = self._board[w][h]
        return np_array

    
    def __hash__(self)  :
        return hash( self.toNpArray().tobytes()  )
    
    def __eq__(self, other) -> bool:
        return np.all(self.toNpArray() == other.toNpArray() )
    
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

