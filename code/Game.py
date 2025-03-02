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

        #Sons
        self.sound_line_clear = pygame.mixer.Sound('./asset/Winner.mp3')  # Som de linha limpa

        #Música de Fundo
        pygame.mixer_music.load('./asset/tetris-theme.mp3')
        pygame.mixer_music.play(-1)

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
                pygame.draw.rect(self.screen, self.board[y][x],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, Colors.white, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

    def draw_block(self, block):
        """Desenha a peça atual"""
        shape = block.get_shape()
        color = block.get_color()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color,
                                     ((block.x + x) * BLOCK_SIZE, (block.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_block(self):
        """Desenha a próxima peça no canto direito"""
        shape = self.next_block.get_shape()
        color = self.next_block.get_color()

        # Caixa de fundo para destacar a próxima peça no canto direito
        next_block_rect = pygame.Rect(SCREEN_WIDTH - 160, 100, 140, 140)  # Localização ajustada para o canto direito

        # Desenha a peça dentro da caixa
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, (
                    SCREEN_WIDTH - 140 + x * BLOCK_SIZE, 300 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self):
        """Verifica se há colisão com as bordas ou outras peças"""
        shape = self.current_block.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Verifica se a peça ultrapassou as bordas da tela
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
        """Limpa as linhas completas e toca o som quando linhas são limpas"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            # Verifica se todos os blocos na linha estão preenchidos (não são (0, 0, 0))
            if all(self.board[y][x] != (0, 0, 0) for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)

        # Se houverem linhas para limpar
        if lines_to_clear:
            for line in lines_to_clear:
                # Remove a linha e insere uma linha vazia no topo
                del self.board[line]
                self.board.insert(0, [(0, 0, 0)] * GRID_WIDTH)

            # Atualiza a pontuação (cada linha limpa adiciona 100 pontos)
            self.score += len(lines_to_clear) * 100

            # Toca o som de linha limpa
            self.sound_line_clear.play()

    def move_left(self):
        """Move a peça para a esquerda"""
        self.current_block.x -= 1
        # Impede que a peça ultrapasse a borda esquerda (x < 0)
        if self.check_collision() or self.current_block.x < 0:
            self.current_block.x += 1  # Impede de passar da borda esquerda

    def move_right(self):
        """Move a peça para a direita"""
        self.current_block.x += 1
        if self.check_collision():
            self.current_block.x -= 1

    def move(self, dx, dy):
        """Move a peça na direção dada"""
        self.current_block.x += dx
        self.current_block.y += dy
        if self.check_collision():
            if dy:
                self.current_block.y -= dy
                self.merge_block()
                self.clear_lines()
                self.current_block = self.next_block
                self.next_block = Block()
            if dx:
                self.current_block.x -= dx

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
        """Desenha a pontuação com o texto 'Score' antes do valor"""
        score_label_surface = font.render("Score", True, Colors.white)
        screen.blit(score_label_surface, (365, 20))  # Desenha "Score"

        score_value_surface = font.render(str(self.score), True, Colors.white)
        screen.blit(score_value_surface, (365, 60))  # Desenha o valor da pontuação abaixo de "Score"

    def draw_game_over(self, screen, font):
        """Desenha a tela de Game Over"""
        game_over_surface = font.render("GAME OVER", True, Colors.white)
        screen.blit(game_over_surface, (320, 450))

    def update(self):
        """Atualiza a lógica do jogo"""
        if not self.game_over:
            self.move(0, 1)
        if self.game_over_check():
            self.game_over = True

    def draw(self, screen):
        """Desenha a tela do jogo"""
        self.screen = screen
        self.screen.fill(Colors.dark_blue)
        self.draw_board()
        self.draw_block(self.current_block)
        self.draw_next_block()  # Agora com a próxima peça no canto direito
        self.draw_score(self.screen, pygame.font.Font(None, 40))  # Chama para desenhar "Score" e o valor
        if self.game_over:
            self.draw_game_over(self.screen, pygame.font.Font(None, 40))
        pygame.display.update()
