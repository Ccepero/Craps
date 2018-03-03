#! /usr/bin/env python
__author__ = 'Cindalis Cepero'

from die import *

class Craps(object):
    def __init__(self):
        self.die1 = Die()
        self.die2 = Die()
        self.firstRoll = True
        self.lastRoll = 0

    def __str__(self):
        return("Die1: {0} Die2: {1}".format(self.die1.getValueRolled(), self.die2.getValueRolled()))

    def play(self):
        self.valueRolled = self.die1.roll() + self.die2.roll()
        if self.firstRoll:
            if self.valueRolled == 7 or self.valueRolled == 11:
                self.valueRolled.setText("You win!")
            elif self.valueRolled in (2, 3, 12):
                self.valueRolled.setText("You lose!")
            else:
                self.firstRoll = False
                self.lastRoll = self.valueRolled
        else:
            if self.firstRoll == self.lastRoll:
                print("You Win!!")
            else:
                print("You lose!!")
            self.firstRoll = True
myGame = Craps()
userInput = input("r/b/q: ")
while userInput != 'q':
    myGame.play()
    print(myGame)
    userInput = input("r/b/q: ")
print(myGame)
