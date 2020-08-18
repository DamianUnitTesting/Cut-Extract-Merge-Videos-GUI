# -*- coding: utf-8 -*-

################################################################################
## Cut & Merge Videos with MoviePy implementation GUI
##
## Created by: Damian Ledesma - PySide2 and Python 3.8
##
##
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt, QThread, Signal, QRunnable, QThreadPool)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient,QMovie)

from PySide2.QtWidgets import *
import configparser
import sys
import time
import json
import moviepy.editor
from moviepy.editor import *
import os
import math
import platform

class MainThread(QRunnable):
    def __init__(self, parent = None):
        super(MainThread, self).__init__(parent)
        self.signals = WorkerSignals()

    def run(self):
        import cutandmerge
        runThread = cutandmerge.configMovieConcatenate()
        self.signals.finished.emit()

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)


class Ui_ScrollArea(object):
    def setupUi(self, ScrollArea):
        if ScrollArea.objectName():
            ScrollArea.setObjectName(u"ScrollArea")
            
        flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        ScrollArea.setWindowFlags(flags)
        ScrollArea.resize(899, 603)
        ScrollArea.setMaximumSize(QSize(899, 671))
        ScrollArea.setStyleSheet(u"background-color: #2c3e50;")
        ScrollArea.setWidgetResizable(False)
        #ScrollArea.setAlignment(Qt.AlignCenter)

        self.threadpool = QThreadPool()
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 897, 601))
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 901, 81))
        self.label.setStyleSheet(u"background-color: #262b33;")
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 80, 901, 591))

        font = QFont()
        font.setBold(True)
        font.setWeight(75);

        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("QTabWidget>QWidget>QWidget{background: #2f3640;}\n" "QTabBar::tab{background-color: #2f3640;color: white}\n"  "QTabBar::tab:selected{background-color: rgb(29, 29, 29);}\n  QTabBar{qproperty-drawBase: 0;}")         
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tabWidget.setIconSize(QSize(70, 100))
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)

        iconSave = QIcon()
        iconSave.addFile(os.path.join('gpr', 'ButtonSaveIcon.png'), QSize(), QIcon.Normal, QIcon.On)

        PlayButton = QIcon()
        PlayButton.addFile(os.path.join('gpr', 'PlayButton.png'), QSize(), QIcon.Normal, QIcon.On)        

        AddMore = QIcon()
        AddMore.addFile(os.path.join('gpr', 'Addmore.png'), QSize(), QIcon.Normal, QIcon.On)   

        iconMinus = QIcon()
        iconMinus.addFile(os.path.join('gpr', 'RemoveButton.png'), QSize(), QIcon.Normal, QIcon.On)

        icon = QIcon()
        icon.addFile(os.path.join('gpr', 'FolderIcon.png'), QSize(), QIcon.Normal, QIcon.On)

        icon2 = QIcon()
        icon2.addFile(os.path.join('gpr', 'ico2.png'), QSize(), QIcon.Normal, QIcon.On)

        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 0, 251, 231))
        self.label_9.setStyleSheet(u"background-color: #8BC34A;")
        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(270, 0, 541, 231))
        self.label_10.setStyleSheet(u"background-color: #CDDC39;")
        self.label_12 = QLabel(self.tab)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 240, 801, 341))
        self.label_12.setStyleSheet(u"background-color: #222f3e;")

        self.OpenFileFolder = QPushButton(self.tab)
        self.OpenFileFolder.setObjectName(u"OpenFileFolder")
        self.OpenFileFolder.setGeometry(QRect(80, 40, 120, 120))
        self.OpenFileFolder.setStyleSheet(u"border:none;\n" "background-color: rgb(46, 52, 54)\n;" "color:white;")
        self.OpenFileFolder.setIcon(AddMore)
        self.OpenFileFolder.setIconSize(QSize(100, 100))

        self.WidthVideo = QLineEdit(self.tab)
        self.WidthVideo.setObjectName(u"WidthMany")
        self.WidthVideo.setGeometry(QRect(320, 100, 201, 27))
        self.WidthVideo.setStyleSheet(u"border:none;\n" "background-color: white;\n" "color: black;")
        
        self.SaveVideo = QPushButton(self.tab)
        self.SaveVideo.setObjectName(u"SaveMany")
        self.SaveVideo.setGeometry(QRect(550, 40, 141, 141))
        self.SaveVideo.setStyleSheet(u"border:none;\n" "background-color: rgb(46, 52, 54);\n" "color:white")
        self.SaveVideo.setIcon(iconSave)
        self.SaveVideo.setIconSize(QSize(100, 100))

        self.animatedContainer = QLabel(self.tab)
        self.animatedContainer.setObjectName(u"animated")
        self.animatedContainer.setGeometry(QRect(100, 435, 80, 80))
        self.animatedContainer.setScaledContents(False)
        self.animatedContainer.setStyleSheet(u"border:none;\n" "background-color: #222f3e")
        
        self.movieAnimation = QMovie(os.path.join('gpr', 'Loading', 'animation.gif'))
        self.animatedContainer.setMovie(self.movieAnimation)

        self.InfoText = QLineEdit(self.tab)
        self.InfoText.setObjectName(u"InfoText")
        self.InfoText.setGeometry(QRect(470, 480, 300, 27))
        self.InfoText.setStyleSheet(u"background-color: #222f3e;\n" "border:none;\n" "color:white;")
        self.InfoText.setReadOnly(True)

        self.CloseX = QPushButton(self.scrollAreaWidgetContents)
        self.CloseX.setObjectName(u"CloseButtonX")
        self.CloseX.setGeometry(QRect(850, 0, 31, 27))
        self.CloseX.setStyleSheet(u"background-color:2f3640;\n" "color:white;\n" "border:none;")
        self.MinimizedWindow = QPushButton(self.scrollAreaWidgetContents)
        self.MinimizedWindow.setObjectName(u"Minimized Window")
        self.MinimizedWindow.setGeometry(QRect(810, 0, 31, 27))
        self.MinimizedWindow.setStyleSheet(u"background-color:2f3640;\n" "color:white;\n" "border:none;")

        self.MinusButton = QPushButton(self.tab)
        self.MinusButton.setObjectName(u"SaveMany")
        self.MinusButton.setGeometry(QRect(190, 165, 60, 60))
        self.MinusButton.setStyleSheet(u"border:none;\n" "background-color: rgb(46, 52, 54);")
        self.MinusButton.setIcon(iconMinus)
        self.MinusButton.setIconSize(QSize(50, 50))

        self.HeightVideo = QLineEdit(self.tab)
        self.HeightVideo.setObjectName(u"HeightVideo")
        self.HeightVideo.setGeometry(QRect(320, 40, 201, 27))
        self.HeightVideo.setStyleSheet(u"border:none;\n" "background-color: white;\n" "color: black;")

        self.Fps = QLineEdit(self.tab)
        self.Fps.setObjectName(u"FPS")
        self.Fps.setGeometry(QRect(320, 160, 201, 27))
        self.Fps.setStyleSheet(u"border:none;\n" "background-color: white;\n" "color: black;")

        self.OpenFolder = QPushButton(self.tab)
        self.OpenFolder.setObjectName(u"OpenFolder")
        self.OpenFolder.setGeometry(QRect(670, 430, 90, 90))
        self.OpenFolder.setStyleSheet(u"border:none;\n" "background-color: rgb(46, 52, 54);")
        self.OpenFolder.setIcon(icon)
        self.OpenFolder.setIconSize(QSize(80, 80))
        self.OpenFolder.setEnabled(False);
        self.OpenFolder.setVisible(False);

        self.areaTabTable = QTableWidget(self.tab)
        self.areaTabTable.setGeometry(QRect(10, 240, 781, 192))
        self.areaTabTable.setShowGrid(True)
        self.areaTabTable.setColumnCount(2)
        self.areaTabTable.setStyleSheet(u"border:none;\n" "background-color: white;\n" "color: black;")
        self.areaTabTable.setHorizontalHeaderLabels(['Videos', 'Extract Time Range (From-To)'])
        self.areaTabTable.horizontalHeader().resizeSection(0, 380);
        self.areaTabTable.horizontalHeader().resizeSection(1, 380);

        self.StartButton = QPushButton(self.tab)
        self.StartButton.setObjectName(u"StartButton")
        self.StartButton.setGeometry(QRect(360, 435, 91, 81))
        self.StartButton.setStyleSheet(u"border:none;\n" "background-color: rgb(46, 52, 54);")
        self.StartButton.setIcon(PlayButton)
        self.StartButton.setIconSize(QSize(40, 40))

        icon3 = QIcon()
        icon3.addFile(u"gpr\ico4.png", QSize(), QIcon.Normal, QIcon.On)
        self.tabWidget.addTab(self.tab, icon3, "1")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(350, 120, 31, 41))
        self.label_3.setStyleSheet(u"background-color: #2f3640;")
        self.label_3.setPixmap(QPixmap(os.path.join('gpr', 'LogoTopSmall.png')))
        self.label_3.setScaledContents(True)

        icon4 = QIcon()
        icon4.addFile(os.path.join('gpr', 'ico3.png'), QSize(), QIcon.Normal, QIcon.On)

        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(50, 20, 31, 41))
        self.label_11.setStyleSheet(u"background-color: #262b33;")
        self.label_11.setPixmap(QPixmap(os.path.join('gpr', 'LogoTopSmall.png')))
        self.label_11.setScaledContents(True)

        self.Tagline = QLineEdit(self.scrollAreaWidgetContents)
        self.Tagline.setObjectName(u"lineEdit")
        self.Tagline.setGeometry(QRect(660, 50, 200, 27))
        self.Tagline.setStyleSheet(u"background-color: #262b33;\n" "border:none;\n" "color:white;")
        self.Tagline.setReadOnly(True)

        ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.CloseX.pressed.connect(self.CloseProgram)
        self.MinimizedWindow.pressed.connect(self.Minimize)

        self.OpenFileFolder.pressed.connect(self.AppendMovieTimeSheet)
        self.MinusButton.pressed.connect(self.RemoveTable)
        self.StartButton.pressed.connect(self.SaveCSVFile)
        self.SaveVideo.pressed.connect(self.SaveConfigurationVideo)
        self.StartButton.setEnabled(False);
        self.OpenFolder.pressed.connect(self.FolderPath)

        self.retranslateUi(ScrollArea)

        self.tabWidget.setCurrentIndex(2)

        QMetaObject.connectSlotsByName(ScrollArea)


    def FolderPath(self):
        pathOS = os.getcwd()
        if platform.system() == "Windows":
            os.startfile(os.getcwd(pathOS))
        else:
            QMessageBox.information(None, "Successful!", "The file has been saved at " + pathOS)


    def CloseProgram(self):
        app.quit()

    def Minimize(self):
        ScrollArea.setWindowState(Qt.WindowMinimized)

    def Processing(self):
        time.sleep(0.1)
        self.movieAnimation.start()
        self.animatedContainer.setVisible(True)
        self.InfoText.setText("Processing, Grab a Cup of Coffee! ..")
        self.ThreadProcess()
        self.StartButton.setEnabled(False);
        self.OpenFolder.setEnabled(False);
        self.OpenFolder.setVisible(False);

    def ThreadProcess(self):
        threadClass = MainThread()
        time.sleep(0.1)
        self.threadpool.start(threadClass)
        threadClass.signals.finished.connect(self.OnComplete)
        return

    def OnComplete(self):
        self.InfoText.setText("Done!")
        self.movieAnimation.stop()
        self.StartButton.setEnabled(True);
        self.OpenFolder.setEnabled(True);
        self.OpenFolder.setVisible(True);
        self.animatedContainer.setVisible(False)
        return

    def AppendMovieTimeSheet(self):
        global videosFolders
        videosFolders = QFileDialog.getOpenFileName(None, "Select Videos","","*.avi *.mp4 *.mov")
                
        getVideoPath = map(str, videosFolders)
        sanatizePath = 'removeme'.join(getVideoPath)
        splitPath = sanatizePath.split('removeme')
        extractString = map(str,splitPath[0])
        readytoAppendPath = ''.join(extractString)
        
        if readytoAppendPath != "": 
            AppendTimes = "00:00:00-00:00:00"

            rowPosition = self.areaTabTable.rowCount()
            self.areaTabTable.insertRow(rowPosition)            

            self.areaTabTable.setItem(rowPosition,1, QTableWidgetItem(AppendTimes))
            self.areaTabTable.setItem(rowPosition,0, QTableWidgetItem(readytoAppendPath))
            self.StartButton.setEnabled(True);
        else:
            print("Error Missing Data, No videos were Added")


    def RemoveTable(self):
        self.areaTabTable.removeRow(0);
    
    def SaveCSVFile(self):
        import csv
        path = "movies.csv"
        if path != '':
            with open(path, 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.areaTabTable.rowCount()):
                    row_data = []
                    for column in range(self.areaTabTable.columnCount()):
                        item = self.areaTabTable.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
        self.Processing()


    def SaveConfigurationVideo(self):
        from configparser import ConfigParser
        SetFps = self.Fps.text()
        SetWidthVideo = self.WidthVideo.text()
        SetHeightVideo = self.HeightVideo.text()

        if SetFps and SetHeightVideo and SetWidthVideo  != "":

            config = ConfigParser()

            config.add_section('Settings')
            config.set('Settings', 'Height', SetHeightVideo)
            config.set('Settings', 'Width', SetWidthVideo)
            config.set('Settings', 'FPS', SetFps)
            self.InfoText.setText("Saved Configuration!")

            with open('CSettings.cfg', 'w') as configfile:
                config.write(configfile)
                configfile.close()

        else:
            QMessageBox.critical(None, "Mising Fields", "Please Complete All Fields")


    def retranslateUi(self, ScrollArea):
        ScrollArea.setWindowTitle(QCoreApplication.translate("ScrollArea", u"ExtractAndMerge 0.1 Beta", None))
        self.WidthVideo.setPlaceholderText(QCoreApplication.translate("ScrollArea", u"Set Width", None))
        self.HeightVideo.setPlaceholderText(QCoreApplication.translate("ScrollArea", u"Set Height", None))
        self.OpenFileFolder.setToolTip(QCoreApplication.translate("ScrollArea", u"Add a Video", None))
        self.SaveVideo.setToolTip(QCoreApplication.translate("ScrollArea", u"Save Configuration", None))
        self.Fps.setPlaceholderText(QCoreApplication.translate("ScrollArea", u"FPS: 25", None))
        self.label_9.setText("")
        self.label_10.setText("")
        self.label_12.setText("")
        self.OpenFileFolder.setText("")

#if QT_CONFIG(tooltip)
        self.WidthVideo.setToolTip(QCoreApplication.translate("ScrollArea", u"Set Width", None))
#endif // QT_CONFIG(tooltip)
        self.WidthVideo.setText("")
        self.SaveVideo.setText("")
#if QT_CONFIG(tooltip)
        self.HeightVideo.setToolTip(QCoreApplication.translate("ScrollArea", u"Set Height", None))
#endif // QT_CONFIG(tooltip)
        self.HeightVideo.setText("")
#if QT_CONFIG(tooltip)
        self.Fps.setToolTip(QCoreApplication.translate("ScrollArea", u"FPS del Video", None))

#endif // QT_CONFIG(tooltip)
        self.Fps.setText("")
        #self.StartVideo.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "")
        self.CloseX.setText(QCoreApplication.translate("ScrollArea", u"X", None))
        self.MinimizedWindow.setText(QCoreApplication.translate("ScrollArea", u"_", None))
        self.label_11.setText("")
        self.Tagline.setText(QCoreApplication.translate("ScrollArea", u"ExtractAndMerge 0.1 Beta", None))
    # retranslateUi

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    splash_pix = QPixmap('Splashtest.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    ScrollArea = QScrollArea()
    ui = Ui_ScrollArea()
    ui.setupUi(ScrollArea)
    ScrollArea.show()
    splash.finish(ScrollArea)
    sys.exit(app.exec_())
