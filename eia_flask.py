
# coding: utf-8

# In[1]:


# # Update a document
# db.usage.update_one(
#     {'name': 'Farley'},
#     {'$set':
#         {'row': 4}
#      }
# )

# # Add an item to a document array
# db.usage.update_one(
#     {'name': 'Farley'},
#     {'$push':
#         {'hobbies': 'Listening to country music'}
#      }
# )

# # Delete a field from a document
# db.usage.update_one({'name': 'Farley'},
#                         {'$unset':
#                          {'gavecandy': ""}
#                          }
#                         )


# # Delete a document from a collection
# db.usage.delete_one(
#     {'name': 'Farley'}
# )


eia_data={}
# Dependencies
import matplotlib.pyplot as plt
#%matplotlib inline 
from matplotlib.pyplot import rcParams
rcParams['figure.figsize']=10,6
import numpy as np
import pandas as pd
import requests
from config import api_key
import eia
import datetime
import re
from sqlalchemy import create_engine
from datetime import datetime
import statsmodels.api as sm


# In[2]:


# test if api_key variable works
# (remove this line output when making public)
#api_key


# In[3]:


# save variable to call in api data w/ key
api = eia.API(api_key)


# In[4]:


# save all relevant api endings as an iterable object
series = ['TOTAL.TEICBUS.M','TOTAL.TERCBUS.M','TOTAL.TEACBUS.M','TOTAL.TXCCBUS.M','TOTAL.TXEIBUS.M','TOTAL.TXICBUS.M','TOTAL.TXRCBUS.M','TOTAL.TXACBUS.M','TOTAL.TETCBUS.M']


# In[5]:


# test one api ending; import to pandas dataframe
test_import = api.data_by_series(series='TOTAL.TECCBUS.M')
eia_df = pd.DataFrame(test_import)
#eia_df.head()


# In[6]:


# iterate through api endings and save to above dataframe
for x in series:
    series_search = api.data_by_series(series=x)
    df = pd.DataFrame(series_search)
    eia_df = eia_df.join(df, how="outer")


# In[7]:


# print all data in df
#eia_df.tail()


# In[8]:


# create numeric index (unique identifier)
eia_df = eia_df.reset_index()
eia_df = eia_df.rename(columns={"index":"Time"})
#eia_df.head()


# In[9]:


# scatter plot of total US consumption by month

plt.figure(figsize=(20,10))
plt.title("Total US Primary Energy Consumption Since 1973")
plt.xlabel("Time")
plt.ylabel("Energy Consumption in Trillion British Thermal Units(BTU)")
plt.xticks(rotation=45)
plt.scatter(eia_df['Time'], eia_df['Total Primary Energy Consumption, Monthly (Trillion Btu)'], )


# In[10]:


# new dataframe with just datestamp and total usage. Adjust here to test of different datasets.
total_monthly_df = eia_df[["Time", "Total Primary Energy Consumption, Monthly (Trillion Btu)"]]


# time column still needs to be converted to datetime for time series analysis


# In[11]:


# create object for existing timestamp column and an empty list for converted timestamp
timestamp = total_monthly_df["Time"]
datetime_list = []


# In[12]:


# fill empty list with dates converted to datetime
for i in timestamp:
    i = i.replace(" ", "-")
    i = i + "01"
    i = pd.to_datetime(i, infer_datetime_format = True)
    datetime_list.append(i)


# In[13]:


# convert to array so it can be added to pandas df
datetime_array = np.asarray(datetime_list)


# In[14]:


# add datetime array to total consumption df
total_monthly_df['Date'] = datetime_array


# In[15]:


raw_df = total_monthly_df[["Date", "Total Primary Energy Consumption, Monthly (Trillion Btu)"]]
raw_df = raw_df.set_index("Date")
#raw_df.head()


# ## Start Time Series Testing Here

# In[16]:


raw_df.plot()


# In[17]:


import plotly
from plotly.plotly import plot_mpl
plotly.tools.set_credentials_file(username='disco_nap', api_key='MHGkYkGLiSjaQMb13IuC')
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(raw_df, model='multiplicative')
fig = result.plot()
plot_mpl(fig)


# In[18]:


from pyramid.arima import auto_arima
stepwise_model = auto_arima(raw_df, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
#print(stepwise_model.aic())


# In[19]:


#print(stepwise_model)


# In[20]:


# SARIMAX= Seasonal AutoRegressive Integrated Moving Average with eXogenous regressors model
# To me it looks like the whole AR and MA is built in using SARIMAX. Maybe our original way 
# was just a super round about way
model=sm.tsa.statespace.SARIMAX(raw_df["Total Primary Energy Consumption, Monthly (Trillion Btu)"],order=(1,1,1), seasonal_order=(2,1,1,12))
results=model.fit()


# In[28]:


# this is predicting the data based on our test data 
raw_df["Forecast"]=results.predict(start=450, end=549, dynamic=True)
raw_df[["Total Primary Energy Consumption, Monthly (Trillion Btu)", "Forecast"]].plot(figsize=(30,8))


# In[29]:


# this is predicting the data based on our test data 
raw_df["Forecast"]=results.predict(start=450, end=549, dynamic=True)
raw_df[["Total Primary Energy Consumption, Monthly (Trillion Btu)", "Forecast"]][450:].plot(figsize=(30,8))


# In[36]:


# 48 refers to how many months you will predict into the future
from pandas.tseries.offsets import DateOffset
future_dates=[raw_df.index[-1]+DateOffset(months=x) for x in range (0,1000)]


# In[37]:


futures_datest_df=pd.DataFrame(index=future_dates[1:], columns=raw_df.columns)


# In[38]:


#futures_datest_df.tail()


# In[39]:


future_df=pd.concat([raw_df, futures_datest_df])


# In[41]:


# this chart below is projecting into the future. The start value is when you start predicting.
# 549 is the length of our data so I am predicting 151 months out. This number is easily adjusted but you have to adjust the number above (currently 48)
future_df["Forecast"]=results.predict(start= 549, end= 1000, dynamic=True)
future_df[["Total Primary Energy Consumption, Monthly (Trillion Btu)", "Forecast"]].plot(figsize=(30,8))


# In[27]:


# this is the dataframe that shows actual numeric forecasted values. 
#future_df.tail()


# In[42]:


date_input = '2022-04-01'
future_df["Forecast"].loc[future_df.index == date_input][0]

eia_data["Date"]=future_df.index[0]
eia_data["Forecast"]=future_df["Forecast"]


# Module used to connect Python with MongoDb
import pymongo

# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define the 'eiaDB' database in Mongo
db = client.eiaDB

# Query all students
# Here, db.students refers to the collection 'classroom '
usage = db.usage.find()

# Iterate through each student in the collection
#for student in usage:
#    print(student)
pre_json_df = future_df[["Forecast"]]
pre_json_df = pre_json_df.dropna()


string_time = []

for i in pre_json_df.index:
    string = str(i)
    date_str = string[:10]
    string_time.append(date_str)

predsList = list(pre_json_df['Forecast'])
predictions = []

for q in predsList:
    string2 = str(q)
    predictions.append(string2)


# Insert a document into the 'students' collection
db.usage.insert(
{
        'Date': string_time,
        'Forecast': predictions
    }
)
