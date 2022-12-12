# Blackjack-Ultracounter
Card counting on steroids

## Files
Blackjack.py is the basic blackjack game
Counter.py is the 'brain' of the machine, which uses an advanced method of card counting (where every card is kept track of) in order to recommend the optimal move to the player.

## Background: About Blackjack and Card Counting
Blackjack is the only gambling game played in casinos in which you are able to consistently beat the house, given enough time and money. To do this, players must first learn "basic strategy", which dictates what you should do (hit, stand, double down, etc) based on your cards, and the one card the dealer is showing. Using this alone, you can get around a 49% chance of winning against the house - not horrible. Dedicated players will go even further, and learn card counting. In essence, you keep track of how many high (10-A) cards remain relative to how many low (2-6) cards remain. This method will bring your edge to approximately 51% -- however, recently casino's have started to fight back against card counting, implementing various rules (for example shuffling the cards every round) in order to remove the edge players have over the house.

## Abstract: How much of an edge can I get over the Casino?
Having card counted myself in the past, I wondered how much further players could push their edge over the house. Card counting is only a crude estimation of what cards remain. However, anyone with a perfect memory -- in this case computers -- should theoretically be able to gain an even larger edge over the house by tracking exactly which cards remain, and developing an optimized strategy based off of that. This is what I set out to do with code.

Disclaimer: this code is not intended to be used in order to play blackjack for money
