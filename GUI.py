from MC_TreeSearch import MC_TreeSearcher
from FourInRow import Game
import pygame
import sys
import math
import numpy as np

pygame.init()

SQUARESIZE = 100

BLUE = (0,0,255)
BLACK = ( 0, 0 ,0)
RED = (255,0,0)
YELLOW = (255,255,0)
width = 7 * SQUARESIZE
height = (6+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
myfont = pygame.font.Font( None, 75)

screen = pygame.display.set_mode(size)

humanPlayer = 2
Bot =  MC_TreeSearcher(3-humanPlayer, 20, 2, seed = 26)

def draw_board():
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    board = Bot.npArrayPos

    for c in range(7):
        for r in range(6):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


game_over = False

def game_end():
    global game_over
    flag = Bot.Status
    print(flag)
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
    pygame.display.update()
    draw_board()
    pygame.display.update()
    if flag == 0:
        label = myfont.render("Draw", 1, RED)
        screen.blit(label, (40,10))
    else:
        label = myfont.render( f'Player { flag } wins', 1, RED)
        screen.blit(label, (40,10))
    pygame.display.update()
    game_over = True

    print('Total visited position: ', Bot.quantPos )



while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
        draw_board()

        if Bot.Status != -1:
            game_end()
            break

        if Bot.CurrPlayer == 3-humanPlayer:
            mes = myfont.render("Bot's turn", 1, RED)
            screen.blit(mes, (40,10))
            pygame.display.update()
            Bot.MakeGameMove()
            draw_board()
            if Bot.Status != -1:
                game_end()
                break

        else:
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if humanPlayer == 1:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            draw_board()
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN :
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                Bot.MakeGameMove( Game.move(col) )
                draw_board()
                if Bot.Status != -1:
                    game_end()
                    break
        break

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()