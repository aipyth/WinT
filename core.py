#coding: utf8
import pdb
import re
import time
import ctypes
import ctypes.wintypes as wintypes

LPOFNHOOKPROC = ctypes.c_voidp
LPCTSTR = LPTSTR = ctypes.c_wchar_p
GetOpenFileName = ctypes.windll.comdlg32.GetOpenFileNameW
OFN_ENABLESIZING = 0x00800000
OFN_PATHMUSTEXIST = 0x00000800
OFN_NOCHANGEDIR = 0x00000008
MAX_PATH = 1024

class OPENFILENAME(ctypes.Structure):
    _fields_ = [("lStructSize", wintypes.DWORD),
                ("hwndOwner", wintypes.HWND),
                ("hInstance", wintypes.HINSTANCE),
                ("lpstrFilter", LPCTSTR),
                ("lpstrCustomFilter", LPTSTR),
                ("nMaxCustFilter", wintypes.DWORD),
                ("nFilterIndex", wintypes.DWORD),
                ("lpstrFile", LPTSTR),
                ("nMaxFile", wintypes.DWORD),
                ("lpstrFileTitle", LPTSTR),
                ("nMaxFileTitle", wintypes.DWORD),
                ("lpstrInitialDir", LPCTSTR),
                ("lpstrTitle", LPCTSTR),
                ("flags", wintypes.DWORD),
                ("nFileOffset", wintypes.WORD),
                ("nFileExtension", wintypes.WORD),
                ("lpstrDefExt", LPCTSTR),
                ("lCustData", wintypes.LPARAM),
                ("lpfnHook", LPOFNHOOKPROC),
                ("lpTemplateName", LPCTSTR),
                ("pvReserved", wintypes.LPVOID),
                ("dwReserved", wintypes.DWORD),
                ("flagsEx", wintypes.DWORD)]

class core(object) :

    def _buildOFN(title, default_extension, filter_string, fileBuffer):

        ofn = OPENFILENAME()
        ofn.lStructSize = ctypes.sizeof(OPENFILENAME)
        ofn.lpstrTitle = title
        ofn.lpstrFile = ctypes.cast(fileBuffer, LPTSTR)
        ofn.nMaxFile = MAX_PATH
        ofn.lpstrDefExt = default_extension
        ofn.lpstrFilter = filter_string
        ofn.Flags = OFN_ENABLESIZING | OFN_PATHMUSTEXIST | OFN_NOCHANGEDIR
        return ofn

    def getOpenFileName(title, default_extension, filter_string, initialPath):  # don't know what it does
                                                                                # but it works. it gives me a path
        if initialPath is None:
            initialPath = ""
        filter_string = filter_string.replace("|", "\0")
        fileBuffer = ctypes.create_unicode_buffer(initialPath, MAX_PATH)
        ofn = core._buildOFN(title, default_extension, filter_string, fileBuffer)

        if GetOpenFileName(ctypes.byref(ofn)):
            return fileBuffer[:]
        else:
            return None


    def MakingIntList(self, DevidedMainText, SeekingWord):
        counter = 0
        SeekingWordsIntergers = []
        passFlag = False
        # pdb.set_trace()
        if self.SeekingWordOneWord:
            for TotalWord in DevidedMainText :
                for letter in TotalWord:
                    if letter == '<':
                        passFlag = True
                    elif letter == '>':
                        passFlag = False
                        continue
                if passFlag: continue

                if SeekingWord.lower() in TotalWord.lower():
                    SeekingWordsIntergers.append(counter)

                counter += 1
                value = float(counter * 100 / len(DevidedMainText))
                self.NewProgressBarValue.emit(value)
        else :
            SeekingWord = SeekingWord.lower().split()
            DevidedMainText = ' '.join(DevidedMainText).lower().split()

            for counter in range(len(DevidedMainText)) :
                coordT2 = counter + len(SeekingWord)
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
                value = float(counter * 100 / len(SeekingWord))
                self.NewProgressBarValue.emit(value)

        return SeekingWordsIntergers, SeekingWord

    def InsertingHTML(self, SeekingWordsIntergers, SeekingWord, DevidedMainText):
        iteration = 1                                                           # to count iteration

        for i in SeekingWordsIntergers :
            TotalWord = DevidedMainText[i]
            DevidedMainText[ i ] = ' <strong> <font color=#30577c> ' + TotalWord \
                                    + ' </font> </strong> '

            value = float(iteration * 100 / len(SeekingWordsIntergers))
            self.NewProgressBarValue.emit(value)                                           # setting new value on PB
            iteration += 1

        point = len(SeekingWord)
        if len(SeekingWordsIntergers) / point > 1 : ending_of_final_str = 'ies'
        else : ending_of_final_str = 'y'

        return DevidedMainText, point, ending_of_final_str

    def SeekingWordOneWord(SeekingWord):      # whether SeekingWord is
        SeekingWord = SeekingWord.split()     # a one word
        flag = True
        if len(SeekingWord) > 1 :
            flag = False
        return flag

    def DevidingText(self, MainText):         # just split()
        MainText = re.sub('\n', ' \n ', MainText)
        DevidedMainText = MainText.split(' ')
        return DevidedMainText

    def WipingSpases(word):                                                     # wipes spases
        word = re.sub(' ', '', word)
        return word

    def ChangingCH(text):                                                # replacing control characters
        text = re.sub('\n', ' <br> ', text)
        text = re.sub('\t', ' &nbsp;&nbsp;&nbsp;&nbsp; ', text)
        return text

    def WipeSumbols(word):                                                      # wipes unnecessary symbols
        SymList = [',', '.', '?', '(', ')', '/', '\\', ';', '|', '[', ']', \
        '{', '}']
        for i in SymList :
            if i in word :
                word = re.sub(i, '', word)
        return word
