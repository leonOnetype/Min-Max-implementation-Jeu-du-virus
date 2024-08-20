import numpy as np
import time
import copy, random, time
import pygame.time
import constantes as cst
from player import Player

class IA(Player):
    def __init__(self, name=""):
        super().__init__(name)
        self.player_tile_type = ''
        

    def setTileType(self,tile_type):
            self.tile_type = tile_type
            if tile_type == cst.WHITE_TILE:
                self.color = cst.WHITE_COLOR
                self.player_tile_type = cst.BLACK_TILE
            if tile_type == cst.BLACK_TILE:
                self.color = cst.BLACK_COLOR
                self.player_tile_type = cst.WHITE_TILE
    
    # Effectue un deplacement. Dans la phase de recherche de la meilleur position, on n'a 
    # pas besoin d'afficher quoi que ce soit à l'écran ou alors de faire une animation.
    def __simulateMove__(self, position,  tile_type,  board, tileManager):
        """
        Simule le placement d'un pion
        
        return: un tableau numpy de points des joueurs
       ------------
        
       """
        # les points gagnés
        ia_points, player_points = [0, 0]
        
        # position ou poser le pion
        posX, posY  = position
        
        # On pose le pion
        board[posX][posY] = tile_type
        
        # actualisation de la valeur des points
        if tile_type == self.tile_type:
            ia_points +=1
        else:
            player_points += 1
            
        # Gestion de la contamination
        posNeighbors = tileManager.getPosNeighbors(position)
        for x, y in posNeighbors:
            if(board[x][y] != cst.EMPTY_SPACE and board[x][y] != cst.HELP_TILE and board[x][y] != tile_type):
                board[x][y] = tile_type
                if tile_type == self.tile_type:
                     ia_points +=1
                     player_points -= 1
                else:
                    player_points += 1
                    ia_points -=1
        return np.array([ia_points, player_points])
                               
    def __getFils__(self,board, tile_type, tileManager):
        """ Fonction qui cherhe les positions de tous les pions IA du plateau qui ont encore la 
        possbilité de jouer et qui renvoie les différents coups possibles liés a ces positions"""
        
        Fils = []
        for x in range(cst.BOARD_SIZE):
            for y in range(cst.BOARD_SIZE):
                if(board[x][y] == tile_type):
                    possibleMoves = tileManager.findPossibleMoves(board, (x,y))
                    if(len(possibleMoves) != 0):
                       Fils.append(possibleMoves) 
        Fils = np.array(Fils, dtype=list)
        random.shuffle(Fils)
        return Fils
    
    def __pushTile__(self, position, board, tile_manager, screen, eat_sound_path):
       super().pushTile(position, board, tile_manager, screen, eat_sound_path)
                

    def __saveBoard__(self,board):
        """ Fonction qui sauvegarde l'etat du jeu """
        boardCopy = copy.deepcopy(board)
        return boardCopy

    
    def pushTile(self, board, tile_manager, screen, eat_sound_path):
         position = self.__choix_miniMax__(board, tile_manager, cst.PROFONDEUR)
         # Make it look like the computer is thinking by pausing a bit.
         pauseUntil = random.randint(5, 10) * 0.1
         time.sleep(pauseUntil)
         return self.__pushTile__(position, board, tile_manager, screen, eat_sound_path)

    # ------------------------------ Algorithme minimax ------------------------------------
    ########################################################################################
    def __evaluation__(self, points):
        """ Fonction d'évaluation: C'est la différence entre le nombre de pions que de l'ia
         sur le plateau celui de l'adversaire """

        return points[0] - points[1]

    # Algorithme pour le max   
    def __Max__(self, coup_a_jouer, board, points, tile_manager, depth):
        """C'est une fonction récursive en fait il y'aura une recursibité mutuelle 
        # entre elle et la fonction Min
        # NB: le coup à jour est la position de la case ou on souhaite placer le pion """
        
        #Condition d'arret  
        if depth == 0:
            return self.__evaluation__(points)
        
        #Valeur temporaire du max
        m_max = float('-inf')
        
        # On sauvegarde le plateau
        copieBoard = self.__saveBoard__(board)
        
        # Simulation du jeu coté adversaire ie on pose pose son pion
        tmp_points = np.array(points)
        tmp_points +=self.__simulateMove__( coup_a_jouer, self.player_tile_type, copieBoard, tile_manager)
        
        # Etape 1:Fils des pions Ia ayant encore la possibilité de jouer 
        Fils = self.__getFils__(copieBoard, self.tile_type, tile_manager)

        # Etape 2
        for fils in Fils: 
            #Pour chaque coup, on fait jouer l'adversaire et on évalue la position
            # puis on s'arrage a prendre le max de ces évaluations et le coup qui le donne 
            for i in range(0, len(fils)):
                m_value = self.__Min__(fils[i], copieBoard, tmp_points, tile_manager, depth-1)
                if  m_value >= m_max:
                    m_max = m_value    
        return m_max
    
    # Algorithme pour le min    
    def __Min__(self, coup_a_jouer, board, points, tile_manager, depth):
        """C'est une fonction récursive en fait il y'aura une recursibité mutuelle 
         entre elle et la fonction Min
         NB: le coup à jour est la position de la case ou l'ia place son pion;
          En min c'est a l'adversaire de jouer apres le tour de l'IA  """

        if depth == 0:
            return self.__evaluation__(points)
        
        #Valeur temporaire du min
        m_min = float('inf')

        # On sauvegarde le plateau
        copieBoard = self.__saveBoard__(board)
        
        # Simulation du jeu coté de l'IA ie on pose pose son pion
        tmp_points = np.array(points)
        tmp_points += self.__simulateMove__(coup_a_jouer, self.tile_type, copieBoard, tile_manager)
        
        # Simulation du jeu  côté adversaire sur le tableau copié
        Fils = self.__getFils__(copieBoard, self.player_tile_type, tile_manager)
        for fils in Fils:
            for j in range(0,len(fils)):
                tmp_min = self.__Max__(fils[j], copieBoard, tmp_points,  tile_manager, depth-1)
                if tmp_min <= m_min:
                    m_min = tmp_min
        return m_min
    
    # Recherche  Minimax
    def __choix_miniMax__(self, board, tile_manager, depth):
        """Renvoie le meilleur choix trouvé par l'algorithme"""
        
        bestChoise = []
        tmp_value = float('-inf')
        
        # les points actuel des joueurs
        points = np.array([tile_manager.tilesCount(board, self.tile_type), tile_manager.tilesCount(board, self.player_tile_type)])
         
        debut = time.time()
        #  Etape 1: On repère tous les fils des pions de l'IA sur le plateau
        Fils = self.__getFils__(board, self.tile_type, tile_manager)
        # Etape 2
        for fils in Fils:
            # Etape 2-2: Pour chaque coup, on fait jouer l'adversaire et on évalue la position
            # puis on s'arrage a prendre le max de ces évaluations et le coup qui le donne 
            for j in range(0, len(fils)):
                m_value = self.__Min__(fils[j], board, points , tile_manager,  depth)
                if  m_value >= tmp_value:
                    tmp_value = m_value
                    bestChoise = fils[j]
                    
        print("############################################################""") 
        fin = time.time()
        print(f"Fonction miniMax. Le temps mis {fin - debut}")
        return bestChoise
    #---------------------------- MinMax fin ------------------------------------------
    ###################################################################################
    
    
    #--------------------------- Egalage alpha-beta -----------------------------------
    ##################################################################################
    
    
    #-------------------------- Egalage alpha-beta fin -------------------------------
    ##################################################################################