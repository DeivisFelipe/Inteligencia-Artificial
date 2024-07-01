'''
(Exerc. 4) O problema do Quebra-Cabeça de 8 consiste em movimentar as peças do quebra-cabeça horizontal ou 
verticalmente (para ocupar a posição vazia adjacente à peça) de modo que a conguração final seja alcançada:
Por exemplo, expandindo o estado corrente acima, temos:
Agora, usando uma função heurística, o algoritmo de busca deveria expandir o melhor entre esses dois estados 
sucessores. Mas como decidir qual deles é o melhor? Uma possibilidade é verificar o quão longe cada peça encontra-se 
de sua posição na conguração final e apontar como melhor estado aquele cuja soma das distâncias é mínima. Por 
exemplo, no estado s1, as peças 1, 5, 6, 7 e 8 já estão em suas posições finais. Para as peças 2, 3 e 4, a distância é 1. 
Portanto, h(s1) = 3. Analogamente, temos h(s2) = 5. Esses valores indicam que uma solução a partir do estado s1 pode 
ser obtida com no mínimo mais três expansões, enquanto que uma solução a partir de s2 requer no mínimo mais cinco 
expansões. Então, o algoritmo de busca deve expandir o estado s1.
a) Para esse problema, qual algoritmo seria mais apropriado: (i) o algoritmo de busca gulosa pela melhor escolha
considerando que cada ação tem custo 1 ou (ii) o algoritmo de busca gulosa pela melhor escolha considerando as 
estimativas heurísticas calculadas? 
Apresentar o b) passo a passo o estado das listas de novos abertos e nodos fechados e c) desenhe a árvore de busca
produzida pelos algoritmos citados em (i) e ii) para justificar a resposta apresentada.
Considere que no Quebra-Cabeça de 8 cada ação tem custo 1. Usando a heurística da soma das distâncias, apresentar: d) o passo a passo o estado das listas de novos abertos e nodos fechados usados pelo algoritmo A*
e) desenhe a árvore de busca produzida pelo algoritmo A* quando o estado inicial do quebra-cabeça é [[1, 2, 3], [b, 6,
4], [8, 7, 5]].
f) implementação dos algoritmos considerados neste exercício, onde deve ser entregue (i) print (em pdf) do passo a 
passo de execução dos algoritmos e das soluções do problema e (ii) código fonte das implementações: legível, identado, 
variáveis nomeadas de forma compreensível, comentado - padrão JavaDoc ou Doxigen, e orientado a objetos.
'''

# Classe estado
class Estado:
    # Atributos
    # Matriz
    matriz = None
    # Pai
    pai = None
    # Distancia
    distancia = None
    # Numero de acoes
    numeroacoes = None

    # Construtor
    def __init__(self, matriz):
        self.matriz = matriz

    # Set numero de acoes
    def setNumeroAcoes(self, numeroacoes):
        self.numeroacoes = numeroacoes

    # Printa o estado
    def printaEstado(self, numeroestado):
        print("Estado " + str(numeroestado) + ": Distancia " + str(self.distancia) + " Numero de acoes " + str(self.numeroacoes))
        # Printa de maneira formatada
        for i in range(0, 3):
            # Se for b, printa vazio
            if self.matriz[i][0] == 'b':
                print(" ", end=" ")
            else:
                print(self.matriz[i][0], end=" ")

            if self.matriz[i][1] == 'b':
                print(" ", end=" ")
            else:
                print(self.matriz[i][1], end=" ")

            if self.matriz[i][2] == 'b':
                print(" ", end=" ")
            else:
                print(self.matriz[i][2], end=" ")

            print("")

    # Verifica se o estado é igual
    def __eq__(self, other):
        # Verifica se a matriz é igual, todas celulas tem que ser iguais
        for i in range(0, 3):
            for j in range(0, 3):
                if self.matriz[i][j] != other.matriz[i][j]:
                    return False
        
        return True
    
    # adiciona o pai
    def addPai(self, pai):
        self.pai = pai

    # Todos os estados a partir do estado atual
    def estadosSucessores(self):
        # Lista de estados
        estados = []
        # Achou o b
        achoub = False
        # Posicao do b
        posicaob = None
        # Acha a posicao do b
        for i in range(0, 3):
            for j in range(0, 3):
                if self.matriz[i][j] == 'b':
                    posicaob = [i, j]
                    achoub = True
                    break
            if achoub:
                break

        # A partir da posicao do b, gera os estados sucessores
        # Cima
        if posicaob[0] > 0:
            # Copia a matriz
            matriz = []
            for i in range(0, 3):
                matriz.append(self.matriz[i].copy())
            # Troca o b
            matriz[posicaob[0]][posicaob[1]] = matriz[posicaob[0] - 1][posicaob[1]]
            matriz[posicaob[0] - 1][posicaob[1]] = 'b'
            # Adiciona o estado
            estados.append(Estado(matriz))

        # Baixo
        if posicaob[0] < 2:
            # Copia a matriz
            matriz = []
            for i in range(0, 3):
                matriz.append(self.matriz[i].copy())
            # Troca o b
            matriz[posicaob[0]][posicaob[1]] = matriz[posicaob[0] + 1][posicaob[1]]
            matriz[posicaob[0] + 1][posicaob[1]] = 'b'
            # Adiciona o estado
            estados.append(Estado(matriz))

        # Esquerda
        if posicaob[1] > 0:
            # Copia a matriz
            matriz = []
            for i in range(0, 3):
                matriz.append(self.matriz[i].copy())
            # Troca o b
            matriz[posicaob[0]][posicaob[1]] = matriz[posicaob[0]][posicaob[1] - 1]
            matriz[posicaob[0]][posicaob[1] - 1] = 'b'
            # Adiciona o estado
            estados.append(Estado(matriz))

        # Direita
        if posicaob[1] < 2:
            # Copia a matriz
            matriz = []
            for i in range(0, 3):
                matriz.append(self.matriz[i].copy())
            # Troca o b
            matriz[posicaob[0]][posicaob[1]] = matriz[posicaob[0]][posicaob[1] + 1]
            matriz[posicaob[0]][posicaob[1] + 1] = 'b'
            # Adiciona o estado
            estados.append(Estado(matriz))

        return estados

    # Pega heuristica
    def getHeuristica(self, estado_final):
        # Distancia
        self.distancia = 0
        for i in range(0, 3):
            for j in range(0, 3):
                # Achou o numero na matriz inicial
                achou = False
                # Acha o mesmo numero na matriz final
                for k in range(0, 3):
                    for l in range(0, 3):
                        if self.matriz[i][j] == estado_final.matriz[k][l]:
                            # Calcula a distancia
                            self.distancia += abs(i - k) + abs(j - l)
                            achou = True
                            break
                    if achou:
                        break

estado_final = Estado([[1, 2, 3], [8, 'b', 4], [7, 6, 5]])
estado_inicial = Estado([[1, 2, 3], ['b', 6, 4], [8, 7, 5]])

print("Estado inicial")
estado_inicial.getHeuristica(estado_final)
estado_inicial.setNumeroAcoes(0)
estado_inicial.printaEstado(0)

# Lista de estados abertos
estados_abertos = []

# Lista de estados fechados
estados_fechados = []

# Função que verifica se o estado já está na lista de estados abertos ou fechados
def estadoEstaNaLista(estado):
    global estados_abertos
    global estados_fechados

    # Achou
    achou = False

    # Verifica se está na lista de abertos
    for estado_aberto in estados_abertos:
        if estado_aberto == estado:
            achou = True
            break

    # Verifica se está na lista de fechados
    if not achou:
        for estado_fechado in estados_fechados:
            if estado_fechado == estado:
                achou = True
                break

    return achou


# Funcao de busca considerando a heuristica
def busca(estado_inicial, estado_final):
    # Abre o estado inicial
    possiveis_estados = estado_inicial.estadosSucessores()
    # Para cada estado sucessor verificar se já foi visitado ou se já está na lista de estados abertos
    for estado in possiveis_estados:
        if estadoEstaNaLista(estado) == False:
            # Adiciona o pai
            estado.addPai(estado_inicial)
            # Adiciona o estado sucessor
            estados_abertos.append(estado)
            # Calcula a heuristica
            estado.getHeuristica(estado_final)
            # Set numero de acoes
            estado.setNumeroAcoes(estado_inicial.numeroacoes + 1)

    # Ordena a lista de estados abertos
    estados_abertos.sort(key=lambda x: x.distancia + x.numeroacoes)

    # Fecha o estado inicial
    estados_fechados.append(estado_inicial)

    # Estado pos
    estado_pos = 1

    while len(estados_abertos) > 0:
        # Pega o primeiro estado
        estado_atual = estados_abertos.pop(0)
        # Printa o estado atual
        estado_atual.printaEstado(estado_pos)
        estado_pos += 1
        # Verifica se é o estado final
        if estado_atual == estado_final:
            return estado_atual
        # Abre o estado atual
        possiveis_estados = estado_atual.estadosSucessores()
        # Para cada estado sucessor verificar se já foi visitado ou se já está na lista de estados abertos
        for estado in possiveis_estados:
            if estadoEstaNaLista(estado) == False:
                # Adiciona o pai
                estado.addPai(estado_atual)
                # Adiciona o estado sucessor
                estados_abertos.append(estado)
                # Calcula a heuristica
                estado.getHeuristica(estado_final)
                # Set numero de acoes
                estado.setNumeroAcoes(estado_atual.numeroacoes + 1)

        # Ordena a lista de estados abertos
        estados_abertos.sort(key=lambda x: x.distancia + x.numeroacoes)

        # Fecha o estado atual
        estados_fechados.append(estado_atual)
    # Nao achou o estado final
    return None

# Busca
estado_final = busca(estado_inicial, estado_final)

# ##########
print("------------------  Estados abertos  ------------------")
for estado in estados_abertos:
    estado.printaEstado(0)