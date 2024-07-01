import pygame
import random

# Classes
from Models.Room import Room
from Models.Environment import Environment

# Variaveis de configuracao
SCREEN_SIZE = 800, 600
UNIT_SIZE = 10, 10
MARGIN = 10
NUMBER_ROOMS = random.randint(10, 20)


# instancia a tela
screen = pygame.display.set_mode(SCREEN_SIZE)

# cria um relogio
clock = pygame.time.Clock()

# mostra a tela em amarelo
screen.fill((255, 255, 0))

# atualiza a tela
pygame.display.flip()


environment = Environment()


# cria as salas
for i in range(NUMBER_ROOMS):
    environment.create_room(SCREEN_SIZE, MARGIN)


def draw_grid():
    for x in range(0, SCREEN_SIZE[0], UNIT_SIZE[0]):
        for y in range(0, SCREEN_SIZE[1], UNIT_SIZE[1]):
            pygame.draw.rect(
                screen, (255, 0, 0), (x, y, UNIT_SIZE[0], UNIT_SIZE[1]), 1)


# gera os links
environment.generate_links()

# gera os caminhos
environment.generate_paths()


def print_infos():
    print("Salas: ", len(environment.rooms))
    print("Salas visitadas: ", len(environment.rooms_visited))
    print("Salas nao visitadas: ", len(environment.rooms_unvisited))
    print("Caminhos: ", len(environment.links))


print_infos()


# loop principal
while True:
    # pega os eventos
    for event in pygame.event.get():
        # se o evento for sair
        if event.type == pygame.QUIT:
            # sai do jogo
            pygame.quit()
            exit()
    # limita a taxa de quadros por segundo
    clock.tick(30)

    # Desenha GRID
    # draw_grid()

    # Desenha o ambiente
    environment.draw(screen)

    # atualiza a tela
    pygame.display.flip()
