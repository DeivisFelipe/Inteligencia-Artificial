# -*- coding: utf-8 -*-
# Importando o Gym
import gym
# Criando 
env = gym.make("Taxi-v3")

# metodos que sera utilizado
method = 2

if method == 1:

    env.reset()
    # Listando as ações
    print("Total de Ações {}".format(env.action_space))
    # Total de Estados
    print("Total de Estados {}".format(env.observation_space))
    # Troca de Estado
    state = env.encode(3, 1, 2, 1)
    env.s = state
    env.render()

    # Rewards
    # -1 por cada passo ou bater em uma parede
    # -10 pegar ou deixar um passageiro em um local errado
    # 20 pegar ou deixar um passageiro em um local correto

    # Tabela de recompensas, onde cada linha é um estado e cada coluna uma ação, total de 500 estados e 6 ações possíveis = 3000
    env.P[329]

    # Tentando resolver o problema com ações aleatórias
    env.s = 329
    env.reset()
    epochs = 0 # Contador de passos
    penalties = 0 # Contador de penalidades
    done = False # Flag para indicar se o jogo terminou
    truncated = False # Flag para indicar se o jogo foi truncado

    while not done and not truncated:
        action = env.action_space.sample() # Escolhe uma ação aleatória
        state, reward, done, truncated, info = env.step(action) # Executa a ação

        if reward == -10:
            penalties += 1
        
        env.render()

        epochs += 1

    print("Timesteps tomados: {}".format(epochs)) # Total de passos
    print("Penalidades recebidas: {}".format(penalties)) # Total de penalidades

    # Finaliza o ambiente
    env.close()
elif method == 2:
    import numpy as np
    import time

    # Inicializa a tabela de valores Q
    # verifica se existe uma tabela Q salva no computador
    try:
        q_table = np.load("q_table.npy")
        print("Carregando tabela Q")
    except:
        print("Criando tabela Q")
        q_table = np.zeros(
            [env.observation_space.n, env.action_space.n]
        )

    import random

    # Hiperparâmetros
    alpha = 0.1 # Taxa de aprendizado
    gamma = 0.6 # Fator de desconto
    epsion = 0.1 # Taxa de exploração

    # Total de ações e penalidades recebidas durando a aprendizagem
    epochs = 0
    penalties = 0

    for i in range(1, 1): # 100000 versoões de treinamento
        state = env.reset() # incialização aleatória do ambiente
        state = state[0]
        done = False
        truncated = False
        rewards = 0
        epsodies = 0

        # Salva o q-table de forma definitiva no computador
        if i % 100000 == 0:
            np.save("q_table.npy", q_table)
            print("Salvando tabela Q")
            time.sleep(1)

        while not done and not truncated and epsodies < 200:
            if random.uniform(0, 1) < epsion:
                action = env.action_space.sample() # Escolhe uma ação aleatória
            else:
                action = np.argmax(q_table[state]) # Escolhe a melhor ação

            next_state, reward, done, truncated, info = env.step(action) # Executa a ação

            # Somatório das recompensas
            rewards += reward

            old_value = q_table[state, action] # Valor antigo da tabela Q
            next_max = np.max(q_table[next_state]) # Valor máximo da tabela Q para o próximo estado

            # Atualiza a tabela Q com base na equação de Bellman
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state, action] = new_value

            if reward == -10:
                penalties += 1

            state = next_state # Mudança de estado
            epsodies += 1

        print("Geração: {}, Episódio: {}, Recompensas: {}".format(i, epsodies, rewards))


    print("Treinamento finalizado.\n")
    print("Timesteps tomados: {}".format(epochs)) # Total de passos
    print("Penalidades recebidas: {}".format(penalties)) # Total de penalidades

    # Executa o ambiente com a tabela Q treinada, 100 vezes
    epochs = 0
    penalties = 0
    env = gym.make("Taxi-v3", render_mode="human")
    
    for i in range(1, 101):
        state = env.reset()
        state = state[0]
        done = False
        truncated = False
        rewards = 0
        epsodies = 0

        while not done and not truncated and epsodies < 200:
            action = np.argmax(q_table[state])
            state, reward, done, truncated, info = env.step(action)

            rewards += reward

            if reward == -10:
                penalties += 1

            epsodies += 1

        print("Geração: {}, Episódio: {}, Recompensas: {}, Penalidades: {}".format(i, epsodies, rewards, penalties))

env.close()