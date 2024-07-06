'''
Descrição da questão

(Exerc. 01) O Problema do Fazendeiro consiste no seguinte:
Um fazendeiro encontra-se na margem esquerda de um rio, levando consigo um lobo, uma ovelha e um repolho. O
fazendeiro precisa atingir a outra margem do rio com toda a sua carga intacta, mas para isso dispõe somente de um
pequeno bote com capacidade para levar apenas ele mesmo e mais uma de suas cargas. O fazendeiro poderia cruzar o
rio quantas vezes fossem necessárias para trasportar seus pertences, mas o problema é que, na ausência do fazendeiro,
o lobo pode comer a ovelha e essa, por sua vez, pode comer o repolho. Encontrar:
a) uma sequência de passos que resolva esse problema.
Para representar os estados desse problema, podemos usar uma estrutura da forma [F, L, O, R], cujas variáveis denotam,
respectivamente, as posições do fazendeiro, do lobo, da ovelha e do repolho. Cada variável pode assumir os valores e ou
d, dependendo da margem do rio onde o objeto se encontra. As ações podem ser representadas pelos seguintes
operadores:
oper(vai, [e, L, O, R], [d, L, O, R]) ← L ≠ O; O ≠ R
oper(levaLobo, [e, e, O, R], [d, d, O, R]) ← O ≠ R
oper(levaOvelha, [e, L, e, R], [d, L, d, R])
oper(levaRepolho, [e, L, O, e], [d, L, O, d]) ← L ≠ O
oper(volta, [d, L, O, R], [e, L, O, R]) ← L ≠ O, O ≠ R
oper(trazLobo, [d, d, O, R], [e, e, O, R]) ← O ≠ R
oper(trazOvelha, [d, L, d, R], [e, L, e, R])
oper(trazRepolho, [d, L, O, d], [e, L, O, e]) ← L ≠ O
O estado inicial é s0 = [e; e; e; e] e o conjunto de estados meta é G = {[d, d, d, d]}. Com base nessa especificação,
apresentar:
b) o passo a passo o estado das listas de novos abertos e nodos fechados usada pelo algoritmo de busca em
profundidade e pelo algoritmo de busca em largura
c) desenhe a árvore de busca criada pelo algoritmo de busca em profundidade e pelo algoritmo de busca em largura
ao procurar a solução do problema.
c) Implementar algoritmos para solucionar as questões propostas. Entregar (i) print (em pdf) do passo a passo de
execução dos algoritmos e das soluções do problema e (ii) código fonte das implementações: legível, identado, variáveis
nomeadas de forma compreensível, comentado - padrão JavaDoc ou Doxigen, e orientado a objetos.
'''

# cria a classe estado
class Estado:
    # atributos
    lobo = None
    ovelha = None
    repolho = None
    fazendeiro = None

    # construtor
    def __init__(self, fazendeiro, lobo, ovelha, repolho):
        self.lobo = lobo
        self.ovelha = ovelha
        self.repolho = repolho
        self.fazendeiro = fazendeiro

    def verificaValido(self):
        # Verifica se o lobo comeu a ovelha
        if self.lobo == self.ovelha and self.fazendeiro != self.lobo:
            return False

        # Verifica se a ovelha comeu o repolho
        if self.ovelha == self.repolho and self.fazendeiro != self.ovelha:
            return False

        return True
    
    def printaEstado(self, numeroestado):
        # Header
        print('F | L | O | R | Acessado: ' + str(numeroestado))
        # Estado
        print(self.fazendeiro + ' | ' + self.lobo + ' | ' + self.ovelha + ' | ' + self.repolho)
        # Pula linha
        print('')

    # verifica se o estado é igual
    def __eq__(self, other):
        # verifica se o fazendeiro é igual
        if self.fazendeiro != other.fazendeiro:
            return False

        # verifica se o lobo é igual
        if self.lobo != other.lobo:
            return False

        # verifica se a ovelha é igual
        if self.ovelha != other.ovelha:
            return False

        # verifica se o repolho é igual
        if self.repolho != other.repolho:
            return False

        return True

# Estado inicial
estado_inicial = Estado('e', 'e', 'e', 'e')

# Estado final
estado_final = Estado('d', 'd', 'd', 'd')

# Lista de todos os estados já visitados
estados_visitados = []

# Lista de todos os estados que ainda não foram visitados
estados_nao_visitados = []

# Estado acessado número de forma global
numeroestado = 0

# acessa o estado 
def acessa_estado_busca_profundidade(estado):
    global numeroestado
    # incrementa o numero de estados acessados de forma global
    numeroestado += 1
    # printa o estado final
    estado.printaEstado(numeroestado)

    # verifica se o estado é o estado final
    if estado == estado_final:
        return estado

    # adiciona o estado na lista de estados visitados
    estados_visitados.append(estado)

    # Gera todos os estados possíveis a partir do estado atual
    estados_possiveis = gera_estados_possiveis(estado)

    # Inverte a lista de estados possíveis
    estados_possiveis.reverse()

    # adiciona os estados possíveis na lista de estados não visitados
    for estadoNovo in estados_possiveis:
        estados_nao_visitados.append(estadoNovo)

    # Enquanto tiver tiver estados posiíveis, vai dando pop e acessando os estados
    while len(estados_nao_visitados) > 0:
        # Pega o primeiro estado da lista de estados não visitados
        estadoRetirado = estados_nao_visitados.pop(len(estados_nao_visitados) - 1)

        # Acessa o estado
        resposta = acessa_estado_busca_profundidade(estadoRetirado)

        # verifica se reposta é um estado ou null
        if resposta is not None:
            return resposta
        
    return None

# Gera todos os estados possíveis a partir do estado atual
def gera_estados_possiveis(estado):
    # Lista de estados possíveis
    estados_possiveis = []

    # Verifica se o fazendeiro está na margem esquerda
    estado1 = Estado('d' if estado.fazendeiro == 'e' else 'e', estado.lobo, estado.ovelha, estado.repolho)

    estado2 = Estado('d' if estado.fazendeiro   == 'e' else 'e', 'd' if estado.lobo == 'e' else 'e', estado.ovelha, estado.repolho)

    estado3 = Estado('d' if estado.fazendeiro == 'e' else 'e', estado.lobo, 'd' if estado.ovelha == 'e' else 'e', estado.repolho)

    estado4 = Estado('d' if estado.fazendeiro == 'e' else 'e', estado.lobo, estado.ovelha, 'd' if estado.repolho == 'e' else 'e')

    # verifica se não é um estado visitado e se é um estado valido
    if not verifica_estado_visitado_ou_nao_visitado(estado1) and estado1.verificaValido():
        estados_possiveis.append(estado1)
    if not verifica_estado_visitado_ou_nao_visitado(estado2) and estado2.verificaValido():
        estados_possiveis.append(estado2)
    if not verifica_estado_visitado_ou_nao_visitado(estado3) and estado3.verificaValido():
        estados_possiveis.append(estado3)
    if not verifica_estado_visitado_ou_nao_visitado(estado4) and estado4.verificaValido():
        estados_possiveis.append(estado4)

    return estados_possiveis

# Verifica se o estado esta dentro de estados visitados
def verifica_estado_visitado_ou_nao_visitado(estado):
    for estadoVisitado in estados_visitados:
        if estado == estadoVisitado:
            return True
    
    for estadoNaoVisitado in estados_nao_visitados:
        if estado == estadoNaoVisitado:
            return True
    
    return False

# Busca em Largura
def acessa_estado_busca_largura(estado):
    global numeroestado
    numeroestado += 1
    # printa o estado final
    estado.printaEstado(numeroestado)

    # verifica se o estado é o estado final
    if estado == estado_final:
        return estado

    # adiciona o estado na lista de estados visitados
    estados_visitados.append(estado)

    # Gera todos os estados possíveis a partir do estado atual
    estados_possiveis = gera_estados_possiveis(estado)

    # adiciona os estados possíveis na lista de estados não visitados
    for estadoNovo in estados_possiveis:
        estados_nao_visitados.append(estadoNovo)

    # Enquanto tiver tiver estados posiíveis, vai dando pop e acessando os estados
    while len(estados_nao_visitados) > 0:
        # Pega o primeiro estado da lista de estados não visitados
        estadoRetirado = estados_nao_visitados.pop(0)

        # Acessa o estado
        resposta = acessa_estado_busca_largura(estadoRetirado)

        # verifica se reposta é um estado ou null
        if resposta is not None:
            return resposta
        
    return None

# Inicia o programa
if __name__ == '__main__':
    numeroestado = 0
    print("Busca em profundidade")
    # Acessa o estado inicial
    acessa_estado_busca_profundidade(estado_inicial)

    # Limpando as listas
    estados_visitados = []
    estados_nao_visitados = []

    # Zerando o estado acessado
    numeroestado = 0

    print("Busca em largura")
    # Acessa o estado inicial
    acessa_estado_busca_largura(estado_inicial)