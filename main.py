#!/usr/bin/env python3

import random

def roll_dice() -> int:
    """Simulate rolling a single die with a specified number of sides."""
    return random.randint(1, 6)



all_combinations: dict[int, list[tuple[int]]] = {
    50: [(2, 3), (5,)],
    100: [(1,)],
    200: [(2, 2, 2)],
    300: [(3, 3, 3)],
    400: [(4, 4, 4), (2, 2, 2, 2)],
    500: [(5, 5, 5)],
    600: [(6, 6, 6)],
    600: [(3, 3, 3, 3)],
    800: [(4, 4, 4, 4)],
    1000: [(1, 1, 1), (5, 5, 5, 5)],
    1200: [(6, 6, 6, 6)],
    2000: [(1, 1, 1, 1)],
    # Ignore 5 dice combinations
}


def test(score, dice: list):
    """
        Test whether some dice combination can be interpreted as a score given the rules
    """
    dice = tuple(sorted(dice))
    if score in all_combinations and any(x == dice for x in all_combinations[score]):
        # print('Yes', score, dice)
        return True
    else:
        # Recurse
        recursive_steps = [([1], 100), ([5], 50), ([2, 3], 50)]  # Taking the usuals with their points
        recursive_steps += [([2], 0), ([3], 0), ([4], 0), ([5], 0), ([6], 0)]  # Removing useless dice
        recursive_steps += [([1], 0), ([5], 0)]  # Removing dice ignoring their points
        for to_remove, current_score in recursive_steps:
            if all(i in dice for i in to_remove):
                current_dice = list(dice)
                for i in to_remove:
                    current_dice.remove(i)
                if test(score - current_score, current_dice):
                    # print(f"Removing {to_remove} success")
                    return True
                else:
                    # print(f"Removing {to_remove} failed")
                    pass
        
        return False


class GameState:
    current_score = 0
    kept_dice_history: list[int] = []
    kept_dice: list[int] = []
    available_dice: list[int] = None

    def __init__(self) -> None:
        self.new_dice()
    
    def new_dice(self) -> None:
        self.available_dice = [roll_dice() for i in range(5)]
    
    def roll(self) -> None:
        self.available_dice = [roll_dice() for i in range(len(self.available_dice))]
    
    def keep(self, descr: str):
        score, *chosen_dice = descr.split()
        score = int(score)

        if score == 1500:
            # Separate case
            dice_set = set(self.available_dice)
            elem1 = list(dice_set)[0]
            num_elem1 = len([x for x in self.available_dice if x == elem1])
            full_house = len(dice_set) == 2 and (num_elem1 == 2 or num_elem1 == 3)
            if full_house:
                print('Full House !!!')
            grande_suite = dice_set == {1, 2, 3, 4, 5} or dice_set == {2, 3, 4, 5, 6}
            if grande_suite:
                print('Grande Suite !!!')
            assert full_house or grande_suite, f"To take 1500 points you must have either a full house or a grande suite. You had '{self.available_dice}'"

            self.available_dice = []
            self.current_score += 1500
        else:
            assert len(chosen_dice) > 0
            chosen_dice = [int(x) for x in chosen_dice]

            """
                score -> score to add to current score
                dice -> dice we keep at current game step
            """
            if test(score, self.available_dice) and test(score, chosen_dice) and len(chosen_dice) <= len(self.available_dice):
                self.available_dice = self.available_dice[len(chosen_dice):]
                self.current_score += score
            else:
                raise RuntimeError(f"You tried to keep a score of {score} by keeping {chosen_dice} with a roll of {self.available_dice}. This is not allowed.")
            
        
        # Main pleine
        if len(self.available_dice) == 0:
            self.new_dice()
            self.kept_dice_history.extend(self.kept_dice)
            self.kept_dice = []
        else: 
            self.roll()



    def show(self):
        print(f'''
        Current score is {self.current_score:d}
        Available dice: {self.available_dice}
        Fixed dice: {self.kept_dice}
        ''')

    
def main():
    game = GameState()

    game.show()

    while True:
        try:
            user_input = input("Enter the dice combinations you want to keep (prepend 'done ' to stop) -> ")

            if not user_input:
                print('Stopping ...')
                exit()

            if user_input.startswith('done '):
                stop = True
                user_input = user_input[5:]
            else:
                stop = False
            game.keep(user_input)

            if stop:
                print(f"You finished with a score of {game.current_score}")
                exit()
        
            game.show()
            print('\n\n\n')
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