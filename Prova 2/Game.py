# Importa o Estado.py
from Estado import Estado
# Importa o p5
from p5 import *
# Importa o numpy
import numpy as np

# Setup do p5
width = 600
height = 600

# Cria um estado inicial com matriz zerada
tamanho = 3
estado = Estado(tamanho, np.zeros((tamanho, tamanho)), width, height)


def setup():
    size(width, height)
    background(204)
    # Titulo da janela
    title("Jogo da Velha MiniMax - Deivis Felipe")

    f = create_font("arial.ttf", 30,)  # Arial, 16 point, anti-aliasing on
    text_font(f)  # Set the font to "f"
    textAlign(CENTER, CENTER)  # Centraliza o texto horizontal e verticalmente


coutner = 0

# Função de desenho do p5


def draw():
    # Limpa a tela
    background(204)
    global estado
    # Desenha o estado inicial
    estado.desenha()

# Função de clique do p5


def mouse_pressed():
    # Pega a posição do mouse
    x = mouse_x
    y = mouse_y
    if (estado.vencedor == 0 and not estado.empate):
        # Considerando a espessura, verifica se algum centro de celula foi clicado
        for i in range(0, len(estado.centros_celulas)):
            if (x >= estado.centros_celulas[i][0] - estado.espessura/2 and x <= estado.centros_celulas[i][0] + estado.espessura/2 and y >= estado.centros_celulas[i][1] - estado.espessura/2 and y <= estado.centros_celulas[i][1] + estado.espessura/2):
                # Se foi clicado, verifica se a celula está vazia
                if (estado.matriz[i // estado.size][i % estado.size] == 0):
                    # Se estiver vazia, coloca o jogador atual
                    estado.matriz[i // estado.size][i %
                                                    estado.size] = estado.jogador

                    if (estado.fim()):
                        return
                    estado.jogador = 2

                    melhor_jogada()

                    if (estado.fim()):
                        return

                    estado.jogador = 1

                break

# Função de tecla do p5


def key_pressed():
    # se clicar em r, reseta o jogo
    if (key == "r"):
        global estado
        estado = Estado(tamanho, np.zeros((tamanho, tamanho)), width, height)
        estado.jogador = 1

# Algoritmo melhor jogada


def melhor_jogada():
    global estado
    melhor_pontuacao = math.inf
    melhor_jogada_estado = None
    for estado_novo in estado.estados_possiveis():
        pontuacao = minimax(estado_novo, True, 0)

        if (pontuacao < melhor_pontuacao):
            melhor_pontuacao = pontuacao
            melhor_jogada_estado = estado_novo

    estado = melhor_jogada_estado


def minimax(estadoMinMax, maximizando, profundidade=0):
    if (estadoMinMax.fim()):
        if (estadoMinMax.empate):
            return 0
        else:
            multiplicador = 1 if estadoMinMax.vencedor == 1 else -1
            if profundidade == 0:
                return multiplicador * 10
            elif profundidade == 1:
                return multiplicador * 9
            elif profundidade == 2:
                return multiplicador * 8
            elif profundidade == 3:
                return multiplicador * 7
            elif profundidade == 4:
                return multiplicador * 6
            elif profundidade == 5:
                return multiplicador * 5
            elif profundidade == 6:
                return multiplicador * 4
            elif profundidade == 7:
                return multiplicador * 3
            elif profundidade == 8:
                return multiplicador * 2
            else:
                return multiplicador

    pontucaoes = []

    for estado_novo in estadoMinMax.estados_possiveis():
        pontucaoes.append(
            minimax(estado_novo, not maximizando, profundidade + 1))

    if (maximizando):
        return max(pontucaoes)
    else:
        return min(pontucaoes)


# Roda o p5
run(renderer="vispy")
