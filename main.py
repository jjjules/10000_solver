#!/usr/bin/env python3

import random

def roll_dice() -> int:
    """Simulate rolling a single die with a specified number of sides."""
    return random.randint(1, 6)



def get_dice_combination_from_string(s):
    match s:
        case '1':
            return One()
        case '5':
            return Five()
        case '23':
            return TwoThree()

class DiceCombination:
    score: int
    consumed_dice: list[int]

class One(DiceCombination):
    score = 100
    consumed_dice = [1]

    def __init__(self):
        pass

class Five(DiceCombination):
    score = 50
    consumed_dice = [5]

    def __init__(self):
        pass

class TwoThree(DiceCombination):
    score = 50
    consumed_dice = [2, 3]

    def __init__(self):
        pass




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
        combinations = descr.split()
        assert len(combinations) > 0

        for s in combinations:
            comb = get_dice_combination_from_string(s)
            if comb is None:
                raise RuntimeError(f"Unknown combination of dice to keep: '{s}'")
            self.update_with_combination(get_dice_combination_from_string(s))
        
        # Main pleine
        if len(self.available_dice) == 0:
            self.new_dice()
            self.kept_dice_history.extend(self.kept_dice)
            self.kept_dice = []
        else: 
            self.roll()

    def update_with_combination(self, x: DiceCombination):
        for y in x.consumed_dice:
            self.available_dice.remove(y)
            self.kept_dice.append(y)

        self.current_score += x.score




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
            user_input = input("Enter the dice combinations you want to keep (empty for stopping) -> ")

            if user_input == '':
                if game.current_score >= 500 and game.current_score % 100 == 0:
                    print(f"Yay! You entered the game with {game.current_score}.")
                    exit()
                else:
                    print(f"It's not allowed to finish your turn here!")
            else:
                game.keep(user_input)
                game.show()
                print('\n\n\n')
        except KeyboardInterrupt:
            exit()
        except EOFError:
            exit()



if __name__ == "__main__":
    main()