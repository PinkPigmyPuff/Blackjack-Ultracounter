import random

# variables
remainingCards = []
gameOver = False

values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
# suits = ['♦', '♣', '♥', '♠']

cards = []
playerList = []

# house specific rules
bjPayout = 3/2

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
        cards.append([remainingCards[-1]]) # not ok
        remainingCards.pop()
    for x in range(0, len(playerList)):
        giveCard(x)


def total(hand):
    total = 0
    for card in cards[hand]:
        if card == 'J' or card == 'Q' or card == 'K' or card == '10':
            total += 10
        elif card == 'A':
            total += 11
        else:
            total += int(card)

    if total > 21:
        for x in range(0, cards[hand].count('A')):
            total -= 10

    return total


def info(hand):
    print('Your hand: ' + ', '.join(cards[hand]))
    print('Dealers hand: ' + str(cards[-1][0]) + ', Hidden')


def giveCard(hand):
    cards[hand].append(remainingCards[-1])
    remainingCards.pop()


def play(player, action, hidden):
    if(action == 'H'):
        giveCard(player)
        info(hidden)
    if(action == 'D'):
        giveCard(player)
        info(hidden)

# main

# before the game starts, set up (name and bankroll for each player), (set up deck)
print('Welcome to Blackjack!')

playerNum = int(input('How many players? '))
for x in range(0, playerNum):
    name = input('What is your  name? ')
    playerList.append(name)
playerList.append('dealer')
print(playerList)


deckNum = int(input('How many decks? '))
remainingCards += shuffle(deckNum)
print(remainingCards)

bankrolls = int(input('What bankroll? ')) * playerNum

roundOver = False

while gameOver == False:
# at the start of every round
    # create status lists
    bets = []
    status = ['PUSH'] * (playerNum + 1)
    insurance = [0] * playerNum

    for player in playerList[:-1]:
        print('\nHello ' + str(player) + '!')
        bet = input('How much do you want to bet? ')
        while bet.isdigit() == False:
            bet = input('How much do you want to bet? ')
        bets.append(bet)
    print('\n')

    # deal cards
    deal()
    print(cards)

    # manual dealing
    cards = [['2', '9'], ['A', '2'], ['A', '10']]
    print('new cards lol ' + str(cards))




    # check for insurance, and for non-insurable BJ
    if cards[-1][0] == 'A':
        for x in range (0, len(playerList)-1):
            ins = input((playerList[x] + ', would you like insurance (y/n)? '))
            ins = ins.upper()
            if ins == 'Y':
                insurance[x] = int(input('How much would you like to wager? Up to ' + bets[x]/2 + '$.'))
                bets[x] -= insurance[x]

    if total(cards[-1]) == '21':
        print('Dealer has Blackjack')
        for x in range(0, len(playerList) - 1):
            if insurance[x] != 0:
                print(playerList[x] + ', you won your insurance bet of ' + insurance[x])
                bets[x] += insurance[x] * 2

    print(str(insurance))
    # each player plays
    for player in playerList[:-1]:
        turn = int(playerList.index(player))

        # welcome the player and show them their hand
        print('\nHello ' + str(player) + '!')
        info(turn)

        # check if player has BJ
        if total(turn) == 21:
            print('You have Blackjack!')
            status[turn] = 'BJ'

        # get the players move
        while total(turn) < 21:
            split = False
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
                # if(cards[turn][0] == cards[turn][1]):
                split = True
                playerList.insert(turn + 1, playerList[turn] + 'H2')
                status.insert(turn + 1, 'PUSH')
                bets.insert(turn + 1, bets[turn])
                cards.insert(turn + 1, [cards[turn][1]])
                cards[turn].pop()
                giveCard(turn)
                giveCard(turn + 1)
                print(playerList)
                print(bets)
                print(cards)

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
        else:
            status[turn] = total(turn)


    # have dealer play
    if total(-1) <= 16:
        while total(-1) <= 16:
            print('\nDealer is playing:')
            giveCard(-1)
            print('Dealers hand: ' + ', '.join(cards[-1]))
    else:
        print('Dealers hand: ' + ', '.join(cards[-1]))

    if total(-1) > 21:
        status[-1] = 'BUST'
    else:
        status[-1] = total(-1)
    print(status)

    # determine who won
    for x in range(0, len(status) - 1):
        if status[-1] == 'BUST':
            if status[x] != 'BUST' and status[x] != 'SUR':
                print(playerList[x] + ', you won ' + str(bets[x]) + '$!')
                bankrolls[x] += bets[x]
            else:
                print(playerList[x] + ', you lost ' + str(bets[x]) + '$.')
                bankrolls[x] -= bets[x]
        else:
            if status[x] == 'BUST' or status[x] == 'SUR':
                print(playerList[x] + ', you lost ' + str(bets[x]) + '$.')
                bankrolls[x] -= bets[x]
            if int(status[x]) > int(status[-1]):
                print(playerList[x] + ', you won ' + str(bets[x]) + '$!')
                bankrolls[x] += bets[x]
            elif int(status[x]) < int(status[-1]):
                print(playerList[x] + ', you lost ' + str(bets[x]) + '$.')
                bankrolls[x] -= bets[x]
            else:
                print('push')

    for x in range(0, len(status) - 1):
        print(playerList[x] + ': ' + str(bankrolls[x]))

    # add cards if low
    print('cards remaining: ' + str(len(remainingCards)) + '\n')
    if len(remainingCards) < 40:
        shuffle(int(input('Enter how many more decks you would like to deal: ')))

    if input('End game (y/n)? ') == 'y':
        gameOver = True