# coding: utf8
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextEdit, QPushButton, QLayout, QSizePolicy, QLabel, \
    QPlainTextEdit, QProgressBar
from core import core

class MyWindow(QtGui.QWidget):
    def __init__ (self, parent = None):

        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags( QtCore.Qt.Window )

        desktop = QtGui.QApplication.desktop()

        size_of_window = QtCore.QSize(desktop.width()- 300,\
                                    desktop.height() - 300)
        start_point = \
            QtCore.QPoint((desktop.width() - size_of_window.width())  // 2 ,
                         (desktop.height() - size_of_window.height()) // 2)

        self.resize(size_of_window)
        self.setMinimumSize(300, 200)

        self.move(start_point)

        self.setWindowTitle(" WinT ")

        self.MainTextField = QTextEdit(self)
        self.SeekingWordTextField = QTextEdit(self)

        self.MainTextField.setText("<font color = #ff0000>Write your Text here</font>")
        self.SeekingWordTextField.setText("<font color = #ff0000>Here write seeking word</font")
        self.MainTextField.zoomIn( 3 )
        self.SeekingWordTextField.zoomIn( 3 )

        self.CheckUpButton = QPushButton(' Check Up ', self)
        self.CheckUpButton.setShortcut("Alt+S")
        self.CheckUpButton.setToolTip('Alt + S')
        self.CheckUpButton.setFlat(False)
        self.CheckUpButton.clicked.connect(self.ChekingMetod)
        self.connect(self.CheckUpButton, QtCore.SIGNAL("new_value"),
                     self.set_new_value)

        self.ClearButton = QPushButton(' Clear ', self)
        self.ClearButton.setShortcut("Alt+Z")
        self.ClearButton.setToolTip('Alt + Z')
        self.ClearButton.setFlat(False)
        self.ClearButton.clicked.connect(self.clear_text_fields)

        self.ClearSecondFieldButton = QPushButton(' Clear SF ', self)
        self.ClearSecondFieldButton.setShortcut("Alt+X")
        self.ClearSecondFieldButton.setToolTip('Alt + X')
        self.ClearSecondFieldButton.setFlat(False)
        self.ClearSecondFieldButton.clicked.connect(self.clear_second_field)

        self.AboutButton = QPushButton(' About ', self)
        self.AboutButton.clicked.connect(self.about_start)

        self.ProgressBar = QProgressBar(self)
        self.ProgressBar.setTextVisible(True)
        self.ProgressBar.setRange(0, 100)
        self.ProgressBar.setValue(0)

        self.StatusLabel = QLabel("<font size = 4 color = DarkRed > First\
                                    clear the textfields </font>", self)

        ButtonLayout = QtGui.QHBoxLayout()
        ButtonLayout.addWidget(self.CheckUpButton, alignment =
                               QtCore.Qt.AlignCenter)
        ButtonLayout.addWidget(self.ClearButton, alignment =
                               QtCore.Qt.AlignCenter)
        ButtonLayout.addWidget(self.ClearSecondFieldButton, alignment =
                               QtCore.Qt.AlignCenter)
        ButtonLayout.addWidget(self.AboutButton, alignment =
                               QtCore.Qt.AlignCenter)

        TextFieldsLayout = QtGui.QHBoxLayout()
        TextFieldsLayout.addWidget(self.MainTextField)
        TextFieldsLayout.addWidget(self.SeekingWordTextField)
        TextFieldsLayout.setSpacing(10)

        StatusLayout = QtGui.QHBoxLayout()
        StatusLayout.addWidget(self.ProgressBar, alignment =
                              QtCore.Qt.AlignLeft)
        StatusLayout.addWidget(self.StatusLabel, alignment =
                              QtCore.Qt.AlignRight)
        StatusLayout.setSpacing(10)

        TextFields_SizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding,
                                            QSizePolicy.MinimumExpanding)
        self.MainTextField.setSizePolicy(TextFields_SizePolicy)
        self.SeekingWordTextField.setSizePolicy(TextFields_SizePolicy)


        MainLayout = QtGui.QVBoxLayout()
        MainLayout.addLayout(ButtonLayout)
        MainLayout.addLayout(TextFieldsLayout)
        MainLayout.addLayout(StatusLayout)
        self.setLayout( MainLayout )

    def resizeEvent(self, qresizeEvent):
        self.ProgressBar_width = qresizeEvent.size().width() // 2 - 30
        self.ProgressBar.setFixedSize(self.ProgressBar_width, 14)
        QtGui.QWidget.resizeEvent(self, qresizeEvent)

    def clear_text_fields(self):
        self.MainTextField.setText('')
        self.SeekingWordTextField.setText('')
        self.StatusLabel.setText("<font size = 4 color = DarkGreen> \
                                    Cleared </font>")
        self.ProgressBar.setRange(0, 0)

    def clear_second_field(self):
        self.SeekingWordTextField.setText('')
        self.StatusLabel.setText("<font size = 4 color = DarkGreen> \
                                    Cleared </font>")
        self.ProgressBar.setRange(0, 0)

    def ChekingMetod(self):

        Answer = None
        EndOfStroke = ''
        MainText = self.MainTextField.toPlainText()
        SeekingWord = self.SeekingWordTextField.toPlainText()

        EmptynessFlag_MainText = MainText == '' or MainText ==  ' '
        EmptynessFlag_SeekingWord = SeekingWord == '' or SeekingWord == ' ' or SeekingWord == '/n'
        if EmptynessFlag_MainText or EmptynessFlag_SeekingWord:
            if EmptynessFlag_MainText and EmptynessFlag_SeekingWord:
                EndOfStroke = 's'
            self.StatusLabel.setText('<font color=#563bff> <b> Empty field%s \
            </b> </font>' %(EndOfStroke))
            return False
        self.StatusLabel.setText('<font color = #090074>Preparing</font>')
        self.ProgressBar.setRange(0, 100)
        DevidedMainText = core.DevidingText(self, MainText)

        if core.SeekingWordOneWord(SeekingWord):

            self.SeekingWordOneWord = True
            SeekingWord = core.WipingSpases(SeekingWord)
            SeekingWordsIntergers = core.MakingIntList(DevidedMainText,\
             SeekingWord, self)
            Answer = core.InsertingHTML(SeekingWordsIntergers[0],\
             SeekingWordsIntergers[1], DevidedMainText, self)
            Answer = ' '.join(Answer)

        else:

            self.SeekingWordOneWord = False
            SeekingWordsIntergers = core.MakingIntList(DevidedMainText,\
             SeekingWord, self)
            Answer = core.InsertingHTML(SeekingWordsIntergers[0], \
            SeekingWordsIntergers[1], DevidedMainText, self)
            Answer = ' '.join(Answer)

        self.MainTextField.setText(Answer)

    def set_new_value(self, value):
        self.ProgressBar.setValue(value)

    def about_start(self):
        about.show()

class AboutWindow(QtGui.QWidget):
    def __init__(self, parrent = None):

        QtGui.QWidget.__init__(self, parrent)
        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.resize(200, 170)
        self.setWindowModality(2)
        self.setWindowTitle(' About ')

        self.About = QLabel('<font size = 4> This program was created by \
                            <br> Ivan Zhytkevych <br> Telegram Link - <a href = \
                            "https://t.me/thlght"> \
                            t.me\\thlght </a> <br> \
                            VK Link - <a href = \
                            "https://vk.com/python10"> \
                            vk.com/python10 </a> <br><font color = DarkGrey > \
                            Version 0.2.21 <br> written 20.10.2017 <br>\
                            builded 10.11.2017 </font> </font>' ,self)
        self.About.setWordWrap(True)
        self.About.setOpenExternalLinks(True)

        self.CloseButton = QPushButton('Close' , self)
        self.CloseButton.clicked.connect(self.close)

        AboutLayout = QtGui.QVBoxLayout()
        AboutLayout.addWidget(self.About)
        AboutLayout.addWidget(self.CloseButton, alignment =
                              QtCore.Qt.AlignHCenter)

        self.setLayout(AboutLayout)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    about = AboutWindow()
    window.setWindowIcon(QtGui.QIcon("icon.ico"))
    window.show()
    sys.exit(app.exec_())
