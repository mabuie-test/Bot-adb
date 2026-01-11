"""
envs/simulator.py
Gerador de rounds para treino e testes.
"""
import random
import math

class Simulator:
    def __init__(self, seed: int = None, crash_prob_base: float = 0.02):
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self.crash_prob_base = crash_prob_base

    def generate_round(self, max_steps=1000):
        seq = []
        mul = 1.0
        step = 0
        while step < max_steps:
            growth = 1.0 + random.random() * 0.12
            mul *= growth
            seq.append(round(mul, 4))
            step += 1
            crash_p = self.crash_prob_base + math.log1p(step) * 0.0005
            if random.random() < crash_p:
                break
        return seq

