import gym #importação do Gym
import tensorflow as tf
import numpy as np

env = gym.make("CartPole-v1", render_mode="human") # Criando um ambiente do CartPole-v1 e 
#salvando os frames em um array RGB



def play_one_step(env, obs, model, loss_fn):
    with tf.GradientTape() as tape:  # Define um contexto para calcular gradientes
        left_proba = model(obs[np.newaxis])  # Calcula a probabilidade de ação "esquerda"
        action = (tf.random.uniform([1, 1]) > left_proba)  # Escolhe aleatoriamente entre "esquerda" e "direita" com base na probabilidade calculada
        y_target = tf.constant([[1.]]) - tf.cast(action, tf.float32)  # Calcula o alvo para o treinamento da rede neural
        loss = tf.reduce_mean(loss_fn(y_target, left_proba))  # Calcula a perda (loss) com base no alvo e na probabilidade de ação "esquerda"

    grads = tape.gradient(loss, model.trainable_variables)  # Calcula os gradientes da perda em relação aos parâmetros do modelo
    obs, reward, done, truncated, info = env.step(int(action))  # Executa a ação escolhida no ambiente do OpenAI Gym
    return obs, reward, done, truncated, grads  # Retorna a observação atual, a recompensa, se o episódio terminou, se a execução foi truncada e os gradientes calculados.
    
def discount_rewards(rewards, discount_factor):
    discounted = np.array(rewards)
    for step in range(len(rewards) - 2, -1, -1):
        discounted[step] += discounted[step + 1] * discount_factor
    return discounted

def discount_and_normalize_rewards(all_rewards, discount_factor):
    all_discounted_rewards = [discount_rewards(rewards, discount_factor)
                              for rewards in all_rewards]
    flat_rewards = np.concatenate(all_discounted_rewards)
    reward_mean = flat_rewards.mean()
    reward_std = flat_rewards.std()
    return [(discounted_rewards - reward_mean) / reward_std
            for discounted_rewards in all_discounted_rewards]

def play_multiple_episodes(env, n_episodes, n_max_steps, model, loss_fn):
    all_rewards = []       # Lista vazia para armazenar as recompensas de todos os episódios
    all_grads = []         # Lista vazia para armazenar os gradientes de todos os episódios
    for episode in range(n_episodes):     # Loop pelos episódios
        current_rewards = []              # Lista vazia para armazenar as recompensas do episódio atual
        current_grads = []                # Lista vazia para armazenar os gradientes do episódio atual
        obs, info = env.reset()           # Reseta o ambiente e obtém o estado inicial
        for step in range(n_max_steps):   # Loop pelo número máximo de passos permitidos em um episódio
            obs, reward, done, truncated, grads = play_one_step(
                env, obs, model, loss_fn) # Realiza um passo e obtém a observação, a recompensa, o sinal de conclusão, o sinal de trucamento e os gradientes do modelo
            current_rewards.append(reward) # Adiciona a recompensa do passo atual à lista de recompensas do episódio atual
            current_grads.append(grads)    # Adiciona os gradientes do passo atual à lista de gradientes do episódio atual
            if done or truncated:          # Se a condição de término ou truncamento for atendida, sai do loop de passos
                break
        all_rewards.append(current_rewards) # Adiciona a lista de recompensas do episódio atual à lista de todas as recompensas
        all_grads.append(current_grads)     # Adiciona a lista de gradientes do episódio atual à lista de todos os gradientes

    return all_rewards, all_grads          # Retorna todas as recompensas e gradientes obtidos nos episódios

def pg_policy(obs): # define uma função que recebe uma observação como entrada
    left_proba = model.predict(obs[np.newaxis], verbose=0) # calcula a probabilidade de tomar uma ação para a esquerda com base na observação usando o modelo neural
    return int(np.random.rand() > left_proba) # retorna 0 ou 1 com base na probabilidade de tomar uma ação para a esquerda ou para a direita

n_iterations = 300
n_episodes_per_update = 10
n_max_steps = 500
discount_factor = 0.95

tf.random.set_seed(42)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(5, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])

obs, info = env.reset(seed=42)

optimizer = tf.keras.optimizers.Nadam(learning_rate=0.01)
loss_fn = tf.keras.losses.binary_crossentropy

obs, info = env.reset(seed=42) # Inicializa o ambiente, bem como um dicionário que pode conter informações extras
obs

for iteration in range(n_iterations):
    all_rewards, all_grads = play_multiple_episodes(env, n_episodes_per_update, n_max_steps, model, loss_fn)

    # código extra – exibe algumas informações de depuração durante o treinamento
    total_rewards = sum(map(sum, all_rewards))
    print(f"\rIteration: {iteration + 1}/{n_iterations},"
          f" mean rewards: {total_rewards / n_episodes_per_update:.1f}", end="")

    all_final_rewards = discount_and_normalize_rewards(all_rewards,
                                                       discount_factor)
    all_mean_grads = []
    for var_index in range(len(model.trainable_variables)):
        mean_grads = tf.reduce_mean(
            [final_reward * all_grads[episode_index][step][var_index]
             for episode_index, final_rewards in enumerate(all_final_rewards)
                 for step, final_reward in enumerate(final_rewards)], axis=0)
        all_mean_grads.append(mean_grads)

    optimizer.apply_gradients(zip(all_mean_grads, model.trainable_variables))

env.close()