#!/usr/bin/env python3


import random
import numpy as np
from multiset import Multiset

from game import GameState
from environment import GameEnv

def main():
    
    np.random.seed(1)
    random.seed(1)

    env = GameEnv()

    while(True):
        if env.game_state.is_done:
            print()
            print('NEW GAME')
            print()
            env = GameEnv()
        env.render()
        i1 = int(input('input1 '))
        i2 = [x == '1' for x in input('input2 ').split(' ')]
        i3 = int(input('input3 '))
        i4 = int(input('input4 '))
        print(i1, i2, i3, i4)
        env.step((
            i1,
            i2,
            i3,
            i4,
        ))
    exit(0)
    
    """
        5
        1 1 1 1 1
        0
        0

        7
        1 1 0 1 0
        2
        0


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