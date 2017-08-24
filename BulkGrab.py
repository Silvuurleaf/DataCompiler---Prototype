from PyQt5.QtWidgets import QFileDialog, QErrorMessage
from glob import glob


"""
    Purpose: User will be prompted with a window asking them to select a directory (folder).
            Once a folder has been selected it will grab all files that follow the filename convention

            FORMAT: TestSample(any characters). csv.
"""

class DataList(object):
    def __init__(self):
        super(DataList, self).__init__()
        self.BulkFileGrab()

    def BulkFileGrab(self):


        #1).#Open directory window and grab path of directory we want to pull data from

        self.path = QFileDialog.getExistingDirectory()
        self.Error = QErrorMessage()

        try:
            if self.path == "":
                self.Error.showMessage("invalid filepath given")
                self.NoneReturn = True
            elif self.path != "":
                #print statements made for debugging purposes.

                print(self.path)
                #2). Grab all csv files following proper name convention

                print(("{}/TestSample*.csv").format(self.path))
                self.filepaths = glob(("{}/TestSample*.csv").format(self.path))
                self.NoneReturn = False
                print(self.filepaths)
            else:
                self.Error.showMessage("Directory not given")
                self.NoneReturn = True


        except Exception as e:
            print(e)

