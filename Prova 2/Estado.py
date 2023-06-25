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

    # É empate
    empate = False

    # Vencedor do jogo
    vencedor = 0

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
        self.fimX = self.inicioX + (self.espessura * (self.size - 2))
        self.inicioY = self.height / 2 - \
            (self.espessura * (self.size // 2 - 1))
        if (self.size % 2 == 1):
            self.inicioY -= self.espessura/2
        self.fimY = self.inicioY + (self.espessura * (self.size - 2))

        # Define os centros das celulas
        self.centros_celulas = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                self.centros_celulas.append(
                    ((self.inicioX - self.espessura/2) + i * self.espessura, (self.inicioY - self.espessura/2) + j * self.espessura))

    # Função que desenha o estado
    def desenha(self):
        # Verifica se o jogo acabou
        if (self.vencedor != 0 or self.empate):
            no_stroke()
            # Escreve o vencedor
            if (self.vencedor == 1):
                fill(255, 0, 0)
                text("Vencedor: X", (self.width / 2, 40))
            elif (self.vencedor == 2):
                fill(0, 255, 0)
                text("Vencedor: O", (self.width / 2, 40))
            else:
                fill(0)
                text("Empate", (self.width / 2, 40))
        stroke(0)
        stroke_weight(self.borda)
        for i in range(0, self.size - 1):
            # Desenha linhas horizontais
            line((self.inicioX + i * self.espessura, self.inicioY - self.espessura),
                 (self.inicioX + i * self.espessura, self.fimY + self.espessura))
            # Desenha linhas verticais
            line((self.inicioX - self.espessura, self.inicioY + i * self.espessura),
                 (self.fimX + self.espessura, self.inicioY + i * self.espessura))

        # Desenha uma bolinha azul de raio 2 em cada centro de celula
        stroke(0, 0, 255)
        stroke_weight(1)
        fill(0, 0, 255)
        for i in range(0, len(self.centros_celulas)):
            circle(self.centros_celulas[i], 1)

        # Desenha as bolinhas e xis
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.matriz[i][j] == 1):
                    self.desenhaX(i, j)
                elif (self.matriz[i][j] == 2):
                    self.desenhaO(i, j)

    # Desenha um xis na celula i, j
    def desenhaX(self, i, j):
        stroke_weight(5)
        stroke(255, 0, 0)
        line((self.centros_celulas[i * self.size + j][0] - self.espessura/4, self.centros_celulas[i * self.size + j][1] - self.espessura/4),
             (self.centros_celulas[i * self.size + j][0] + self.espessura/4, self.centros_celulas[i * self.size + j][1] + self.espessura/4))
        line((self.centros_celulas[i * self.size + j][0] + self.espessura/4, self.centros_celulas[i * self.size + j][1] - self.espessura/4),
             (self.centros_celulas[i * self.size + j][0] - self.espessura/4, self.centros_celulas[i * self.size + j][1] + self.espessura/4))

    # Desenha um circulo na celula i, j. Sem preenchimento
    def desenhaO(self, i, j):
        stroke_weight(5)
        stroke(0, 255, 0)
        no_fill()
        circle(self.centros_celulas[i * self.size + j], self.espessura/2)

    # Verifica o fim do jogo
    def fim(self):
        # If se o tamanho for maior que 3, ganha quem fizer 4 em linha
        # Else, ganha quem fizer 3 em linha
        if (self.size > 3):
            result = self.fim4()
        else:
            result = self.fim3()

        if not result:
            self.empate = self.verifica_empate()
            return self.empate
        else:
            return result

    def verifica_empate(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.matriz[i][j] == 0):
                    return False
        return True

    # Verifica o fim do jogo para 3 em linha
    def fim3(self):
        for i in range(0, self.size):
            # Verifica se alguma linha tem 3 em linha
            if (self.matriz[i][0] == self.matriz[i][1] and self.matriz[i][1] == self.matriz[i][2] and self.matriz[i][0] != 0):
                self.vencedor = self.matriz[i][0]
                return True

            # Verifica se alguma coluna tem 3 em linha
            if (self.matriz[0][i] == self.matriz[1][i] and self.matriz[1][i] == self.matriz[2][i] and self.matriz[0][i] != 0):
                self.vencedor = self.matriz[0][i]
                return True

        # Verifica se alguma diagonal tem 3 em linha
        if (self.matriz[0][0] == self.matriz[1][1] and self.matriz[1][1] == self.matriz[2][2] and self.matriz[0][0] != 0):
            self.vencedor = self.matriz[0][0]
            return True
        if (self.matriz[0][2] == self.matriz[1][1] and self.matriz[1][1] == self.matriz[2][0] and self.matriz[0][2] != 0):
            self.vencedor = self.matriz[0][2]
            return True

        # Se não tiver nenhuma linha, coluna ou diagonal com 3 em linha, retorna falso
        return False

    # Verifica o fim do jogo para 4 em linha
    def fim4(self):
        for i in range(0, self.size):
            for j in range(0, self.size - 3):
                # Verifica se alguma linha tem 4 em linha
                if (self.matriz[i][j] == self.matriz[i][j + 1] and self.matriz[i][j + 1] == self.matriz[i][j + 2] and self.matriz[i][j + 2] == self.matriz[i][j + 3] and self.matriz[i][j] != 0):
                    self.vencedor = self.matriz[i][j]
                    return True

                # Verifica se alguma coluna tem 4 em linha
                if (self.matriz[j][i] == self.matriz[j + 1][i] and self.matriz[j + 1][i] == self.matriz[j + 2][i] and self.matriz[j + 2][i] == self.matriz[j + 3][i] and self.matriz[j][i] != 0):
                    self.vencedor = self.matriz[j][i]
                    return True

        # Verifica se alguma diagonal tem 4 em linha
        for i in range(0, self.size - 3):
            for j in range(0, self.size - 3):
                if (self.matriz[i][j] == self.matriz[i + 1][j + 1] and self.matriz[i + 1][j + 1] == self.matriz[i + 2][j + 2] and self.matriz[i + 2][j + 2] == self.matriz[i + 3][j + 3] and self.matriz[i][j] != 0):
                    self.vencedor = self.matriz[i][j]
                    return True
        for i in range(0, self.size - 3):
            for j in range(3, self.size):
                if (self.matriz[i][j] == self.matriz[i + 1][j - 1] and self.matriz[i + 1][j - 1] == self.matriz[i + 2][j - 2] and self.matriz[i + 2][j - 2] == self.matriz[i + 3][j - 3] and self.matriz[i][j] != 0):
                    self.vencedor = self.matriz[i][j]
                    return True

        # Se não tiver nenhuma linha, coluna ou diagonal com 4 em linha, retorna falso
        return False

    # Função que pega todos os estados possiveis a partir do estado atual
    def estados_possiveis(self):
        estados = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                if (self.matriz[i][j] == 0):
                    # Cria uma copia do estado atual
                    novo_estado = Estado(self.size, np.copy(self.matriz),
                                         self.width, self.height)
                    novo_estado.jogador = self.jogador
                    # Coloca o jogador atual na celula i, j
                    novo_estado.matriz[i][j] = self.jogador
                    # Muda o jogador
                    if (novo_estado.jogador == 1):
                        novo_estado.jogador = 2
                    else:
                        novo_estado.jogador = 1
                    # Adiciona o estado na lista de estados
                    estados.append(novo_estado)
        return estados

    # string
    def __str__(self):
        return "Estado: \n" + str(self.matriz) + "\nJogador: " + str(self.jogador) + "\nVencedor: " + str(self.vencedor) + "\nEmpate: " + str(self.empate)
