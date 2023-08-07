import pickle

import numpy as np
from  FourInRow import Game


class DataObj:
    def __init__(self, res, moveStrate) -> None:
        self.res = res
        self.moveStrate = moveStrate
        self.__alpha = 0.1
    
    def update(self, moveStrate, res: int):
        self.res  = (1-self.__alpha) * self.res + self.__alpha * res
        self.moveStrate  = (1-self.__alpha) * self.moveStrate + self.__alpha * moveStrate

class DataSet:
    def __init__(self) :
        self.Set = {}

    
    def add(self, pos: Game, moveStrate, res: int):
        """
        res = 1: win current player
        res = 0: draw
        res = -1: loss
        """
        tempDataObj = self.Set.get( pos, None )
        if tempDataObj is None:
            newDataObj = DataObj( res, moveStrate )
            self.Set[pos] = newDataObj
            print(0)
        else:
            tempDataObj.update( moveStrate, res)
            print(1)
        
    
    def BuildDataSet( self):
        X, Y = [], []
        for pos, data in self.Set.items():
            X.append(  pos.toNpArray() )
            Y.append( ( data.res,  data.moveStrate  ) )
        self.X = X
        self.Y = Y
    
    def save(self,  filename ):
        with open(filename, "wb") as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
    


