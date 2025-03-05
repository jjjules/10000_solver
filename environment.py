import numpy as np
import gymnasium as gym
from gymnasium import Env
from gymnasium.spaces import Tuple, Discrete, MultiBinary
from multiset import Multiset

from game import GameState


class GameEnv(gym.Env):
    def __init__(self):
        self.game_state = GameState()

        self.action_space = Tuple([
            Discrete(int(2000 / 50)),  # score to keep, max 2000 with 4 one's
            MultiBinary(5),  # dice to keep
            Discrete(5),  # Number of dice left
            Discrete(2),  # Whether to stop and keep the current_score
        ])
        self.observation_space = Tuple([
            Discrete(101),  # Current tier (no tier history for now)
            Discrete(2),    # Number of tick for current tier
            Discrete(101),  # Current score
            Discrete(5),    # Number of dice left
        ])

    def step(self, action):
        # Apply action and advance game state
        self.apply_action_to_game(action)

        return self.game_state, self.game_state.reward, self.game_state.is_done
    
    def render(self):
        self.game_state.show()

    def reset(self):
        # TODO
        pass

    def convert_action_to_action_info(self, action):
        action_score_id, chosen_dice_mask, num_dice_left, stop = action
        assert len(chosen_dice_mask) == 5

        available_dice_np = self.game_state.get_dice_as_numpy()
        num_available_dice = (available_dice_np>0).sum()
        chosen_dice = available_dice_np[chosen_dice_mask]
        chosen_dice = Multiset(chosen_dice.tolist())
        action_score = 50 + action_score_id * 50
        stop = stop == 1

        action_info = {
            'chosen_dice': chosen_dice,
            'action_score': action_score,
            'stop': stop == 1,
            'num_dice_left': num_dice_left,
            'num_available_dice': num_available_dice,
        }
        
        return action_info

    def apply_action_to_game(self, action):
        self.game_state.keepv2(self.convert_action_to_action_info(action))
        # TODO: add observation
