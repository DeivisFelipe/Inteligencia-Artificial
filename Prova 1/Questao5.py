'''
(Exerc. 5) Consider o seguinte problema.
Dados 10 palitos cada jogador pode retirar 1, 2 ou 3 por turno. Perde o jogador que retira o último palito. A pergunta é: 
será que max pode ganhar o jogo?
Usando a seguinte função de utilidade: F(S) = +1 se MAX ganhar, -1 se MIN ganhar, desenhar a árvore de busca. 
a) Apresentar os valores de min e max propagados na árvore de busca construída
b) Adotando a poda alfa-beta, nos sentidos i) da esquerda para a direita e ii) da direita para a esquerda, indicar quais 
arestas/subárvores serão podadas.
c) Implementar algoritmos para solucionar as questões propostas. Entregar (i) print (em pdf) do passo a passo de 
execução dos algoritmos e das soluções do problema e (ii) código fonte das implementações: legível, identado, variáveis 
nomeadas de forma compreensível, comentado - padrão JavaDoc ou Doxigen, e orientado a objetos.
'''

# Classe do estado
class Estado:
    # numero de palitos
    palitos = 0
    # jogador atual
    jogador = 0
    # Pai
    pai = None

    # Construtor
    def __init__(self, palitos, jogador):
        self.palitos = palitos
        self.jogador = jogador

    # Retorna o numero de palitos
    def getPalitos(self):
        return self.palitos
    
    # Retorna o jogador atual
    def getJogador(self):
        return self.jogador
        
    # Seta o pai
    def setPai(self, pai):
        self.pai = pai
    

# Cria o estado inicial
estadoInicial = Estado(10, 1)

# Funcao Min Max
def minMax(estado):
    # Se o estado atual eh terminal
    if estado.getPalitos() <= 0:
        # Se o jogador atual eh o max
        if estado.getJogador() == 1:
            # Retorna -1
            return estado, -1
        # Se o jogador atual eh o min
        else:
            # Retorna 1
            return estado, 1
    # Se o estado atual nao eh terminal
    else:
        # Se o jogador atual eh o max
        if estado.getJogador() == 1:
            # Inicializa o valor maximo
            valorMax = -9999
            estadoRetorno = None
            # Para cada jogada possivel
            for i in range(1, 4):
                # Cria o novo estado
                novoEstado = Estado(estado.getPalitos() - i, 2)
                novoEstado.setPai(estado)
                # Chama a funcao minMax
                temp, valor = minMax(novoEstado)
                # Se o valor eh maior que o valor maximo
                if valor > valorMax:
                    # Atualiza o valor maximo
                    valorMax = valor
                    estadoRetorno = temp
            # Retorna o valor maximo
            return estadoRetorno, valorMax
        # Se o jogador atual eh o min
        else:
            # Inicializa o valor minimo
            valorMin = 9999
            estadoRetorno = None
            # Para cada jogada possivel
            for i in range(1, 4):
                # Cria o novo estado
                novoEstado = Estado(estado.getPalitos() - i, 1)
                novoEstado.setPai(estado)
                # Chama a funcao minMax
                temp, valor = minMax(novoEstado)
                # Se o valor eh menor que o valor minimo
                if valor < valorMin:
                    # Atualiza o valor minimo
                    valorMin = valor
                    estadoRetorno = temp
            # Retorna o valor minimo
            return estadoRetorno, valorMin
        

# Executa a funcao minMax
estado, valor = minMax(estadoInicial)

print("Valor: " + str(valor))

# Header
print("Estado: Palitos Jogador MAX/MIN")

# Importa modulo que cria tabela
from tabulate import tabulate

# Imprime o estado
if estado.getJogador() == 1:
    # Printa formato: Estado: Palitos Jogador MAX
    print("Estado: " + str(estado.getPalitos()) + " " + str(estado.getJogador()) + " MAX")
else:
    # Printa formato: Estado: Palitos Jogador MIN
    print("Estado: " + str(estado.getPalitos()) + " " + str(estado.getJogador()) + " MIN")

# Percorre os pais
while estado.pai != None:
    # Jogador
    if estado.pai.getJogador() == 1:
        print("Estado: " + str(estado.pai.getPalitos()) + "\t\t\t\t" + str(estado.pai.getJogador()) + " MAX")
    else:
        print("Estado: " + str(estado.pai.getPalitos()) + "\t\t\t\t" + str(estado.pai.getJogador()) + " MIN")
    
    # Atualiza o estado
    estado = estado.pai


# Cria a tabela usando o modulo tabulate
tabela = [["Estado", "Palitos", "Jogador"],
            ["Inicial", "10", "MAX"],
            ["1", "9", "MIN"],
            ["2", "8", "MAX"],
            ["3", "7", "MIN"],
            ["4", "6", "MAX"],
            ["5", "5", "MIN"],
            ["6", "4", "MAX"],
            ["7", "3", "MIN"],
            ["8", "2", "MAX"],
            ["9", "1", "MIN"],
            ["10", "0", "MAX"]]
# Imprime a tabela
print(tabulate(tabela, headers='firstrow', tablefmt='fancy_grid'))