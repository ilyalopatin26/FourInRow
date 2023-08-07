import numpy as np
import pickle

from DataSet import DataSet, DataObj
from FourInRow import Game

Set = DataSet()

with open("dataSet.pkl", "rb") as f:
    Set = pickle.load(f)

n = 90
print( Set.X[n] )
print( Set.Y[n] )
print( f'sum: { np.sum(Set.Y[n][1])}' )

print( Set.len )