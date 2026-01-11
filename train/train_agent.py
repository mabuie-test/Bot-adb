"""
train/train_agent.py
Treina um agente PPO no ambiente AviatorEnv.
"""
import os
import yaml
import sys
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "envs")))
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), "")))

from envs.env_aviator import AviatorEnv

CFG = yaml.safe_load(open(os.path.join('configs', 'agent_config.yaml'), 'r'))

def make_env():
    return AviatorEnv(config={'seed': CFG.get('simulator', {}).get('seed', None)})

def train():
    env = make_env()
    policy_kwargs = CFG.get('agent', {}).get('policy_kwargs', {})
    model = PPO('MlpPolicy', env, verbose=1, policy_kwargs=policy_kwargs, learning_rate=CFG.get('train', {}).get('learning_rate', 3e-4))
    os.makedirs('models/checkpoints', exist_ok=True)
    checkpoint_cb = CheckpointCallback(save_freq=5000, save_path='models/checkpoints', name_prefix='ppo_aviator')
    total = CFG.get('train', {}).get('total_timesteps', 200000)
    model.learn(total_timesteps=total, callback=checkpoint_cb)
    model.save('models/policy_latest')
    print('Treino terminado. Modelo salvo em models/policy_latest.zip')

if __name__ == '__main__':
    train()

