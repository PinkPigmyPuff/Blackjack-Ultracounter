import Blackjack as bj

# variables
remainingCards = []
gameOver = False

values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
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
deckNum = 4
DAS = True # not implemented
RSA = True # not implemented
earlySurrended = False # not implemented

# before the game starts, set up (name and bankroll for each player), (set up deck)
print('Welcome to Blackjack!')

playerNum = bj.get_int('How many players? ', 1, maxPlayers)
for x in range(0, playerNum):
    name = input('What is your  name? ')
    playerList.append(name)
playerList.append('dealer')
print(playerList) # DEBUG

remainingCards += bj.shuffle(deckNum, values)
print(remainingCards) # DEBUG

bankrolls = bj.get_int('What bankroll? ', bankrollMin, 1000000) * playerNum


while gameOver == False:
# at the start of every round
    # create status lists
    bets = []
    status = ['PUSH'] * (playerNum + 1)
    insurance = [0] * playerNum
    split = [False] * playerNum
    for player in playerList[:-1]:
        print('\nHello ' + str(player) + '!')
        bet = bj.get_int('How much do you want to bet? ', minBet, maxBet)
        bets.append(bet)

    # deal cards
    bj.deal(playerList, cards, remainingCards)
    print(cards) # DEBUG

    # manual dealing
    cards = [['9', '9'], ['A', '10'], ['J', '3']] # DEBUG
    # cards = [['A', 'A'], ['Q', '4']] # DEBUG
    print('new cards lol ' + str(cards)) # DEBUG


    # check for insurance
    if cards[-1][0] == 'A':
        for x in range (0, len(playerList)-1):
            ins = bj.get_bool(playerList[x] + ', would you like insurance (y/n)? ')
            if ins:
                insurance[x] = bj.get_int('How much would you like to wager? ', 0, bets[x] / 2)
                bankrolls[x] -= insurance[x]

        if bj.total(-1) == 21:
            print('Dealer has Blackjack')
            print('Dealers hand: ' + ', '.join(cards[-1]))
            for x in range(0, len(playerList) - 1):
                if insurance[x] != 0:
                    print(playerList[x] + ', you won your insurance bet of ' + str(insurance[x]))
                    bankrolls[x] += insurance[x] * 2
                if bj.total(x) == 21:
                    print(playerList[x] + ', you push.')
                else:
                    bj.lose(x, splitNum)
            gameOver = bj.reset(0)
            continue

    # non insurable BJ
    elif cards[-1][0] == '10' or cards[-1][0] == 'J' or cards[-1][0] == 'Q' or cards[-1][0] == 'K':
        if cards[-1][1] == 'A':
            print('Dealer has Blackjack!')
            print('Dealers hand: ' + ', '.join(cards[-1]))
            for x in range(0, len(playerList)-1):
                if bj.total(x) == 21:
                    print(playerList[x] + ', you push.')
                else:
                    bj.lose(x, 0)
            gameOver = bj.reset(0)
            continue


    # each player plays
    turn = 0
    while turn < len(playerList)-1:
        # turn = int(playerList.index(player))

        # welcome the player and show them their hand
        print('\nHello ' + str(playerList[turn]) + '!')
        bj.info(turn)

        # check if player has BJ
        if bj.total(turn) == 21:
            print('You have Blackjack!')
            bets[turn] *= bjPayout
            status[turn] = 'BJ'

        # get the players move
        while bj.total(turn) < 21:
            choice = input('What would you like to do (H, S, D, Sur, Spl): ').upper()
            if choice == 'H':
                bj.giveCard(turn)
                bj.info(turn)

            elif choice == 'S':
                break

            elif choice == 'D':
                bets[turn] *= 2
                print('New bet: ' + str(bets[turn]))
                bj.giveCard(turn)
                bj.info(turn)
                break

            elif choice == 'SPL':
                if cards[turn][0] == cards[turn][1] and len(cards[turn]) == 2:

                    playerList.insert(turn + 1, playerList[turn] + ' (split hand)')
                    status.insert(turn + 1, 'PUSH')
                    split.insert(turn + 1, True)
                    bets.insert(turn + 1, bets[turn])
                    cards.insert(turn + 1, [cards[turn][1]])

                    cards[turn].pop()
                    bj.giveCard(turn)
                    bj.giveCard(turn + 1)
                    bj.info(turn)

            elif choice == 'SUR':
                bets[turn] = bets[turn] * .5
                print('Surrendered. Returned amount is: ' + str(bets[turn]*.5))
                status[turn] = 'SUR'
                bj.info(turn)
                break


        # check if player busted
        if bj.total(turn) > 21:
            print('Busted')
            status[turn] = 'BUST'
        elif status[turn] != 'SUR' or status[turn] != 'BJ':
            status[turn] = total(turn)
        turn += 1


    # have dealer play
    print('\nDealer is playing:')
    if bj.total(-1) <= 16:
        while bj.total(-1) <= 16:
            bj.giveCard(-1)
            print('Dealers hand: ' + ', '.join(cards[-1]))
    else:
        print('Dealers hand: ' + ', '.join(cards[-1]))

    if bj.total(-1) > 21:
        status[-1] = 'BUST'
    else:
        status[-1] = bj.total(-1)
    print(status) # DEBUG

    # determine who won
    for x in range(0, len(playerList) - 1):
        splitNum = bj.findPrevSplits(x)
        print(str(playerList[x]) + ' splitNum = ' + str(splitNum))
        # if dealer busted
        if status[-1] == 'BUST':
            # and u didn't bust
            if status[x] != 'BUST' and status[x] != 'SUR':
                bj.win(x, splitNum)
            # and you did bust
            else:
                bj.lose(x, splitNum)
        # if dealer did not bust
        else:
            # and you busted
            if status[x] == 'BUST' or status[x] == 'SUR':
                bj.lose(x, splitNum)
            # if you scored higher dealer
            elif int(status[x]) > int(status[-1]):
                bj.win(x, splitNum)
            # if you scored lower than dealer
            elif int(status[x]) < int(status[-1]):
                bj.lose(x, splitNum)
            else:
                print(playerList[x] + ', you push.')

    gameOver = bj.reset()

# todo
    # make the huge chunka code into a def
    # extra payout on BJ
    # test edge cases (?)

# calculate the odds of each result, based on the deck

def getOdds(deck):
    print('hi')

getOdds(bj.cards)
