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

print("="*50,"TRAIN DATA TABLE EXPLORATION","="*80,"\n")
#Analys the feature of the train data set
print("\n","Demensions of train set:",train_data.shape[0])

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
Descriptive Statistics:
    As the description shows the average customer spend amount is 9.5$, however we have days
    when some store is closed. Less than 25% of the customer spend 7.9$ on average and
    more than 75% of them spend 10.9$. The maximum spend amount of a customer on average was
    64.95$ on average.\n""")

#Explore missing values in train data:
nr_closed_stores=len(train_data[(train_data.Open==0) & (train_data.Sales==0)])
rate_closed_stores=round(nr_closed_stores/train_data.shape[0] * 100,2)
nullsl_opened_stores=len(train_data[(train_data.Open !=0) & (train_data.Sales==0)])

print("""
Exploration of missing values in train data:
    We have {0} closed stores in our train data set, which is {1}% of the observations.
    We can also explore such stores which were opened in the reporting period, but their sales was 0.
    The number of opened stores with null sales: {2}
    These stores was opened on working days. Assumption: External factor is behind this.
""".format(nr_closed_stores,rate_closed_stores, nullsl_opened_stores))

#Store data set exploration:
#This table contain additional info about the stores
print("="*50,"STORE DATA TABLE EXPLORATION","="*80,"\n")

print("Head of store table:\n",store_data.head())


#Explore missing values in store data:
print("\nExplore missing values in store data:\n",store_data.isnull().sum())

print("\nDescription of CompetitionDistance of store data:\n",store_data['CompetitionDistance'].describe())

#Explore missing values in CompetitionDistance of Store table:
print("\nExplore missing values in CompetitionDistance of store data:\n",store_data[pd.isnull(store_data.CompetitionDistance)])
print("""
The listed occurances are not following any pattern. They are simply missing from the data set / data base.
In this case we can substitute the NaNs by the median (almost half of the mean) as common practice to impute missing values.
""")

#Impute missing values in CompetitionDistance of Store table:
store_data['CompetitionDistance'].fillna(store_data['CompetitionDistance'].median(), inplace =True)

#Explore missing values in Promo2SinceWeek of Store table:
missv_promo2SW=store_data[pd.isnull(store_data.Promo2SinceWeek)]
print("\nExplore missing values in Promo2SinceWeek of store data:\n",missv_promo2SW.head())
print("""
As there is no Promo2, we do not have information about any further Promo related feature.
At those points where there is no promotion compaign the values change to 0 from NaN.
The same has been done with Competition related information except the CompetitionDistance,
which was already treated.
    """)
store_data.fillna(0,inplace=True) #changing NaNs to 0 in store data

