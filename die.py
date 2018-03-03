#! /usr/bin/env python
__author__ = 'Cindalis Cepero'

from random import randint

class Die(object):
    def __init__(self, startingNumberOfSides = 6):
        self.numberOfSides = startingNumberOfSides
        self.valueRolled = 0
        self.minValue = 1
        self.maxValue = self.numberOfSides
    def __str__(self):
        return "{0}".format(self.valueRolled)

    def setNumberOfSides(self, newNumberOfSides):
        self.numberOfSides = newNumberOfSides
    def getNumberOfSides(self):
        return self.numberOfSides

    def setValueRolled(self, newValueRolled):
        self.valueRolled = newValueRolled
    def getValueRolled(self):
        return self.valueRolled

    def setMinValue(self, newMinValue):
        self.minValue = newMinValue
    def getMinValue(self):
        return self.minValue

    def setMaxValue(self, newMaxValue):
        self.maxValue = newMaxValue
    def getMaxValue(self):
        return self.maxValue

    def roll(self):
        self.valueRolled = randint(1, 6)
        return self.valueRolled

