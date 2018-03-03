#!/usr/bin/env python

from die import * 
import sys
import crapsResources_rc
from time import sleep
from PyQt5.QtCore import pyqtSlot, QSettings
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication

class Craps(QMainWindow) :
    """A game of Craps."""

    def __init__( self, parent=None ):

        super().__init__(parent)
        uic.loadUi('Craps.ui', self)
        self.appSettings = QSettings()
        if self.appSettings.contains('logFile'):
            self.logFileName = self.appSettings.Value('logFile', type=str)
        self.buttonBox.rejected.connect(self.cancelClickedHandler)
        self.buttonBox.accepted.connect(self.okayClickedHandler)

        self.updateUI()

        self.die1 = Die()
        self.die2 = Die()
        self.firstRoll = True
        self.lastRoll = 0
        self.winsCount = 0
        self.lossesCOunt = 0
        self.rollAmt = 0
        self.bankAmount = 1000
        self.buttonText = "roll"
        uic.loadUi("Craps.ui", self)
        self.bidSpinBox.setRange ( 10, 100 )
        self.bidSpinBox.setSingleStep ( 5 )
        self.lossesLabel.setText("")
             #          0  1  2  3  4    5    6    7    8    9    10   11   12
        self.payout = {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 1.2}
        self.rollButton.clicked.connect(self.rollButtonClickedHandler)

    def __str__( self ):
        """String representation for Dice.
        """
        return "Die1: %s\nDie2: %s" % ( str(self.die1),  str(self.die2) )

    def updateUI ( self ):
        print("Die1: %i, Die2: %i" % (self.die1.getValueRolled(),  self.die2.getValueRolled()))
        self.die1View.setPixmap(QtGui.QPixmap( ":/" + str( self.die1.getValueRolled() ) ) )
        self.die2View.setPixmap(QtGui.QPixmap( ":/" + str( self.die2.getValueRolled() ) ) )

        # Add your code here to update the GUI view so it matches the game state.

        self.winsLabel.setText(str(self.winsCount))
        self.lossesLabel.setText(str(self.lossesCOunt))
        if self.firstRoll:
            self.rollingForLabel.setText("")
        else:
            self.rollingForLabel.setText(str(self.lastRoll))
        self.bankValue.setText(str(self.bankAmount))

    # Player asked for another roll of the dice.
    def rollButtonClickedHandler ( self ):
        self.currentBet = self.bidSpinBox.value()
        self.valueRolled = self.die1.roll() + self.die2.roll()
        if self.firstRoll:
            if self.valueRolled in (7,11):
                self.resultsLabel.setText("You win!")
                self.winsCount += 1
                self.bankAmount += self.currentBet
            elif self.valueRolled in (2, 3, 12):
                self.resultsLabel.setText("You lose!")
                self.lossesCOunt += 1
                self.bankAmount -= self.currentBet
            else:
                self.firstRoll = False
                self.resultsLabel.setText("Roll again")
                self.lastRoll = self.valueRolled
        else:
            if self.valueRolled == self.lastRoll:
                self.resultsLabel.setText("You Win!!")
                self.winsCount += 1
                self.bankAmount += (1 - self.payout[self.valueRolled]) * self.currentBet
            else:
                self.resultsLabel.setText("You lose!!")
                self.lossesCOunt += 1
                self.bankAmount -= self.currentBet
            self.firstRoll = True
        self.updateUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    diceApp = Craps()
    diceApp.updateUI()
    diceApp.show()
    sys.exit(app.exec_())


