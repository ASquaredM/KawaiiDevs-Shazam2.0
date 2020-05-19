import sys

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import sounddevice as sd
from SideWindowClass import SideWindowClass
import UI.UI as UI
from soundModel import SoundData as SD
import database.GetSemelarity as GS
import database.main_features as mf
import imagehash


class ApplicationWindow(UI.Ui_MainWindow):
    def __init__(self, mainWindow):
        super(ApplicationWindow, self).setupUi(mainWindow)

        self.DisableMixer()
        self.Init()
        #print("Sorting Status", self.Similarity_View.isSortingEnabled())

        self.UpBtn_1.clicked.connect(lambda: self.GetTrack(0))
        self.UpBtn_2.clicked.connect(lambda: self.GetTrack(1))

        self.MixerSlider.setTracking(False)
        self.MixerSlider.valueChanged.connect(self.mixTracks)

        self.SearchBtn.clicked.connect(self.Search)
        

    def Init(self):
        self.Btns = [self.UpBtn_1, self.UpBtn_2]
        self.SndUp = [False, False]
        self.Snd1 = SD()
        self.Snd2 = SD()
        self.Snd = [self.Snd1, self.Snd2]

    def DisableMixer(self):
        self.MixerSlider.setEnabled(False)

    def EnableMixer(self):
        self.MixerSlider.setEnabled(True)

    def GetTrack(self, i):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.filePath, self.format = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Load Track",
            "",
            "Sound (*.mp3);;",
            options=QtWidgets.QFileDialog.DontUseNativeDialog,
        )
        print("filepath is >>>>>", self.filePath)
        if self.filePath == "":
            sd.stop()
            self.SndUp[i] = False
            self.UpBtn_1.setChecked(False)
        else:
            self.Snd[i] = SD(self.filePath)
            self.Snd[i].playAudio()
            self.SndUp[i] = True
            self.Btns[i].setChecked(True)
            #self.InsertAtIndex(i, 0, self.Snd[i].sndPath)
            if self.SndUp[0] == self.SndUp[1] == True:
                self.mixTracks()

            SongSimilarName = GS.returnInfo(
                GS.GetSimilerTo(self.Snd[i].sndByte, 44100)[0])

            self.InsertAtIndex(i, 1, SongSimilarName[0])

    def mixTracks(self):
        self.EnableMixer()
        self.Mix = SD.mix(self.Snd[0], self.Snd[1],
                          self.MixerSlider.value() / 100.0)
        #self.Mix.playAudio()

    def InsertAtIndex(self, y, x, Item):
        self.Similarity_View.setItem(y, x, QTableWidgetItem(Item))
        #self.Similarity_View.resizeColumnsToContents()

    def ClearAtIndex(self, y, x, Item):
        self.Similarity_View.setItem(y, x, QTableWidgetItem(""))

    def Search(self):
        Song_Names = []
        Song_SimIdx = []
        index1, index2, Similarity = GS.GetSimilerTo(self.Mix.sndByte, 44100)
        index = [index1, index2]
        firstSongName, hash1Sim, firstfeature1Hash, firstfeature2Hash = GS.returnInfo(
            index[0])
        secondSongName, hash2Sim, secondfeature1Hash, secondfeature2Hash = GS.returnInfo(
            index[1])
        hash1Sim = Similarity[index[0]]
        hash2Sim = Similarity[index[1]]

        Song_Names.append(firstSongName)
        Song_Names.append(secondSongName)
        Song_SimIdx.append((100 - hash1Sim).__str__() + "%")
        Song_SimIdx.append((100 - hash2Sim).__str__() + "%")
        
        for i in range(0, 9, 1):
            if Song_Names[i] != None:
                self.InsertAtIndex(i, 0, Song_Names[i])
                self.InsertAtIndex(i, 1, Song_SimIdx[i])
        """
        self.mainWindow=QtWidgets.QMainWindow()
        self.sideWindow = SideWindowClass(self.mainWindow,self.Mix.sndByte,)
        self.mainWindow.show()
        """


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ApplicationWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
