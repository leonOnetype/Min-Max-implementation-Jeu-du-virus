import pygame
import numpy as np
import constantes as cst

class TileManager():
    def __init__(self):
        self.animFPS = cst.FPS
        self.clock = pygame.time.Clock()

    def tilePosition(self,x,y):
        return (cst.X_MARGING + cst.SPACE_SIZE*x + cst.SPACE_SIZE/2, 
                cst.Y_MARGIN + cst.SPACE_SIZE*y+cst.SPACE_SIZE/2)
    
    def imagePosition(self,x,y):
        return (cst.X_MARGING + cst.SPACE_SIZE*x, 
                cst.Y_MARGIN + cst.SPACE_SIZE*y)
    
    def drawTiles(self,screen,board):
        """
            Affiche tous les titles du tableau board passé en paramètre
        """
        for x in range(cst.BOARD_SIZE):
            for y in range(cst.BOARD_SIZE):
                if(board[x][y] == cst.BLACK_TILE):
                    pygame.draw.circle(screen, cst.BLACK_COLOR, self.tilePosition(x,y), cst.RADIUS)    
                elif(board[x][y] == cst.WHITE_TILE):
                    pygame.draw.circle(screen, cst.WHITE_COLOR, self.tilePosition(x,y), cst.RADIUS)     
                elif(board[x][y] == cst.HELP_TILE):
                    pygame.draw.circle(screen, cst.HELP_COLOR, self.tilePosition(x,y), cst.RADIUS, 1)
                elif(board[x][y] == cst.PLAYER_MUTATE_TILE):
                    pygame.draw.circle(screen, cst.PLAYER_MUTATE_COLOR, self.tilePosition(x,y), cst.RADIUS)
                elif(board[x][y] == cst.IA_MUTATE_TILE):
                    pygame.draw.circle(screen, cst.IA_MUTATE_COLOR, self.tilePosition(x,y), cst.RADIUS)

    def drawTile(self, screen, pos, tileType):
        """
            Affiche un tile de type passé en paramètre et à la position passée aussi en paramètre
        """
        pygame.draw.circle(screen, tileType, self.tilePosition(*pos), cst.RADIUS)
        
                    
    def animContamination(self, screen, posTarget, tileTarget):
        """
            Animation de la contamination du jouer adverse
        """
       
        for rgbValues in range(0, 255, int(cst.ANIMATIONSPEED * 2.55)):
            if rgbValues > 255:
                rgbValues = 255
            elif rgbValues < 0:
                rgbValues = 0
                
            if tileTarget == cst.WHITE_TILE or cst.IA_MUTATE_COLOR:
                color = tuple([rgbValues, 0, 0]) # rgbValues goes from 0 to 255
            elif tileTarget == cst.BLACK_TILE or cst.PLAYER_MUTATE_COLOR:
                color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

            l, c = posTarget
            x, y = self.tilePosition(l, c)
            pygame.draw.circle(screen, color, (x, y), cst.RADIUS)
            pygame.display.update()
            self.clock.tick(self.animFPS)
   
    def is_possible_to_push_in(self, position, board,  tileType):
        """
            Elle regarde si avant de poser un pion d'une couleur donnée il y'a une couleur de ce type
            dans les environs
        """
        #on determine la position sur la grille du pion
        posX, posY  = position
        axisMoves = [[0,-1],[0,1],[-1,0],[1,0],[-1,-1],[-1,1],[1,-1],[1,1]]
        
        if (posX >= 0 and posX < cst.BOARD_SIZE) and (posY >= 0 and posY < cst.BOARD_SIZE):
            if board[posX][posY] != cst.EMPTY_SPACE and board[posX][posY] != cst.HELP_TILE:
                return False   
        for x, y in axisMoves:
            x += posX
            y += posY
            if x >=0 and x < cst.BOARD_SIZE and y >= 0 and y < cst.BOARD_SIZE :
                if(board[x][y] == tileType):
                    return True 
        return False
            
    def findPossibleMoves(self, board, position):
        """
            Renvoile la liste de coups possibles pour une position donnée
        """
        
        posX, posY  = position
        possibleMoves = []
        axisMoves = [[0,-1],[0,1],[-1,0],[1,0],[-1,-1],[-1,1],[1,-1],[1,1]]
        # Genere les positions possibles
        for x,y in axisMoves:
            x += posX
            y += posY 
            if x >=0 and x < cst.BOARD_SIZE and y >= 0 and y < cst.BOARD_SIZE :
                if(board[x][y] == cst.EMPTY_SPACE or board[x][y] == cst.HELP_TILE):
                    possibleMoves.append([x,y])
       
        return np.array(possibleMoves)
    
    def getPosNeighbors(self, position):
        """
            Retourne les positions des case voisines à cele situé en Pos
        """
        posNeighbors = []
        posX, posY = position
        # Les differents deplacements possible
        axisMoves = [[0,-1],[0,1],[-1,0],[1,0],[-1,-1],[-1,1],[1,-1],[1,1]]
        # Genere les positions possibles
        for x,y in axisMoves:
            x += posX
            y += posY 
            if x >=0 and x < cst.BOARD_SIZE and y >= 0 and y < cst.BOARD_SIZE :
                posNeighbors.append((x,y))
        return np.array(posNeighbors)
    
    
    def findTilePos(self, board, tileType):
        """
            Retourne toutes les positions possibles des pions d'une couleur donné
        """
        
        posTiles = [] 
        for x in range(cst.BOARD_SIZE):
            for y in range(cst.BOARD_SIZE):
                if board[x][y] == tileType:
                    posTiles.append([x,y])
        return np.array(posTiles)
    
      
    def tilesCount(self, board, title_type):
        """
            Retourne le nombre de pions de chaque type présent sur le plateau.
        """
        count = 0

        for x in range(cst.BOARD_SIZE):
            for y in range(cst.BOARD_SIZE):
                if board[x][y] == title_type:
                    count += 1
                    
        return count
    
    
    def getHelp(self, player, board):
    
        """
        Pour gérer l'affichage de l'aide au joueur
        """
        posTiles = self.findTilePos(board, player.tile_type) # Les case voisines
            
        for i in range(0, len(posTiles)):
                possiblePush = self.findPossibleMoves(board, posTiles[i]) # On cherche celles libres 
                t = len(possiblePush)
                if t != 0: # S'il y'a en a on met le tile d'aide
                    for j in range(0, t):
                        l,c = possiblePush[j]
                        board[l][c] = cst.HELP_TILE
                     
    def cleanHint(self, board):
        """
            Efface les indices affcihées sur la tableau
        """
        for x in range(cst.BOARD_SIZE):
            for y in range(cst.BOARD_SIZE):
                if board[x][y] == cst.HELP_TILE:
                    board[x][y] = cst.EMPTY_SPACE   
    
    
    
   