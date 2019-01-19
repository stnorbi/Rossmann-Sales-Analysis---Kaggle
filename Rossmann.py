"""
The current analysis has been prepared for an interview as presentation to a board of team leaders.
The chosen data set was downloaded from the following source:

    https://www.kaggle.com/c/rossmann-store-sales

"""
import pandas as pd
import os

#Extend the output window of IDE
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# Import Data sets
dataPath=os.path.dirname(__file__) + "/Data/"

store_data=pd.read_csv(dataPath + "store.csv")
train_data=pd.read_csv(dataPath + "train.csv")
test_data=pd.read_csv(dataPath + "test.csv")
