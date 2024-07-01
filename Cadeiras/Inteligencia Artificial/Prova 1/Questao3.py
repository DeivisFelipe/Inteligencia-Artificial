'''
Descrição da questão

(Exerc. 3) Considere o mapa de vôos da Figura 1, representado pelos operadores a seguir:
voo(a, b, 1), voo(a, c, 9), voo(a, d, 4), voo(b, c, 7), voo(b, e, 6), voo(b, f, 1), voo(c, f, 7), voo(d, f, 4),
voo(d, g, 5), voo(e, h, 9), voo(f, h, 4), voo(g, h, 1)
Sejam A o conjunto de ações acima:
(a) Apresentar o b) passo a passo o estado das listas de novos abertos e nodos fechados e c) desenhe a árvore de busca
produzida pelo algoritmo de busca gulosa pela melhor escolha para s0 = a e G = [h]. Neste exercício, o algoritmo deve 
usar os valores de custos g(n) (ver Figura 1) apresentados na descrição do problema.
(b) Mostrar que, usando os operadores na ordem declarada acima, os algoritmos de busca em largura e em
profundidade podem encontrar soluções de custo superior àquele encontrada pelo algoritmo de busca gulosa pela 
melhor escolha, quando s0 = a e G = [h]
'''

# cria a classe estado
class Estado:
    # atributos
    voo = None
    cidade1 = None
    cidade2 = None
    pai = None

    # construtor
    def __init__(self, voo, cidade1, cidade2):
        self.voo = voo
        self.cidade1 = cidade1
        self.cidade2 = cidade2

    def printaEstado(self, numeroestado):
        if numeroestado > 0:
            print("voo(" + self.cidade1 + ", " + self.cidade2 + ", " +
                str(self.voo) + ") = Numero: " + str(numeroestado))
        else:
            print("voo(" + self.cidade1 + ", " + self.cidade2 + ", " +
                str(self.voo) + ")")
        
    def addPai(self, pai):
        self.pai = pai

    # verifica se o estado é igual
    def __eq__(self, other):
        # verifica se a voo
        if self.voo != other.voo:
            return False

        # verifica se a cidade1 é igual
        if self.cidade1 != other.cidade2:
            return False

        # verifica se a cidade2 é igual
        if self.cidade2 != other.cidade2:
            return False

        return True


# Lista de todos os estados
estados = []
# Adiciona os estados
estados.append(Estado(1, 'a', 'b'))
estados.append(Estado(9, 'a', 'c'))
estados.append(Estado(4, 'a', 'd'))
estados.append(Estado(7, 'b', 'c'))
estados.append(Estado(6, 'b', 'e'))
estados.append(Estado(1, 'b', 'f'))
estados.append(Estado(7, 'c', 'f'))
estados.append(Estado(4, 'd', 'f'))
estados.append(Estado(5, 'd', 'g'))
estados.append(Estado(9, 'e', 'h'))
estados.append(Estado(4, 'f', 'h'))
estados.append(Estado(1, 'g', 'h'))


# cidade inicial
cidade_inicial = 'a'

# Cidade final
cidade_final = 'h'

# Cidades visitadas
cidades_visitadas = []

# Cidade atual
cidade_atual = None

# Pilha de estados
estados_nao_visitados = []

# Estado acessado número de forma global
numeroestado = 1

# ultimo estado acessado
ultimoestado = None

def abreno(no, estadoOrigem = None):
    for estado in estados:
        if estado.cidade1 == no and estado.cidade2 not in cidades_visitadas:
            estado.addPai(estadoOrigem)
            estados_nao_visitados.append(estado)
        if estado.cidade2 == no and estado.cidade1 not in cidades_visitadas:
            estado.addPai(estadoOrigem)
            estados_nao_visitados.append(estado)
            
    cidades_visitadas.append(no)

# Abre o nó guloso
def abrenoGuloso(no, estadoOrigem = None):
    menorCusto = None
    for estado in estados:
        if estado.cidade1 == no and estado.cidade2 not in cidades_visitadas:
            if menorCusto is None:
                menorCusto = estado
            elif estado.voo < menorCusto.voo:
                menorCusto = estado
        if estado.cidade2 == no and estado.cidade1 not in cidades_visitadas:
            if menorCusto is None:
                menorCusto = estado
            elif estado.voo < menorCusto.voo:
                menorCusto = estado
    
    if menorCusto is not None:
        menorCusto.addPai(estadoOrigem)
        estados_nao_visitados.append(menorCusto)
    cidades_visitadas.append(no)

# Cidade que esta na lista de cidades visitadas
def cidade_visitada(estado):
    if estado.cidade1 in cidades_visitadas:
        return estado.cidade1
    if estado.cidade2 in cidades_visitadas:
        return estado.cidade2
    return None

# Cidade que nao esta na lista de cidades visitadas
def cidade_nao_visitada(estado):
    if estado.cidade1 not in cidades_visitadas:
        return estado.cidade1
    if estado.cidade2 not in cidades_visitadas:
        return estado.cidade2
    return None

# acessa o estado
def acessa_estado_busca_profundidade(cidade):
    global numeroestado
    global ultimoestado
    global cidade_atual
    cidade_atual = cidade
    destino = None
    if(verifica_fim(cidade)):
        return
    abreno(cidade)
    while len(estados_nao_visitados) > 0:
        nonovo = estados_nao_visitados.pop(-1)
        cidade_atual = cidade_visitada(nonovo)
        destino = cidade_nao_visitada(nonovo)
        if destino not in cidades_visitadas and destino is not None:
            numeroestado += 1
            nonovo.printaEstado(numeroestado)
            abreno(destino, nonovo)
            if(verifica_fim(destino)):
                ultimoestado = nonovo
                break
    caminho()

# pega o caminho
def caminho():
    # mostra o caminho considerando o pai
    global ultimoestado
    print("\tCaminho")
    fim = False
    while not fim:
        print("\t\t", end="")
        ultimoestado.printaEstado(0)
        if ultimoestado.pai is None:
            fim = True
        ultimoestado = ultimoestado.pai


def verifica_fim(cidade):
    global cidade_final
    if cidade == cidade_final:
        print("Cidade final encontrada")
        return True
    return False

# Busca em Largura
def acessa_estado_busca_largura(cidade):
    global numeroestado
    global ultimoestado
    global cidade_atual
    cidade_atual = cidade
    destino = None
    if(verifica_fim(cidade)):
        return
    abreno(cidade)
    while len(estados_nao_visitados) > 0:
        nonovo = estados_nao_visitados.pop(0)
        cidade_atual = cidade_visitada(nonovo)
        destino = cidade_nao_visitada(nonovo)
        if destino not in cidades_visitadas and destino is not None:
            numeroestado += 1
            nonovo.printaEstado(numeroestado)
            abreno(destino, nonovo)
            if(verifica_fim(destino)):
                ultimoestado = nonovo
                break
    caminho()

# Busca gulosa
def acessa_estado_busca_gulosa(cidade):
    global numeroestado
    global ultimoestado
    global cidade_atual
    cidade_atual = cidade
    destino = None
    if(verifica_fim(cidade)):
        return
    abrenoGuloso(cidade)
    while len(estados_nao_visitados) == 1:
        nonovo = estados_nao_visitados.pop(0)
        cidade_atual = cidade_visitada(nonovo)
        destino = cidade_nao_visitada(nonovo)
        if destino not in cidades_visitadas and destino is not None:
            numeroestado += 1
            nonovo.printaEstado(numeroestado)
            abrenoGuloso(destino, nonovo)
            if(verifica_fim(destino)):
                ultimoestado = nonovo
                break
    caminho()

# Apaga as informações
def apaga_Informacoes():
    global cidades_visitadas
    global estados_nao_visitados
    global numeroestado
    global cidade_atual
    for estado in estados:
        estado.pai = None
    cidades_visitadas = []
    estados_nao_visitados = []
    numeroestado = 0
    cidade_atual = None

# Inicia o programa
if __name__ == '__main__':
    # Apaga as informações
    apaga_Informacoes()

    print("Busca em profundidade")
    # Acessa o estado inicial
    acessa_estado_busca_profundidade(cidade_inicial)

    # Apaga as informações
    apaga_Informacoes()
    
    print("\nBusca em largura")
    # Acessa o estado inicial
    acessa_estado_busca_largura(cidade_inicial)

    # Apaga as informações
    apaga_Informacoes()

    print("\nBusca gulosa")
    # Acessa o estado inicial
    acessa_estado_busca_gulosa(cidade_inicial)
