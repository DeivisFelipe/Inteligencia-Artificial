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
tamanho = 8
estado = Estado(tamanho, np.zeros((tamanho, tamanho)), width, height)


def setup():
    size(width, height)
    background(204)
    # Titulo da janela
    title("Jogo da Velha MinMax - Deivis Felipe")


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
    # Considerando a espessura, verifica se algum centro de celula foi clicado
    for i in range(0, len(estado.centros_celulas)):
        if (x >= estado.centros_celulas[i][0] - estado.espessura/2 and x <= estado.centros_celulas[i][0] + estado.espessura/2 and y >= estado.centros_celulas[i][1] - estado.espessura/2 and y <= estado.centros_celulas[i][1] + estado.espessura/2):
            # Se foi clicado, verifica se a celula está vazia
            if (estado.matriz[i // estado.size][i % estado.size] == 0):
                # Se estiver vazia, coloca o jogador atual
                estado.matriz[i // estado.size][i %
                                                estado.size] = estado.jogador
                # Ve for o jogador 1, muda para o jogador 2
                if (estado.jogador == 1):
                    estado.jogador = 2
                # Se for o jogador 2, muda para o jogador 1
                else:
                    estado.jogador = 1


# Roda o p5
run(renderer="vispy")
