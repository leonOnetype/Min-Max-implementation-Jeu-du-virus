# Virus MIN-MAX: Un jeu de stratégie et de contamination
Ce jeu met au défi votre stratégie et votre capacité à contrôler le territoire. On joue ici contre une IA(Basé sur l'algorithme MIN-MAX). Le but du jeu est de convertir le plus de pions adverses à votre propre couleur en les contaminant.

## Le principe du jeu :

**Grille** : Le jeu se déroule sur une grille carrée, de taille variable.
**Pions** : Chaque joueur possède une couleur de pions, et le but est de convertir le plus de pions adverses à sa propre couleur.
**Contamination** : Un pion peut contaminer les pions adverses adjacents (les 8 cases au maximum autour de lui).
**Placement de pions** : Un joueur peut placer un pion sur une case vide uniquement si au moins un pion de sa couleur se trouve dans les 8 cases adjacentes à cette case.

## Le but du jeu :

Le but du jeu est de contrôler le plus de territoire possible en contaminant les pions adverses. Le joueur qui a le plus de pions de sa couleur à la fin du jeu remporte la partie.

**Quelques stratégies :**

Le jeu de virus nécessite une stratégie réfléchie. Les joueurs doivent :

- **Planifier leur placement de pions** : Ils doivent choisir des positions stratégiques pour maximiser la contamination et bloquer les mouvements adverses.
- **Créer des chaînes de pions :** En plaçant des pions adjacents de la même couleur, les joueurs peuvent créer des chaînes de contamination, permettant de convertir rapidement les pions adverses.
- **Isoler les pions adverses :** En entourant les pions adverses, les joueurs peuvent les empêcher de contaminer d'autres pions.

# L'intelligence artificielle :

Le jeu utilise un algorithme MIN-MAX pour simuler l'intelligence d'un adversaire. L'IA analyse les mouvements possibles et choisit celui qui maximise ses chances de gagner.

# Développement :

Le jeu Virus MIN-MAX a été développé en Python. Ce jeu a été développé pour explorer les possibilités de l'intelligence artificielle dans les jeux de société.


