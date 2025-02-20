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
        # recursive_steps += [([2], 0), ([3], 0), ([4], 0), ([5], 0), ([6], 0)]  # Removing useless dice
        # recursive_steps += [([1], 0), ([5], 0)]  # Removing dice ignoring their points
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
            assert len(chosen_dice) > 0, "You must specify how you keep the dice."
            chosen_dice = [int(x) for x in chosen_dice]

            dice_sets = [self.available_dice] + self.add_dice_combination(self.available_dice)

            found = False
            for current_dice in dice_sets:
                if set(chosen_dice).issubset(current_dice) and test(score, chosen_dice):
                    self.available_dice = self.available_dice[len(chosen_dice):]
                    self.current_score += score
                    found = True
                    break
            if not found:
                raise RuntimeError(f"You tried to keep a score of {score} by keeping {chosen_dice} with a roll of {self.available_dice}. This is not allowed.")
        
        # Main pleine
        if len(self.available_dice) == 0:
            self.new_dice()
        else: 
            self.roll()
            
    def add_dice_combination(self, dice_combination) -> list[list[int]]:
        added_combinations = []
        if (2 in dice_combination and 3 in dice_combination):
            new_combination = dice_combination.copy()
            new_combination.remove(2)
            new_combination.remove(3)
            new_combination.append(5)
            added_combinations.append(new_combination)
            added_combinations.extend(self.add_dice_combination(new_combination))
        elif 5 in dice_combination:
            new_combination = dice_combination.copy()
            new_combination.remove(5)
            if 5 in new_combination:
                new_combination.remove(5)
                new_combination.append(1)
                added_combinations.append(new_combination)
                added_combinations.extend(self.add_dice_combination(new_combination))
        
        return added_combinations




    def show(self):
        print(f'''
        Current score is {self.current_score:d}
        Available dice: {self.available_dice}
        ''')

    
def main():
    game = GameState()
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
                game.keep(user_input)

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