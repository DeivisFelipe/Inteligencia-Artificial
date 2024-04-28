# instala a lib grafica de jogos
import pygame
# importa o random
import random

# Variaveis de configuracao
TAMANHO = 800, 600
TAMANHO_GRID = 10, 10
MARGEM_ENTRE_SALAS = 10
numero_salas = random.randint(10, 20)
salas = []


# instancia a tela
tela = pygame.display.set_mode(TAMANHO)

# cria um relogio
relogio = pygame.time.Clock()

# mostra a tela em amarelo
tela.fill((255, 255, 0))

# atualiza a tela
pygame.display.flip()


class Ambiente:

    def __init__(self):
        self.salas_nao_visitadas = []
        self.salas_visitadas = []
        self.conexoes = []

    def visitar_sala(self, sala):
        self.salas_visitadas.append(sala)
        self.salas_nao_visitadas.remove(sala)

    def adicionar_caminho(self, porta1, porta2):
        self.conexoes.append((porta1, porta2))

    def gera_caminhos(self):
        # Pega uma sala aleatória
        origem = random.choice(self.salas_nao_visitadas)
        self.visitar_sala(origem)

        # Pega uma porta aleatória
        porta_origem = random.choice(origem.get_portas())

        # Pega uma sala aleatória
        destino = random.choice(self.salas_nao_visitadas)
        self.visitar_sala(destino)

        # Pega uma porta aleatória
        porta_destino = random.choice(destino.get_portas())

        self.adicionar_caminho(porta_origem, porta_destino)

        # visitar as portas
        origem.portas_nao_visitadas.remove(porta_origem)
        origem.portas_visitadas.append(porta_origem)
        destino.portas_nao_visitadas.remove(porta_destino)
        destino.portas_visitadas.append(porta_destino)

        # enquanto tiver salas não visitadas
        while (len(self.salas_nao_visitadas) > 0):

            # Salas origem possiveis
            salas_origem = self.salas_visitadas
            # Pega uma sala aleatória
            origem = random.choice(self.salas_visitadas)
            # Remove a origem da lista de possiveis origens
            salas_origem.remove(origem)
            while (len(origem.portas_nao_visitadas) == 0 and len(salas_origem) > 0):
                origem = random.choice(salas_origem)
                salas_origem.remove(origem)

            print("Origem: ", origem.portas_nao_visitadas,
                  origem.portas_visitadas)

            # Pega uma porta aleatória
            porta_origem = random.choice(origem.portas_nao_visitadas)

            # Pega uma sala aleatória
            destino = random.choice(self.salas_nao_visitadas)
            self.visitar_sala(destino)

            # Pega uma porta aleatória
            porta_destino = random.choice(destino.get_portas())

            self.adicionar_caminho(porta_origem, porta_destino)

            # visitar as portas
            origem.portas_nao_visitadas.remove(porta_origem)
            origem.portas_visitadas.append(porta_origem)
            destino.portas_nao_visitadas.remove(porta_destino)
            destino.portas_visitadas.append(porta_destino)

        # já fez todas as conexões base, agora junta todas as portas que ainda não foram visitadas e faz conexões aleatórias
        portas_nao_visitadas = []
        for sala in self.salas_visitadas:
            for porta in sala.portas_nao_visitadas:
                portas_nao_visitadas.append((sala, porta))

        while (len(portas_nao_visitadas) > 1):
            origem = random.choice(portas_nao_visitadas)
            portas_nao_visitadas.remove(origem)

            destino = random.choice(portas_nao_visitadas)
            portas_nao_visitadas.remove(destino)

            self.adicionar_caminho(origem[1], destino[1])

        # se sobrou só uma porta, apenas deleta ela da sala
        if (len(portas_nao_visitadas) == 1):
            porta = portas_nao_visitadas[0]
            porta[0].portas_nao_visitadas.remove(porta[1])
            portas_nao_visitadas.remove(porta)


ambiente = Ambiente()


class Sala:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.portas = []
        self.portas_visitadas = []
        self.portas_nao_visitadas = []
        self.gerar_portas()

    def desenha(self):
        pygame.draw.rect(tela, (255, 0, 0),
                         (self.x, self.y, self.w, self.h), 1)

        for porta in self.portas:
            pygame.draw.circle(tela, (0, 0, 255), porta, 2)

    def gerar_portas(self):
        numero_portas = random.randint(2, 4)
        lados_disponiveis = [0, 1, 2, 3]
        distancia_canto = 10
        for i in range(numero_portas):
            lado = random.choice(lados_disponiveis)
            if (lado == 0):
                x = random.randint(self.x + distancia_canto,
                                   self.x + self.w - distancia_canto)
                y = self.y
            elif (lado == 1):
                x = random.randint(self.x + distancia_canto,
                                   self.x + self.w - distancia_canto)
                y = self.y + self.h
            elif (lado == 2):
                x = self.x
                y = random.randint(self.y + distancia_canto,
                                   self.y + self.h - distancia_canto)
            elif (lado == 3):
                x = self.x + self.w
                y = random.randint(self.y + distancia_canto,
                                   self.y + self.h - distancia_canto)
            self.portas.append((x, y))
            self.portas_nao_visitadas.append((x, y))

            # remove o lado da lista
            lados_disponiveis.remove(lado)

    def get_portas(self):
        return self.portas


def cria_sala():
    colide = True
    while (colide):
        # Não pode sair da tela
        w = random.randint(50, 200)
        h = random.randint(50, 200)
        x = random.randint(0, TAMANHO[0] - w - 10)
        y = random.randint(0, TAMANHO[1] - h - 10)

        # verifica se colide com outra sala=
        colide = False
        for sala in salas:
            # verifica a colisão considerando a margem
            if (x < sala.x + sala.w + MARGEM_ENTRE_SALAS and x + w + MARGEM_ENTRE_SALAS > sala.x and y < sala.y + sala.h + MARGEM_ENTRE_SALAS and y + h + MARGEM_ENTRE_SALAS > sala.y):
                colide = True
                break

        if (not colide):
            nova_sala = Sala(x, y, w, h)
            salas.append(nova_sala)

            # Adiciona a sala as salas não visitadas
            ambiente.salas_nao_visitadas.append(nova_sala)


# cria as salas
for i in range(numero_salas):
    cria_sala()


def desenha_grid():
    for x in range(0, TAMANHO[0], TAMANHO_GRID[0]):
        for y in range(0, TAMANHO[1], TAMANHO_GRID[1]):
            pygame.draw.rect(
                tela, (255, 0, 0), (x, y, TAMANHO_GRID[0], TAMANHO_GRID[1]), 1)


# gera os caminhos
ambiente.gera_caminhos()


def printa_infos():
    print("Salas: ", len(salas))
    print("Salas visitadas: ", len(ambiente.salas_visitadas))
    print("Salas nao visitadas: ", len(ambiente.salas_nao_visitadas))
    print("Caminhos: ", len(ambiente.conexoes))


printa_infos()


# loop principal
while True:
    # pega os eventos
    for evento in pygame.event.get():
        # se o evento for sair
        if evento.type == pygame.QUIT:
            # sai do jogo
            pygame.quit()
            exit()
    # limita a taxa de quadros por segundo
    relogio.tick(30)

    # Desenha GRID
    # desenha_grid()

    # Desenha as salas
    for sala in salas:
        sala.desenha()

    # Desenha os caminhos
    for caminho in ambiente.conexoes:
        pygame.draw.line(tela, (0, 255, 0), caminho[0], caminho[1], 1)

    # atualiza a tela
    pygame.display.flip()
