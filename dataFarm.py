import numpy as np
from  FourInRow import Game
from MC_TreeSearch import MC_TreeSearcher
from   DataSet import DataSet

from copy import deepcopy


def playGame(seed, rollout , depth) :

    Bot1 = MC_TreeSearcher( 1,  rollout, depth, seed = seed)
    Bot2 = MC_TreeSearcher( 2,  rollout, depth, seed = seed+1)

    status = -1
    current_player = 1
    history = []

    while status == -1:
        move = None
        strate = None
        if current_player == 1:
            move, strate = Bot1.makeMoveWithStrate(flagPrint=False)     
            Bot2.MakeGameMove( move, flagPrint = False)
        else:
            move, strate = Bot2.makeMoveWithStrate(flagPrint= False)     
            Bot1.MakeGameMove( move, flagPrint = False)
        

        history.append( ( move, strate) )
        status = Bot1.Status
        current_player = 3 - current_player
        if Bot1.forcedWin :
            return 1, history
        if Bot2.forcedWin :
            return 2, history
    
    return status, history

def playGameAndSave( DataSet: DataSet, seed, rollout , depth):
    status, history = playGame(seed, rollout, depth)
    print( len(history))
    pos = Game()
    insertPos = deepcopy(pos)
    currPlayer = 1
    for it in history:
        if status == 0:
            DataSet.add( insertPos, it[1], 0)
        elif status == currPlayer:
            DataSet.add( insertPos , it[1], 1)
        else:
            DataSet.add( insertPos, it[1], -1)
        
        pos.get_and_MakeMove( it[0])
        insertPos = deepcopy(pos)
        currPlayer = 3 - currPlayer


DS = DataSet()

while DS.len < 200 :
    playGameAndSave( DS, 1 , rollout = 1 , depth = 1)

DS.BuildDataSet()

print( DS.len )
print( len(DS.X) )

DS.save( 'dataSet.pkl' )

        