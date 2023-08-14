import random
import Counter as co
# variables
auto = True
autoNum = 30000

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]


# house specific rules
bjPayout = 3/2
minBet = 2
maxBet = 1000
bankrollMin = 1
cutCard = 20
maxPlayers = 10
deckNum = 1
DAS = True # not implemented
RSA = True # not implemented
earlySurrended = False # not implemented

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

def deal(peopleToDealTo, peoplesCards, remainingDeck):
    print('dealing...')
    # Give each player 1 card, essentially "initializing" the array
    for x in range(peopleToDealTo):
        peoplesCards.append([remainingDeck[-1]])
        remainingDeck.pop()
    # Give each player 1 more card, for a total of 2
    for x in range(peopleToDealTo):
        peoplesCards, remainingDeck = giveCard(peoplesCards, remainingDeck, x)

    return peoplesCards, remainingDeck


def total(peoplesCards, hand):
    total = 0
    for card in peoplesCards[hand]:
        total += int(card)

    if total > 21:
        for x in range(0, peoplesCards[hand].count(11)):
            total -= 10
            if total <= 21:
                break
    return total


def info(peoplesCards, hand):
    print('Your hand: ' + ''.join(str(peoplesCards[hand])))
    print('Dealers hand: ' + str(peoplesCards[-1][0]) + ', Hidden')


def giveCard(peoplesCards, remainingDeck, currentHand):
    peoplesCards[currentHand].append(remainingDeck[-1])
    remainingDeck.pop()
    return peoplesCards, remainingDeck


def findPrevSplits(turn, splits):
    prevSplits = 0
    for x in range(0, turn + 1):
        if splits[x] == True:
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

def win(players, turn, bankrollModifier, moneyBet, bankrolls):
    print(players[turn] + ', you won ' + str(moneyBet[turn]) + '$!')
    # BANKROLL MODIFIER NEEDS TO EQUAL HOW MANY SPLITS HAVE COME BEFORE IT, NOT TOTAL SPLITS
    bankrolls[turn - bankrollModifier] += moneyBet[turn]
    return bankrolls

def lose(players, turn, bankrollModifier, moneyBet, bankrolls):
    print(players[turn] + ', you lost ' + str(moneyBet[turn]) + '$.')
    bankrolls[turn - bankrollModifier] -= moneyBet[turn]
    return bankrolls

def reset(playerNum, split, playerList, bankrolls, cards, discard, remainingCards, cutCard, automated):
    print('\nTotal bankroll:')
    for x in range(playerNum - 1):
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

    if not auto:
        if get_bool('End game (y/n)? '):
            print('See you next time!')
            return True, playerList, discard, cards, remainingCards

    return False, playerList, discard, cards, remainingCards

# main
def main(automated, autoIterate):
    remainingCards = []
    gameOver = False
    playerNum = 0
    cards = []
    discard = []
    playerList = []
    bankrolls = []
    repetitions = 0
    # before the game starts, set up (name and bankroll for each player), (set up deck)
    print('Welcome to Blackjack!')

    if automated:
        playerNum = 1
    else:
        playerNum = get_int('How many players? ', 1, maxPlayers)

    for x in range(0, playerNum):
        if automated:
            name = 'Bot'
            playerList.append(name)
        else:
            name = input('What is your name? ')
            playerList.append(name)
    playerList.append('dealer')
    print(f'List of players: {playerList}')

    remainingCards += shuffle(deckNum)
    print(f'Remaining cards: {remainingCards}')

    if automated:
        bankrolls = [1000]
    else:
        bankrolls = [get_int('What bankroll? ', bankrollMin, 1000000)] * playerNum

    while gameOver == False:
    # at the start of every round
        # create status lists
        bets = []
        status = ['PUSH'] * (playerNum + 1)
        insurance = [0] * playerNum
        split = [False for _ in range(playerNum)]
        for player in playerList[:-1]:
            print('\nHello ' + str(player) + '!')
            if automated:
                bet = co.whatShouldIBet(remainingCards)
                print('You bet: ' + str(bet))
                bets.append(bet)
            else:
                bet = get_int('How much do you want to bet? ', minBet, maxBet)
                bets.append(bet)

        # deal cards
        cards, remainingCards = deal(playerNum + 1, cards, remainingCards)
        print(cards) # DEBUG

        # check for insurance
        if cards[-1][0] == 11:
            for x in range (0, len(playerList)-1):
                ins = False
                if automated:
                    insurance[x] = co.insurance()
                else:
                    ins = get_bool(playerList[x] + ', would you like insurance (y/n)? ')
                    if ins:
                        insurance[x] = get_int('How much would you like to wager? ', 0, bets[x] / 2)
                        bankrolls[x] -= insurance[x]

            if total(cards, -1) == 21:
                print('Dealer has Blackjack')
                print('Dealers hand: ' + ''.join(str(cards[-1])))
                for x in range(0, len(playerList) - 1):
                    if insurance[x] != 0:
                        print(playerList[x] + ', you won your insurance bet of ' + str(insurance[x]))
                        bankrolls[x] += insurance[x] * 2
                    if total(cards, x) == 21:
                        print(playerList[x] + ', you push.')
                    else:
                        bankrolls = lose(playerList, x, 0, bets, bankrolls)
                gameOver, playerList, discard, cards, remainingCards = reset(playerNum, split, playerList, bankrolls, cards, discard, remainingCards, cutCard, auto)
                continue

        # non insurable BJ
        elif cards[-1][0] == '10' or cards[-1][0] == 'J' or cards[-1][0] == 'Q' or cards[-1][0] == 'K':
            if cards[-1][1] == '11':
                print('Dealer has Blackjack!')
                print('Dealers hand: ' + ''.join(str(cards[-1])))
                for x in range(0, len(playerList)-1):
                    if total(cards, x) == 21:
                        print(playerList[x] + ', you push.')
                    else:
                        bankrolls = lose(playerList, x, 0, bets, bankrolls)
                gameOver, playerList, discard, cards, remainingCards = reset(playerNum, split, playerList, bankrolls, cards, discard, remainingCards, cutCard, auto)
                continue


        # each player plays
        turn = 0
        while turn < len(playerList)-1:
            # turn = int(playerList.index(player))

            # welcome the player and show them their hand
            print('\nHello ' + str(playerList[turn]) + '!')
            info(cards, turn)
            # check if player has BJ
            if total(cards, turn) == 21:
                print('You have Blackjack!')
                bets[turn] *= bjPayout
                status[turn] = 'BJ'

            # get the players move
            while total(cards, turn) < 21:
                print(remainingCards)
                choice = co.whatShouldIPlay(total(cards, turn), cards[-1][0], remainingCards.copy())
                if not automated:
                    choice = input('What would you like to do (H, S, D, Sur, Spl): ').upper()
                    print(f'deck: {remainingCards}')
                if choice == 'H':
                    print(f'cards: {cards}')
                    print(f'remcards: {remainingCards}')
                    cards, remainingCards = giveCard(cards, remainingCards, turn)
                    info(cards, turn)

                elif choice == 'S':
                    break

                elif choice == 'D':
                    bets[turn] *= 2
                    print('New bet: ' + str(bets[turn]))
                    cards, remainingCards = giveCard(cards, remainingCards, turn)
                    info(cards, turn)
                    break

                elif choice == 'SPL':
                    if cards[turn][0] == cards[turn][1] and len(cards[turn]) == 2:
                        playerList.insert(turn + 1, playerList[turn] + ' (split hand)')
                        status.insert(turn + 1, 'PUSH')
                        split.insert(turn + 1, True)
                        bets.insert(turn + 1, bets[turn])
                        cards.insert(turn + 1, [cards[turn][1]])

                        cards[turn].pop()
                        cards, remainingCards = giveCard(cards, remainingCards, turn)
                        cards, remainingCards = giveCard(cards, remainingCards, turn + 1)
                        info(cards, turn)

                elif choice == 'SUR':
                    bets[turn] = bets[turn] * .5
                    print('Surrendered. Returned amount is: ' + str(bets[turn]*.5))
                    status[turn] = 'SUR'
                    info(cards, turn)
                    break


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
                cards, remainingCards = giveCard(cards, remainingCards, -1)
                print('Dealers hand: ' + ''.join(str(cards[-1])))
        else:
            print('Dealers hand: ' + ''.join(str(cards[-1])))

        if total(cards, -1) > 21:
            status[-1] = 'BUST'
        else:
            status[-1] = total(cards, -1)
        print(status) # DEBUG

        # determine who won
        for x in range(0, len(playerList) - 1):
            splitNum = findPrevSplits(x, split)
            # if dealer busted
            if status[-1] == 'BUST':
                # and u didn't bust
                if status[x] != 'BUST' and status[x] != 'SUR':
                    bankrolls = win(playerList, x, splitNum, bets, bankrolls)
                # and you did bust
                else:
                    bankrolls = lose(playerList, x, splitNum, bets, bankrolls)
            # if dealer did not bust
            else:
                # and you busted
                if status[x] == 'BUST' or status[x] == 'SUR':
                    bankrolls = lose(playerList, x, splitNum, bets, bankrolls)
                # if you scored higher dealer
                elif int(status[x]) > int(status[-1]):
                    bankrolls = win(playerList, x, splitNum, bets, bankrolls)
                # if you scored lower than dealer
                elif int(status[x]) < int(status[-1]):
                    bankrolls = lose(playerList, x, splitNum, bets, bankrolls)
                else:
                    print(playerList[x] + ', you push.')

        if automated:
            if repetitions < autoIterate:
                repetitions += 1
                gameOver, playerList, discard, cards, remainingCards = reset(playerNum, split, playerList, bankrolls, cards, discard, remainingCards, cutCard, auto)
            else:
                gameOver = True
        else:
            gameOver, playerList, discard, cards, remainingCards = reset(playerNum, split, playerList, bankrolls, cards, discard, remainingCards, cutCard, automated)

main(auto, autoNum)
# todo
    # make the huge chunka code(main) into a def ## Done
    # extra payout on BJ ## Done
    #
    # test edge cases (?)
