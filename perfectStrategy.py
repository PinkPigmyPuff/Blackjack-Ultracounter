import pandas as pd
import numpy as np

strategyChart = pd.read_csv('blackjackstrategychartMOD.csv')
#print(strategyChart)

# Read CSV data into a DataFrame
df = pd.read_csv(('blackjackstrategychartMOD.csv'), index_col=0)

# Display the DataFrame
print(df)

data_file_name = 'blackjackstrategychartMOD.csv'


class StrategyChart:
    def __init__(self, data_file_name):
        self.hardStrat = np.genfromtxt(data_file_name, delimiter=',', skip_header=1, usecols=range(1, 11), max_rows=17)
        self.softStrat = np.genfromtxt(data_file_name, delimiter=',', skip_header=17, usecols=range(1, 11), max_rows=10)
        self.pairStrat = np.genfromtxt(data_file_name, delimiter=',', skip_header=26, usecols=range(1, 11), max_rows=10)

    def decideAction(self, playerHand, dealerHand, playerHandSum):
        if len(playerHand) == 2 and playerHand[0] == playerHand[1]:
            playerAction = self.pairStrat[int(playerHand[0]) - 1, dealerHand - 1]
        elif min(playerHand) == 1 and playerHandSum == 12:
            playerAction = self.decideAction([2, 10], dealerHand, 12)
        elif min(playerHand) == 1 and np.sum(playerHand == 1) == 1:
            playerAction = self.softStrat[playerHandSum - 13, dealerHand - 1]
        elif min(playerHand) == 1 and np.sum(playerHand == 1) > 1:
            playerHand = np.sort(playerHand)
            sumOtherCards = np.sum(playerHand[1:])
            if sumOtherCards >= 11:
                playerAction = self.decideAction([1, sumOtherCards], dealerHand, sumOtherCards + 1)
            else:
                playerAction = self.softStrat[sumOtherCards - 1, dealerHand - 1]
        else:
            playerAction = self.hardStrat[playerHandSum - 5, dealerHand - 1]
        return playerAction

# Create an instance of the StrategyChart class
strategy_chart = StrategyChart(data_file_name)

# Test cases
test_cases = [
    ([5, 5], 6, 10),    # Pair
    ([1, 10], 5, 11),   # Soft hand with one ace
    ([1, 2, 8], 7, 21), # Soft hand with multiple aces
    ([6, 5], 10, 11),   # Hard hand
]

# Test the decideAction function
for player_hand, dealer_hand, player_hand_sum in test_cases:
    player_action = strategy_chart.decideAction(player_hand, dealer_hand, player_hand_sum)
    print(f"Player hand: {player_hand}, Dealer hand: {dealer_hand}, Player hand sum: {player_hand_sum}, Action: {player_action}")

#def what_should_i_play(myTotal, dealerCard):
def what_should_i_play(my_cards, dealer_card):
    print(my_cards)
    print(dealer_card)
    # try:
    #     value = df.iloc[row, column]
    #     return value
    # except IndexError:
    #     return "Invalid row or column index"