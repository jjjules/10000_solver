#!/usr/bin/env python3


from multiset import Multiset

import numpy as np
import gymnasium as gym

from game import GameState
from rl import GameEnv

def main():
    
    gym.register(
        id="gymnasium_env/10000-v0",
        entry_point=GameEnv,
    )
    env = GameEnv()
    env.reset(seed=2)

    while(True):
        if env.game_state.is_done:
            print()
            print('NEW GAME')
            print()
            env = GameEnv()
        env.render()
        correct = False
        while(not correct):
            try:
                user_input = input("Select your move (score_to_keep-dice_to_keep-num_dice_kept-end_turn): ")
                score_to_keep, dice_to_keep, num_dice_left, end_turn = user_input.split('-')
                dice_to_keep = [x == '1' for x in dice_to_keep]
                num_dice_left = int(num_dice_left)
                end_turn = end_turn == '1'

                assert len(dice_to_keep) == 5
                correct = True
            except Exception as e:
                print('ERROR:', e)
                continue

        env.step((score_to_keep, dice_to_keep, num_dice_left, end_turn))
    exit(0)
    
    """
        Inputs for good game start:

        300-11111-0-0
        400-11100-2-0
        100-10000-1-1
        550-11111-0-0
        100-10000-4-0
        200-11110-0-0
        1050-11110-1-1

    """

    game.available_dice = Multiset([1,2,3,5,6])
    game.show()

    while True:
        try:
            user_input = input("Enter the dice combinations you want to keep (prepend 'done ' to stop) -> ")

            if not user_input or user_input.startswith('done '):
                if user_input.startswith('done '):
                    user_input = user_input[5:]

                stop = True
            else:
                stop = False

            if user_input:
                chosen_score, *chosen_dice = user_input.split()
                chosen_score = int(chosen_score)
                chosen_dice = Multiset([int(x) for x in chosen_dice])
                game.keep(chosen_score, chosen_dice)

            if stop:
                if not user_input:
                    print(f"You lost a score of {game.current_score}")
                else:
                    print(f"You finished with a score of {game.current_score}")
                user_input = input("Would you like to play again (n/Y)? ")
                if not user_input or user_input.lower() == 'Y' :
                    print()
                    print('New game --->')
                    game = GameState()
                else:
                    exit()

            game.show()
            print()
        except KeyboardInterrupt:
            exit()
        except EOFError:
            exit()



if __name__ == "__main__":
    # print('------')
    # a = test(50, [1, 6, 5, 4, 5])
    # print(a)
    # a = test(50, [5])
    # print(a)
    # print('------')
    # a = test(500, [5, 5, 5])
    # print(a)
    # print('------')
    # a = test(200, [1, 1])
    # print(a)
    # print('------')
    # a = test(300, [1, 2, 3, 2, 3])
    # print(a)
    # print('------')
    # a = test(200, [1, 2, 3, 2, 3])
    # print(a)
    # print('------')
    # exit()
    main()