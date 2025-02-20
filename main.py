#!/usr/bin/env python3

import random

from multiset import Multiset

def roll_dice() -> int:
    """Simulate rolling a single die with a specified number of sides."""
    return random.randint(1, 6)


class DiceCombinationChecker:
    up_to_four_dice_combinations: dict[int, list[Multiset[int]]] = {
        50: [Multiset([2, 3]), Multiset([5,])],
        100: [Multiset([1,])],
        200: [Multiset([2, 2, 2])],
        300: [Multiset([3, 3, 3])],
        400: [Multiset([4, 4, 4]), Multiset([2, 2, 2, 2])],
        500: [Multiset([5, 5, 5])],
        600: [Multiset([6, 6, 6])],
        600: [Multiset([3, 3, 3, 3])],
        800: [Multiset([4, 4, 4, 4])],
        1000: [Multiset([1, 1, 1]), Multiset([5, 5, 5, 5])],
        1200: [Multiset([6, 6, 6, 6])],
        2000: [Multiset([1, 1, 1, 1])],
        # Ignore 5 dice combinations
    }

    def __init__(self):
        pass

    def is_full_house(self, dice: Multiset[int]) -> bool:
        """
            If and only if each element's multiplicity is 2 or 3
        """
        return all(2 <= dice[elem] <= 3 for elem in dice.distinct_elements())
    
    def is_grande_suite(self, dice: Multiset[int]) -> bool:
        return dice == {1, 2, 3, 4, 5} or dice == {2, 3, 4, 5, 6}

    def match(self, score: int, dice: Multiset[int]) -> bool:
        """
            Test whether some dice combination corresponds to the given score. The match has to be exact.

            For example:
                - 300 for [1, 1, 1] returns True
                - 1000 for [1, 1, 1] returns True
                - 1000 for [1, 1, 1, 6] returns False
                - 150 for [2, 3, 5, 5] return True
        """
        if score in self.up_to_four_dice_combinations and any(x == dice for x in self.up_to_four_dice_combinations[score]):
            return True
        else:
            # Take some points away and recurse
            recursive_steps = [(set([1]), 100), (set([5]), 50), (set([2, 3]), 50)]
            for to_remove, current_score in recursive_steps:
                if to_remove.issubset(dice):
                    if self.match(score - current_score, dice - to_remove):
                        # print(f"Removing {to_remove} success")
                        return True
                    else:
                        # print(f"Removing {to_remove} failed")
                        pass
            
            return False

    def create_combinations_and_match(self, available_dice: Multiset[int], chosen_score: int, chosen_dice: Multiset[int]) -> int:
        """
            Check whether the move chosen by the player, that is choosing to keep this score with these dice, is valid.
            For a grande suite or a full house, chosen_dice can be empty.

            Return the number of dice used by the player for the validated move.
        """

        if chosen_score == 1500:
            # Separate case to be able to just enter 1500 without specifying the dice
            full_house = self.is_full_house(available_dice)
            if full_house:
                print('Full House !!!')
            grande_suite = self.is_grande_suite(available_dice)
            if grande_suite:
                print('Grande Suite !!!')
            assert full_house or grande_suite, f"To take 1500 points you must have either a full house or a grande suite. You had '{available_dice}'"

            return 5
        else:
            assert len(chosen_dice) > 0, "You must specify how you keep the dice."

            dice_combinations: list[Multiset[int]] = self.get_all_dice_combination(available_dice)

            found = False
            for current_dice in dice_combinations:
                if chosen_dice.issubset(current_dice) and self.match(chosen_score, chosen_dice):
                    found = True
                    break
            if found:
                return len(chosen_dice)
            else:
                raise RuntimeError(f"You tried to keep a score of {chosen_score} by keeping {chosen_dice} with a roll of {available_dice}. This is not allowed.")

    def get_all_dice_combination(self, initial_dice: Multiset[int]) -> list[Multiset[int]]:
        added_combinations = [initial_dice]
        if {2, 3}.issubset(initial_dice):
            new_dice = initial_dice - {2, 3}
            new_dice.add(5)
            added_combinations.append(new_dice)
            added_combinations.extend(self.get_all_dice_combination(new_dice))
        elif Multiset([5, 5]).issubset(initial_dice):
            new_dice = initial_dice - Multiset([5, 5])
            new_dice.add(1)
            added_combinations.append(new_dice)
            added_combinations.extend(self.get_all_dice_combination(new_dice))
        
        return added_combinations


class GameState:
    current_score = 0
    available_dice: Multiset[int] = None

    def __init__(self) -> None:
        self.roll_new_dice(5)
        self.dice_checker = DiceCombinationChecker()
    
    def roll_new_dice(self, num_dice: int) -> None:
        self.available_dice = Multiset([roll_dice() for i in range(num_dice)])
    
    def keep(self, chosen_score: int, chosen_dice: Multiset[int]):
        num_used_dice = self.dice_checker.create_combinations_and_match(self.available_dice, chosen_score, chosen_dice)
        if len(self.available_dice) == num_used_dice:
            # Main pleine
            self.roll_new_dice(5)
        else:
            self.roll_new_dice(len(self.available_dice) - num_used_dice)
        self.current_score += chosen_score

    def show(self):
        print(f'''
        Current score is {self.current_score:d}
        Available dice: {sorted(self.available_dice)}
        ''')


def main():
    game = GameState()
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