import pygame
from code.Block import Block
from code.Colors import Colors

# Definindo as dimensões
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 620
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

GAME_UPDATE = pygame.USEREVENT + 1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

        self.board = [[(0, 0, 0)] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  # Tabuleiro inicial
        self.score = 0
        self.current_block = Block()  # Peça atual
        self.next_block = Block()  # Próxima peça
        self.game_over = False

        pygame.time.set_timer(GAME_UPDATE, 500)  # A cada 500ms a peça desce

    def reset(self):
        """Reseta o jogo"""
        self.board = [[(0, 0, 0)] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.current_block = Block()
        self.next_block = Block()
        self.game_over = False

    def draw_board(self):
        """Desenha o tabuleiro"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.board[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, Colors.white, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

    def draw_block(self, block):
        """Desenha a peça atual"""
        shape = block.get_shape()
        color = block.get_color()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, ((block.x + x) * BLOCK_SIZE, (block.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_block(self):
        """Desenha a próxima peça"""
        shape = self.next_block.get_shape()
        color = self.next_block.get_color()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, (GRID_WIDTH * BLOCK_SIZE + 20 + x * BLOCK_SIZE, 20 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self):
        """Verifica se há colisão"""
        shape = self.current_block.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if self.current_block.y + y >= GRID_HEIGHT or \
                       self.current_block.x + x < 0 or \
                       self.current_block.x + x >= GRID_WIDTH or \
                       self.board[self.current_block.y + y][self.current_block.x + x] != (0, 0, 0):
                        return True
        return False

    def merge_block(self):
        """Adiciona a peça no tabuleiro"""
        shape = self.current_block.get_shape()
        color = self.current_block.get_color()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_block.y + y][self.current_block.x + x] = color

    def clear_lines(self):
        """Limpa as linhas completas"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.board[y][x] != (0, 0, 0) for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)
        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [(0, 0, 0)] * GRID_WIDTH)
            self.score += 100

    def move_left(self):
        """Move a peça para a esquerda"""
        self.current_block.x -= 1
        if self.check_collision():
            self.current_block.x += 1

    def move_right(self):
        """Move a peça para a direita"""
        self.current_block.x += 1
        if self.check_collision():
            self.current_block.x -= 1

    def move_down(self):
        """Move a peça para baixo"""
        self.current_block.y += 1
        if self.check_collision():
            self.current_block.y -= 1
            self.merge_block()
            self.clear_lines()
            self.current_block = self.next_block
            self.next_block = Block()

    def rotate(self):
        """Rotaciona a peça"""
        self.current_block.rotate()
        if self.check_collision():
            self.current_block.rotate()  # Desfaz a rotação

    def game_over_check(self):
        """Verifica se o jogo acabou"""
        for x in range(GRID_WIDTH):
            if self.board[0][x] != (0, 0, 0):
                return True
        return False

    def update_score(self, x, y):
        """Atualiza a pontuação"""
        self.score += 10

    def draw_score(self, screen, font):
        """Desenha a pontuação"""
        score_value_surface = font.render(str(self.score), True, Colors.white)
        screen.blit(score_value_surface, (365, 540))

    def draw_game_over(self, screen, font):
        """Desenha a tela de Game Over"""
        game_over_surface = font.render("GAME OVER", True, Colors.white)
        screen.blit(game_over_surface, (320, 450))

    def update(self):
        """Atualiza a lógica do jogo"""
        if not self.game_over:
            self.move_down()
        if self.game_over_check():
            self.game_over = True

    def draw(self, screen):
        """Desenha a tela do jogo"""
        self.screen = screen
        self.screen.fill(Colors.dark_blue)
        self.draw_board()
        self.draw_block(self.current_block)
        self.draw_next_block()
        self.draw_score(self.screen, pygame.font.Font(None, 40))
        if self.game_over:
            self.draw_game_over(self.screen, pygame.font.Font(None, 40))
        pygame.display.update()
