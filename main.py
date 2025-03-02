import pygame, sys
from code.Game import Game
from code.Colors import Colors

pygame.init()

# Fontes
title_font = pygame.font.Font(None, 40)

# Cores e retângulos
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

# Tela e relógio
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")
clock = pygame.time.Clock()

# Jogo
game = Game()

# Evento para atualizar o jogo
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 600)

def handle_keydown(event):
    """Função para lidar com eventos de teclas pressionadas"""
    if game.game_over:
        game.game_over = False
        game.reset()
        return

    if event.key == pygame.K_LEFT:
        game.move(-1, 0)  # Mover para a esquerda
    elif event.key == pygame.K_RIGHT:
        game.move(1, 0)  # Mover para a direita
    elif event.key == pygame.K_DOWN:
        game.move(0, 1)  # Mover para baixo
        game.update_score(0, 1)
    elif event.key == pygame.K_UP:
        game.rotate()

def handle_game_update():
    """Função para lidar com o evento de atualização do jogo"""
    if not game.game_over:
        game.move(0, 1)  # Mover para baixo

def draw_game():
    """Função para desenhar o jogo na tela"""
    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))

    if game.game_over:
        game.draw_game_over(screen, title_font)

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    game.draw(screen)

def game_loop():
    """Função principal do loop do jogo"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                handle_keydown(event)
            if event.type == GAME_UPDATE:
                handle_game_update()

        draw_game()
        pygame.display.update()
        clock.tick(60)

# Iniciar o loop do jogo
game_loop()
