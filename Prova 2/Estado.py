from p5 import *

# Estado do jodo da velha


class Estado:
    size = 3
    matriz = []
    espessura = 100
    borda = 10
    width = None
    height = None
    jogador = 1
    centros_celulas = []

    # informação de print do tabuleiro
    inicioX = None
    fimX = None
    inicioY = None
    fimY = None

    def __init__(self, size, matriz, width, height):
        self.matriz = matriz
        self.size = size
        self.width = width
        self.height = height

        # Com base no tamanho da matriz, define a espessura das linhas
        self.espessura = self.width / (self.size + 3)

        # Inicios
        self.inicioX = self.width / 2 - (self.espessura * (self.size // 2 - 1))
        if (self.size % 2 == 1):
            self.inicioX -= self.espessura/2
        self.fimX = self.width / 2 + (self.espessura * (self.size // 2 - 1))
        self.inicioY = self.height / 2 - \
            (self.espessura * (self.size // 2 - 1))
        if (self.size % 2 == 1):
            self.inicioY -= self.espessura/2
        self.fimY = self.height / 2 + (self.espessura * (self.size // 2 - 1))

        # Define os centros das celulas
        for i in range(0, self.size):
            for j in range(0, self.size):
                self.centros_celulas.append(
                    ((self.inicioX - self.espessura/2) + i * self.espessura, (self.inicioY - self.espessura/2) + j * self.espessura))

    # Função que desenha o estado
    def desenha(self):
        fill(0, 0, 0)
        stroke_weight(self.borda)
        for i in range(0, self.size - 1):
            # Desenha linhas horizontais
            line((self.inicioX + i * self.espessura, self.inicioY - self.espessura),
                 (self.inicioX + i * self.espessura, self.fimY + self.espessura))
            # Desenha linhas verticais
            line((self.inicioX - self.espessura, self.inicioY + i * self.espessura),
                 (self.fimX + self.espessura, self.inicioY + i * self.espessura))

        # Desenha uma bolinha azul de raio 2 em cada centro de celula
        fill(0, 0, 255)
        stroke_weight(0)
        for i in range(0, len(self.centros_celulas)):
            circle(self.centros_celulas[i], 2)

    # Verifica o fim do jogo
    def fim(self):
        # If se o tamanho for maior que 3, ganha quem fizer 4 em linha
        # Else, ganha quem fizer 3 em linha
        if (self.size > 3):
            return self.fim4()
        else:
            return self.fim3()

    # Verifica o fim do jogo para 3 em linha
    def fim3(self):
        # Verifica se alguma linha tem 3 em linha
        for i in range(0, self.size):
            if (self.matriz[i][0] == self.matriz[i][1] and self.matriz[i][1] == self.matriz[i][2] and self.matriz[i][0] != 0):
                return True

        # Verifica se alguma coluna tem 3 em linha
        for i in range(0, self.size):
            if (self.matriz[0][i] == self.matriz[1][i] and self.matriz[1][i] == self.matriz[2][i] and self.matriz[0][i] != 0):
                return True

        # Verifica se alguma diagonal tem 3 em linha
        if (self.matriz[0][0] == self.matriz[1][1] and self.matriz[1][1] == self.matriz[2][2] and self.matriz[0][0] != 0):
            return True
        if (self.matriz[0][2] == self.matriz[1][1] and self.matriz[1][1] == self.matriz[2][0] and self.matriz[0][2] != 0):
            return True

        # Se não tiver nenhuma linha, coluna ou diagonal com 3 em linha, retorna falso
        return False

    # Verifica o fim do jogo para 4 em linha
    def fim4(self):
        # Verifica se alguma linha tem 4 em linha
        for i in range(0, self.size):
            for j in range(0, self.size - 3):
                if (self.matriz[i][j] == self.matriz[i][j + 1] and self.matriz[i][j + 1] == self.matriz[i][j + 2] and self.matriz[i][j + 2] == self.matriz[i][j + 3] and self.matriz[i][j] != 0):
                    return True

        # Verifica se alguma coluna tem 4 em linha
        for i in range(0, self.size):
            for j in range(0, self.size - 3):
                if (self.matriz[j][i] == self.matriz[j + 1][i] and self.matriz[j + 1][i] == self.matriz[j + 2][i] and self.matriz[j + 2][i] == self.matriz[j + 3][i] and self.matriz[j][i] != 0):
                    return True

        # Verifica se alguma diagonal tem 4 em linha
        for i in range(0, self.size - 3):
            for j in range(0, self.size - 3):
                if (self.matriz[i][j] == self.matriz[i + 1][j + 1] and self.matriz[i + 1][j + 1] == self.matriz[i + 2][j + 2] and self.matriz[i + 2][j + 2] == self.matriz[i + 3][j + 3] and self.matriz[i][j] != 0):
                    return True
        for i in range(0, self.size - 3):
            for j in range(3, self.size):
                if (self.matriz[i][j] == self.matriz[i + 1][j - 1] and self.matriz[i + 1][j - 1] == self.matriz[i + 2][j - 2] and self.matriz[i + 2][j - 2] == self.matriz[i + 3][j - 3] and self.matriz[i][j] != 0):
                    return True

        # Se não tiver nenhuma linha, coluna ou diagonal com 4 em linha, retorna falso
        return False