from p5 import *

# Estado do jodo da velha


class Estado:
    size = 3
    matriz = []
    espessura = 100
    borda = 10
    width = None
    height = None

    def __init__(self, size, matriz, width, height):
        self.matriz = matriz
        self.size = size
        self.width = width
        self.height = height

    # Função que desenha o estado
    def desenha(self):
        # Verfica se o tamanho da matriz é impar ou par
        if self.size % 2 == 0:
            # Desenha linhas verticais e horizontais com distancia igual a espessura
            # Inicio das linhas
            inicioX = self.width / 2 - (self.espessura * (self.size / 2 - 1))
            fimX = self.width / 2 + (self.espessura * (self.size / 2 - 1))
            inicioY = self.height / 2 - (self.espessura * (self.size / 2 - 1))
            fimY = self.height / 2 + (self.espessura * (self.size / 2 - 1))
            fill(0, 0, 0)
            stroke_weight(self.borda)
            for i in range(0, self.size - 1):
                # Desenha linhas horizontais
                line((inicioX + i * self.espessura, inicioY - self.espessura),
                     (inicioX + i * self.espessura, fimY + self.espessura))
                # Desenha linhas verticais
                line((inicioX - self.espessura, inicioY + i * self.espessura),
                     (fimX + self.espessura, inicioY + i * self.espessura))

        else:
            # Desenha linhas verticais e horizontais com distancia igual a espessura
            # Inicio das linhas
            inicioX = self.width / 2 - self.espessura/2 - \
                (self.espessura * (self.size // 2 - 1))
            fimX = inicioX + self.espessura * (self.size - 2)
            inicioY = self.height / 2 - self.espessura/2 - \
                (self.espessura * (self.size // 2 - 1))
            fimY = inicioY + self.espessura * (self.size - 2)
            fill(0, 0, 0)
            stroke_weight(self.borda)
            for i in range(0, self.size - 1):
                # Desenha linhas horizontais
                line((inicioX + i * self.espessura, inicioY - self.espessura),
                     (inicioX + i * self.espessura, fimY + self.espessura))
                # Desenha linhas verticais
                line((inicioX - self.espessura, inicioY + i * self.espessura),
                     (fimX + self.espessura, inicioY + i * self.espessura))
