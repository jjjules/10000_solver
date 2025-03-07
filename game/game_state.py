from warnings import warn
from typing import Optional

import numpy as np
from multiset import Multiset

from .dice_checker import DiceCombinationChecker

TARGET_TIER = 10_000

class GameState:
    """
        Notes:
            - Ignoring yathzee's
            - A die with a value of zero should be ignored. Need that to have a mask of constant size
            - Simplify the tiers: only current tier (no history) and if you get 3 ticks, you lose 1000 points.
    """
    
    current_score: int
    current_tier: int
    current_number_of_ticks: int
    is_done: bool
    num_step: int
    available_dice: Multiset[int]
    reward: int
    np_random: np.random.Generator

    dice_checker = DiceCombinationChecker()

    def __init__(self, np_random: Optional[np.random.Generator] = None) -> None:
        if np_random is None:
            self.np_random = np.random.default_rng()
        else:
            self.np_random = np_random
        self.roll_new_dice(5)
        self.current_score = 0
        self.current_tier = 0
        self.current_number_of_ticks = 0
        self.reward = 0
        self.is_done = False

    
    def roll_new_dice(self, num_dice: int) -> None:
        self.available_dice = Multiset(self.np_random.integers(1, 7, num_dice, dtype=int))
    
    def keep(self, chosen_score: int, chosen_dice: Multiset[int]):
        """
            First function made to iterate through the command using command line
        """
        warn('Old function', DeprecationWarning)

        num_used_dice = self.dice_checker.create_combinations_and_match(self.available_dice, chosen_score, chosen_dice)
        if len(self.available_dice) == num_used_dice:
            # Main pleine
            self.roll_new_dice(5)
        else:
            self.roll_new_dice(len(self.available_dice) - num_used_dice)
        self.current_score += chosen_score
    
    def take_action(self, action_info):

        chosen_dice = action_info['chosen_dice']
        action_score = action_info['action_score']
        num_dice_left = action_info['num_dice_left']
        num_available_dice = action_info['num_available_dice']
        stop = action_info['stop']

        assert action_score >= 0

        # Verify action
        illegal = False
        if 0 in chosen_dice:
            # Chose a die that was not available
            illegal = True
        elif action_score == 0:
            # Correct way to handle that? How should the model tell to say "Ok take a tick the current tier and move on"
            # It should still be punished to try to make an illegal move?
            # TODO
            pass
        elif stop and num_dice_left == 0:
            # Can't stop if "main pleine"
            illegal == True
        elif not self.dice_checker.match(action_score, chosen_dice):
            # The chosen_dice {chosen_dice} does not correspond to a score of {action_score}
            illegal = True
        else:
            combinations = self.dice_checker.get_all_dice_combination(chosen_dice)
            kept_dice = next(filter(lambda x: len(x) + num_dice_left == num_available_dice, combinations), None)

            if kept_dice is None:
                # You can't combine {chosen_dice} to keep only {num_kept_dice} of them
                illegal = True
            else:
                if stop:
                    # You can't validate your current score if its not a multiple of 100
                    illegal = (self.current_score + action_score) % 100 != 0
                else:
                    # Valid move
                    # print(f"Success !!! You're keeping {kept_dice}")
                    pass
                
            
        if illegal:
            num_dice_left = 0
            self.is_done = True
            self.reward -= 100
            
            return
        else:
            self.reward -= 1
            
        if stop:
            new_tier = self.current_tier + self.current_score + action_score
            self.current_score = 0
            if action_score == 0 or new_tier > TARGET_TIER:
                if self.current_number_of_ticks >= 2:
                    
                    self.current_number_of_ticks = 0
                    self.current_tier -= 1000
                else:
                    self.current_number_of_ticks += 1
            else:
                self.current_tier = new_tier
                self.current_number_of_ticks = 0

                if self.current_tier == TARGET_TIER:
                    self.is_done = True
                    self.reward += 10000
            
            if self.is_done:
                num_dice_left = 0
            else:
                num_dice_left = 5
        else:
            self.current_score += action_score

            if num_dice_left == 0:
                # Main pleine
                num_dice_left = 5
        
        self.roll_new_dice(num_dice_left)

        return illegal
                
    def show(self):
        print(f'''
        Current score is {self.current_score:d}
        Current tier is {self.current_tier:d} with {self.current_number_of_ticks} tick(s)
        Current reward is {self.reward:d}
        Available dice: {[int(i) for i in sorted(self.available_dice)]}

        ''')

