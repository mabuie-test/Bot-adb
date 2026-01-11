"""
envs/env_aviator.py
Gym/Gymnasium environment que simula um round aviator-like.
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Tuple, Dict

try:
    from simulator import Simulator
except Exception:
    from ..simulator import Simulator  # quando importado a partir da raiz do projecto

class AviatorEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, config: Dict = None):
        self.config = config or {}
        seed = self.config.get('seed', None)
        self.sim = Simulator(seed=seed)
        self.max_history = 16
        self.observation_space = spaces.Box(low=0.0, high=1e6, shape=(self.max_history,), dtype=np.float32)
        self.action_space = spaces.Discrete(2)
        self._episode_seq = []
        self._tick_index = 0
        self._done = False

    def reset(self, seed=None, options=None) -> Tuple[np.ndarray, dict]:
        self._episode_seq = self.sim.generate_round()
        self._tick_index = 0
        self._done = False
        return self._get_obs(), {}

    def _get_obs(self) -> np.ndarray:
        hist = np.zeros(self.max_history, dtype=np.float32)
        for i in range(min(self._tick_index + 1, len(self._episode_seq))):
            hist[i] = float(self._episode_seq[i])
        return hist

    def step(self, action: int):
        if self._done:
            return self._get_obs(), 0.0, True, False, {}
        if self._tick_index >= len(self._episode_seq):
            self._done = True
            return self._get_obs(), 0.0, True, False, {}

        current_mul = self._episode_seq[self._tick_index]
        reward = 0.0
        done = False

        if action == 1:
            reward = current_mul - 1.0
            done = True
            self._done = True
        else:
            self._tick_index += 1
            if self._tick_index >= len(self._episode_seq):
                reward = -1.0
                done = True
                self._done = True
            else:
                reward = 0.0
                done = False

        return self._get_obs(), float(reward), bool(done), False, {}

    def render(self):
        cur = self._episode_seq[self._tick_index] if self._tick_index < len(self._episode_seq) else "CRASH"
        print(f"Tick {self._tick_index}/{len(self._episode_seq)}: {cur}")

