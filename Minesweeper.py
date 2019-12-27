# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 22:17:02 2019

@author: Cong Feng
"""

import numpy as np
import random
import pygame
import time
import os



def creategrid(rows, cols, bombs):
    # Input: no. of rows (int), cols (int), bombs (int)
    # Output: grid with specified rows, cols, bombs (array) + winning condition grid
    
    grid = np.array([0]*rows*cols)
    grid = np.reshape(grid,(rows,cols))
    wincond = np.array([1]*rows*cols)
    wincond = np.reshape(wincond,(rows,cols))
    bombloc = random.sample(range(rows*cols), bombs)
    for bombloc in bombloc:
        grid[bombloc//cols][bombloc%cols] = 9
        wincond[bombloc//cols][bombloc%cols] = 0
        neighborhood = neighbors(grid, bombloc//cols, bombloc%cols)
        for tile in neighborhood:
            if grid[tile[0]][tile[1]]<9:
                grid[tile[0]][tile[1]] += 1
    
    return grid, wincond

def neighbors(grid, rpos, cpos):
    # Input: grid (array), rpos of tile (int), cpos of tile (int)
    # Output: list of (rpos, cpos) of neighbours
    
    neighbors = []
    rows, cols = grid.shape
    if rpos != rows-1:
        neighbors.append((rpos+1, cpos))
    if rpos != 0:
        neighbors.append((rpos-1, cpos))
    if cpos != cols-1:
        neighbors.append((rpos, cpos+1))
    if cpos != 0:
        neighbors.append((rpos, cpos-1))
    if rpos != rows-1 and cpos != cols-1:
        neighbors.append((rpos+1, cpos+1))
    if rpos != 0 and cpos != cols-1:
        neighbors.append((rpos-1, cpos+1))
    if rpos != rows-1 and cpos != 0:
        neighbors.append((rpos+1, cpos-1))
    if rpos != 0 and cpos != 0:
        neighbors.append((rpos-1, cpos-1))
    
    return neighbors


def Game(rows = 8, cols = 8, bombs = 10, sqsize = 50):
    
    def Open(rpos, cpos): #Cover the tile with a white surface, then cover that with the number 
        
        pygame.draw.rect(screen,(192,192,192),pygame.Rect(cpos*sqsize+2,rpos*sqsize+52,sqsize-3,sqsize-3))
        font = pygame.font.Font(None, 60)
        if grid[rpos][cpos] != 0:
            textsurface = font.render(str(grid[rpos][cpos]), True, colordict[grid[rpos][cpos]])
            text_width, text_height = textsurface.get_width(), textsurface.get_height()
            screen.blit(textsurface, (cpos*sqsize + sqsize//2 - text_width//2, rpos*sqsize + sqsize//2 - text_height//2 + 50))
        pygame.display.update()
    
    def Flag(rpos, cpos): #Cover the tile with a flag sprite
        
        flag = pygame.image.load(os.path.join('flag.png'))
        flag = pygame.transform.scale(flag,(sqsize-3,sqsize-3))
        screen.blit(flag, (cpos*sqsize+2, rpos*sqsize + 52))
        pygame.display.update()
        
    def finish(win): #Update screen when gameplay ends
        
        font = pygame.font.Font(None, 60)
        if win:
            fintext = font.render("Congratulations!", True, (0,0,0), (255,255,255))
        else:
            bomb = pygame.image.load(os.path.join('bomb.png'))
            bomb = pygame.transform.scale(bomb,(sqsize-3,sqsize-3))
            screen.blit(bomb, (i*sqsize+2, j*sqsize + 52))
            fintext = font.render("You lose.", True, (0,0,0), (255,255,255))
        text_width, text_height = fintext.get_width(), fintext.get_height()
        screen.blit(fintext, (width//2 - text_width//2, height//2 - text_height//2 + 50))
        pygame.display.update()
        
    def clock(): #Timer for the game
        
        font = pygame.font.Font(None, 70)
        timetext = font.render("{:.2f}".format(time.time() - startTime), True, (0,0,0), (255,255,255))
        screen.blit(timetext, (0,0))
        pygame.display.update()
        
    def zeroes(grid, rpos, cpos, opened = set()):
        # Input: grid (array), rpos of zero (int), cpos of zero (int)
        # Output: list of (rpos, cpos) of all things that are supposed to be opened
        
        opened.update({(rpos,cpos)})
        for tile in neighbors(grid,rpos,cpos):
            if grid[tile[0],tile[1]] == 0 and tile not in opened:
                opened.update(zeroes(grid,tile[0],tile[1],opened))
                
            else:
                opened.update({(tile[0],tile[1])})
                continue
        return opened
    
    grid, wincond = creategrid(rows, cols, bombs)
    print(grid)
    winstate = np.array([0]*rows*cols)
    winstate = np.reshape(winstate,(rows,cols))
    width = cols*sqsize
    height = rows*sqsize
    colordict = {1:(1,0,254), 2:(1,127,1), 3:(254,0,0), 4:(1,0,128), 5:(129,1,2), 6:(0,127,126), 7:(0,0,0), 8:(128,128,128)}
    
    pygame.init()
    screen = pygame.display.set_mode((width, height+50))
    screen.fill((192,192,192))
    pygame.display.set_caption("Feng's Minesweeper")
    
    for i in range(0,cols+1): #Draw vertical lines
        pygame.draw.line(screen,(128,128,128),(i*sqsize,50),(i*sqsize,height+50),3)
    for i in range(0,rows+1): #Draw horizontal lines
        pygame.draw.line(screen,(128,128,128),(0,i*sqsize+50),(width,i*sqsize+50),3)
    
    for i in range(cols): #Adding tile sprites
        for j in range(rows):
            tile = pygame.image.load(os.path.join('tile.png'))
            tile = pygame.transform.scale(tile,(sqsize-3,sqsize-3))
            screen.blit(tile, (i*sqsize+2, j*sqsize + 52))
        
    pygame.display.update()

    done = False #For quitting the display
    ended = False #To stop collecting input
    timerstart = False # To display timer only after 1st click
    
    while not done: #Loop for the main window
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #Quit the game at the end upon clicking red X
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
                Game(rows,cols,bombs,50)
                ended = True
                done = True
                
        while not ended: # Loop for gameplay                    
            if timerstart:
                clock()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Quit the game during the gameplay upon clicking red X
                    ended = True
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
                    Game(rows,cols,bombs,50)
                    ended = True
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #If left mouse button is pressed
                    
                    x, y = pygame.mouse.get_pos()
                    
                    if y>50:
                        if not timerstart:
                            startTime = time.time()
                            timerstart = True
                        i,j = x//sqsize, (y-50)//sqsize
                        if winstate[j][i] == 0:
                            if grid[j][i] == 9: #If bomb is opened
                                finish(0)
                                ended = True
                            elif grid[j][i] == 0: #If empty tile is opened
                                for tile in zeroes(grid,j,i):
                                    Open(tile[0],tile[1])
                                    winstate[tile[0]][tile[1]] = 1
                            else: #If number tile is opened
                                Open(j,i)
                                winstate[j][i] = 1
                        if winstate[j][i] == 1 and grid[j][i] not in (0,9): #Chording
                            nearbombs = 0
                            getopened = neighbors(grid,j,i).copy()
                            for chord in neighbors(grid,j,i):
                                if winstate[chord[0]][chord[1]] == -1:
                                  nearbombs += 1
                                  getopened.remove(chord)
                            if nearbombs == grid[j][i]:
                                for j,i in getopened:
                                    if winstate[j][i] == 0:
                                        if grid[j][i] == 9: #If bomb is opened
                                            finish(0)
                                            ended = True
                                        elif grid[j][i] == 0: #If empty tile is opened
                                            for tile in zeroes(grid,j,i):
                                                Open(tile[0],tile[1])
                                                winstate[tile[0]][tile[1]] = 1
                                        else: #If number tile is opened
                                            Open(j,i)
                                            winstate[j][i] = 1
                            
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    if y>50:
                        if not timerstart:
                            startTime = time.time()
                            timerstart = True
                        i,j = x//sqsize, (y-50)//sqsize
                        if winstate[j][i] == 0:
                            Flag(j,i)
                            winstate[j][i] = -1
                        elif winstate[j][i] == -1:
                            tile = pygame.image.load(os.path.join('tile.png'))
                            tile = pygame.transform.scale(tile,(sqsize-3,sqsize-3))
                            screen.blit(tile, (i*sqsize+2, j*sqsize + 52))
                            winstate[j][i] = 0
                            
                elif np.array_equal(np.where(winstate==1), np.where(wincond==1)): #If win condition satisfied
                    finish(1)
                    ended = True
    pygame.display.quit()
    
    
    

# %% Play Game
'''
while True:
    try:
        rows, cols, bombs = map(int,input("Enter number of rows, columns, and bombs (separated by a comma): ").split(","))
        if rows>0 and cols>0 and bombs>=0 and bombs<=rows*cols:
            break
        else:
            print("Try again.")
    except ValueError:
        print("Try again.")

        
Game(rows, cols, bombs, 50)
'''
Game()
