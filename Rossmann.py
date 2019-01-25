"""
The chosen data set was downloaded from the following source:

    https://www.kaggle.com/c/rossmann-store-sales

"""
import os
import warnings

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seab
import xlsxwriter
import numpy as np

# warnings.filterwarnings("ignore")


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
    NOTE: THE CLOSED STORES WILL BE REMOVED FROM THE FURTHER ANALYSIS, NOT DESTORTING IT.
""".format(nr_closed_stores,rate_closed_stores, nullsl_opened_stores))

train_data=train_data[(train_data["Open"] != 0) & (train_data['Sales'] != 0)]

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

print("="*50,"SET TOGETHER THE TEST DATA WITH ADDITIONAL STORE DETAILS","="*80,"\n")

print("""
As in SQL practice joining tables is more handy and in the environment pandas package also
allows inner join to put together the necessary data sets.
""")
joinData=pd.merge(train_data,store_data, how='inner', on='Store')
print(joinData.shape)
print(joinData.head())

print("="*60,"STORE TYPE ANALYSIS","="*110,"\n")

print("Description of Sales by Store Category:\n",joinData.groupby('StoreType')['Sales'].describe())
print("""
    AS we see in the description, "b" store type is the chempion based on average sale,
    while its coverage is the smallest.
""")

print("\nSale and Attendance description:\n",joinData.groupby('StoreType')['Customers','Sales'].sum())

#Sale time series by Store Category and Promo
seab.catplot(data = joinData, x = 'Month', y = "Sales",
               col = 'StoreType', # per store type in cols
               palette = 'plasma',
               hue = 'StoreType',
               row = 'Promo', # per promo in the store in rows
               kind='point').savefig("Figure_1.png")

print("""
Figure 1:
As we see the difference in scale was coming from the effect of the first promotion.
""")

#Sale time series by Customer
seab.catplot(data = joinData, x = 'Month', y = "Sales_per_Cust",
               col = 'StoreType', # per store type in cols
               palette = 'plasma',
               hue = 'StoreType',
               row = 'Promo', # per promo in the store in rows
               kind="point").savefig("Figure_2.png")

print("""
Figure 2:
Based on the previous results it was seeming the B category stores are the most competitive, but
taking into account the spent money of a customer category D is the winner.
Category D has around 12$ with promotion and without 10$.
The stage of category B is coming from the customer behaviours. Its customers buy cheap things or
small quantities.
""")

#Customer trends by weekday
seab.catplot(data = joinData, x = 'Month', y = "Sales",
               col = 'DayOfWeek', # per store type in cols
               palette = 'plasma',
               hue = 'StoreType',
               row = 'StoreType', # per store type in rows
               kind = "point").savefig("Figure_3.png")
print("""
Figure 3:
In the current plot shows stores of category C are not opened on Sunday.
A strange / interesting aspect: stores of category D are closed on Sunday from October to December
""")

#Stores opened on Sunday
print("\nSunday opened stores:\n",joinData[(joinData.Open == 1) & (joinData.DayOfWeek == 7)]['Store'].unique())

# monthly open of competition
joinData['CompetitionOpen'] = 12 * (joinData.Year - joinData.CompetitionOpenSinceYear) + \
                                 (joinData.Month - joinData.CompetitionOpenSinceMonth)

# Promo opens
joinData['PromoOpen'] = 12 * (joinData.Year - joinData.Promo2SinceYear) + \
                           (joinData.WeekofYear - joinData.Promo2SinceWeek) / 4.0

# replace NA's by 0
joinData.fillna(0, inplace=True)

# average PromoOpen time and CompetitionOpen time per store type
print("\nAverage PromoOpen time and CompetitionOpen time per store type:\n",\
      joinData.loc[:, ['StoreType', 'Sales', 'Customers', 'PromoOpen', 'CompetitionOpen']].groupby('StoreType').mean(),\
      "\nWhile store type 'A' is the most crowded, it is not in danger because of competitors. Category B has \n"
      "the most extensive competition on store average. B also runs the longest period of promotion.\n"
      )

#save result into excel sheet:
# writer=pd.ExcelWriter("Rossmann_Final.xlsx")
# joinData.to_excel(writer,'Sheet1',engine='xlsxwriter')
# writer.save()


print("="*60,"CORRELATION ANALYSIS","="*110,"\n")

#Correlation matrix without taking into acount "Opene":
correlation_matrix=joinData.drop('Open',axis=1).corr()
print("Correlation Matrix:\n",correlation_matrix)

# Taking the half of the correlation matrix
triangle=np.zeros_like(correlation_matrix, dtype=np.bool)
triangle[np.triu_indices_from(triangle)]=True

#Plot the heatmap of correlation matrix
f, ax=plt.subplots(figsize=(11,9))

seab.heatmap(correlation_matrix,mask=triangle, square=True, linewidths= 0.7, ax=ax, cmap="Greens")
print("""
Figure 4:
In the heatmap of the correlation we can focuse on the relation of the Promo compaigns and the
number of customers. As it is seen the performance of the first promo compaign was better than
the second one, because the correlation between the first compaign and the sale per customer is
positive (More than 0.5). The relation between the first compaign and number of customers makes
this fact more obvious by a strong correlation (about 0.8). 
An other fact is the compaigns are getting weaker day by day within a week (The correlation is negative
between DayOfWeek and the promotion in the stores.
""")
plt.savefig("Figure_4.png")


# Customer trends by Promotion
seab.catplot(data = joinData, x = 'DayOfWeek', y = "Sales",
               col = 'Promo',
               row = 'Promo2',
               hue = 'Promo2',
               palette = 'RdBu',
               kind='point').savefig("Figure_5.png")

print("""
Figure 5:
AS deeper analysis of the German Rossmann promotion campaigns it can be said Sunday has peek
without any promotion (NOTE: CATEGORY C IS CLOSED ON SUNDAYS).
Ultimately, the first campaign brought the most revenue on Mondays with intensive reduction in
the rest of the weeks.
The second (Promo2) campaign played the weakest role, because it did not bring so much in respect
to the first campaign.
The two campaign together performed almost as the first campaign individually. It means the first 
campaign supported the performance of Promo2.
""")