from typing import Optional

import numpy as np
import gymnasium as gym
from gymnasium.spaces import Tuple, Dict, Box, Discrete, MultiBinary
from multiset import Multiset

from game import GameState


class GameEnv(gym.Env):
    def __init__(self, config=None):
        # self.game_state = GameState()

        self.action_space = Tuple([
            Box(0, 2000, dtype=int),       # score to keep, max 2000 with 4 one's
            MultiBinary(5),                 # dice to keep
            Discrete(5),                    # Number of dice left
            Discrete(2),                    # Whether to stop and keep the current_score
        ])
        self.observation_space = Dict({
            'Tier': Box(0, 10000, dtype=int),    #  Current tier (no tier history for now)
            'Ticks': Discrete(2),                # Number of tick for current tier
            'Score': Box(0, 10000, dtype=int),   # Current score
            'Dice': Discrete(5),                    # Number of dice left
        })

    def render(self):
        self.game_state.show()

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self.game_state = GameState(np_random=self.np_random)

        return self._get_obs(), self._get_info()

    def _get_obs(self):
        return {
            'Tier': self.game_state.current_tier,
            'Ticks': self.game_state.current_number_of_ticks,
            'Score': self.game_state.current_score,
            'Dice': 5 - len(self.game_state.available_dice),
        } 

    def _get_info(self):
        # TODO
        return {}

    def step(self, action):
        # Apply action and advance game state
        illegal = self.game_state.take_action(self.convert_action_to_action_info(action))

        truncated = False # TODO: ?

        info = self._get_info()
        info['illegal'] = True

        return self._get_obs(), self.game_state.reward, self.game_state.is_done, truncated, info
    
    def convert_action_to_action_info(self, action):
        action_score, chosen_dice_mask, num_dice_left, stop = action
        assert len(chosen_dice_mask) == 5

        available_dice_np = self.get_available_dice_as_numpy()
        num_available_dice = (available_dice_np>0).sum()
        chosen_dice = available_dice_np[chosen_dice_mask]
        chosen_dice = Multiset(chosen_dice.tolist())
        stop = stop == 1

        action_info = {
            'chosen_dice': chosen_dice,
            'action_score': int(action_score),
            'stop': stop == 1,
            'num_dice_left': num_dice_left,
            'num_available_dice': num_available_dice,
        }
        
        return action_info
    
    def get_available_dice_as_numpy(self) -> np.ndarray[int]:
        """
            Must be reliable and deterministic as we use a mask
            Fixed length of 5
            Return 0 for dice that are not available
        """
        available_dice = self.game_state.available_dice
        available_dice_np = np.zeros((5,))
        available_dice_np[:len(available_dice)] = sorted(available_dice)

        return available_dice_np
