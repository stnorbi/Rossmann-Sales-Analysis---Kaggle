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
train_data=pd.read_csv(dataPath + "train.csv", parse_dates=True, low_memory=False, index_col='Date')
test_data=pd.read_csv(dataPath + "test.csv", parse_dates=True, low_memory=False, index_col='Date')

#Analys the feature of the data set
print(store_data.head())
print("\n","Demensions of train set:",train_data.shape)

print("\n",train_data.head())

#Get time series elements:
train_data['Year']=train_data.index.year
train_data['Month']=train_data.index.month
train_data['Day']=train_data.index.day
train_data['WeekofYear']=train_data.index.weekofyear

#Calculate the sales / customer amount:
train_data['Sales_per_Cust']=train_data['Sales']/train_data['Customers']
print("\n Description of Sales per Customers:\n",train_data['Sales_per_Cust'].describe())
print("""
    As the description shows the average customer spend amount is 9.5$, however we have days
    when some store is closed. Less than 25% of the customer spend 7.9$ on average and
    more than 75% of them spend 10.9$. The maximum spend amount of a customer on average was
    64.95$ on average.""")




