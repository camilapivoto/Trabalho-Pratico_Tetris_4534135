import pygame
import random

# Definição de cores
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Laranja
    (0, 0, 255),    # Azul
    (255, 0, 0),    # Vermelho
    (0, 255, 0),    # Verde
    (255, 255, 0),  # Amarelo
    (128, 0, 128)   # Roxo
]

# Definindo as formas das peças
SHAPES = [
    [[1, 1, 1, 1]],  # Linha
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # Quadrado
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]

class Block:
    def __init__(self, shape=None, color=None):
        self.shape = shape if shape else random.choice(SHAPES)
        self.color = color if color else random.choice(COLORS)
        self.x = 3  # Posição inicial (parte superior central)
        self.y = 0  # Começa no topo

    def rotate(self):
        """Rotaciona a peça"""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def get_shape(self):
        """Retorna o formato da peça"""
        return self.shape

    def get_color(self):
        """Retorna a cor da peça"""
        return self.color
