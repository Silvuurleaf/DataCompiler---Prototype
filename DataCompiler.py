#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Program name - DataCompiler.py
# Written by - Mark Taylor (Taylor26@seattleu.edu)
# Date and version No:  9/15/17

# This is a description of what the program does
# and how its should be used.


import sys
import pandas as pd
import os
import urllib
import json
import BulkGrab
import DataClassifier
import Formatter
import StatsCalc
import Save

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget,QMainWindow)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Data Formatter")

        # Initializes the user interface window
        self.BootUpUI()

    def BootUpUI(self):
        print("widgets will be pulled up when executable is called")

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        #Creating Buttons/Widgets_______________________________________________________________________________________

        self.ImportCompile = QPushButton("Import | Compile")
        self.ImportCompile.clicked.connect(self.FileImport)

        self.EndBtn = QPushButton("Close Window")
        self.EndBtn.clicked.connect(self.CloseFN)

        self.MainLayout = QHBoxLayout(self.main_widget)


        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.ImportCompile)
        self.Vbox.addWidget(self.EndBtn)

        self.MainLayout.addLayout(self.Vbox)

        self.TrendReportList = []

        self.show()
    def CloseFN(self):
        self.close()
    def FileImport(self):
        print("ImportingFile")
        try:
            self.GrabDataWindow = QtWidgets.QFileDialog()

            self.DataLocation = BulkGrab.DataList()         #Creates an object using DataList class in BulkGrab.py
        except Exception as FileLocationErr:
            print("error occured when grabbing file locations....ERROR: {}".format(FileLocationErr))
        print("after DataLocation")

        try:
            if self.DataLocation.NoneReturn == True:
                print("None type is true")
            else:
                self.filesLocations = self.DataLocation.filepaths       #Gathers a list of the file paths of each file that will be merged

                self.FileSearch()
        except Exception as NoneReturnErr:
            print("error occured when trying to return a none-type when cancel is clicked.......ERROR:{}".format(NoneReturnErr))

    def FileSearch(self):
        NumberOfFiles = len(self.filesLocations)

        self.PastTrendReport = pd.DataFrame()    #Variable to store trend reports as we iterate through multiple reports
        """
            For each trend report we create an Object PastTrendReport using the DataClassifier.py file and the class File_Attributes.
            
            The file is opened, read, and then converted to a pandas dataframe. From there the data is classified in the Files_attributes class
            The object is then stored in a list of all the trendreports.
            
            encoding="ISO-8859-1" is so that the program can read incoming CSV. There was one csv file my program couldn't read and this fixed that problem.
        """

        for i in range(NumberOfFiles):
                self.PastTrendReport = DataClassifier.File_Attributes(pd.read_csv(open((self.filesLocations[i]), encoding="ISO-8859-1")))
                self.TrendReportList.append(self.PastTrendReport)

        self.CallFormat(self.TrendReportList)

    def CallFormat(self, TrendReports):
        self.FormattedObject = Formatter.Reformat(TrendReports)     #creates an object from the file Formatter.py and the class Reformat
                                                                    #Object should include actual values and nominal/tolerance measurements in the form of a Pandas Dataframe

        self.DataAndStats = StatsCalc.DataStatistics(self.FormattedObject)          #calls the file StatsCalc.py and the class DataStatistics
                                                                                    #calculates statistical information appends itself to the dataframe

        UnSavedData = self.DataAndStats.CompletedData        #Looks into the object DataAndStats and grabs the CompletedData (Actual Values, Nominal/Tol, and Stats calculations)

        self.CallSave(UnSavedData)

    def CallSave(self, Unsaved):
        Save.FileSave(Unsaved)

        try:
            #Once fil has been saved we clear out the data so if we use the program again it doesn't merge the old file as well
            self.DataAndStats = None
            self.PastTrendReport = None
            self.TrendReportList = []
        except Exception as ClearData:
            print("an error occured while trying to reset the data.........ERROR: {}".format(ClearData))


def main():
    # main loop is run so that the window remains until the user exits the program
    app = QApplication(sys.argv)

    # instance
    window = MainWindow()
    window.show()
    # appWindow = MainWindow()
    sys.exit(app.exec_())


if __name__.endswith('__main__'):
    #== "__main__":
    main()