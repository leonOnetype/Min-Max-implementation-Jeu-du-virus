import pygame.time
import constantes as cst


class Player():
    def __init__(self, name=""):
        self.name = name
        self.tile_type = ''
        self.color = (0, 0, 0)
        self.score = 4
        self.pos_mutate_tile = {}

    def setTileType(self,tile_type):
            self.tile_type = tile_type
            if tile_type == cst.WHITE_TILE:
                self.color = cst.WHITE_COLOR
            if tile_type == cst.BLACK_TILE:
                self.color = cst.BLACK_COLOR
                
    def setName(self,name):
        self.name = name
        
    
    def pushTile(self, position, board, tile_manager, screen, eat_sound_path):
        """push a tile on the board"""

        try:
            posX, posY = position
        except ValueError:
            return
        
        # on place le pion  
        board[posX][posY] = self.tile_type
        tile_manager.drawTile(screen, (posX, posY), self.color)
            
            
        # Gestion de la contamination
        # Détermination des voisins
        posNeighbors = tile_manager.getPosNeighbors((posX, posY))
        
        # sauvegarde du nombre de points du joueur
        for x, y in posNeighbors:
            if(board[x][y] != cst.EMPTY_SPACE and board[x][y] != cst.HELP_TILE and board[x][y] != self.tile_type):

                board[x][y] = self.tile_type
                tile_manager.animContamination(screen, (x,y), self.tile_type)
                if eat_sound_path != None:
                    pygame.mixer.music.load(eat_sound_path)
                    pygame.mixer.music.play()
                self.score += 1
            
        # le point du pion posé
        self.score +=1
        
                              
