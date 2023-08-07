from abc import ABC, abstractmethod
import numpy as np


class absGame(ABC):
    def __init__(self):
        self._status = -1  # -1: in progress, 0: draw, 1: player 1 wins, 2: player 2 wins
        self._curPlayer = 1
        self._board = None
    
    @property
    def Status(self) -> int:
        return self._status

    @property
    def CurPlayer(self) -> int:
        return self._curPlayer

    @property
    def getOpp(self) -> int:
        return 3 - self._curPlayer

    @abstractmethod
    def checkValidMove(self, move) -> bool:
        pass

    @abstractmethod
    def getValidMoves(self) -> list:
        pass

    @abstractmethod
    def _checkDraw(self) -> bool:
        pass

    @abstractmethod
    def _checkWinLastMove(self, move) -> bool:
        pass

    @abstractmethod    
    def _makeMove(self, move) :
        pass

    def _updateStatus(self, move):
        if self._checkWinLastMove( move ):
            self._status = self.CurPlayer
        elif self._checkDraw() :
            self._status = 0
    
    def get_and_MakeMove(self, move):
        if self.checkValidMove(move):
            self._makeMove(move)
            self._updateStatus(move)
            self._curPlayer = self.getOpp
        else:
            raise ValueError("Invalid move")

    @abstractmethod
    def toNpArray(self) -> np.array:
        pass


