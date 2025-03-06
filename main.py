#!/usr/bin/env python3


import numpy as np
import gymnasium as gym

from game import GameState
from rl_utils import GameEnv

def main():
    
    gym.register(
        id="gymnasium_env/10000-v0",
        entry_point=GameEnv,
    )
    env = GameEnv()
    env.reset(seed=2)

    print()


if __name__ == "__main__":
    main()