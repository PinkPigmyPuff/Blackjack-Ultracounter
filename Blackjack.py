# Blackjack Game, V2
# import sys
# sys.setrecursionlimit(2000)
import random
import Counter as co

# variables
remainingCards = []
gameOver = False

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
# suits = ['♦', '♣', '♥', '♠']

cards = []
discard = []
playerList = []

# house specific rules
bjPayout = 3/2 # not implemented
minBet = 2
maxBet = 1000
bankrollMin = 1
cutCard = 20
maxPlayers = 10
deckNum = 1
DAS = True # not implemented
RSA = True # not implemented
earlySurrended = False # not implemented

# functions
def shuffle(num):
    deck = []
    for i in range(0, num):
        for value in values:
            for suit in range(0, 4):
                card = value
                deck.append(card)
    random.shuffle(deck)
    return deck

def deal():
    print('dealing...')
    for x in range(0, len(playerList)):
        cards.append([remainingCards[-1]])
        remainingCards.pop()
    for x in range(0, len(playerList)):
        giveCard(x)


def total(hand):
    total = 0
    for card in cards[hand]:
        # if card == 'J' or card == 'Q' or card == 'K' or card == '10':
        #     total += 10
        # elif card == 'A':
        #     total += 11
        # else:
            total += int(card)

    if total > 21:
        for x in range(0, cards[hand].count(11)):
            total -= 10
            if total <= 21:
                break


    return total


def info(hand):
    print('Your hand: ' + ''.join(str(cards[hand])))
    print('Dealers hand: ' + str(cards[-1][0]) + ', Hidden')


def giveCard(hand):
    cards[hand].append(remainingCards[-1])
    remainingCards.pop()


def findPrevSplits(turn):
    prevSplits = 0
    for x in range(0, turn + 1):
        if split[x] == True:
            prevSplits += 1
    return prevSplits


def get_int(prompt, minVal, maxVal):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("You must enter a positive integer")
            continue

        if value < minVal:
            print("Number must be at least " + str(minVal))
            continue
        elif value > maxVal:
            print("Number cannot be more than " + str(maxVal))
            continue
        else:
            break
    return value

def get_bool(prompt):
    answer = input(str(prompt)).lower()
    # raw_input returns the empty string for "enter"
    yes = {'yes', 'y', 'ye', 'ya', 'yuh', 'yeah', 'yep', 'yup', 'fosho', 'why not', 'any day'}
    no = {'no', 'n', 'na', 'nah', 'nope',  'not today chief'}

    if answer in yes:
        return True
    elif answer in no:
        return False
    else:
        print("Please respond with 'yes' or 'no'")
        get_bool(prompt)

def win(turn, bankrollModifier):
    print(playerList[turn] + ', you won ' + str(bets[turn]) + '$!')
    # print(turn) # DEBUG
    # print(bankrolls) # DEBUG
    # print(bets) # DEBUG

    # BANKROLL MODIFIER NEEDS TO EQUAL HOW MANY SPLITS HAVE COME BEFORE IT, NOT TOTAL SPLITS
    bankrolls[turn - bankrollModifier] += bets[turn]

def lose(turn, bankrollModifier):
    print(playerList[turn] + ', you lost ' + str(bets[turn]) + '$.')
    bankrolls[turn - bankrollModifier] -= bets[turn]

def reset():
    print('\nTotal bankroll:')
    for x in range(0, len(playerList) - 1):
        if(split[x]) == True:
            playerList.pop(x)
    for x in range(0, len(playerList) -1):
        print(playerList[x] + ': ' + str(bankrolls[x]) + '$')

    # put all cards into the discard pile
    for hand in cards:
        discard.extend(hand)
    cards.clear()

    # shuffle cards if low
    print('cards remaining: ' + str(len(remainingCards)) + '\n')
    if len(remainingCards) < cutCard:
        discard.extend(remainingCards)
        remainingCards.clear()
        random.shuffle(discard)
        remainingCards.extend(discard)
        discard.clear()

    if get_bool('End game (y/n)? '):
        print('See you next time!')
        return True

    return False

# main

# before the game starts, set up (name and bankroll for each player), (set up deck)
print('Welcome to Blackjack!')

playerNum = get_int('How many players? ', 1, maxPlayers)
for x in range(0, playerNum):
    name = input('What is your  name? ')
    playerList.append(name)
playerList.append('dealer')
print(playerList) # DEBUG

remainingCards += shuffle(deckNum)
print(remainingCards) # DEBUG

bankrolls = [get_int('What bankroll? ', bankrollMin, 1000000)] * playerNum
print(bankrolls)

while gameOver == False:
# at the start of every round
    # create status lists
    bets = []
    status = ['PUSH'] * (playerNum + 1)
    insurance = [0] * playerNum
    split = [False] * playerNum
    for player in playerList[:-1]:
        print('\nHello ' + str(player) + '!')
        bet = get_int('How much do you want to bet? ', minBet, maxBet)
        bets.append(bet)

    # deal cards
    deal()
    print(cards) # DEBUG

    # manual dealing
    # cards = [['9', '9'], ['A', '10'], ['J', '3']] # DEBUG
    # cards = [['A', 'A'], ['Q', '4']] # DEBUG
    # print('new cards lol ' + str(cards)) # DEBUG


    # check for insurance
    if cards[-1][0] == 11:
        for x in range (0, len(playerList)-1):
            ins = get_bool(playerList[x] + ', would you like insurance (y/n)? ')
            if ins:
                insurance[x] = get_int('How much would you like to wager? ', 0, bets[x] / 2)
                bankrolls[x] -= insurance[x]

        if total(-1) == 21:
            print('Dealer has Blackjack')
            print('Dealers hand: ' + ''.join(str(cards[-1])))
            for x in range(0, len(playerList) - 1):
                if insurance[x] != 0:
                    print(playerList[x] + ', you won your insurance bet of ' + str(insurance[x]))
                    bankrolls[x] += insurance[x] * 2
                if total(x) == 21:
                    print(playerList[x] + ', you push.')
                else:
                    lose(x, 0)
            gameOver = reset()
            continue

    # non insurable BJ
    elif cards[-1][0] == '10' or cards[-1][0] == 'J' or cards[-1][0] == 'Q' or cards[-1][0] == 'K':
        if cards[-1][1] == '11':
            print('Dealer has Blackjack!')
            print('Dealers hand: ' + ''.join(str(cards[-1])))
            for x in range(0, len(playerList)-1):
                if total(x) == 21:
                    print(playerList[x] + ', you push.')
                else:
                    lose(x, 0)
            gameOver = reset()
            continue


    # each player plays
    turn = 0
    while turn < len(playerList)-1:
        # turn = int(playerList.index(player))

        # welcome the player and show them their hand
        print('\nHello ' + str(playerList[turn]) + '!')
        info(turn)

        # check if player has BJ
        if total(turn) == 21:
            print('You have Blackjack!')
            bets[turn] *= bjPayout
            status[turn] = 'BJ'

        # get the players move
        while total(turn) < 21:
            co.whatShouldIPlay(total(turn), cards[-1][0], remainingCards)
            choice = input('What would you like to do (H, S, D, Sur, Spl): ').upper()
            if choice == 'H':
                giveCard(turn)
                info(turn)

            elif choice == 'S':
                break

            elif choice == 'D':
                bets[turn] *= 2
                print('New bet: ' + str(bets[turn]))
                giveCard(turn)
                info(turn)
                break

            elif choice == 'SPL':
                if cards[turn][0] == cards[turn][1] and len(cards[turn]) == 2:

                    playerList.insert(turn + 1, playerList[turn] + ' (split hand)')
                    status.insert(turn + 1, 'PUSH')
                    split.insert(turn + 1, True)
                    bets.insert(turn + 1, bets[turn])
                    cards.insert(turn + 1, [cards[turn][1]])

                    cards[turn].pop()
                    giveCard(turn)
                    giveCard(turn + 1)
                    info(turn)

            elif choice == 'SUR':
                bets[turn] = bets[turn] * .5
                print('Surrendered. Returned amount is: ' + str(bets[turn]*.5))
                status[turn] = 'SUR'
                info(turn)
                break


        # check if player busted
        if total(turn) > 21:
            print('Busted')
            status[turn] = 'BUST'
        elif status[turn] != 'SUR' or status[turn] != 'BJ':
            status[turn] = total(turn)
        turn += 1


    # have dealer play
    print('\nDealer is playing:')
    if total(-1) <= 16:
        while total(-1) <= 16:
            giveCard(-1)
            print('Dealers hand: ' + ''.join(str(cards[-1])))
    else:
        print('Dealers hand: ' + ''.join(str(cards[-1])))

    if total(-1) > 21:
        status[-1] = 'BUST'
    else:
        status[-1] = total(-1)
    print(status) # DEBUG

    # determine who won
    for x in range(0, len(playerList) - 1):
        splitNum = findPrevSplits(x)
        print(str(playerList[x]) + ' splitNum = ' + str(splitNum))
        # if dealer busted
        if status[-1] == 'BUST':
            # and u didn't bust
            if status[x] != 'BUST' and status[x] != 'SUR':
                win(x, splitNum)
            # and you did bust
            else:
                lose(x, splitNum)
        # if dealer did not bust
        else:
            # and you busted
            if status[x] == 'BUST' or status[x] == 'SUR':
                lose(x, splitNum)
            # if you scored higher dealer
            elif int(status[x]) > int(status[-1]):
                win(x, splitNum)
            # if you scored lower than dealer
            elif int(status[x]) < int(status[-1]):
                lose(x, splitNum)
            else:
                print(playerList[x] + ', you push.')

    gameOver = reset()

# todo
    # make the huge chunka code(main) into a def
    # extra payout on BJ
    # test edge cases (?)
