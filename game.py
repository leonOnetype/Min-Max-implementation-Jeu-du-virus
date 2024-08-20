import pygame
from board import BoardManager
from tileManager import TileManager
from player import Player
from ia import IA
import constantes as cst
import numpy as np

pygame.mixer.music
pygame.mixer.init()


# Creer une class qui va representer notre jeu
class Game:

    def __init__(self):
        
        self._is_running = True
        
        self._is_gameEnd = False
        
        self._background_song_activate = False

        # Le gestionnaire du plateu
        self._board_manager = BoardManager()

        # Le plateau
        self._board = []

        # Le gestionnaire de tiles
        self._tile_manager = TileManager()

        # Les joueurs
        #-------------------------------(A gerer plustard de manaière automatique)
        self._player = Player()
        self._ia = IA()
        #------------------------------

        # Le font
        self._font = pygame.font.Font('freesansbold.ttf', 32)
        
        # Other attributes
        self._game_over_sound_path = None
        
        self._game_win_sound_path = None
        
        self._eat_sound_path = None
        
        self._invalide_move_sound_path = None
        

    def start(self, screen):
        """
        Configure tous les éléments du jeu à leurs valeurs par défaut et lance le jeu.
        """
        print("Initialisation des paramètres du jeu !!!! \n\n ")
        # Le type de tile de chaque joueur (A gérer plutard de facon dynamique)
        self._player.setTileType(cst.BLACK_TILE)
        self._ia.setTileType(cst.WHITE_TILE)
        
        # initialisation du plateau
        self._board = self._board_manager.initBoard(self._player.tile_type, self._ia.tile_type)

        # Affichage du plateau
        self._board_manager.drawLines(screen)
        self._tile_manager.drawTiles(screen, self._board)

        # Affichage des scores initiaux des joueurs
        self.__printScore__(screen)
        
        pygame.display.update()

            
    def update(self,screen):
        """
        Met à jour les éléments du jeu
        """

        # Actualisation du  plateau
        self._board_manager.drawLines(screen)
        self._tile_manager.drawTiles(screen, self._board)

        # Actualisation des scores des joueurs
        self.__printScore__(screen)

        
        # Actualisation de l'animation au cas ou si le jeu est terminé
        if self._is_gameEnd:
            self.showGameOVerOption(screen)
             
    
    def isRunning(self):
        return self._is_running

    def getPlayerNames(self): 
        return [self._player.name, self._ia.name]  
    
    def pushTitle(self, position, player_name, screen):
        """
        Traitement puis appel les fonctions de placement de tile pour le jouer appelant
        """
        
        # Si c'est l'IA
        if  player_name == self._ia.name:
            self._ia.pushTile(self._board, self._tile_manager, screen, self._eat_sound_path)

        # Si c'est le joueur
        elif player_name == self._player.name:
            
            # La identification de position  sur la grille 
            pos_on_board = self._board_manager.getLocationOnBoard(position)
            
            # Si c'est possible de push le pion on le fait 
            if self._tile_manager.is_possible_to_push_in(pos_on_board, self._board, self._player.tile_type):
                self._player.pushTile(pos_on_board, self._board, self._tile_manager, screen, self._eat_sound_path)
                return True
            
            # Sinon 
            else: 
                if self._invalide_move_sound_path != None:
                    pygame.mixer.music.load(self._invalide_move_sound_path)
                    pygame.mixer.music.play()
                return False
            
            
    def __printScore__(self, screen):
        """
        Calcule et affiche le score de chaque joueur.
        """
        
        # Calcul des points de chaque joueur(Le points d'un joueur est le nombre de pionts qu'il a sur le plateau)
        points = np.array([self._tile_manager.tilesCount(self._board, self._player.tile_type),
                self._tile_manager.tilesCount(self._board, self._ia.tile_type)])

        score_center = [(200, 50), (600, 50)]
        player_names = [self._player.name, self._ia.name]
        
        for i in range(len(player_names)):
            text_surface_obj = self._font.render(f"{player_names[i]}: {points[i]} points", True, cst.TEXT_COLOR)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = score_center[i]
            screen.blit(text_surface_obj, text_rect_obj)


    def __finishedState__(self, player):
        """
            Determine si la partie est terminer ou pas pour le joueur passé en paramètre.
        """
        
        tile_player_pos = self._tile_manager.findTilePos(self._board, player.tile_type)
        for pos in tile_player_pos:
            if len(self._tile_manager.findPossibleMoves(self._board, pos)) > 0:
                return False
        
        return True
    
        
    def __getPlayersFinishedState__(self):
        """
            Vérifie si le jeu est terminer. 
            NB: Le jeu sera dit terminer si le tableau est plein ou alors si un jour n'a plus de possibilités de
            poser un pion.
            
            Return type: Un dictionnaire dont les clés sont les noms des joueurs et les valeurs des booleens indiquant si je 
            joueur peut encore poser un pion ou pas.
        """
        
        player_finish_states = {self._player.name:self.__finishedState__(self._player), self._ia.name:self.__finishedState__(self._ia)}
        
        return player_finish_states


    
    def isGameEnd(self):
        """
            Regarde si la partie est fini ou pas.
        """
        # On recupère le finished state de chaque jouer
        player_finished_states =  self.__getPlayersFinishedState__()
        
        # Si y'a un joueur qui ne peu plus poser de pions alors le jeu est terminé
        if True in player_finished_states.values():
            # On met _is_gameEnd as true
            self._is_gameEnd = True
            return True
        
        
        return False
    

    def __getWinner__(self):
        """  
            Détermine et renvoie le gagant(son nom et son nombre de point)  de la partie
        """
        # On recupère le finished state de chaque jouer
        player_finished_states =  self.__getPlayersFinishedState__()
        
        # Calcul des points de chaque joueur
        points = {}

        for player_name, finished_state in player_finished_states.items():
            if player_name == self._ia.name:
                points[player_name] = self._tile_manager.tilesCount(self._board, self._ia.tile_type)
                if finished_state == False:
                    points[player_name] += self._board_manager.getNumberOfEmptySpace()
            elif player_name == self._player.name:
                points[player_name] = self._tile_manager.tilesCount(self._board, self._player.tile_type)
                if finished_state == False:
                    points[player_name] += self._board_manager.getNumberOfEmptySpace() 
       
        # Extraction du gagnant(il suffit d'ordonner la liste par valeur et prendre le premier élément)     
        points = dict(sorted(points.items(), key=lambda item:item[1]))
        winner = list(points.items())[1]
        
        return winner
    
      
    def showGameOVerOption(self, screen):
        """
            Affiche toutes informations de la fin de la partie(le nombre de points du gagnant, un petit méssage et 
            des options pour quitter ou pour faire une nouvelle partie).
        """
        
        # Affichage d'un petit filtre 
        rectangle = pygame.Surface((cst.WIN_WIDTH, cst.WIN_HEIGHT))
        rectangle.set_alpha(128)
        rectangle.fill((150, 150, 150))
        
        #  Le vainqueur (Ceci afin de le selectionner le bon texte à afficher)
        winner = self.__getWinner__()
        
        texte_to_draw = ""
        if winner[0] != self._ia.name:
            texte_to_draw = "Good job, you win the game!"
            # Lancement de la musique
            if self._game_win_sound_path != None and self._background_song_activate == False:
                pygame.mixer.music.load(self._game_win_sound_path)
                pygame.mixer.music.play(-1)        
                self._background_song_activate = True       
        else:
            texte_to_draw = "Game over! You lost the game"
            # Lancement de la musique
            if self._game_over_sound_path != None and self._background_song_activate == False:
                pygame.mixer.music.load(self._game_over_sound_path)
                pygame.mixer.music.play(-1)
                self._background_song_activate = True  
        
        # Affichage du texte de fin de partie
        text = self._font.render(texte_to_draw, True, cst.TEXT_COLOR)
        text_rect_obj = text.get_rect()
        text_rect_obj.center = (cst.WIN_WIDTH//2 , cst.WIN_HEIGHT//2 - 100)
        screen.blit(rectangle, (0,0))
        screen.blit(text, text_rect_obj)
        
        # Les boutons pour recommencer la partie ou quitter le jeu
        restart_button = TextButton(220, 300, 'Restart')
        exit_button = TextButton(500, 300, "Quit")
         
        restart_button.draw(screen)
        if restart_button.clicked() == True:
            # Réinitialisation du plateau
            self._board.clear()
            self._board = self._board_manager.initBoard(self._player.tile_type, self._ia.tile_type)
            # On signale que la partie n'est plus terminée
            self._is_gameEnd = False
            self._background_song_activate = False  
            
        exit_button.draw(screen)
        if exit_button.clicked() == True:
            self._is_running = False
            
    def setSoundPaths(self, game_over_sound_path, game_win_sound_path,  invalide_move_sound_path, eat_sound_path):
        self._game_over_sound_path = game_over_sound_path
        self._game_win_sound_path = game_win_sound_path
        self._invalide_move_sound_path = invalide_move_sound_path
        self._eat_sound_path = eat_sound_path
        
    def setPlayersName(self, player_name, ia_name="IA(Min-Max)"):
        self._player.setName(player_name)
        self._ia.setName(ia_name)
    
        
        
           
        
class TextButton():
    def __init__(self, x, y, text=""):
        self._text = text
        self._font = pygame.font.Font('freesansbold.ttf', 32)
        self._text_button = self._font.render(self._text, True, cst.TEXT_COLOR, cst.NORMAL_BUTTON_COLOR)
        self._hintRect = pygame.Rect(x, y, self._text_button.get_rect().width, self._text_button.get_rect().height)
        self._pos = (x, y)
        self._clicked = False
        
    def draw(self, screen):
        
        color = cst.NORMAL_BUTTON_COLOR
        
        # Position de la souris
        pos = pygame.mouse.get_pos()
        
        # Check mouseover and clicked conditions
        if self._hintRect.collidepoint(pos):
            color = cst.HOVER_BUTTON_COLOR
            if pygame.mouse.get_pressed()[0] == True:
                color = cst.CLIKED_BUTTON_COLOR
                self._clicked = True
        
        self._text_button = self._font.render(self._text, True, cst.TEXT_COLOR, color)  
        
        screen.blit(self._text_button, self._pos)
        
    def clicked(self):
        return self._clicked    
    
