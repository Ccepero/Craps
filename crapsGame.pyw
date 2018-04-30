#!/usr/bin/env python
from sys import path
from die import * 
import sys
from os import path
import crapsResources_rc
from time import sleep
from logging import basicConfig, getLogger, DEBUG, INFO, CRITICAL
from pickle import dump, load
from PyQt5.QtCore import pyqtSlot, QSettings, QCoreApplication, Qt, QTimer
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication, QDialog, QMessageBox

startingBankDefault = 100
maximumBetDefault = 100
minimumBetDefault = 10
logFileNameDefault = 'dice.log'
pickleFileNameDefault = ".crapsSavedObjects.pl"

class Dice(QMainWindow) :
    """A game of Craps."""
    die1 = die2 = None

    def __init__( self, parent=None ):

        super().__init__(parent)

        self.logger = getLogger("dice")
        self.appSettings = QSettings()
        self.quitCounter = 0; #used in a workaround for a QT5 Bug.

        uic.loadUi('Craps.ui', self)

        self.payouts = {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 1.2}
        self.pickleFileName = pickleFileNameDefault
        self.restoreSettings()

        if path.exists(self.pickleFileName):
            self.die1, self.die2, self.firstRoll, self.lastRoll, self.winsCount, self.lossesCOunt, self.rollAmt, self.bankAmount, self.buttonText = self.restoreGame()
        else:
            self.restartGame()

        self.rollButton.clicked.connect(self.rollButtonClickedHandler)
        self.bailButton.clicked.connect(self.bailButtonClickedHandler)
        self.preferencesSelectButton.clicked.connect(self.preferencesSelectButtonClickedHandler)
        self.restartButton.clicked.connect(self.restartButtonClickedHandler)

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

    def restartGame(self):
        self.die1 = Die()
        self.die2 = Die()
        self.firstRoll = True
        self.lastRoll = 0
        self.winsCount = 0
        self.lossesCOunt = 0
        self.rollAmt = 0
        self.bankAmount = 1000
        self.buttonText = "roll"
        self.bidSpinBox.setRange ( 10, 100 )
        self.bidSpinBox.setSingleStep ( 5 )
        self.lossesLabel.setText("")

    def saveGame(self):
        saveItems = ( self.die1, self.die2, self.firstRoll, self.lastRoll, self.winsCount, self.lossesCOunt, self.rollAmt, self.bankAmount, self.buttonText)
        if self.appSettings.contains('pickleFileName'):
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFileName', type= str)), 'wb') as pickleFile:
                dump(saveItems, pickleFile)
        else:
            self.logger.critical("No pickle Filename")

    def restoreGame(self):
        if self.appSettings.contains('pickleFileName'):
            self.appSettings.value('pickleFileName', type = str)
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFileName', type= str)), 'rb') as pickleFile:
                return load(pickleFile)
        else:
            self.logger.critical("No pickle Filename")
            
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
        if self.appSettings.contains('createPickleFile'):
            self.createPickleFile=appSettings.value('createPickleFile',type=bool)
        else:
            self.createPickleFile= pickleFileNameDefault
            self.appSettings.setValue('createPickleFile', self.createPickleFile)
#set a break point before restore settings and look at all variables and they should have the values that you just changed.
    def saveSettings(self):
        self.logger.info("starting saveSettings")
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
        if self.appSettings.contains('createPickleFile'):
            self.createPickleFile=appSettings.value('createPickleFile',type=bool)
        else:
            self.createPickleFile= pickleFileNameDefault
            self.appSettings.setValue('createPickleFile', self.createPickleFile)




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
                self.firstRoll = True
                self.bailButton.setEnabled(False)
            elif self.valueRolled in (2, 3, 12):
                self.resultsLabel.setText("You lose!")
                self.lossesCOunt += 1
                self.bankAmount -= self.currentBet
                self.firstRoll = True
                self.bailButton.setEnabled(False)
            else:
                self.firstRoll = False
                self.resultsLabel.setText("Roll again")
                self.lastRoll = self.valueRolled
                self.bailButton.setEnabled(True)
        else:
            if self.valueRolled == self.lastRoll:
                self.resultsLabel.setText("You Win!!")
                self.winsCount += 1
                self.bankAmount += round(self.payouts[self.lastRoll] * self.currentBet)
                self.firstRoll = True
                self.bailButton.setEnabled(False)
            else:
                self.resultsLabel.setText("You lose!!")
                self.lossesCOunt += 1
                self.bankAmount -= round(self.payouts[self.lastRoll] * self.currentBet)
                self.firstRoll = True
                self.bailButton.setEnabled(False)
        self.updateUI()

    @pyqtSlot()
    def bailButtonClickedHandler(self):
        self.lossesCOunt += 1
        self.bankAmount -= self.currentBet
        self.firstRoll = True
        self.rollAmt = "Bailed!"
        self.bailButton.setEnabled(False)
        #self.buttonText = "Roll"
        self.updateUI()


    @pyqtSlot() #user is requesting preferences editing dialog box.
    def preferencesSelectButtonClickedHandler(self):
        print("Setting preferences")
        preferencesDialog = PreferencesDialog()
        preferencesDialog.show()
        preferencesDialog.exec_()
        self.restoreSettings()
        self.updateUI()

    @pyqtSlot()
    def restartButtonClickedHandler(self):
        self.restartGame()
        self.saveGame()
        self.updateUI()

    @pyqtSlot() #Player asked to quite game
    def closeEvent(self, event):
        if self.quitCounter == 0:
            self.quitCounter += 1
            quitMessage = "Are you sure you want to quit?"
            reply = QMessageBox.question(self, 'Message', quitMessage, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.saveGame()
                event.accept()
            else:
                event.ignore()
            return super().closeEvent(event)


class PreferencesDialog(QDialog):
    def __init__(self, parent = Dice):
        super(PreferencesDialog, self).__init__()
        self.logger = getLogger("dice")

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
    startingFolderName = path.dirname(path.realpath(__file__))
    if appSettings.contains('logFile'):
        logFileName = appSettings.value('logFile', type= str)
    else:
        logFileName = logFileNameDefault
        appSettings.setValue('logFile', logFileName)
    basicConfig(filename= path.join(startingFolderName, logFileName), level=INFO, format='%(asctime)s %(name)-8s %(levelName)-8s %(message)s')

    app = QApplication(sys.argv)
    diceApp = Dice()
    diceApp.updateUI()
    diceApp.show()
    sys.exit(app.exec_())


