import pygame, sys
from pygame.locals import *
import constantes as cst
from game import Game

import random


def main():
    
    # Intialisation de pygame
    pygame.init()

    # Création de la fénètre et définition du titre
    screen = pygame.display.set_mode(size=(cst.WIN_WIDTH, cst.WIN_HEIGHT))
    pygame.display.set_caption("Jeu du virus by Onetype")
 
    # Initialisation des éléments
    screen.fill(cst.BACKGROUND_COLOR) # On colorie l'écran en noir

    # Instantiation de la classe Game et initialisation du jeu
    game = Game()
    game.start(screen)

    
    # Paramètre de song
    eat_sound_path = 'datas/audio/bruitage/manger.mp3'
    invalide_move_sound_path = 'datas/audio/bruitage/jeu_non_valide.mp3'
    game_over_sound_path = 'datas/audio/bruitage/game_over.mp3'
    game_win_sound_path = 'datas/audio/bruitage/game_win.mp3' 
    game.setSoundPaths(game_over_sound_path, game_win_sound_path, invalide_move_sound_path, eat_sound_path)
    
    # Pramètre des joueurs
    #---------------------------------------------------------------------
    # Démander au joeur son nom et sont type de tile qu'il préfère et le
    # Paramétrer avec ces informations.-------->
    #---------------------------------------------------------------------
    player_names = ["Player1", "IA(Min-Max)"]
    game.setPlayersName(*player_names)
    
    # Extras
    # Gestion de la selection aléatoire d'un joueur au début de la partie.
    tmp_value = random.randint(0, len(player_names)-1)
    currentPlayerName = player_names[tmp_value]
    
    clock = pygame.time.Clock()

    while game.isRunning() == True:
        event = pygame.event.poll()

        # qui the window
        if event.type == pygame.QUIT:
            break  
        
        if game.isGameEnd() == False:
            if currentPlayerName == player_names[0]:

                # Handle if player have cliked
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    # Push if possible player tile
                    if game.pushTitle(event.pos, currentPlayerName, screen): 
                        tmp_value += 1 
                        currentPlayerName = player_names[tmp_value%len(player_names)]

            else:
                game.pushTitle(None, currentPlayerName, screen)
                tmp_value += 1 
                currentPlayerName = player_names[tmp_value%len(player_names)]
                
        
        else: # Le jeu est terminer pour un jouer
            tmp_value = random.randint(0, len(player_names)-1)
            currentPlayerName = player_names[tmp_value]

        # On éfface l'écran
        screen.fill(cst.BACKGROUND_COLOR)
        
        game.update(screen)
        
        pygame.display.update() # on met à jour l'écran


        clock.tick(cst.FPS)
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
    