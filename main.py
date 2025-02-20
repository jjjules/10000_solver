#!/usr/bin/env python3

import random

from collections import defaultdict

def roll_dice() -> int:
    """Simulate rolling a single die with a specified number of sides."""
    return random.randint(1, 6)


class DiceCombinationChecker:
    up_to_four_dice_combinations: dict[int, list[tuple[int]]] = {
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

    def __init__(self):
        pass

    def match(self, score: int, dice: list[int]) -> bool:
        """
            Test whether some dice combination corresponds to the given score. The match has to be exact.

            For example:
                - 300 for [1, 1, 1] returns True
                - 1000 for [1, 1, 1] returns True
                - 1000 for [1, 1, 1, 6] returns False
                - 150 for [2, 3, 5, 5] return True
        """
        dice = tuple(sorted(dice))
        if score in self.up_to_four_dice_combinations and any(x == dice for x in self.up_to_four_dice_combinations[score]):
            return True
        else:
            # Take some points away and recurse
            recursive_steps = [([1], 100), ([5], 50), ([2, 3], 50)]
            for to_remove, current_score in recursive_steps:
                if all(i in dice for i in to_remove):
                    current_dice = list(dice)
                    for i in to_remove:
                        current_dice.remove(i)
                    if self.match(score - current_score, current_dice):
                        # print(f"Removing {to_remove} success")
                        return True
                    else:
                        # print(f"Removing {to_remove} failed")
                        pass
            
            return False

    def create_combinations_and_match(self, available_dice, chosen_score, chosen_dice) -> int:
        chosen_score = int(chosen_score)
        chosen_dice = [int(x) for x in chosen_dice]

        if chosen_score == 1500:
            # Separate case to be able to just enter 1500 without specifying the dice
            dice_set = set(available_dice)
            elem1 = list(dice_set)[0]
            num_elem1 = len([x for x in available_dice if x == elem1])
            full_house = len(dice_set) == 2 and (num_elem1 == 2 or num_elem1 == 3)
            if full_house:
                print('Full House !!!')
            grande_suite = dice_set == {1, 2, 3, 4, 5} or dice_set == {2, 3, 4, 5, 6}
            if grande_suite:
                print('Grande Suite !!!')
            assert full_house or grande_suite, f"To take 1500 points you must have either a full house or a grande suite. You had '{available_dice}'"

            return 5
        else:
            assert len(chosen_dice) > 0, "You must specify how you keep the dice."

            dice_sets = self.get_all_dice_combination(available_dice)

            found = False
            for current_dice in dice_sets:
                if set(chosen_dice).issubset(current_dice) and self.match(chosen_score, chosen_dice):
                    found = True
                    break
            if found:
                return len(chosen_dice)
            else:
                raise RuntimeError(f"You tried to keep a score of {chosen_score} by keeping {chosen_dice} with a roll of {available_dice}. This is not allowed.")

    # def get_available_actions(self, available_dice):
    #     actions: dict[int, list[list[int]]] = defaultdict(list)
    #     data: tuple[int, list[int], list[int]] = []

    #     for current_dice in self.get_all_dice_combination(available_dice):
    #         for score, combinations in self.up_to_four_dice_combinations.items():
    #             for combination in combinations:
    #                 if combination
            
    def get_all_dice_combination(self, initial_dice) -> list[list[int]]:
        added_combinations = [initial_dice]
        if (2 in initial_dice and 3 in initial_dice):
            new_combination = initial_dice.copy()
            new_combination.remove(2)
            new_combination.remove(3)
            new_combination.append(5)
            added_combinations.append(new_combination)
            added_combinations.extend(self.get_all_dice_combination(new_combination))
        elif 5 in initial_dice:
            new_combination = initial_dice.copy()
            new_combination.remove(5)
            if 5 in new_combination:
                new_combination.remove(5)
                new_combination.append(1)
                added_combinations.append(new_combination)
                added_combinations.extend(self.get_all_dice_combination(new_combination))
        
        return added_combinations


class GameState:
    current_score = 0
    available_dice: list[int] = None

    def __init__(self) -> None:
        self.new_dice()
        self.dice_checker = DiceCombinationChecker()
    
    def new_dice(self) -> None:
        self.available_dice = [roll_dice() for i in range(5)]
    
    def roll(self) -> None:
        self.available_dice = [roll_dice() for i in range(len(self.available_dice))]
    
    def keep(self, chosen_score: int, chosen_dice: list[int]):
        num_used_dice = self.dice_checker.create_combinations_and_match(self.available_dice, chosen_score, chosen_dice)

        self.available_dice = self.available_dice[num_used_dice:]
        self.current_score += chosen_score

        # Main pleine
        if len(self.available_dice) == 0:
            self.new_dice()
        else: 
            self.roll()




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
                chosen_score, *chosen_dice = user_input.split()
                chosen_score = int(chosen_score)
                chosen_dice = [int(x) for x in chosen_dice]
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