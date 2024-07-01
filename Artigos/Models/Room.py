
import pygame
import random

"""
    Essa classe tem as definições de uma sala, como suas portas, tamanho e a posição dentro do mundo
"""


class Room:
    def __init__(self, x, y, z, w, h):
        self.x = x  # Posição x
        self.y = y  # Posição y
        self.z = z  # Posição z
        self.w = w  # Largura
        self.h = h  # Altura
        self.doors = []  # Portas
        self.doors_unvisited = []  # Portas não visitadas
        self.doors_visited = []  # Portas visitadas
        self.generate_doors()  # Gera as portas

    # Desenha a sala
    def draw(self, tela):
        pygame.draw.rect(tela, (255, 0, 0),
                         (self.x, self.y, self.w, self.h), 1)

        for door in self.doors:
            pygame.draw.circle(tela, (0, 0, 255), door, 2)

    """
        Gera as portas da sala
        Número de portas: 2 a 4	
        Nenhum delas pode ser no mesmo lado
    """

    def generate_doors(self):
        number_doors = random.randint(2, 4)  # Número de portas
        sides_available = [0, 1, 2, 3]  # Lados disponíveis
        offset_of_corner = 10  # Distância do canto
        for i in range(number_doors):
            side = random.choice(sides_available)  # Lado da porta
            if (side == 0):
                x = random.randint(self.x + offset_of_corner,
                                   self.x + self.w - offset_of_corner)
                y = self.y
            elif (side == 1):
                x = random.randint(self.x + offset_of_corner,
                                   self.x + self.w - offset_of_corner)
                y = self.y + self.h
            elif (side == 2):
                x = self.x
                y = random.randint(self.y + offset_of_corner,
                                   self.y + self.h - offset_of_corner)
            elif (side == 3):
                x = self.x + self.w
                y = random.randint(self.y + offset_of_corner,
                                   self.y + self.h - offset_of_corner)
            self.doors.append((x, y))
            self.doors_unvisited.append((x, y))

            # remove o lado da lista
            sides_available.remove(side)

    # Retorna as portas
    def get_doors(self):
        return self.doors
