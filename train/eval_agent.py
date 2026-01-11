"""
train/eval_agent.py
Avalia o modelo treinado por N episódios.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'envs')))
sys.path.insert(0, os.path.abspath(os.getcwd()))
from envs.env_aviator import AviatorEnv
from stable_baselines3 import PPO

def evaluate(model_path='models/policy_latest', episodes=100):
    env = AviatorEnv()
    model = PPO.load(model_path)
    total_reward = 0.0
    for ep in range(episodes):
        obs, _ = env.reset()
        done = False
        ep_r = 0.0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, r, done, truncated, info = env.step(int(action))
            ep_r += r
        total_reward += ep_r
    print('Avg reward:', total_reward / episodes)

if __name__ == '__main__':
    evaluate()

