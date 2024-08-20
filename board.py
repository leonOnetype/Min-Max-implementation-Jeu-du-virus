import pygame
import constantes as cst


class BoardManager():

    def __init__(self):
        self.nbLines = cst.BOARD_SIZE
        self.nbColumns = cst.BOARD_SIZE
        self.board = []


    # Initialise le tableau
    def initBoard(self, player1_tile_type, player2_tile_type):
        for x in range(self.nbLines):
            self.board.append([cst.EMPTY_SPACE]*self.nbLines)
            
        # Les pions par defaut sur la grille
        self.board[0][0] = cst.BLACK_TILE
        self.board[self.nbLines-1][self.nbColumns-1] = player1_tile_type
        self.board[0][self.nbColumns-1] = player2_tile_type
        self.board[self.nbLines-1][0] = player2_tile_type
        
        self.board[self.nbLines//2 - 2][self.nbColumns//2 - 2] = player2_tile_type
        self.board[self.nbLines//2 - 2][self.nbColumns//2 + 2] = player1_tile_type
        self.board[self.nbLines//2 + 2][self.nbColumns//2 - 2] = player1_tile_type
        self.board[self.nbLines//2 + 2][self.nbColumns//2 + 2] = player2_tile_type
        
        return self.board


    # Affiche les lignes
    def drawLines(self,screen):
        # Les lignes horizontales
        for x in range(self.nbLines+1):
            startx = cst.X_MARGING
            starty = cst.Y_MARGIN +(cst.SPACE_SIZE*x)
            endx = cst.X_MARGING +(cst.SPACE_SIZE*self.nbLines)
            endy =  cst.Y_MARGIN +(cst.SPACE_SIZE*x)
            pygame.draw.line(screen,cst.BLACK_COLOR, (startx,starty),(endx,endy))
        
        # Les lignes verticales
        for y in range(self.nbColumns+1):
            startx = cst.X_MARGING + (cst.SPACE_SIZE*y)
            starty = cst.Y_MARGIN
            endx = cst.X_MARGING +(cst.SPACE_SIZE*y)
            endy =  cst.Y_MARGIN +(cst.SPACE_SIZE*self.nbColumns)
            pygame.draw.line(screen,cst.BLACK_COLOR, (startx,starty),(endx,endy))

    def getLocationOnBoard(self, clicked_pos):
        """renvoie la position de souris sur la grille"""
        xMouse, yMouse = clicked_pos
        for x in range(self.nbLines):
            for y in range(self.nbColumns):                               
                if (xMouse > cst.X_MARGING + cst.SPACE_SIZE*x) and (xMouse < cst.X_MARGING + cst.SPACE_SIZE*(x+1)):
                    if (yMouse > cst.Y_MARGIN + cst.SPACE_SIZE*y) and (yMouse < cst.Y_MARGIN + cst.SPACE_SIZE*(y+1)):
                        return(x,y)
                    
        # Au cas on click a l'exterieur du tableau, on se positionne très hors du tableau
        # pour éviter tout traitement
        return (-2, -2)  
    
    
    def getNumberOfEmptySpace(self):
        """
            Renvoir le nombre de case vide dans le tableau
        """
        compteur = 0
        for x in range(self.nbLines):
            for y in range(self.nbColumns):
                if self.board[x][y] == cst.EMPTY_SPACE:
                    compteur +=1 
                    
        return compteur

        


        

