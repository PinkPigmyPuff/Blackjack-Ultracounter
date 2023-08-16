import numpy as np


def decide_action(player_hand, dealer_hand, player_hand_sum, late_surrender, DAS):
    # 7 = late surrender

    # 0 = don't split, 1 = split, 2 = split if DAS
    pair_strat = np.loadtxt('pair_strat.csv', delimiter=',', dtype=str)

    # 3 = hit, 4 = stand, 5 = double if allowed, otherwise hit, 6 = double if allowed, otherwise stand
    soft_strat = np.loadtxt('soft_strat.csv', delimiter=',', dtype=str)

    # 3 = hit, 4 = stand, 5 = double if allowed, otherwise hit
    hard_strat = np.loadtxt('hard_strat.csv', delimiter=',', dtype=str)

    player_action = None

    dealer_hand -= 1

    if late_surrender and ((player_hand_sum == 16 and (dealer_hand == 9 or dealer_hand == 10 or dealer_hand == 11))
                           or (player_hand_sum == 15 and dealer_hand == 10)):
        return 7
    elif len(player_hand) == 2 and player_hand[0] == player_hand[1]:
        player_action = pair_strat[player_hand[0] - 1, dealer_hand]
        if player_action == '1' or (player_action == '2' and DAS):
            return player_action
    if np.max(player_hand) == 11:
        column_index = player_hand_sum - 11 - 1
        player_action = soft_strat[column_index, dealer_hand]
        return player_action
    if player_hand_sum > 17:
        return 4
    if player_hand_sum < 8:
        return 3
    else:
        player_action = hard_strat[player_hand_sum - 7, dealer_hand]
    return player_action


# action([5, 5], 6, 10) # 0
# action([11, 11], 9, 12) # 1
# action([6,6], 2, 12) # 2
# print(action([11, 4], 4, 15)) # 2]
#print(decide_action([6, 7], 6, 13, False, False))# 1



strategy_dict = {
    0: "Don't split",
    1: "Split",
    2: "Split if DAS is offered, otherwise don't",
    3: "Hit",
    4: "Stand",
    5: "Double if possible, otherwise hit",
    6: "Double if possible, otherwise stand",
    7: "Surrender late if offered"
}

return_dict = {
    0: "Well, this wasn't supposed to happen",
    1: "SPL",
    2: "SPL",
    3: "H",
    4: "S",
    5: "D",
    6: "D",
    7: "SUR"
}
