from FourInRow import Game
from MC_TreeSearch import MC_TreeSearcher

human_player = 1

Bot = MC_TreeSearcher( 3-human_player, 20, 1)

while True:
    print( Bot.npArrayPos )
    print('  0, 1, 2, 3, 4, 5, 6' )
    if Bot.CurrPlayer == Bot.targetPlayer:
        Bot.MakeGameMove()
    else:
        c  = input("Enter your move: ")
        c = int(c)
        move = Game.move(  c )
        Bot.MakeGameMove( move )
    if Bot.Status != -1 :
        print( Bot.npArrayPos )
        if Bot.Status == 0:
            print('Draw')
        elif Bot.Status == human_player:
            print('You win')
        else:
            print('You lose')
        break
        
