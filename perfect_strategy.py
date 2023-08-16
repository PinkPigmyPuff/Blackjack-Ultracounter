import numpy as np

data_file_name = 'blackjackstrategychartMOD.csv'


def action(player_hand, dealer_hand, player_hand_sum, lateSurrender):
    # 0 = don't split, 1 = split, 2 = split if DAS
    pair_strat = np.loadtxt('pair_strat.csv', delimiter=',', dtype=str)

    # 3 = hit, 4 = stand, 5 = double if allowed, otherwise hit, 6 = double if allowed, otherwise stand, 7 = late surrender
    soft_strat = np.loadtxt('soft_strat.csv', delimiter=',', dtype=str)

    # 3 = hit, 4 = stand, 5 = double if allowed, otherwise hit
    hard_strat = np.loadtxt('hard_strat.csv', delimiter=',', dtype=str)
    player_action = None

    dealer_hand -= 1
    if lateSurrender and ((player_hand_sum == 16 and (dealer_hand == 9 or dealer_hand == 10 or dealer_hand == 11))
                          or (player_hand_sum == 15 and dealer_hand == 10)):
        return 7
    elif len(player_hand) == 2 and player_hand[0] == player_hand[1]:
        player_action = pair_strat[player_hand[0] - 1, dealer_hand]
    elif np.max(player_hand) == 11:
        column_index = player_hand_sum - 11 - 1
        player_action = soft_strat[column_index, dealer_hand]
    elif player_hand_sum > 17:
        return 4
    elif player_hand_sum < 8:
        return 3
    else:
        player_action = hard_strat[player_hand_sum - 6, dealer_hand]
    return player_action


# action([5, 5], 6, 10) # 0
# action([11, 11], 9, 12) # 1
# action([6,6], 2, 12) # 2
# print(action([11, 4], 4, 15)) # 2]
print(action([6, 7], 6, 13), False)  # 1


class StrategyChart:
    def __init__(self, data_file_name):
        self.hardStrat = np.loadtxt(data_file_name, delimiter=',', skiprows=1, usecols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                                    max_rows=17)
        self.softStrat = np.loadtxt(data_file_name, delimiter=',', skiprows=18, usecols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                                    max_rows=10)
        self.pairStrat = np.loadtxt(data_file_name, delimiter=',', skiprows=27, usecols=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                                    max_rows=10)

    def decide_action(self, playerHand, dealerHand, playerHandSum):
        if len(playerHand) == 2 and playerHand[0] == playerHand[1]:
            player_action = self.pairStrat[playerHand[0] - 1, dealerHand - 1]
        elif np.min(playerHand) == 1 and playerHandSum == 12:
            player_action = self.decide_action([2, 10], dealerHand, 12)
        elif np.min(playerHand) == 1 and np.sum(playerHand == 1) == 1:
            player_action = self.softStrat[playerHandSum - 12, dealerHand - 1]
        elif np.min(playerHand) == 1 and np.sum(playerHand == 1) > 1:
            playerHand = np.sort(playerHand)
            sumOtherCards = np.sum(playerHand[1:])
            if sumOtherCards >= 11:
                player_action = self.decide_action([1, sumOtherCards], dealerHand, sumOtherCards + 1)
            else:
                player_action = self.softStrat[sumOtherCards - 1, dealerHand - 1]
        else:
            player_action = self.hardStrat[playerHandSum - 4, dealerHand - 1]

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
    ([5, 5], 6, 10),  # Pair
    ([1, 10], 5, 11),  # Soft hand with one ace
    ([1, 2, 8], 7, 21),  # Soft hand with multiple aces
    ([6, 5], 10, 11),  # Hard hand
]
