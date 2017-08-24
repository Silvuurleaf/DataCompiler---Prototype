import pandas as pd

"""
        Purpose" DataClassifier.py works as a blueprint for creating our Data in its specified format
            - the program saves traits such as Entity Type, Tolerance Value, and Nominal Value
            - Program reformats data so it saves the part names and actual values as pandas dataframe
"""

class File_Attributes(object):
    def __init__(self, file):
        super(File_Attributes, self).__init__()
        print("inside File_Attributes")

        #List of EntityTypes grouped together by their shared traits
        self.EntityTypeList1 = ["Surface Profile", "Flatness", "Circularity"]

        self.EntityTypeList2 = ["Linear Dim.", "Angular Dim.", "Radial Dim."]

        self.Data = file

        #Call methods to instantiate data attributes Entity, Tolerance, and Nominal Value
        self.EntityFind()
        self.ToleranceFind()
        self.NominalFind()

        #Calls method to reorganize data
        self.Clean()

    def EntityFind(self):

        ENlist = pd.unique(self.Data['Unnamed: 1'].ravel())     #Creates an array of all the unique values in specified column

        # for loop creates variable Entype and sets it equal the entity type of whatever was measured
        # loop checks every element in the list until it finds something that is not a NaN value or the title string 'Entity Type'

        for i in range(len(ENlist)):
            if ENlist[i] != 'Entity Type' and 'NaN':
                self.EntityType = ENlist[i]

        print("Entity type is {}".format(self.EntityType))

    def ToleranceFind(self):


        print("Tolerance")
        """
            Function works in the same way as EntityFind() except there are two loops depending on the Entity Type of the file.
            
            each group of entity types has a different file format so the column where tolerance is located is different
            so in order find the tolerance we have to run a case by case basis.
        """


        try:
            if self.EntityType in self.EntityTypeList1:     #checks to see if the entity type of the data is in group 1

                ToleranceList = pd.unique(self.Data['Unnamed: 3'].ravel())

                for i in range(len(ToleranceList)):
                    if ToleranceList[i] != 'Tolerance' and 'NaN':
                        self.Tolerance = ToleranceList[i]

                print("                               ")
                print("Tolerance is {}".format(self.Tolerance))

            elif self.EntityType in self.EntityTypeList2:   #checks to see if the entity type of the data is in group 2

                ToleranceList = pd.unique(self.Data['Unnamed: 5'].ravel())


                for i in range(len(ToleranceList)):
                    if ToleranceList[i] != 'Tolerance' and 'NaN':
                        self.Tolerance = ToleranceList[i]

                print("Tolerance is {}".format(self.Tolerance))
            else:
                pass
        except Exception as ToleranceErr:
            print("error found when trying to find Tolerance value of unformatted data..........ERROR:{}".format(ToleranceErr))

    def NominalFind(self):
        """
            Works just like the previous two functions. See EntityFind() for more information

            Since only EntityType2 has nominal values we only have to loop through their list
        """

        if self.EntityType in self.EntityTypeList2:
            NominalList = pd.unique(self.Data['Unnamed: 2'].ravel())

            for i in range(len(NominalList)):
                if NominalList[i] != 'Nominal Value' and 'NaN':
                    self.Nominal = NominalList[i]
            print("                               ")
            print("Nominal Value is {}".format(self.Nominal))

        else:
            self.Nominal = 'NaN'
            print("No Nominal Value Present {}".format(self.Nominal))

    def Clean(self):
        """
            Purpose: Drop any superflous data. The goal is to have just the Actual values and the part names, since we already collected all the other information
        """

        self.Data.dropna(thresh=1, axis=1, inplace=True) #Drops all columns that don't have at least one value that isn't a null value



        self.Data.drop('Name', 1, inplace=True)     # Filter Statistical Information:(USL, LSL, Cp, CPU, etc...) provided by the datasheet


        self.Data.drop('Unnamed: 1', 1, inplace=True)
        self.Data.drop('Unnamed: 4', 1, inplace=True)
        self.Data.drop('Actual Value', 1, inplace=True)
        self.Data.dropna(how='any', inplace=True)


        #We have to run case by case filtration because each EntityList has a different file format
        #In the end all that we should have left are the alpha part names column and the actual value measurements column
        if self.EntityType in self.EntityTypeList1:
            self.Data.drop('Unnamed: 3', 1, inplace=True)

            self.Data.reset_index(inplace=True)
            self.Data.drop([0], inplace=True)
            self.Data.reset_index(inplace=True)
            self.Data.drop('index', 1, inplace=True)        #drop = True
            self.Data.drop('level_0', 1, inplace=True)

            self.Data.rename(columns={'Unnamed: 0': "Name" }, inplace=True)
            self.Data.rename(columns={'Unnamed: 2': "Actual Value"}, inplace=True)



        elif self.EntityType in self.EntityTypeList2:
            self.Data.drop('Unnamed: 2', 1, inplace=True)
            self.Data.drop('Unnamed: 5', 1, inplace=True)

            self.Data.reset_index(inplace=True)
            self.Data.drop([0], inplace=True)
            self.Data.reset_index(inplace=True)
            self.Data.drop('index', 1, inplace=True)
            self.Data.drop('level_0', 1, inplace=True)

            self.Data.rename(columns={'Unnamed: 0': "Name" }, inplace=True)
            self.Data.rename(columns={'Unnamed: 3': "Actual Value"}, inplace=True)

        print(self.Data)

        length = len(self.Data.index)

        print("length of data is {}".format(length))

        length = len(self.Data.index)

        print("length of data is {}".format(length))

        self.CleanData = self.Data

        print("Data has been cleaned and formatted to include only names and measurements")
        print(self.CleanData)





