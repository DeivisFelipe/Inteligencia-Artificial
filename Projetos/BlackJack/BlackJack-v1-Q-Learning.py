import gym
import numpy as np
import time

# Treinamento
env = gym.make("Blackjack-v1", natural=True, render_mode="ansi")

# Ações possíveis (0 = parar, 1 = pedir carta)
actions_space = env.action_space
print("Total de Ações {}".format(actions_space))

# Total de Estados
states_space = env.observation_space
print("Total de Estados {}".format(states_space))

# Tabela Q, verifica se existe uma tabela Q salva no computador
try:
    q_table = np.load("./Estudo/Taxi/q_table_blackjack.npy")
    print("Carregando tabela Q")
except:
    q_table = np.zeros([32, 11, 2, 2])
    print("Criando tabela Q")

# Variaivel se tem que treinar ou não
train = False

if train:
    # Hiperparametros
    alpha = 0.1 # Taxa de aprendizado
    gamma = 0.6 # Fator de desconto
    epsion = 0.1 # Taxa de exploração
    gerations = 1000 # Total de gerações de treinamento

    for i in range(1, gerations):
        # Total de ações, recompensas, penalidades recebidas durando a aprendizagem
        penalties = 0
        rewards = 0
        epsodies = 0

        # Inicializa o ambiente
        state = env.reset()
        state = state[0]
        done = False
        truncated = False

        # Salva o q-table de forma definitiva no computador
        if i % 100000 == 0:
            np.save("./Estudo/Taxi/q_table_blackjack.npy", q_table)
            print("Salvando tabela Q")
            time.sleep(1)

        while not done and not truncated and epsodies < 5:
            if np.random.uniform(0, 1) < epsion:
                action = env.action_space.sample() # Escolhe uma ação aleatória
            else:
                auxBool = 1 if state[2] else 0
                action = np.argmax(q_table[state[0], state[1], auxBool, :]) # Escolhe a melhor ação

            # Executa a ação
            next_state, reward, done, truncated, info = env.step(action)

            # Atualiza a pontuação
            rewards += reward

            auxBoolState = 1 if state[2] else 0
            old_value = q_table[state[0], state[1], auxBoolState, action] # Valor antigo da tabela Q
            auxBool = 1 if next_state[2] else 0
            next_max = np.max(q_table[next_state[0], next_state[1], auxBool, :]) # Valor máximo da tabela Q

            # Atualiza a tabela Q com base na equação de Bellman
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            
            q_table[state[0], state[1], auxBoolState, action] = new_value

            if reward == -1:
                penalties += 1

            state = next_state
            epsodies += 1

        print("Geração: {}, Episódio: {}, Recompensas: {}".format(i, epsodies, rewards))

    print("Treinamento finalizado.\n")

else:
    # Executa o ambiente com a tabela Q treinada, 100 vezes
    epochs = 0
    penalties = 0
    env = gym.make("Blackjack-v1", render_mode="human", natural=True)

    vitorias = 0
    derrotas = 0
    empates = 0
    
    for i in range(1, 101):
        state = env.reset()
        state = state[0]
        done = False
        truncated = False
        rewards = 0
        epsodies = 0

        while not done and not truncated and epsodies < 5:
            auxBool = 1 if state[2] else 0
            action = np.argmax(q_table[state[0], state[1], auxBool, :])
            state, reward, done, truncated, info = env.step(action)

            rewards += reward

            if reward == -1:
                penalties += 1

            epsodies += 1

        if rewards == 1:
            vitorias += 1
        elif rewards == 0:
            empates += 1
        else:
            derrotas += 1

        print("Geração: {}, Episódio: {}, Recompensas: {}, Penalidades: {}".format(i, epsodies, rewards, penalties))

    # Porcentagem de vitórias comparado com o total de jogos
    print("Vitórias: {}%".format(vitorias))
    print("Empates: {}%".format(empates))
    print("Derrotas: {}%".format(derrotas))

#env.close()