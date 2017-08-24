
import pandas as pd
import numpy as np

class Reformat(object):
    def __init__(self, CleanData):
        super(Reformat, self).__init__()

        self.DataSet = CleanData

        #Create empty lists to store values
        self.NominalValList = []
        self.ToleranceValList = []
        self.ReformattedData = []

        self.initializingFormat()

    def initializingFormat(self):
        print("Formatting proccess beginning")

        self.TransposedDataList = []     #list to store data once its been transposed
        ActualValues = pd.Series()      #instantiate a series to hold the measurements

        #DataSet is a list of objects that stores the Cleandata from DataClassifier.py
        print(self.DataSet)


        for j in (self.DataSet):
            print("inside j loop")

            self.UnFormattedData = j

            #grab attributes from from the cleandata(unformatted data)
            self.EntityVal = self.UnFormattedData.EntityType
            self.NominalValList.append(self.UnFormattedData.Nominal)
            self.ToleranceValList.append(self.UnFormattedData.Tolerance)

            print(self.UnFormattedData.CleanData)

            for i in range((len(self.UnFormattedData.CleanData.index))): #loops that loops through depending on the length of the index

                print("I value is {}".format(i))

                #Loops through unformatted data and goes through the measurement(actual value) columns and appends the values to our empty Pandas Series
                ActualValues = ActualValues.set_value(i, self.UnFormattedData.CleanData.loc[i, 'Actual Value'])

                ActualValuesDF = pd.DataFrame(ActualValues)                 # Convert ActualValues (Series) to DataFrame

                self.TransposedData = ActualValuesDF.transpose()            # transpose data

            print(self.NominalValList)
            print(self.ToleranceValList)

            self.rename() #Call rename to change column headers

    def rename(self):
        print("inside rename method")

        print(len(self.TransposedDataList))

        for k in range(len(self.TransposedData.columns.values)): #loops through depending on the number of column headers of transposed dataset

            print("VALUE OF k IS {}...........................".format(k))

            self.TransposedData.rename(columns={k: self.UnFormattedData.CleanData.loc[k, 'Name']}, inplace=True) #takes the part names and sets them as the header names

            print(self.TransposedData)

        self.TransposedDataList.append(self.TransposedData)     #appends data to list to so we can pass all the data at once

        self.Combine() #calls combine to concatenate all the data into one sheet

    def Combine(self):
        print("Inside combine")
        self.CombinedData = pd.concat(self.TransposedDataList, axis = 0) #combines all pandas dataframes in the transposed list
        print("Outputting COMBINED DATA here..........")

        self.CombinedData = self.CombinedData.reset_index(drop = True) #resets index and drops old index column
        print(self.CombinedData)

        self.NomTol_Attach() #Call NomTol to attache nominal/tolerance columns to dataframe

    def NomTol_Attach(self):
        print("attaching Nominal and Tolerance to our transposed data")
        print(type(self.NominalValList[0]))
        for i in range(len(self.NominalValList)):
            if self.NominalValList[i] == 'NaN':
                self.NominalValList[i] = np.nan # replace string NaNs with float np.nan value so it can be filtered out later
            else:
                pass
        print(self.NominalValList)

        #turn list -> series -> dataframes

        NominalSeries = pd.Series(self.NominalValList)
        NominalDataFrame = pd.DataFrame(NominalSeries)

        ToleranceSeries = pd.Series(self.ToleranceValList)
        ToleranceDataFrame = pd.DataFrame(ToleranceSeries)

        ToleranceDataFrame.rename(columns={0: "Tolerance"}, inplace= True)
        NominalDataFrame.rename(columns={0: "Nominal Value"}, inplace=True)

        print("finished creating NomTol")

        NomTol = pd.concat([NominalDataFrame, ToleranceDataFrame], axis=1) #combine nominal tolerance values into one dataframe (column-wise)
        print(NomTol)

        self.FormattedData = pd.concat([self.CombinedData, NomTol], axis=1) #combine all our data
