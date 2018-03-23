#!/usr/bin/env python

from die import * 
import sys
from os import path
import crapsResources_rc
from time import sleep
from PyQt5.QtCore import pyqtSlot, QSettings, QCoreApplication, Qt
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication, QDialog, QMessageBox

startingBankDefault = 100
maximumBetDefault = 100
minimumBetDefault = 10
logFileNameDefault = 'logFile.lg'

class Dice(QMainWindow) :
    """A game of Craps."""
    die1 = die2 = None

    def __init__( self, parent=None ):
        super().__init__(parent)
        self.appSettings = QSettings()
        uic.loadUi('Craps.ui', self)
        if self.appSettings.contains('logFile'):
            self.logFileName = self.appSettings.value('logFile', type=str)
        else:
            self.logFileName = "dice.log"
            self.logFile.setText(self.logFileName)

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
        self.preferencesSelectButton.clicked.connect(self.preferencesSelectButtonClickedHandler)

        self.updateUI()

    def __str__( self ):
        """String representation for Dice.
        """
        return "Die1: %s\nDie2: %s" % ( str(self.die1),  str(self.die2) )

    def updateUI ( self ): #move max and min bet values in constructor of update UI. #leave starting bank value in the constructor.
        print("Die1: %i, Die2: %i" % (self.die1.getValueRolled(),  self.die2.getValueRolled()))
        self.die1View.setPixmap(QtGui.QPixmap( ":/" + str( self.die1.getValueRolled() ) ) )
        self.die2View.setPixmap(QtGui.QPixmap( ":/" + str( self.die2.getValueRolled() ) ) )

        self.winsLabel.setText(str(self.winsCount))
        self.lossesLabel.setText(str(self.lossesCOunt))
        if self.firstRoll:
            self.rollingForLabel.setText("")
        else:
            self.rollingForLabel.setText(str(self.lastRoll))
        self.bankValue.setText(str(self.bankAmount))

    def restoreSettings(self):
        if self.appSettings.contains('startingBank'):
            self.startingBank = self.appSettings.value('startingBank', type=int)
        else:
            self.startingBank = startingBankDefault
            self.appSettings.setValue('startingBank', self.startingBank)
        if self.appSettings.contains('maximumBet'):
            self.maximumBet = self.appSettings.value('maximumBet', type=int)
        else:
            self.maximumBet = maximumBetDefault
            self.appSettings.setValue('maximumBet', self.maximumBet)
        if self.appSettings.contains('minimumBet'):
            self.minimumBet = self.appSettings.value('minimumBet', type=int)
        else:
            self.minimumBet = minimumBetDefault
            self.appSettings.setValue('minimumBet', self.minimumBet)
        if self.appSettings.contains('createLogFile'):
            self.createLogFile=appSettings.value('createLogFile',type=bool)
        else:
            self.createLogFile= logFileNameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)
#set a break point before restore settings and look at all variables and they should have the values that you just changed.
    def saveSettings(self):
        if self.appSettings.contains('startingBank'):
            self.startingBank = self.appSettings.value('startingBank', type=int)
        else:
            self.startingBank = startingBankDefault
            self.appSettings.setValue('startingBank', self.startingBank)
        if self.appSettings.contains('maximumBet'):
            self.maximumBet = self.appSettings.value('maximumBet', type=int)
        else:
            self.maximumBet = maximumBetDefault
            self.appSettings.setValue('maximumBet', self.maximumBet)
        if self.appSettings.contains('minimumBet'):
            self.minimumBet = self.appSettings.value('minimumBet', type=int)
        else:
            self.minimumBet = minimumBetDefault
            self.appSettings.setValue('minimumBet', self.minimumBet)
        if self.appSettings.contains('createLogFile'):
            self.createLogFile=appSettings.value('createLogFile',type=bool)
        else:
            self.createLogFile= logFileNameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)


    @pyqtSlot()
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


    @pyqtSlot() #user is requesting preferences editing dialog box.
    def preferencesSelectButtonClickedHandler(self):
        print("Setting preferences")
        preferencesDialog = PreferencesDialog()
        preferencesDialog.show()
        preferencesDialog.exec_()
        self.restoreSettings()
        self.updateUI()


class PreferencesDialog(QDialog):
    def __init__(self, parent = Dice):
        super(PreferencesDialog, self).__init__()

        uic.loadUi('PreferencesDialog.ui', self)
        self.appSettings = QSettings()
        if self.appSettings.contains('startingBank'):
            self.startingBank = self.appSettings.value('startingBank', type=int)
        else:
            self.startingBank = startingBankDefault
            self.appSettings.setValue('startingBank', self.startingBank)
        if self.appSettings.contains('maximumBet'):
            self.maximumBet = self.appSettings.value('maximumBet', type=int)
        else:
            self.maximumBet = maximumBetDefault
            self.appSettings.setValue('maximumBet', self.maximumBet)
        if self.appSettings.contains('minimumBet'):
            self.minimumBet = self.appSettings.value('minimumBet', type=int)
        else:
            self.minimumBet = minimumBetDefault
            self.appSettings.setValue('minimumBet', self.minimumBet)
        if self.appSettings.contains('createLogFile'):
            self.createLogFile=appSettings.value('createLogFile',type=bool)
        else:
            self.createLogFile= logFileNameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)

        self.buttonBox.accepted.connect(self.okayClickedHandeler)
        self.buttonBox.rejected.connect(self.cancleClickedHandler)
        self.startingBankValue.editingFinished.connect(self.startingBankValueChanged)
        self.maximumBetValue.editingFinished.connect(self.maximumBetValueChanged)
        self.minimumBetValue.editingFinished.connect(self.minimumBetValueChanged)

        self.updateUI()

    def startingBankValueChanged(self):
        self.startingBank=int(self.startingBankValue.text())

    def maximumBetValueChanged(self):
        self.maximumBet=int(self.maximumBetValue.text())

    def minimumBetValueChanged(self):
        self.minimumBet=int(self.minimumBetValue.text())

    def createLogFileChanged(self):
        self.createLogFile=self.createLogFileCheckBox

    def updateUI(self):
        self.startingBankValue.setText(str(self.startingBank))
        self.maximumBetValue.setText(str(self.maximumBet))
        self.minimumBetValue.setText(str(self.minimumBet))
        if self.createLogFile:
            self.createLogFileCheckBox.setCheckState(Qt.Checked)
        else:
            self.createLogFileCheckBox.setCheckState(Qt.Unchecked)


    def okayClickedHandeler(self):
        #print("Clicked okay handler")
        basePath = path.dirname(path.realpath(__file__))
        #self.logFileName = self.logFileNameEdit.text()
        self.logFileName = "dice.log"
        #write out all settings
        self.preferencesGroup = (('logFile', self.logFileName), )
        #write settings values.
        for setting, variableName in self.preferencesGroup:
            #if self.appSettings.contains(setting):
            self.appSettings.setValue(setting, variableName)
        self.close()


    def cancleClickedHandler(self):
        self.close()


if __name__ == "__main__":
    QCoreApplication.setOrganizationName("Cindalis Software");
    QCoreApplication.setOrganizationDomain("cindalissoftware.com");
    QCoreApplication.setApplicationName("Craps");
    appSettings = QSettings()
    app = QApplication(sys.argv)
    diceApp = Dice()
    diceApp.updateUI()
    diceApp.show()
    sys.exit(app.exec_())


