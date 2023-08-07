import pickle

import numpy as np
from  FourInRow import Game


class DataObj:
    def __init__(self, res, moveStrate) -> None:
        self.res = res
        self.moveStrate = moveStrate
        self.N = 1
    
    def update(self, moveStrate, res: int):
        self.res  =  (self.N * self.res + res) / ( self.N + 1 )
        self.moveStrate  =  (self.N * self.moveStrate +  moveStrate) / ( self.N + 1 )
        self.N += 1

class DataSet:
    def __init__(self) :
        self.__Set = {}
        self.X = None
        self.Y = None
    
    def add(self, pos: Game, moveStrate, res: int):
        """
        res = 1: win current player
        res = 0: draw
        res = -1: loss
        """
        tempDataObj = self.__Set.get( pos, None )
        if tempDataObj is None:
            newDataObj = DataObj( res, moveStrate )
            self.__Set[pos] = newDataObj
        else:
            tempDataObj.update( moveStrate, res)
        
    
    def BuildDataSet( self):
        X, Y = [], []
        for pos, data in self.__Set.items():
            X.append(  pos.toNpArray() )
            Y.append( ( data.res,  data.moveStrate  ) )
        self.X = X
        self.Y = Y
    
    def save(self,  filename ):
        with open(filename, "wb") as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    @property
    def len(self):
        return len(self.__Set)
    


