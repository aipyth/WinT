# coding: utf8
import sys, pdb, re
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtWidgets import QTextEdit, QPushButton, QLayout, QSizePolicy,\
 QLabel, QPlainTextEdit, QProgressBar, QHBoxLayout, QVBoxLayout, QWidget
from core import core


class MyWindow(QtWidgets.QWidget):
    NewProgressBarValue = QtCore.pyqtSignal(float)
    def __init__ (self, parent = None):

        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags( QtCore.Qt.Window )

        self.md = 'r'
        self.HtmlSupport = False
        buttons_list = [['self.OpenFileButton', 'Alt+O', 'Alt + O', self.open_file],
                        ['self.CheckUpButton', 'Alt+S', 'Alt + S', self.cheking_metod],
                        ['self.ClearButton', 'Alt+Z', 'Alt + Z', self.clear_text_fields],
                        ['self.ClearSFButton', 'Alt+X', 'Alt + X', self.clear_second_field],
                        ['self.SettingsButton', 'Alt+T', 'Alt + T', self.settings_start],
                        ['self.AboutButton', 'Alt+I', 'Alt + I', self.about_start]]
        desktop = QtWidgets.QApplication.desktop()
        size_of_window = QtCore.QSize(desktop.width() - (desktop.width()*0.15625),
                                    desktop.height() - (desktop.height()*0.27778))
        start_point = QtCore.QPoint((desktop.width() - size_of_window.width()) // 2 ,
                                    (desktop.height() - size_of_window.height()) // 2)

        self.resize(size_of_window)
        self.move(start_point)
        self.setWindowTitle(" WinT ")

        self.MainTextField = QTextEdit(self)
        self.MainTextField.zoomIn(3)
        self.MainTextField.setAcceptRichText(True)
        self.MainTextField.setTabChangesFocus(False)
        self.SeekingWordTextField = QTextEdit(self)
        self.SeekingWordTextField.zoomIn(3)
        self.SeekingWordTextField.setAcceptRichText(True)

        self.OpenFileButton = QPushButton('Open File', self)
        self.CheckUpButton = QPushButton('Check Up', self)
        self.ClearButton = QPushButton('Clear', self)
        self.ClearSFButton = QPushButton('Clear SF', self)
        self.SettingsButton = QPushButton('Settings', self)
        self.AboutButton = QPushButton('About', self)

        for total_button in buttons_list:
            eval(total_button[0]).setShortcut(total_button[1])
            eval(total_button[0]).setToolTip(total_button[2])
            eval(total_button[0]).setFlat(True)
            eval(total_button[0]).clicked.connect(total_button[3])
            eval(total_button[0]).setStyleSheet(""" QPushButton {
            color: #ffffff;
            font-weight: bold;}""")

        self.NewProgressBarValue.connect(self.set_new_value)

        self.ProgressBar = QProgressBar(self)
        self.ProgressBar.setRange(0, 100)
        self.ProgressBar.setValue(0)
        self.ProgressBar.setStyleSheet(""" QProgressBar {
        border: 2px solid #30577c;
        border-radius: 4px;
        text-align: middle;
        color: #012342;
        font-weight: bold;
        }
        QProgressBar::chunk {background-color: #0ca5de}""")

        self.StatusLabel = QLabel("Ready!", self)
        self.StatusLabel.setStyleSheet(""" QLabel{
        font-family: sans serif;
        font-weight: bold;
        color: #f4f6f5;
        }""")

        ButtonLayout = QHBoxLayout()
        for total_button in buttons_list:
            ButtonLayout.addWidget(eval(total_button[0]))
        ButtonLayout.setAlignment(QtCore.Qt.AlignLeft)

        TextFieldsLayout = QHBoxLayout()
        TextFieldsLayout.addWidget(self.MainTextField)
        TextFieldsLayout.addWidget(self.SeekingWordTextField)
        TextFieldsLayout.setSpacing(10)

        StatusLayout = QHBoxLayout()
        StatusLayout.addWidget(self.ProgressBar, alignment =
                              QtCore.Qt.AlignLeft | QtCore.Qt.AlignHCenter)
        StatusLayout.addWidget(self.StatusLabel, alignment =
                              QtCore.Qt.AlignRight | QtCore.Qt.AlignHCenter)
        StatusLayout.setSpacing(10)

        TextFields_SizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding,
                                            QSizePolicy.MinimumExpanding)
        self.MainTextField.setSizePolicy(TextFields_SizePolicy)
        self.SeekingWordTextField.setSizePolicy(TextFields_SizePolicy)

        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                            QtGui.QColor('#02325f'))
        pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window,
                            QtGui.QColor('#02325f'))
        self.setPalette(pal)

        MainLayout = QVBoxLayout()
        MainLayout.addLayout(ButtonLayout)
        MainLayout.addLayout(TextFieldsLayout)
        MainLayout.addLayout(StatusLayout)
        self.setLayout(MainLayout)

    def resizeEvent(self, qresizeEvent):
        self.ProgressBar_width = qresizeEvent.size().width() // 2 - 30
        self.ProgressBar.setFixedSize(self.ProgressBar_width, 14)
        QWidget.resizeEvent(self, qresizeEvent)

    def clear_text_fields(self):
        self.MainTextField.setText('')
        self.SeekingWordTextField.setText('')
        self.StatusLabel.setText("Cleared")
        self.ProgressBar.setValue(0)

    def clear_second_field(self):
        self.SeekingWordTextField.setText('')
        self.StatusLabel.setText("Cleared")
        self.ProgressBar.setValue(0)

    def open_file(self):
        # pdb.set_trace()
        FilePath = core.getOpenFileName('WinT - Open', None, '', None)
        if FilePath == None:
            self.file_none()
            return 0
        FilePath = re.sub('\x00', '', FilePath)
        FileName = FilePath.split('\\')[-1]


        self.MainTextField.setText(AllText)
        return 0


    def file_none(self):
        self.StatusLabel.setText("No file opened")

    def cheking_metod(self):
        Answer = None
        EndOfStroke = ''
        if self.HtmlSupport : MainText = core.ChangingCH(self.MainTextField.toHtml())
        else: MainText = self.MainTextField.toPlainText()
        print(MainText)
        SeekingWord = self.SeekingWordTextField.toPlainText()

        EmptynessFlag_MainText = MainText == '' or MainText ==  ' '
        EmptynessFlag_SeekingWord = SeekingWord == '' or SeekingWord == ' ' or SeekingWord == '/n'

        if EmptynessFlag_MainText or EmptynessFlag_SeekingWord:
            if EmptynessFlag_MainText and EmptynessFlag_SeekingWord:
                EndOfStroke = 's'
            self.StatusLabel.setText('<b>Empty field{}</b>'.format(EndOfStroke))
            return False

        self.StatusLabel.setText('Preparing')

        DevidedMainText = core.DevidingText(self, MainText)

        if core.SeekingWordOneWord(SeekingWord):
            self.SeekingWordOneWord = True
            SeekingWord = core.WipingSpases(SeekingWord)
        else:
            self.SeekingWordOneWord = False
        self.StatusLabel.setText('Performing')
        SeekingWordsIntergers = core.MakingIntList(self, DevidedMainText,\
         SeekingWord)
        self.StatusLabel.setText('Rendering')
        Answer = core.InsertingHTML(self, SeekingWordsIntergers[0], \
        SeekingWordsIntergers[1], DevidedMainText)

        Answer = (Answer[0], Answer[1], Answer[2])
        FinishedText = ' '.join(Answer[0])
        print(FinishedText)

        self.MainTextField.setText(FinishedText)
        self.StatusLabel.setText( 'Finished! Found %i entr%s' \
        % (len(SeekingWordsIntergers[0]) / Answer[1] , Answer[2]))

    def set_new_value(self, value):
        self.ProgressBar.setValue(value)

    def about_start(self):
        about.show()

    def settings_start(self):
        settings.show()


class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, parrent=None):
        QtWidgets.QWidget.__init__(self, parrent)

        self.resize(300, 600)
        self.setWindowModality(2)
        self.setWindowTitle('Settings')


class AboutWindow(QtWidgets.QWidget):
    def __init__(self, parrent = None):

        QtWidgets.QWidget.__init__(self, parrent)
        self.setWindowFlags(QtCore.Qt.Window |
                           QtCore.Qt.CustomizeWindowHint |
                           QtCore.Qt.MSWindowsFixedSizeDialogHint)

        desktop = QtWidgets.QApplication.desktop()
        size_of_window = QtCore.QSize(800, 550)
        start_point = QtCore.QPoint((desktop.width() - size_of_window.width()) // 2 ,
                                    (desktop.height() - size_of_window.height()) // 2)

        self.resize(200, 170)
        self.move(start_point)
        self.setWindowModality(2)
        self.setWindowTitle('About')


        self.PicLabel = QLabel('')
        self.PicLabel.setPixmap(QtGui.QPixmap('about_logo.png'))
        self.ContactsLabel = QLabel('<b>Contacts:</b>')
        self.ContactsLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.TelegramLink = QLabel('''
        Telegram <a style="background-color: #4b4b4b; color: #f4f6f5; text-decoration: none;
        display: inline-block;" href=https://goo.gl/i84FFV>@aipyth</a><br>
        VK <a style="background-color: #4b4b4b; color: #f4f6f5; text-decoration: none;
        display: inline-block;" href=https://vk.com/python10>python10</a></span>
        <hr>ipython10@gmail.com''')
        self.TelegramLink.setAlignment(QtCore.Qt.AlignHCenter)
        self.TelegramLink.setOpenExternalLinks(True)
        self.CloseButton = QPushButton('Close', self)
        self.CloseButton.setFlat(True)
        self.CloseButton.setShortcut('Esc')
        self.CloseButton.clicked.connect(self.close)

        pal = self.palette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window,
                            QtGui.QColor('#30577c'))
        pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window,
                            QtGui.QColor('#30577c'))
        self.setPalette(pal)

        self.ContactsLabel.setStyleSheet("""QLabel {
        font-family: sans serif;
        font-size: 20px;
        color: #f4f6f5;
        }""")
        self.TelegramLink.setStyleSheet("""QLabel {
        width: 300px;
        font-family: sans serif;
        font-size: 20px;
        color: #05729b;
        border: 10px solid;
        border-color: #b1b5b7;
        background-color: #b1b5b7;
        }""")
        self.CloseButton.setStyleSheet("""QPushButton {
        font-family: "Trebuchet MS", "Lucida Console", monospace;
        font-size: 20px;
        font-weight: bold;
        color: #f4f6f5;
        background-color: #02325f;
        }""")

        AboutLayout = QVBoxLayout()
        AboutLayout.addWidget(self.PicLabel, alignment = QtCore.Qt.AlignHCenter)
        AboutLayout.addWidget(self.ContactsLabel, alignment = QtCore.Qt.AlignHCenter)
        AboutLayout.addWidget(self.TelegramLink, alignment = QtCore.Qt.AlignHCenter)
        AboutLayout.addSpacing(20)
        AboutLayout.addWidget(self.CloseButton, alignment = QtCore.Qt.AlignHCenter)

        self.setLayout(AboutLayout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    about = AboutWindow()
    settings = SettingsWindow()
    window.setWindowIcon(QtGui.QIcon("icon.png"))
    window.show()
    #pdb.set_trace()
    sys.exit(app.exec_())
