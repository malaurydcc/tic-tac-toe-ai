# Importation des modules nécessaires
import copy
import sys
import pygame
import random
import numpy as np
from constants import *

# --- CONFIGURATION DE PYGAME ---

pygame.init()  # Initialise tous les modules Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crée la fenêtre du jeu
pygame.display.set_caption('TIC TAC TOE AI')  # Définit le titre de la fenêtre
screen.fill(BG_COLOR)  # Remplit l'écran avec la couleur de fond

# --- CLASSES ---

# Classe représentant le tableau de jeu
class Board:

    # Initialisation du tableau de jeu (une matrice 3x3 remplie de zéros)
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))  # Création du tableau avec des zéros
        self.empty_squares = self.squares  # Stockage des cases vides
        self.marked_squares = 0  # Compteur pour le nombre de cases marquées

    # Fonction pour vérifier l'état final du jeu (victoire ou non)
    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''
        # Vérifie les colonnes pour une victoire verticale
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:  # Si activé, dessine une ligne pour montrer la victoire
                    color = CROSS_COLOR if self.squares[0][col] == 2 else CIRCLE_COLOR
                    iPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    fPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # Vérifie les lignes pour une victoire horizontale
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CROSS_COLOR if self.squares[row][0] == 2 else CIRCLE_COLOR
                    iPos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    fPos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # Vérifie la diagonale descendante pour une victoire
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CROSS_COLOR if self.squares[1][1] == 2 else CIRCLE_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # Vérifie la diagonale ascendante pour une victoire
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CROSS_COLOR if self.squares[1][1] == 2 else CIRCLE_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # Si aucun joueur n'a gagné, retourne 0
        return 0

    # Marque une case spécifique pour un joueur (1 pour cercle, 2 pour croix)
    def mark_square(self, row, col, player):
        self.squares[row][col] = player  # Place le symbole du joueur dans la case
        self.marked_squares += 1  # Incrémente le compteur de cases marquées

    # Vérifie si une case est vide
    def empty_square(self, row, col):
        return self.squares[row][col] == 0  # Retourne True si la case est vide
    
    # Retourne une liste des cases vides restantes
    def get_empty_squares(self):
        empty_squares = [(row, col) for row in range(ROWS) for col in range(COLS) if self.empty_square(row, col)]
        return empty_squares
    
    # Vérifie si le plateau est plein
    def isfull(self):
        return self.marked_squares == 9  # Retourne True si toutes les cases sont marquées
    
    # Vérifie si le plateau est vide
    def isempty(self):
        return self.marked_squares == 0  # Retourne True si aucune case n'est marquée

# Classe représentant l'intelligence artificielle
class AI:
    
    def __init__(self, level=1, player=2):
        self.level = level  # Niveau de difficulté de l'IA (0 = facile, 1 = difficile)
        self.player = player  # Définit quel joueur est contrôlé par l'IA

    # --- NIVEAU ALEATOIRE (facile) ---   

    # Choisit une case vide au hasard
    def rnd(self, board):
        empty_squares = board.get_empty_squares()  # Récupère les cases vides
        idx = random.randrange(0, len(empty_squares))  # Choisit une case au hasard
        return empty_squares[idx]  # Retourne la case choisie (ligne, colonne)

    # --- ALGORITHME MINIMAX (difficile) ---

    # Fonction minimax pour trouver le meilleur coup possible
    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        if board.isfull():
            return 0, None

        best_move = None
        if maximizing:
            max_eval = -float('inf')
            for (row, col) in board.get_empty_squares():
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval, best_move = eval, (row, col)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for (row, col) in board.get_empty_squares():
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval, best_move = eval, (row, col)
            return min_eval, best_move

    # Évalue le prochain coup de l'IA en fonction de son niveau
    def eval(self, main_board):
        if self.level == 0:  # Si le niveau est facile (0), IA choisit un coup aléatoire
            eval = 'random'
            move = self.rnd(main_board)
        else:  # Si le niveau est difficile (1), IA utilise l'algorithme minimax
            eval, move = self.minimax(main_board, False)
            print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move  # Retourne le mouvement sélectionné

# Classe représentant le jeu principal
class Game:
     
    def __init__(self):
        self.board = Board()  # Initialisation du plateau de jeu
        self.ai = AI()  # Création d'une instance de l'IA
        self.player = 1  # Début du jeu avec le joueur 1 (cercle)
        self.gamemode = 'ai'  # Mode par défaut: joueur vs IA
        self.running = True  # État du jeu actif
        self.show_lines()  # Affichage des lignes du plateau

    # Fonction pour dessiner les lignes du plateau
    def show_lines(self):
        screen.fill(BG_COLOR)  # Remplit l'écran avec la couleur de fond

        # Dessin des lignes verticales
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        # Dessin des lignes horizontales
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

    # Fonction pour dessiner les figures (cercles et croix) sur le plateau
    def draw_figures(self, row, col):
        if self.player == 1:
            # Dessin du cercle
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
        elif self.player == 2:
            # Dessin de la croix
            start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

    # Fonction pour effectuer un mouvement
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)  # Marque la case pour le joueur actuel
        self.draw_figures(row, col)  # Dessine la figure correspondante sur la case
        self.next_turn()  # Passe au joueur suivant

    # Alterne entre les joueurs (1 ou 2)
    def next_turn(self):
        self.player = 3 - self.player

    # Change le mode de jeu (IA ou PvP)
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'  # Alterne entre les deux modes

    # Vérifie si le jeu est terminé
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()  # Retourne True si le jeu est terminé

    # Réinitialise le jeu
    def reset(self):
        self.__init__()  # Réinitialise tous les paramètres du jeu


# --- ÉCRAN DE DÉMARRAGE ---
def start_screen():
    screen.fill(BG_COLOR)  # Remplit l'écran avec la couleur de fond
    font = pygame.font.SysFont(None, 60)
    title = font.render("TIC TAC TOE", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    # Instructions de sélection du mode de jeu
    font_small = pygame.font.SysFont(None, 40)
    options = ["1. Player vs Player", "2. Player vs Easy AI", "3. Player vs Hard AI"]
    for i, option in enumerate(options):
        text = font_small.render(option, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 50))
    
    pygame.display.update()  # Met à jour l'écran
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # PvP
                    return 'pvp'
                elif event.key == pygame.K_2:  # Easy AI
                    return 'ai', 0
                elif event.key == pygame.K_3:  # Hard AI
                    return 'ai', 1
                
# --- ÉCRAN DE FIN ---
def display_end_screen(winner):
    screen.fill(BG_COLOR)  # Remplit l'écran avec la couleur de fond
        
    # Affichage du cercle ou de la croix en haut de l'écran
    if winner == 1:
        pygame.draw.circle(screen, CIRCLE_COLOR, (WIDTH // 2, HEIGHT // 2 - 100), CIRCLE_RADIUS, CIRCLE_WIDTH)
    elif winner == 2:
        pygame.draw.line(screen, CROSS_COLOR, (WIDTH // 2 - SQUARE_SIZE // 2 + OFFSET, HEIGHT // 2 - 100 + SQUARE_SIZE // 2 - OFFSET),
                     (WIDTH // 2 + SQUARE_SIZE // 2 - OFFSET, HEIGHT // 2 - 100 - SQUARE_SIZE // 2 + OFFSET), CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, (WIDTH // 2 - SQUARE_SIZE // 2 + OFFSET, HEIGHT // 2 - 100 - SQUARE_SIZE // 2 + OFFSET),
                     (WIDTH // 2 + SQUARE_SIZE // 2 - OFFSET, HEIGHT // 2 - 100 + SQUARE_SIZE // 2 - OFFSET), CROSS_WIDTH)

    # Affichage du texte de fin de partie ("Winner!" ou "Game Over")
    font = pygame.font.SysFont(None, 60)  # Police pour le message de fin
    if winner == 1 or winner == 2:
        text = font.render("Winner!", True, BLACK)
    else:
        text = font.render("Game Over", True, BLACK)
    
    # Positionne le texte de fin juste en dessous du dessin
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    # Affichage des instructions en dessous
    font_small = pygame.font.SysFont(None, 30)
    options = ["1. Player vs Player", "2. Player vs Easy AI", "3. Player vs Hard AI"]
    for i, instruction in enumerate(options):
        instr_text = font_small.render(instruction, True, BLACK)
        screen.blit(instr_text, (WIDTH // 2 - instr_text.get_width() // 2, HEIGHT // 2 + 60 + i * 40))

    pygame.display.update()  # Met à jour l'écran
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # PvP
                    return 'pvp'
                elif event.key == pygame.K_2:  # Easy AI
                    return 'ai', 0
                elif event.key == pygame.K_3:  # Hard AI
                    return 'ai', 1

# --- FONCTION PRINCIPALE ---
def main():
    mode = start_screen()  # Démarrage : sélection du mode de jeu
    game = Game()
    board = game.board
    ai = game.ai

    # Configuration initiale en fonction du mode choisi
    if mode == 'pvp':
        game.gamemode = 'pvp'
    else:
        game.gamemode, game.ai.level = mode

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gestion des touches clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            # Gestion des clics de souris
            if event.type == pygame.MOUSEBUTTONDOWN and game.running:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False
                        winner = board.final_state()
                        new_mode = display_end_screen(winner)  # Récupère la sélection de l'écran de fin

                        # Réinitialise le jeu avec le nouveau mode
                        if new_mode == 'pvp':
                            game = Game()
                            game.gamemode = 'pvp'
                        else:
                            game = Game()
                            game.gamemode, game.ai.level = new_mode

        # Mode IA
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
                winner = board.final_state()
                new_mode = display_end_screen(winner)  # Récupère la sélection de l'écran de fin

                # Réinitialise le jeu avec le nouveau mode
                if new_mode == 'pvp':
                    game = Game()
                    game.gamemode = 'pvp'
                else:
                    game = Game()
                    game.gamemode, game.ai.level = new_mode

        pygame.display.update()

main()