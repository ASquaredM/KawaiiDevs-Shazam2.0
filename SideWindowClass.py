from PyQt5 import QtCore, QtGui, QtWidgets
import UI.SideWindow as UI
import sys
import database.GetSemelarity as GS 


class SideWindowClass(UI.Ui_MainWindow):
    def __init__(self,mainWindow,Song,sr):
        super(SideWindowClass,self).setupUi(mainWindow)
        index1,index2,Similarity=GS.GetSimilerTo(Song,sr)
        firstSongName,hash1Sim,firstfeature1Hash,firstfeature2Hash=GS.returnInfo(index1)
        secondSongName,hash2Sim,secondfeature1Hash,secondfeature2Hash=GS.returnInfo(index2)
        hash1Sim=Similarity[index1]
        hash2Sim=Similarity[index2]
        self.SongName.setText(firstSongName)
        self.SongName_2.setText(secondSongName)
        self.SongSimilarity.setText((100-hash1Sim).__str__()+"%")
        self.SongSimilarity_2.setText((100-hash2Sim).__str__()+"%")

        self.Song1Name.setText(firstSongName)
        self.SecondSongName.setText(secondSongName)
        self.Feature1_1.setText(firstfeature1Hash)
        self.Feature2_1.setText(firstfeature2Hash)
        self.Feature1_2.setText(secondfeature1Hash)
        self.Feature2_2.setText(secondfeature2Hash)