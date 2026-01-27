# Virus MIN-MAX: A Strategy and Contamination Game
This game challenges your strategy and your ability to control territory. Here you play against an AI (Based on the MIN-MAX algorithm). The goal of the game is to convert as many opponent pieces as possible to your own color by contaminating them.
## Game Principle:
**Grid**: The game takes place on a square grid of variable size.
**Pieces**: Each player has a color of pieces, and the goal is to convert as many opponent pieces to their own color as possible.
**Contamination**: A piece can contaminate adjacent opponent pieces (up to 8 squares around it).
**Piece Placement**: A player can place a piece on an empty square only if at least one piece of their color is located in the 8 adjacent squares to that square.
## Game Objective:
The objective of the game is to control as much territory as possible by contaminating opponent pieces. The player who has the most pieces of their color at the end of the game wins the match.
**Some Strategies**:
The virus game requires thoughtful strategy. Players must:

**Plan their piece placement**: They must choose strategic positions to maximize contamination and block opponent moves.
**Create piece chains**: By placing adjacent pieces of the same color, players can create contamination chains, allowing them to quickly convert opponent pieces.
**Isolate opponent pieces**: By surrounding opponent pieces, players can prevent them from contaminating other pieces.

# Artificial Intelligence:
The game uses a MIN-MAX algorithm to simulate an opponent's intelligence. The AI analyzes possible moves and chooses the one that maximizes its chances of winning.
Development:
The Virus MIN-MAX game was developed in Python. This game was created to explore the possibilities of artificial intelligence in board games.
# Requirements:

numpy==2.0.1
pygame==2.6.0
