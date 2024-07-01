import random
import pygame

from Models.Room import Room
from Models.Path import Path

"""
Essa classe é responsável por cuidar de tudo que é do ambiente, como as salas e as conexões entre elas
"""

DRAW_LINKS = False


class Environment:

    def __init__(self):
        self.rooms = []
        self.rooms_unvisited = []
        self.rooms_visited = []
        self.links = []
        self.paths = []

    def draw(self, screen):
        for room in self.rooms:
            room.draw(screen)

        # Desenha os caminhos
        for path in self.paths:
            path.draw(screen)

        # Desenha os links
        if (DRAW_LINKS):
            for link in self.links:
                pygame.draw.line(screen, (0, 255, 0), link[0], link[1], 1)

    def create_room(self, screen_size, margin):
        collides = True
        while (collides):
            # Não pode sair da tela
            w = random.randint(50, 200)
            h = random.randint(50, 200)
            x = random.randint(0, screen_size[0] - w - 10)
            y = random.randint(0, screen_size[1] - h - 10)

            # verifica se colide com outra sala=
            collides = False
            for room in self.rooms:
                # verifica a colisão considerando a margem
                if (x < room.x + room.w + margin and x + w + margin > room.x and y < room.y + room.h + margin and y + h + margin > room.y):
                    collides = True
                    break

            if (not collides):
                room = Room(x, y, 0, w, h)
                self.rooms.append(room)
                self.rooms_unvisited.append(room)

    def visit_room(self, sala):
        self.rooms_visited.append(sala)
        self.rooms_unvisited.remove(sala)

    def add_link(self, porta1, porta2):
        self.links.append((porta1, porta2))

    def generate_links(self):
        # Pega uma sala aleatória
        origin = random.choice(self.rooms_unvisited)
        self.visit_room(origin)

        # Pega uma porta aleatória
        origin_door = random.choice(origin.get_doors())

        # Pega uma sala aleatória
        destiny = random.choice(self.rooms_unvisited)
        self.visit_room(destiny)

        # Pega uma porta aleatória
        destiny_door = random.choice(destiny.get_doors())

        self.add_link(origin_door, destiny_door)

        # visitar as portas
        origin.doors_unvisited.remove(origin_door)
        origin.doors_visited.append(origin_door)
        destiny.doors_unvisited.remove(destiny_door)
        destiny.doors_visited.append(destiny_door)

        # enquanto tiver salas não visitadas
        while (len(self.rooms_unvisited) > 0):

            # Salas origem possiveis
            origin_rooms = self.rooms_visited
            # Pega uma sala aleatória
            origin = random.choice(self.rooms_visited)
            # Remove a origem da lista de possiveis origens
            origin_rooms.remove(origin)
            while (len(origin.doors_unvisited) == 0 and len(origin_rooms) > 0):
                origin = random.choice(origin_rooms)
                origin_rooms.remove(origin)

            print("Origem: ", origin.doors_unvisited,
                  origin.doors_visited)

            # Pega uma porta aleatória
            origin_door = random.choice(origin.doors_unvisited)

            # Pega uma sala aleatória
            destiny = random.choice(self.rooms_unvisited)
            self.visit_room(destiny)

            # Pega uma porta aleatória
            destiny_door = random.choice(destiny.get_doors())

            self.add_link(origin_door, destiny_door)

            # visitar as portas
            origin.doors_unvisited.remove(origin_door)
            origin.doors_visited.append(origin_door)
            destiny.doors_unvisited.remove(destiny_door)
            destiny.doors_visited.append(destiny_door)

        # já fez todas as conexões base, agora junta todas as portas que ainda não foram visitadas e faz conexões aleatórias
        doors_unvisited = []
        for room in self.rooms_visited:
            for porta in room.doors_unvisited:
                doors_unvisited.append((room, porta))

        while (len(doors_unvisited) > 1):
            origem = random.choice(doors_unvisited)
            doors_unvisited.remove(origem)

            destino = random.choice(doors_unvisited)
            doors_unvisited.remove(destino)

            self.add_link(origem[1], destino[1])

        # se sobrou só uma porta, apenas deleta ela da sala
        if (len(doors_unvisited) == 1):
            porta = doors_unvisited[0]
            porta[0].doors_unvisited.remove(porta[1])
            doors_unvisited.remove(porta)

    def generate_paths(self):
        for link in self.links:
            self.paths.append(Path(link[0], link[1], self.rooms))
