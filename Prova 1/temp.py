import string 

nos = list(string.ascii_lowercase[:14]) 

links = [
 ['a', 'b', 1],
 ['c', 'f', 5],
 ['a', 'c', 2],
 ['a', 'd', 3],
 ['b', 'e', 4],
]

cidadeinicial = 'a'
cidadefinal = 'e'

nosabertos =[]

pilha = []

def abreno(no):
    print(no)
    for nolink in links:
        if nolink[0] == no['no']:
            pilha.append({'no' : nolink[1], 'pai': no})
            
    nosabertos.append(no)
    

def buscalargura(no):
    abreno(no)
    while len(pilha) > 0:
        nonovo = pilha.pop(0)
        if nonovo not in nosabertos:
            abreno(nonovo)


pilha.append({'no' : cidadeinicial , 'pai' : None})
primeiro = pilha.pop(0)

buscalargura(primeiro)

# pega o caminho

caminho = None
for no in nosabertos:
    if no['no'] == cidadefinal:
        caminho = no

print("Caminho")
print(caminho)