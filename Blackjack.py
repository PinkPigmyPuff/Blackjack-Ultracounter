import random
import ultracounter as ultra
import perfect_strategy as perfect

# variables
auto = "perfect"
autoNum = 1000

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

# house specific rules
bjPayout = 3 / 2
minBet = 2
maxBet = 1000
standardBet = 5
minBankroll = 1
maxBankroll = 10000000
standardBankroll = 100 * standardBet
cutCard = 20
maxPlayers = 10
deckNum = 8
DAS = True  # not implemented
RSA = True  # not implemented
lateSurrender = False  # not implemented

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

# Only for temporary usage, until DAS / Late sur implemented
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
# Returns n number of shuffled decks
def shuffle(n):
    deck = []
    for i in range(n):
        for value in values:
            for suit in range(0, 4):
                card = value
                deck.append(card)
    random.shuffle(deck)
    return deck


def deal(people_to_deal_to, peoples_cards, remaining_deck):
    print('dealing...')
    # Give each player 1 card, essentially "initializing" the array
    for x in range(people_to_deal_to):
        peoples_cards.append([remaining_deck[-1]])
        remaining_deck.pop()
    # Give each player 1 more card, for a total of 2
    for x in range(people_to_deal_to):
        peoples_cards, remaining_deck = give_card(peoples_cards, remaining_deck, x)

    return peoples_cards, remaining_deck


def total(peoples_cards, hand):
    card_sum = 0
    for card in peoples_cards[hand]:
        card_sum += int(card)

    if card_sum > 21:
        for x in range(0, peoples_cards[hand].count(11)):
            card_sum -= 10
            if card_sum <= 21:
                break
    return card_sum


def info(peoples_cards, hand):
    print('Your hand: ' + ''.join(str(peoples_cards[hand])))
    print('Dealers hand: ' + str(peoples_cards[-1][0]) + ', Hidden')


def give_card(peoples_cards, remaining_deck, current_hand):
    peoples_cards[current_hand].append(remaining_deck[-1])
    remaining_deck.pop()
    return peoples_cards, remaining_deck


def find_prev_splits(turn, splits):
    prev_splits = 0
    for x in range(0, turn + 1):
        if splits[x]:
            prev_splits += 1
    return prev_splits


def get_int(prompt, min_val, max_val):
    value = None
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("You must enter a positive integer")
            continue

        if value < min_val:
            print("Number must be at least " + str(min_val))
            continue
        elif value > max_val:
            print("Number cannot be more than " + str(max_val))
            continue
        else:
            break
    return value


def get_bool(prompt):
    answer = input(str(prompt)).lower()
    # raw_input returns the empty string for "enter"
    yes = {'yes', 'y', 'ye', 'ya', 'yuh', 'yeah', 'yep', 'yup', 'fosho', 'why not', 'any day'}
    no = {'no', 'n', 'na', 'nah', 'nope', 'not today chief'}

    if answer in yes:
        return True
    elif answer in no:
        return False
    else:
        print("Please respond with 'yes' or 'no'")
        get_bool(prompt)


def win(players, turn, bankroll_modifier, money_bet, bankrolls):
    print(players[turn] + ', you won ' + str(money_bet[turn]) + '$!')
    # BANKROLL MODIFIER NEEDS TO EQUAL HOW MANY SPLITS HAVE COME BEFORE IT, NOT TOTAL SPLITS
    bankrolls[turn - bankroll_modifier] += money_bet[turn]
    return bankrolls


def lose(players, turn, bankroll_modifier, money_bet, bankrolls):
    print(players[turn] + ', you lost ' + str(money_bet[turn]) + '$.')
    bankrolls[turn - bankroll_modifier] -= money_bet[turn]
    return bankrolls


def reset(player_num, split, player_list, bankrolls, cards, discard, remaining_cards, cut_card):
    split_hands = len(split)
    print(player_list)
    print(split_hands)
    print(split)
    print('\nTotal bankroll:')
    for x in range(split_hands):
        if split[x]:
            player_list.pop(x)
    for x in range(0, player_num):
        print(player_list[x] + ': ' + str(bankrolls[x]) + '$')

    # put all cards into the discard pile
    for hand in cards:
        discard.extend(hand)
    cards.clear()

    # shuffle cards if low
    print('cards remaining: ' + str(len(remaining_cards)) + '\n')
    if len(remaining_cards) < cut_card:
        discard.extend(remaining_cards)
        remaining_cards.clear()
        random.shuffle(discard)
        remaining_cards.extend(discard)
        discard.clear()

    print(player_list)
    if not auto:
        if get_bool('End game (y/n)? '):
            print('See you next time!')
            return True, player_list, discard, cards, remaining_cards

    return False, player_list, discard, cards, remaining_cards


# main
def main(automated, auto_iterate):
    remaining_cards = []
    game_over = False
    player_num = 0
    cards = []
    discard = []
    player_list = []
    bankrolls = []
    repetitions = 0

    # before the game starts, set up (name and bankroll for each player), (set up deck)
    print('Welcome to Blackjack!')

    if automated:
        player_num = 1
    else:
        player_num = get_int('How many players? ', 1, maxPlayers)

    for x in range(0, player_num):
        if automated:
            name = 'Bot'
            player_list.append(name)
        else:
            name = input('What is your name? ')
            player_list.append(name)
    player_list.append('dealer')
    print(f'List of players: {player_list}')

    remaining_cards += shuffle(deckNum)
    print(f'Remaining cards: {remaining_cards}')

    if automated == "perfect":
        bankrolls = [standardBankroll] * player_num
    else:
        bankrolls = [get_int('What bankroll? ', minBankroll, 1000000)] * player_num

    while not game_over:
        # at the start of every round
        # create status lists
        bets = []
        status = ['PUSH'] * (player_num + 1)
        insurance = [0] * player_num
        split = [False for _ in range(player_num)]
        for player in player_list[:-1]:
            print('\nHello ' + str(player) + '!')
            if automated == "perfect":
                bet = standardBet
                bets.append(bet)
            elif automated == "ultra":
                bet = ultra.whatShouldIBet(remaining_cards)
                print('You bet: ' + str(bet))
                bets.append(bet)
            else:
                bet = get_int('How much do you want to bet? ', minBet, maxBet)
                bets.append(bet)

        # deal cards
        cards, remaining_cards = deal(player_num + 1, cards, remaining_cards)

        # check for insurance
        if cards[-1][0] == 11:
            for x in range(0, len(player_list) - 1):
                if automated == "perfect":
                    insurance[x] = False
                    bankrolls[x] -= insurance[x]
                if automated:
                    insurance[x] = ultra.insurance()
                    bankrolls[x] -= insurance[x]

                else:
                    ins = get_bool(player_list[x] + ', would you like insurance (y/n)? ')
                    if ins:
                        insurance[x] = get_int('How much would you like to wager? ', 0, bets[x] / 2)
                        bankrolls[x] -= insurance[x]

            if total(cards, -1) == 21:
                print('Dealer has Blackjack')
                print('Dealers hand: ' + ''.join(str(cards[-1])))
                for x in range(0, len(player_list) - 1):




                    if insurance[x] != 0:
                        print(player_list[x] + ', you won your insurance bet of ' + str(insurance[x]))
                        bankrolls[x] += insurance[x] * 2
                    if total(cards, x) == 21:
                        print(player_list[x] + ', you push.')
                    else:
                        bankrolls = lose(player_list, x, 0, bets, bankrolls)
                game_over, player_list, discard, cards, remaining_cards = reset(player_num, split, player_list,
                                                                                bankrolls,
                                                                                cards, discard, remaining_cards,
                                                                                cutCard)
                continue

        # non insurable BJ
        elif cards[-1][0] == '10' or cards[-1][0] == 'J' or cards[-1][0] == 'Q' or cards[-1][0] == 'K':
            if cards[-1][1] == '11':
                print('Dealer has Blackjack!')
                print('Dealers hand: ' + ''.join(str(cards[-1])))
                for x in range(0, len(player_list) - 1):
                    if total(cards, x) == 21:
                        print(player_list[x] + ', you push.')
                    else:
                        bankrolls = lose(player_list, x, 0, bets, bankrolls)
                game_over, player_list, discard, cards, remaining_cards = reset(player_num, split, player_list,
                                                                                bankrolls,
                                                                                cards, discard, remaining_cards,
                                                                                cutCard,
                                                                                )
                continue

        # each player plays
        turn = 0
        while turn < len(player_list) - 1:
            # turn = int(playerList.index(player))

            # welcome the player and show them their hand
            print('\nHello ' + str(player_list[turn]) + '!')
            info(cards, turn)
            # check if player has BJ
            if total(cards, turn) == 21:
                print('You have Blackjack!')
                bets[turn] *= bjPayout
                status[turn] = 'BJ'

            # get the players move
            while total(cards, turn) < 21:
                choice = None
                print(f"FED {cards[turn], cards[-1][0], total(cards, turn)}")
                if automated == "perfect":
                    choice = return_dict[int(perfect.decide_action(cards[turn], cards[-1][0], total(cards, turn), lateSurrender, DAS))]

                elif automated == "ultra":
                    choice = ultra.whatShouldIPlay(total(cards, turn), cards[-1][0], remaining_cards.copy())

                if not automated:
                    choice = input('What would you like to do (H, S, D, Sur, Spl): ').upper()

                if choice == 'H':
                    print(f'cards: {cards}')
                    cards, remaining_cards = give_card(cards, remaining_cards, turn)
                    info(cards, turn)

                elif choice == 'S':
                    break

                elif choice == 'D':
                    bets[turn] *= 2
                    print('New bet: ' + str(bets[turn]))
                    cards, remaining_cards = give_card(cards, remaining_cards, turn)
                    info(cards, turn)
                    break

                elif choice == 'SPL':
                    if cards[turn][0] == cards[turn][1] and len(cards[turn]) == 2:
                        player_list.insert(turn + 1, player_list[turn] + ' (split hand)')
                        status.insert(turn + 1, 'PUSH')
                        split.insert(turn + 1, True)
                        bets.insert(turn + 1, bets[turn])
                        cards.insert(turn + 1, [cards[turn][1]])

                        cards[turn].pop()
                        cards, remaining_cards = give_card(cards, remaining_cards, turn)
                        cards, remaining_cards = give_card(cards, remaining_cards, turn + 1)
                        info(cards, turn)

                elif choice == 'SUR':
                    bets[turn] = bets[turn] * .5
                    print('Surrendered. Returned amount is: ' + str(bets[turn] * .5))
                    status[turn] = 'SUR'
                    info(cards, turn)
                    break

                else:
                    print("Invalid response")

            # check if player busted
            if total(cards, turn) > 21:
                print('Busted')
                status[turn] = 'BUST'
            elif status[turn] != 'SUR' or status[turn] != 'BJ':
                status[turn] = total(cards, turn)
            turn += 1

        # have dealer play
        print('\nDealer is playing:')
        if total(cards, -1) <= 16:
            while total(cards, -1) <= 16:
                cards, remaining_cards = give_card(cards, remaining_cards, -1)
                print('Dealers hand: ' + ''.join(str(cards[-1])))
        else:
            print('Dealers hand: ' + ''.join(str(cards[-1])))

        if total(cards, -1) > 21:
            status[-1] = 'BUST'
        else:
            status[-1] = total(cards, -1)
        print(status)  # DEBUG

        # determine who won
        for x in range(0, len(player_list) - 1):
            split_num = find_prev_splits(x, split)
            #split_num = sum(split)
            # if dealer busted
            if status[-1] == 'BUST':
                # and u didn't bust
                if status[x] != 'BUST' and status[x] != 'SUR':
                    bankrolls = win(player_list, x, split_num, bets, bankrolls)
                # and you did bust
                else:
                    bankrolls = lose(player_list, x, split_num, bets, bankrolls)
            # if dealer did not bust
            else:
                # and you busted
                if status[x] == 'BUST' or status[x] == 'SUR':
                    bankrolls = lose(player_list, x, split_num, bets, bankrolls)
                # if you scored higher dealer
                elif int(status[x]) > int(status[-1]):
                    bankrolls = win(player_list, x, split_num, bets, bankrolls)
                # if you scored lower than dealer
                elif int(status[x]) < int(status[-1]):
                    bankrolls = lose(player_list, x, split_num, bets, bankrolls)
                else:
                    print(player_list[x] + ', you push.')

        if automated:
            if repetitions < auto_iterate:
                repetitions += 1
                game_over, player_list, discard, cards, remaining_cards = reset(player_num, split, player_list,
                                                                                bankrolls,
                                                                                cards, discard, remaining_cards,
                                                                                cutCard,
                                                                                )
            else:
                game_over = True
        else:
            game_over, player_list, discard, cards, remaining_cards = reset(player_num, split, player_list, bankrolls,
                                                                            cards,
                                                                            discard, remaining_cards, cutCard,
                                                                            )


main(auto, autoNum)
# todo
# make the huge chunka code(main) into a def ## Done
# extra payout on BJ ## Done
#
# test edge cases (?)
