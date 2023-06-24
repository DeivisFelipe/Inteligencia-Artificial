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
tamanho = 6
estado = Estado(tamanho, np.zeros((tamanho, tamanho)), width, height)


def setup():
    size(width, height)
    background(204)
    # Titulo da janela
    title("Jogo da Velha MinMax - Deivis Felipe")


# Função de desenho do p5
def draw():
    global estado
    # Desenha o estado inicial
    estado.desenha()

    # Desenha uma bolinha vermelho no meio do tabuleiro
    fill(255, 0, 0)
    stroke_weight(0)
    circle((width/2, height/2), 20)


# Roda o p5
run(renderer="vispy")
