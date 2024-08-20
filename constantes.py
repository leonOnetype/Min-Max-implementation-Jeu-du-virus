# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# parametres de la fenetre 
WIN_WIDTH   =  800
WIN_HEIGHT  = 600

# parametres des tiles
SPACE_SIZE  =  60
BOARD_SIZE  = 7

# parametres pour le décalage de la grille l'ors de l'affichage
X_MARGING   = (WIN_WIDTH - BOARD_SIZE*SPACE_SIZE)/2
Y_MARGIN    = (WIN_HEIGHT - BOARD_SIZE*SPACE_SIZE)/2

# Parametres pour l'animation de la contamination entre les pions
ANIMATIONSPEED = 25
MARGE = 3
RADIUS = SPACE_SIZE/2 -MARGE

# paramètre de temps pour la destruction d'un pion muté
MUTATION_TIME = 500  # 10 secondes

# Frame per second
FPS = 40


# parametres pour la gestion des tiles dans le tableau
EMPTY_SPACE = 'VIDE'
HELP_TILE = 'HELP_TILE'

BLACK_TILE  = 'BLACK_TILE'
ROSE_TILE   = 'ROSE_TILE'
WHITE_TILE = 'WHITE_TILE'
PLAYER_MUTATE_TILE = 'PLAYER_MUTATE_TILE'
IA_MUTATE_TILE = 'IA_MUTATE_TILE'

# le nombre de pions à contaminer pour déclancher une mutation
MIN_TILE_FOR_MUTATION = 8


# Pack de couleurs pour la gestion des tiles
BLACK_COLOR            = (0,   0,    0)
ROSE_COLOR             = (255, 0,   255)
HELP_COLOR             = (0, 16,   0)
WHITE_COLOR            = (255, 255, 255)
PLAYER_MUTATE_COLOR    = (125, 125, 125)
IA_MUTATE_COLOR        = (0,    0,   255)


# Pack de couleurs pour la gestion de l'affichage des textes et des bouttons
TEXT_COLOR     = (0, 0, 0)
NORMAL_BUTTON_COLOR = (255, 100, 100)
HOVER_BUTTON_COLOR = (100, 255, 100)
CLIKED_BUTTON_COLOR = (100, 100, 255)

# pack de couleur pour le background et le frontground
BACKGROUND_COLOR = (100,  100,    100)
FRAME_BACKGROUND_COLOR = "#EDFDED"
FRAME_FONTGROUND_COLOR =  "#06283D"



# profondeur de l'algorithme
PROFONDEUR = 2