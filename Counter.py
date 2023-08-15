# The card counting script

# TODO:
# Make it so that Aces can be one or 11
# winChance needs to be replaced with AVERAGE PAYHOUT, which is used to decide if you should Split or Double down or Surrender
# GetDealerOdds needs to remove cards from the deck when it goes down the recursive bunny holes to be more accurate

# lists of the odds that the player / dealer will get any given total. Indexed by value, ex: dealerOdds[17] represents the % chance the dealer will get a 17
maxPossible = 33
dealerOdds = [0] * maxPossible
playerOdds = [0] * maxPossible

# tells you what you should play
def whatShouldIPlay(myTotal, dealerCard, deck):
    print("\n####   ULTRACOUNTER    ####")
    print("Deck: " + str(deck))
    # FIRST, generate the odds that the dealer gets any combo between 17-BUST
    dealerCardTotal = int(dealerCard)
    dealerOdds[dealerCardTotal] = 100
    getDealerOdds(dealerCardTotal, deck)
    # print("sum of odds: " + str(sum(dealerOdds)))
    print("The dealerOdds are: " + str(dealerOdds))

    # THEN, get the playerOdds.
    getOdds(myTotal, deck)
    print("The playerOdds are: " + str(playerOdds))

    # calculate the chances that the player will win if they stand
    currentWinChance = wtl(myTotal)
    print("Win/Tie/Lose if you stand: " + str(currentWinChance))

    # calculate the chances that the player will win if they draw a card
    hitWinChance = 0.0
    for card in deck:
        newTotal = myTotal + card
        hitWinChance += wtl(newTotal) / len(deck)
    print("average win/tie/lose if you draw a card: " + str(hitWinChance))

    # recommend a course of action based on the odds of winning/losing calculated above
    if currentWinChance > hitWinChance:
        print('Counter reccommends that you stand')
        return 'S'
    elif currentWinChance < hitWinChance:
        print('Counter reccommends that you hit')
        return 'H'
    else:
        print('Counter is befuzzled')

def whatShouldIBet(deck):
    print("Determining what to bet")
    getOdds(0, deck)
    getDealerOdds(0, deck)
    print("The playerOdds are: " + str(playerOdds))
    print("The dealerOdds are: " + str(dealerOdds))

    return 2

def insurance():
    return 0

# creates two arrays, saying ALL possilbe hand totals after you've been delt a card, and the ODDS of each one of those hand totals
def getOdds(total, deck):
    # add every possible card to the current total, and generate the odds for each
    for card in deck:
        playerOdds[total + card] += 100 / len(deck)

def getPlayerOdds(dealerTotal, deck):
    #
    for card in deck:
        playerOdds[card] += 100 / len(deck)
        deck.pop(0)
        for card in deck:
            newTotal = dealerTotal + int(card)
            dealerOdds[newTotal] += redistribute / len(deck)
            playerOdds[card] += 100 / len(deck)
    print(playerOdds)


#getPlayerOdds(15, [11, 11, 7, 10, 9, 10, 9, 7, 7, 5, 8, 5, 11, 9, 10, 10, 10, 11, 6, 4, 2, 4, 2, 10, 10, 3, 10, 3, 3, 10, 3, 9, 2, 10, 5, 8, 4, 7, 6, 10, 8, 10, 4, 8, 10, 6, 2, 6])

# Determine the odds that the dealer reaches any given value
def getDealerOdds(dealerTotal, deck):
    redistribute = dealerOdds[dealerTotal]
    dealerOdds[dealerTotal] = 0
    # if the dealer isn't over 17
    if dealerTotal < 17:
        # for every card
        for card in deck:
            #deck.pop(0) # Test. Shit worked when I commented this out.
            newTotal = dealerTotal + int(card)
            dealerOdds[newTotal] += redistribute / len(deck)
            if newTotal < 17:
                getDealerOdds(newTotal, deck)

# calculate the chance of busting if the player takes another card
def bustChance(odds):
    bust = 0
    for x in range(22, len(odds)):
        bust += odds[x]
    return bust

# calculates the chance of winning / tying / losing
def wtl(playerValue):
    win = 0.0
    tie = 0.0
    lose = 0.0

    if playerValue > 21:
        lose = 100
        return win - lose

    for num in range(playerValue, maxPossible):
        if num > 21:
            win += dealerOdds[num]
            # print("at iteration " + str(num) + ", " + str(dealerOdds[num]) + " is being added to win")
        elif playerValue > num:
            win += dealerOdds[num]
            # print("at iteration " + str(num) + ", " + str(dealerOdds[num]) + " is being added to win")
        elif playerValue < num:
            lose += dealerOdds[num]
            # print("at iteration " + str(num) + ", " + str(dealerOdds[num]) + " is being added to lose")
        else:
            tie += dealerOdds[num]
            # print("at iteration " + str(num) + ", " + str(dealerOdds[num]) + " is being added to tie")
    return win - lose