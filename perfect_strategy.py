import numpy as np

data_file_name = 'blackjackstrategychart.csv'


class StrategyChart:
    def __init__(self, data):
        self.hardStrat = np.genfromtxt(data, delimiter=',', skip_header=1, usecols=range(1, 11), max_rows=17)
        self.softStrat = np.genfromtxt(data, delimiter=',', skip_header=17, usecols=range(1, 11), max_rows=10)
        self.pairStrat = np.genfromtxt(data, delimiter=',', skip_header=26, usecols=range(1, 11), max_rows=10)

    def decide_action(self, player_hand, dealer_hand, player_hand_sum):
        print("\n####   PERFECT STRATEGY    ####")
        if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            player_action = self.pairStrat[int(player_hand[0]) - 1, dealer_hand - 1]
        elif min(player_hand) == 1 and player_hand_sum == 12:
            player_action = self.decide_action([2, 10], dealer_hand, 12)
        elif min(player_hand) == 1 and np.sum(player_hand == 1) == 1:
            player_action = self.softStrat[player_hand_sum - 13, dealer_hand - 1]
        elif min(player_hand) == 1 and np.sum(player_hand == 1) > 1:
            player_hand = np.sort(player_hand)
            sum_other_cards = np.sum(player_hand[1:])
            if sum_other_cards >= 11:
                player_action = self.decide_action([1, sum_other_cards], dealer_hand, sum_other_cards + 1)
            else:
                player_action = self.softStrat[sum_other_cards - 1, dealer_hand - 1]
        else:
            player_action = self.hardStrat[player_hand_sum - 5, dealer_hand - 1]

        print(
            f"Player hand: {player_hand}, Dealer hand: {dealer_hand}, Player hand sum: {player_hand_sum}, "
            f"Action: {player_action}")
        print(f"Perfect strategy recommends that you {strategy_dict[player_action]}\n")

        return return_dict[player_action]


# Create an instance of the StrategyChart class
strategy_chart = StrategyChart(data_file_name)

strategy_dict = {
    1: "Hit",
    2: "Stand",
    3: "Split",
    4: "Double if possible, otherwise hit",
    5: "Double if possible, otherwise stand"
}

return_dict = {
    1: "H",
    2: "S",
    3: "SPL",
    4: "D",
    5: "D"
}


def test(test_data):
    # Test the decideAction function
    for a, b, c in test_cases:
        action = strategy_chart.decide_action(a, b, c)
        print(f"Player hand: {a}, Dealer hand: {b}, Player hand sum: {c}, Action: {action}")


# Test cases
test_cases = [
    ([5, 5], 6, 10),    # Pair
    ([1, 10], 5, 11),   # Soft hand with one ace
    ([1, 2, 8], 7, 21), # Soft hand with multiple aces
    ([6, 5], 10, 11),   # Hard hand
]




