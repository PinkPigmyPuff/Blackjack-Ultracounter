# import Blackjack as bj
deck = ['K', '9', 'A', '4', 'A', '5', '9', '6', 'J', '2', 'J', 'Q', 'J', 'J', '9', '4', '2', '7', 'A', '7', '8', '6', 'K', '7', 'Q', '5', '8', '8', '6', '4', '10', '10', '7', '5', 'K', 'Q', '3', '10', '3', '3', '2', '2', '4', '3', 'K', 'Q', '10', '6', '8', 'A', '9', '5']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
occurence = [4, 4, 4, 4, 4, 4, 4, 4, 16, 4]
deck = values * 4
Odds = [0] * 31

print(deck)
def singleCardTotal(card):
    if card == 'J' or card == 'Q' or card == 'K' or card == '10':
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def whatShouldIPlay(myTotal, dealerCard):
    dealerCardTotal = singleCardTotal(dealerCard)

    # playerOdds = getOdds(myTotal, deck)
    Odds[dealerCardTotal] = 100

    dealerOdds = getDealerOdds2(dealerCardTotal)
    # playerBust = bustChance(playerOdds[0], playerOdds[1])
    # dealerBust = bustChance(dealerOdds[0], dealerOdds[1])
    # print('playerOdds: ' + str(playerOdds) + ', playerBust: ' + str(playerBust))
    print('dealerOdds: ' + str(dealerOdds))


    # print('lose chance: ' + str(loseChance(myTotal, dealerOdds)))

def getOdds(total, deck):
    possible = []
    odds = []
    for card in values:
        possible.append(total + int(card))
        if card != '10':
            odds.append((4 / 52) * 100)
        else:
            odds.append((16 / 52) * 100)

    return (possible, odds)



# pass in a single dealer
def getDealerOdds2(dealerTotal):
    branchScenario = []

    if dealerTotal < 17:
        for card in values:
            branchScenario.append(dealerTotal + int(card))


        print('Branch Scenario: ' + str(branchScenario))
        # print('BRANCH1Odds: ' + str(Odds))

        redistribute = Odds[dealerTotal]
        Odds.pop(dealerTotal)
        for num in branchScenario:
            if num != dealerTotal + 10:
                Odds[num] += redistribute / 13
            else:
                Odds[num] += (redistribute * 4) / 13

            if num < 17:
                getDealerOdds2(num)

    print(sum(Odds))
    return Odds

def getDealerOdds(total, deck):
    # generate initial possibilities and odds
    print('inside')
    possible = []
    odds = []
    for card in values:
        possible.append(total + int(card))
        if card != '10':
            odds.append((4 / 52) * 100)
        else:
            odds.append((16 / 52) * 100)



    print('possible: ' + str(possible))
    print('odds: ' + str(odds))
    # while dealerPossibility contains numbers under 17, redo every number under 17
    # while possible[0] < 17:
    # for every possible number (after hitting)
    for x in range(0, len(possible)):
        print(len(possible))
        # if the number is under 17
        if possible[0] < 17:
            # generate new possibility and odds
            newPossible = []
            newOdds = []
            # populate the new possiblity and odds with the chances for that individual total
            for card in values:
                newPossible.append(possible[0] + int(card))
                if card != '10':
                    newOdds.append((4 / 52) * 100)
                else:
                    newOdds.append((16 / 52) * 100)
            # divy up the popped number, among the rest of the possibilities / odds
            for x in range(0, len(possible)):
                # possible[x] += newPossible[x] / 100
                odds[x] += newOdds[x] / 100
            # get rid of the thang we just divied up
            # possible.pop(0)
            odds.pop(0)

        print('newPossible: ' + str(newPossible))
        print('newOdds: ' + str(newOdds))
        print('possible: ' + str(possible))
        print('odds: ' + str(odds))

    return (possible, odds)


def bustChance(possible, odds):
    bust = 0
    for x in range(0, len(possible)):
        if possible[x] > 21:
            bust += odds[x]

    return bust

def loseChance(myTotal, dealerOdds):
    loseChance = 0
    for x in range(0, len(dealerOdds[0])):
        if dealerOdds[0][x] > myTotal:
            loseChance += dealerOdds[1][x]
    return loseChance
# combined = getOdds(hand, deck)
# print(combined)
# print(bustChance(combined[0], combined[1]))

