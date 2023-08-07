import multiprocessing
from DataSet import DataSet
import numpy as np
from  FourInRow import Game
from MC_TreeSearch import MC_TreeSearcher
from copy import deepcopy

def playGame( args ) :
    seed, rollout , depth = args
    Bot1 = MC_TreeSearcher( 1,  rollout, depth, seed = seed)
    Bot2 = MC_TreeSearcher( 2,  rollout, depth, seed = seed+1)

    status = -1
    current_player = 1
    history = []

    while status == -1:
        move = None
        strate = None
        if current_player == 1:
            move, strate = Bot1.makeMoveWithStrate(flagPrint= False )     
            Bot2.MakeGameMove( move, flagPrint = False)
        else:
            move, strate = Bot2.makeMoveWithStrate(flagPrint=False)     
            Bot1.MakeGameMove( move, flagPrint = False)
        
        history.append( ( move.col , strate) )
        status = Bot1.Status
        current_player = 3 - current_player
        if Bot1.forcedWin :
            return 1, history
        if Bot2.forcedWin :
            return 2, history
    
    return status, history


def saveInDS( DS: DataSet, history, status ):
    pos = Game()
    insertPos = deepcopy(pos)
    currPlayer = 1

    for it in history:
        if status == 0:
            DS.add( insertPos, it[1], 0)
        elif status == currPlayer:
            DS.add( insertPos , it[1], 1)
        else:
            DS.add( insertPos, it[1], -1)
        
        pos.get_and_MakeMove( Game.move(it[0]) )
        insertPos = deepcopy(pos)
        currPlayer = 3 - currPlayer



if __name__ == '__main__':

    DS = DataSet()
    startSeed = 0

    while DS.len < 20 :
        W = multiprocessing.cpu_count()
        print(f'len: {DS.len}')
        arguments = [  ( startSeed+j , 15, 1 ) for j in range( W )  ]
        startSeed += (2*W + 1)

        with multiprocessing.Pool( processes=W) as pool :
            res = pool.map( playGame, arguments)
    
        for it in range( len(res) ):
            saveInDS(DS, res[it][1], res[it][0] )
        
    DS.BuildDataSet()
    DS.save( 'dataSet.pkl' )