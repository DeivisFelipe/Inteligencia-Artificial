import pygame

"""
    Função responsável por fazer o caminho entre conexões usando o A*
"""


class Path:
    def __init__(self, start, end, rooms):
        self.start = start
        self.end = end
        self.path = []
        self.generate_path(rooms)

    def draw(self, screen):
        for i in range(len(self.path) - 1):
            # desenha todos os pixels do caminho
            pygame.draw.line(screen, (0, 0, 0),
                             self.path[i], self.path[i + 1], 1)

    def generate_path(self, rooms):
        points_unvisited = []
        points_visited = []
        points_unvisited.append(self.start)

    def get_closest_point(self, points, end):
        pass

    def get_neighbors(self, point):
        pass
