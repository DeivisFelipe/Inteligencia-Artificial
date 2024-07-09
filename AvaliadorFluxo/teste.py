import matplotlib.pyplot as plt

# Dados
meses = [1, 2, 3, 4, 5, 6]
demanda = [780, 890, 770, 750, 720, 790]
previsao = [650, 750, 850, 800, 700, 850]
erros = [d - f for d, f in zip(demanda, previsao)]
mad = 80
sinal_monitoramento = [sum(erros[:i+1]) / mad for i in range(len(erros))]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(meses, erros, marker='o', label='Erros de Previsão')
plt.plot(meses, sinal_monitoramento, marker='o', linestyle='--', label='Sinal de Monitoramento')
plt.axhline(y=1.5, color='r', linestyle='--', label='Limite Superior (+1.5 MADs)')
plt.axhline(y=-1.5, color='r', linestyle='--', label='Limite Inferior (-1.5 MADs)')
plt.axhline(y=0, color='black', linestyle='-', label='Erro Zero')
plt.title('Erros de Previsão e Sinal de Monitoramento')
plt.xlabel('Mês')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.show()