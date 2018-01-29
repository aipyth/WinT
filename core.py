#coding: utf8
import re
import time

from PyQt4 import QtCore

class core(object) :
    """
    Class "core" was builded for program WinT

    version -- 0.2.20
    """
    def __init__ (self):
        pass

    def DevidingText(self, MainText):         # just split()

        DevidedMainText = MainText.split()
        return DevidedMainText

    def SeekingWordOneWord(SeekingWord):      # whether SeekingWord is
                                              # a one word
        SeekingWord = SeekingWord.split()
        flag = True
        if len(SeekingWord) > 1 :
            flag = False
        return flag

    def MakingIntList(DevidedMainText, SeekingWord, self):
        value = 0.00
        repeat_att = None
        counter = 0
        SeekingWordsIntergers = []
        self.StatusLabel.setText('<font color = #ff0000>Performing</font>')
        if self.SeekingWordOneWord:
            for TotalWord in DevidedMainText :
                flag = SeekingWord.lower() in TotalWord.lower()
                if flag :
                    SeekingWordsIntergers.append(counter)
                counter += 1
                value = float(counter * 100 / len(DevidedMainText))
                self.CheckUpButton.emit(QtCore.SIGNAL('new_value'), value)
        else :
            SeekingWord = core.WipeSumbols(SeekingWord)
            SeekingWord = SeekingWord.lower()
            SeekingWord = SeekingWord.split()
            DevidedMainText = ' '.join(DevidedMainText)
            DevidedMainText = DevidedMainText.lower()
            DevidedMainText = DevidedMainText.split()
            lenSW = len(SeekingWord)
            for counter in range(len(DevidedMainText)) :
                coordT2 = counter + lenSW
                try:
                    CheckingFlagForIndexError = \
                    DevidedMainText[ coordT2 - 1 ] == DevidedMainText[ -1 ]
                except IndexError:
                    break
                if SeekingWord == DevidedMainText[counter:coordT2] :
                    AllIntergersList = list(range(counter, coordT2))
                    for i in AllIntergersList :
                        SeekingWordsIntergers.append(i)
                counter += 1
                value = float(counter * 100 / lenSW)
                self.CheckUpButton.emit(QtCore.SIGNAL('new_value'), value)
        return SeekingWordsIntergers, SeekingWord

    def InsertingHTML(SeekingWordsIntergers, SeekingWord, DevidedMainText, self):
        counter = 1
        len_seekingwordsint = len(SeekingWordsIntergers)
        self.StatusLabel.setText('<font color = #ff7a00> Rendering </font>')
        for i in SeekingWordsIntergers :
            TotalWord = DevidedMainText[i]
            DevidedMainText[ i ] = '<strong> <font color=#ff0000>' + TotalWord \
                                    + '</font> </strong>'
            value = float(counter * 100 / len(SeekingWordsIntergers))
            self.CheckUpButton.emit(QtCore.SIGNAL('new_value'), value)
            counter += 1
        if len_seekingwordsint != 1 : ending_of_final_str = 's'
        else : ending_of_final_str = ''
        if type(SeekingWord) == list: point = len(SeekingWord)
        else: point = 1
        self.StatusLabel.setText( ' <font color = Green size = 4> Finished! \
        Found %i word%s </font>' % (len(SeekingWordsIntergers) / point , \
        ending_of_final_str))
        return DevidedMainText

    def WipingSpases(word):          # wipes spases
        word = re.sub(' ', '', word)
        return word

    def WipeSumbols(word):                # wipes unnecessary symbols
        SymList = [',', '.', '?', '(', ')', '/', '\\', ';', '|', '[', ']', \
        '{', '}']
        for i in SymList :
            if i in word :
                word = re.sub(i, '', word)
        return word
