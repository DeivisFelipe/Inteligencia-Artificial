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
    global estado
    # Desenha o estado inicial
    estado.desenha()


# Roda o p5
run(renderer="vispy")
