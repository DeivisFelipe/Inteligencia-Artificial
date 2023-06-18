'''
Descrição da questõa

(Exerc. 2) Considere os seguintes operadores que descrevem os vôos existentes entre cidades de um país:
oper(1, a, b), 
oper(2, a, b), 
oper(3, a, d), 
oper(4, b, e), 
oper(5, b, f), 
oper(6, c, g), 
oper(7, c, h),
oper(8, c, i), 
oper(9, d, j), 
oper(10, e, k), 
oper(11, e, l), 
oper(12, g, m), 
oper(13, j, n), 
oper(14, j, o),
oper(15, k, f), 
oper(16, l, h), 
oper(17, m, d), 
oper(18, o, a), 
oper(19, n, b)
Por exemplo, o operador oper(1, a, b) indica que o vôo 1 parte da cidade A e chega na cidade B. Com base nesses
operadores, e supondo que eles sejam usados na ordem em que eles foram declarados, apresentar:
a) o passo a passo o estado das listas de novos abertos e nodos fechados usados pelo algoritmo de busca em largura e
algoritmo de busca em profundidade que levem da cidade A até a cidade J
b) desenhe a árvore de busca criada pelo algoritmo de busca em largura e algoritmo de busca em profundidade ao
procurar uma sequência de vôos que levem da cidade A até a cidade J.
c) Implementar algoritmos para solucionar as questões propostas. Entregar (i) print (em pdf) do passo a passo de
execução dos algoritmos e das soluções do problema e (ii) código fonte das implementações: legível, identado, variáveis
nomeadas de forma compreensível, comentado - padrão JavaDoc ou Doxigen, e orientado a objetos.
'''

# Adiciona biblioteca de grafos
import networkx as nx

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
        print("oper( " + str(self.voo) + ", " + self.cidade1 + ", " +
            self.cidade2 + ") = Numero: " + str(numeroestado))
        
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
estados.append(Estado(2, 'a', 'b'))
estados.append(Estado(3, 'a', 'd'))
estados.append(Estado(4, 'b', 'e'))
estados.append(Estado(5, 'b', 'f'))
estados.append(Estado(6, 'c', 'g'))
estados.append(Estado(7, 'c', 'h'))
estados.append(Estado(8, 'c', 'i'))
estados.append(Estado(9, 'd', 'j'))
estados.append(Estado(10, 'e', 'k'))
estados.append(Estado(11, 'e', 'l'))
estados.append(Estado(12, 'g', 'm'))
estados.append(Estado(13, 'j', 'n'))
estados.append(Estado(14, 'j', 'o'))
estados.append(Estado(15, 'k', 'f'))
estados.append(Estado(16, 'l', 'h'))
estados.append(Estado(17, 'm', 'd'))
estados.append(Estado(18, 'o', 'a'))
estados.append(Estado(19, 'n', 'b'))


# cidade inicial
cidade_inicial = 'a'

# Cidade final
cidade_final = 'j'

# Lista de cidade visitadas
cidades_visitadas = []

# Lista de todos os estados que ainda não foram visitados
estados_nao_visitados = []

# Estado acessado número de forma global
numeroestado = 1

def abreno(no):
    for estado in estados:
        if estado.cidade1 == no and estado.cidade2 not in cidades_visitadas:
            estado.addPai(no)
            estados_nao_visitados.append(estado)
            
    cidades_visitadas.append(no)

# acessa o estado
def acessa_estado_busca_profundidade(cidade):
    global numeroestado
    if(verifica_fim(cidade)):
        return
    abreno(cidade)
    while len(estados_nao_visitados) > 0:
        nonovo = estados_nao_visitados.pop(-1)
        if nonovo.cidade2 not in cidades_visitadas:
            numeroestado += 1
            nonovo.printaEstado(numeroestado)
            abreno(nonovo.cidade2)
            if(verifica_fim(nonovo.cidade2)):
                return

def verifica_fim(cidade):
    global cidade_final
    if cidade == cidade_final:
        print("Cidade final encontrada")
        return True
    return False

# Gera todos os estados possíveis a partir do estado atual
def gera_estados_possiveis(estado):
    # Lista de estados possíveis
    estados_possiveis = []

    # Percorre todos os estados e seleciona os estados que tem a cidade1 igual a cidade2 do estado atual
    for estadoPossivel in estados:
        if estadoPossivel.cidade1 == estado.cidade2:
            # verifica se o estado já foi visitado
            if not verifica_estado_visitado_ou_nao_visitado(estadoPossivel):
                estados_possiveis.append(estadoPossivel)

    return estados_possiveis

# Verifica se o estado esta dentro de estados visitados
def verifica_estado_visitado_ou_nao_visitado(estado):
    for cidadeVisitada in estados_visitados:
        if estado.cidade2 == cidadeVisitada:
            return True
    for estadoNaoVisitado in estados_nao_visitados:
        if estado == estadoNaoVisitado:
            return True
    return False

# Busca em Largura
def acessa_estado_busca_largura(cidade):
    global numeroestado
    if(verifica_fim(cidade)):
        return
    abreno(cidade)
    while len(estados_nao_visitados) > 0:
        nonovo = estados_nao_visitados.pop(0)
        if nonovo.cidade2 not in cidades_visitadas:
            numeroestado += 1
            nonovo.printaEstado(numeroestado)
            abreno(nonovo.cidade2)
            if(verifica_fim(nonovo.cidade2)):
                return


# Inicia o programa
if __name__ == '__main__':
    numeroestado = 0
    print("Busca em profundidade")
    # Acessa o estado inicial
    acessa_estado_busca_profundidade(cidade_inicial)

    # Limpando as listas
    cidades_visitadas = []
    estados_nao_visitados = []

    # Zerando o estado acessado
    numeroestado = 0

    print("Busca em largura")
    # Acessa o estado inicial
    acessa_estado_busca_largura(cidade_inicial)
