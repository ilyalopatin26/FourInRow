import numpy as np
import pickle

from DataSet import DataSet, DataObj
from FourInRow import Game

Set = DataSet()

with open("dataSet.pkl", "rb") as f:
    Set = pickle.load(f)


print( Set.X[4] )
print( Set.Y[4] )

print( Set.len )