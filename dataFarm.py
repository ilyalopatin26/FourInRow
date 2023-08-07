import numpy as np
from  FourInRow import Game
from MC_TreeSearch import MC_TreeSearcher
from   DataSet import DataSet


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
            move = Bot1.MakeGameMove( flagPrint = False)
            strate = Bot1.lastMoveStrate
            Bot2.MakeGameMove( move, flagPrint = False)
        else:
            move = Bot2.MakeGameMove( flagPrint = False)
            strate = Bot2.lastMoveStrate
            Bot1.MakeGameMove( move, flagPrint = False)
        
        history.append( ( move, strate) )
        status = Bot1.Status
        current_player = 3 - current_player
    
    print( Bot1.quantPos)
    print( Bot2.quantPos)


    return status, history

def playGameAndSave( DataSet: DataSet, seed, rollout , depth):
    status, history = playGame(seed, rollout, depth)
    print( len(history))
    print( [ it[0].col for it in history   ] )
    pos = Game()
    currPlayer = 1
    for it in history:
        if status == 0:
            DataSet.add( pos, it[1], 0)
        elif status == currPlayer:
            DataSet.add( pos, it[1], 1)
        else:
            DataSet.add( pos, it[1], -1)
        
        pos.get_and_MakeMove( it[0])
        currPlayer = 3 - currPlayer


DS = DataSet()

for i in range(1):
    playGameAndSave( DS, i, rollout = 1 , depth = 0)

DS.BuildDataSet()

print( len(DS.X) )

DS.save( 'dataSet.pkl' )

        