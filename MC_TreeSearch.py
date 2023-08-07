import numpy as np
from numpy import random
from copy import deepcopy

from FourInRow import Game

class Node:
    def __init__(self, pos: Game):
        self.__win = 0
        self.__draw = 0
        self.__loss = 0

        self.__pos = pos
        self.__children = {}
        self.flagInitChild = False
    
        self.P1_win = False
        self.P2_win = False

        if self.__pos.Status == 1:
            self.P1_win = True
        if self.__pos.Status == 2:
            self.P2_win = True

    @property
    def Visit(self):
        return self.__win + self.__draw + self.__loss
    
    @property
    def Statistic(self) -> str:
        return f"Win: {self.__win}, Draw: {self.__draw}, Loss: {self.__loss}, Total: {self.Visit}"

    def UCB(self, parentVisit, eps = 1e-5):
        n = self.Visit
        N1 = max(1.1 , float(parentVisit) )
        return ( self.__win + 0.5 * self.__draw - self.__loss ) / (n+eps) + np.sqrt(2 * np.log2(N1) /( n + eps))

    def getChild(self, move):
        return self.__children[move]
    
    def addChild(self, move, child):
        self.__children[move] = child

    def update(self, reward: int):
        if reward == 1:
            self.__win += 1
        elif reward == 0:
            self.__draw += 1
        elif reward == -1:
            self.__loss += 1
        else:
            raise ValueError("Invalid reward")
    
    @property
    def Pos(self):
        return self.__pos
    

class  MC_TreeSearcher:
    def __init__(self, targetPlayer: int, rollout: int,  deepBruteForce: int, seed = 1):
        self.__player = targetPlayer
        self.__rollout = rollout
        random.seed(seed)
        self.__deepBruteForce = deepBruteForce
        self.__currNode = Node( Game() )
        self.__dictPos = {}
        self.__dictPos[self.__currNode.Pos] = self.__currNode
        self.__lastMoveStrate = np.zeros(7)

    def __initChild(self, node: Node):
        if node.flagInitChild:
            return
        ValidMoves = node.Pos.getValidMoves()
        for move in ValidMoves:
            tempPos = deepcopy(node.Pos)
            tempPos.get_and_MakeMove(move)
            tempNode = self.__dictPos.get(tempPos, None)
            if tempNode is None:
                tempNode = Node(tempPos)
                self.__dictPos[tempPos] = tempNode
            node.addChild(move, tempNode)
        node.flagInitChild = True
    
    def __checkWinBruteForce(self, node: Node, targetPlayer, deep):
        self.__initChild(node)

        if node.P1_win and targetPlayer == 1:
            return True
        if node.P2_win and targetPlayer == 2:
            return True
        if node.Pos.Status != -1 or deep == 0:
            return False
        
        validMoves = node.Pos.getValidMoves()
        if targetPlayer == node.Pos.CurPlayer:
            for move in validMoves:
                if self.__checkWinBruteForce(node.getChild(move), targetPlayer, deep - 1):
                    if targetPlayer == 1:
                        node.P1_win = True
                    else:
                        node.P2_win = True
                    return True
            return False
        else:
            for move in validMoves:
                if not self.__checkWinBruteForce(node.getChild(move), targetPlayer, deep):
                    return False
            if targetPlayer == 1:
                node.P1_win = True
            else:
                node.P2_win = True
            return True
    
    def __Nodeupdate(self, node: Node, result):
        if result == self.__player:
            node.update(1)
        elif result == 0:
            node.update(0)
        else :
            node.update(-1)
    
    def __simulate(self, node: Node):
        if node.P1_win:
            self.__Nodeupdate(node, 1)
            return 1
        if node.P2_win:
            self.__Nodeupdate(node, 2)
            return 2
        if node.Pos.Status != -1:
            self.__Nodeupdate(node, node.Pos.Status)
            return node.Pos.Status
        
        self.__initChild(node)
        validMoves = node.Pos.getValidMoves()

        candidate = []
        bestIndex = -1.0
        for move in validMoves:
            child = node.getChild(move)
            if self.__checkWinBruteForce( child, node.Pos.CurPlayer, 1):
                self.__Nodeupdate( node, node.Pos.CurPlayer)
                return node.Pos.CurPlayer
            if self.__checkWinBruteForce( child, 3-node.Pos.CurPlayer, 1):
                continue

            
            """
            if child.P1_win or child.P2_win:
                if child.P1_win and node.Pos.CurPlayer == 1:
                    self.__Nodeupdate( node, 1)
                    return 1
                if child.P2_win and node.Pos.CurPlayer == 2:
                    self.__Nodeupdate( node, 1)
                    return 2
                continue
            """
            score = child.UCB(node.Visit)
            if score - bestIndex >= 1e-5:
                candidate = [move]
                bestIndex = score
            elif abs(score - bestIndex) < 1e-5:
                candidate.append(move)
        if len( candidate) == 0 :
            candidate = validMoves
        selectedMove = random.choice(candidate)
        result = self.__simulate(node.getChild(selectedMove))
        self.__Nodeupdate(node, result)
        return result
    
    def searchBestMove(self, flagPrint = True) :
        self.__initChild(self.__currNode)
        validMoves = self.__currNode.Pos.getValidMoves()
        for move in validMoves:
            if self.__checkWinBruteForce(self.__currNode.getChild(move), self.__player, self.__deepBruteForce):
                self.__lastMoveStrate = np.zeros(7)
                self.__lastMoveStrate[move.col] = 1
                if flagPrint:
                    print(f'Guaranteed win with move {move}')
                return move

        for _ in range(self.__rollout):
            self.__simulate(self.__currNode)
        
        bestN = -1
        candidate = []
        Sum = 0
        for move in validMoves:
            child = self.__currNode.getChild(move)
            Sum += child.Visit
            if flagPrint:
                print(f"Move {move}: {child.Statistic}")
            if child.Visit > bestN:
                candidate = [move]
                bestN = child.Visit
            elif child.Visit == bestN:
                candidate.append(move)
        if flagPrint:
            print('\n')
        if  np.all( self.__lastMoveStrate == 0):
            for move in validMoves:
                child = self.__currNode.getChild(move)
                N = child.Visit
                self.__lastMoveStrate[move.col] = N / Sum

        return random.choice(candidate)
    
    @property
    def lastMoveStrate(self):
        return self.__lastMoveStrate
    
    def MakeGameMove(self, move: Game.move = None, flagPrint = True):
        self.__initChild(self.__currNode)
        if self.__currNode.Pos.CurPlayer == self.__player:
            SelectedMove = self.searchBestMove( flagPrint= flagPrint)
            self.__currNode = self.__currNode.getChild(SelectedMove)
            if flagPrint:
                print(f'move Strate: {self.__lastMoveStrate}')
            return SelectedMove
        else:
            if move in self.__currNode.Pos.getValidMoves():
                self.__currNode = self.__currNode.getChild(move)
                return move
            else:
                raise ValueError("Invalid move")
    
    @property
    def npArrayPos (self):
        return self.__currNode.Pos.toNpArray()
    
    @property
    def CurrPlayer(self):
        return self.__currNode.Pos.CurPlayer
    
    @property
    def targetPlayer(self):
        return self.__player
    
    @property
    def Status(self):
        return self.__currNode.Pos.Status
    
    @property
    def quantPos(self):
        return len(self.__dictPos)
