# -*- coding: utf-8 -*-
"""Module 2 - Plotting in Financial Markets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IMDJSN_RWvV31Eo0WeK6Wrwg8MT48qFk

# Module 2
### Welcome to the Answer notebook for Module 2 !
"""

!pip install -U -q pydrive

#this notebook is written in google colab

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth 
from oauth2client.client import GoogleCredentials

# Authenticate and create the PyDrive client.
# This only needs to be done once per notebook.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

csv_link= "https://drive.google.com/open?id=1gf39mkMCsAaD6BfjMVwuEOf5TESv2Y_1"
fluff, id= csv_link.split('=')
print(id)

"""## Query 2.1

    Load the week2.csv file into a dataframe. What is the type of the Date column? Make sure it is of type datetime64. Convert the Date column to the index of the dataframe.
    
    Plot the closing price of each of the days for the entire time frame to get an idea of what the general outlook of the stock is:
    
          -- Look out for drastic changes in this stock, you have the exact date when these took place, try to fetch the news for this day of this stock
          -- This would be helpful if we are to train our model to take NLP inputs.
"""

csv_link= "https://drive.google.com/open?id=1gf39mkMCsAaD6BfjMVwuEOf5TESv2Y_1"
fluff, id= csv_link.split('=')
print(id)

import pandas as pd
downloaded= drive.CreateFile({'id' : id})
downloaded.GetContentFile('week2.csv')

#to import the csv files of stocks and save it as a dataframe 
data= pd.read_csv('week2.csv')

"""**This notebook is written in google Colab thus pydrive authentication is used,  in case of local machine just use    data= pd.read_csv("week2.csv")**"""

# Commented out IPython magic to ensure Python compatibility.
#import libararies

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

#we will be using seaborn and matplotlib for plotting purposes

import seaborn as sns
# %matplotlib inline
plt.rcParams['figure.figsize'] = (20,8)    #to fix the size of our graph for better visualization.
import seaborn as sn

type(data['Date'][1])

"""**We can see that each entry in data["Date"] is of str type, we will convert them to datetime object**"""

data['Date']= pd.to_datetime(data['Date'])

"""**We converted elements data["Date"] Series to datatime64(ns) type to make use of Pandas functionality for dates.**"""

#set_index will make our column as our index.
data.set_index('Date', inplace= True)

"""**Converted the Date column to the index of the dataframe.**"""

data.head(3)

data['Close Price'].head()

"""**Plot the closing price of each of the days for the entire time frame to get an idea of what the general outlook of the stock is.**"""

fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111, title='Close Price wrt Dates', ylabel='Close Price')
data['Close Price'].plot(ax=ax1, color='r', lw=1.3, grid= True)
plt.legend(['Close Price'])

'''
plt.title('Close Price wrt Dates')
sns.set_style("darkgrid")
palette = sns.color_palette("mako_r", 3)
sns.lineplot(x= data.index, y= 'Close Price',  
              hue='year', palette= palette, 
                legend="full", data= data, linewidth='1.4')
'''

"""---


##Query 2.2

    A stem plot is a discrete series plot, ideal for plotting daywise data. It can be plotted using the plt.stem() function.

    Display a stem plot of the daily change in of the stock price in percentage. This column was calculated in module 1 and should be already available in week2.csv. Observe whenever there's a large change.
"""

fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111, title='Daily Pecentage Change', xlabel= 'Date', ylabel='Daily Percentage Change')
ax1= plt.stem(data.index, data["Day_Perc_Change"], 
         linefmt=None, markerfmt=None, basefmt=None)

plt.legend(['Daily Perc. Change'])

"""---


## Query 2.3 

    Plot the daily volumes as well and compare the percentage stem plot to it. Document your analysis of the relationship between volume and daily percentage change.
"""

import matplotlib.patches as mpatches
fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111, title='Volume VS Date', ylabel='Daily Volume')
data['Total Traded Quantity'].plot(ax=ax1, color='g', lw=1.2)
#labs = mpatches.Patch(color='red',alpha=.5, label="Highest Trading Volume")
plt.legend(['Trading Volume'])

'''
plt.title('Daily Trading Volume')
sns.set_style("darkgrid")
palette = sns.color_palette("mako_r", 3)
ax= sns.lineplot(x= data.index, y= 'Total Traded Quantity',  
              hue='year', palette= palette, 
                legend="full", data= data, linewidth='1.4')
'''

'''
color='black'
ax= sns.set_style("darkgrid")
palette= sns.dark_palette(color, n_colors=3, reverse=False, as_cmap=False, input='rgb')
ax1= sns.lineplot(x= data.index, y= 'Total Traded Quantity', hue= 'year',
               palette= palette, legend=None, data= data, linewidth='1.8')

'''
fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111, title='Stem Plot and Volume VS Dates')
data['Total Traded Quantity'].plot(ax=ax1, color='k', lw=1.9, grid= False)

ax1.set_ylim(-70000, 100000)
ax1.tick_params(axis='x')

ax2 = ax1.twinx()

ax1.set_zorder(ax2.get_zorder()+1) # put ax in front of ax2 
ax1.patch.set_visible(False)                       

# instantiate a second axes that shares the same x-axis
ax2= plt.stem(data.index, data["Day_Perc_Change"], linefmt=None, markerfmt=None, basefmt='g-')

"""---


## Query 2.4 

    We had created a Trend column in module 1. We want to see how often each Trend type occurs. This can be seen as a pie chart, with each sector representing the percentage of days each trend occurs. Plot a pie chart for all the 'Trend' to know about relative frequency of each trend. You can use the groupby function with the trend column to group all days with the same trend into a single group before plotting the pie chart. From the grouped data, create a BAR plot of average & median values of the 'Total Traded Quantity' by Trend type.
"""

#new dataframe
group_by_trend= data.groupby([(data['trend'])])

group_by_trend['Total Traded Quantity'].count()

fig1, ax1 = plt.subplots()

cmap = plt.get_cmap('Spectral')
colors = [cmap(i) for i in np.linspace(0, 1, 8)]

labels = 'Among Top Gainers', 'Among Top Losers', 'Bull run',  'Negative', 'Positive', 'Slight Negative', 'Slight Positive', 'Slight or No Change' 

ax1.pie(group_by_trend['Total Traded Quantity'].count(), explode=None, colors= colors, labels= None, autopct='%1.1f%%',
          shadow=False, startangle=0)

ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title("%age occurance of each trend")

fig1.set_label('Trend')
plt.legend(labels)
  
plt.show()

fig = plt.figure()

# Add a subplot and label for y-axis
fig.add_subplot(111, title='Mean', ylabel='Daily Volume',  xlabel='Trends')

plt.bar(labels, group_by_trend['Total Traded Quantity'].mean()[:].values, width= 0.4)
plt.legend(['mean'])

fig = plt.figure()

# Add a subplot and label for y-axis
fig.add_subplot(111, title='Median', ylabel='Daily Volume', xlabel='Trends')

plt.bar(labels, group_by_trend['Total Traded Quantity'].median()[:].values, width= 0.4)
plt.legend(['median'])

"""---


## Query 2.5 
    
    Plot the daily return (percentage) distribution as a histogram.
    Histogram analysis is one of the most fundamental methods of exploratory data analysis. In this case, it'd return a frequency plot of various values of percentage changes .
"""

n_bins= 20
fig = plt.figure()

# Add a subplot and label for y-axis
fig.add_subplot(111, title='Daily Percentage Distribution', ylabel='Frequency', xlabel='Daily Percentage Chnage')

#plt.hist(data['Day_Perc_Change'], bins=n_bins)
sns.distplot(data['Day_Perc_Change'])

"""# Data"""

csv_link= "https://drive.google.com/open?id=1tx5NfRR3qG8PG6nEglSzVzNacrchMF34"
fluff, id= csv_link.split('=')
print(id)

downloaded= drive.CreateFile({'id' : id})
downloaded.GetContentFile('ADANIPOWER.csv')

#to import the csv files of stocks and save it as a dataframe 
data_adani= pd.read_csv('ADANIPOWER.csv')
print("Data sucessfully loaded")

csv_link= "https://drive.google.com/open?id=1Y_MhGNal9M9slGHWvvnb2EaHhsb44l5O"
fluff, id= csv_link.split('=')
print(id)

downloaded= drive.CreateFile({'id' : id})
downloaded.GetContentFile('VOLTAS.csv')

#to import the csv files of stocks and save it as a dataframe 
data_voltas= pd.read_csv('VOLTAS.csv')
print("Data sucessfully loaded")

csv_link= "https://drive.google.com/open?id=1vPWqrKNvRoVh9rMyKkVKavXTAiJB0_vV"
fluff, id= csv_link.split('=')
print(id)

downloaded= drive.CreateFile({'id' : id})
downloaded.GetContentFile('RAYMOND.csv')

#to import the csv files of stocks and save it as a dataframe 
data_raymond= pd.read_csv('RAYMOND.csv')
print("Data sucessfully loaded")

csv_link= "https://drive.google.com/open?id=1P7Q_4GXUd3iZYYeMXAnXFRsOrVt3Nyrx"
fluff, id= csv_link.split('=')
print(id)

downloaded= drive.CreateFile({'id' : id})
downloaded.GetContentFile('IDBI.csv')

#to import the csv files of stocks and save it as a dataframe 
data_idbi= pd.read_csv('IDBI.csv')
print("Data sucessfully loaded")

csv_link= "https://drive.google.com/open?id=1nZq75F4WqSY1U2ZnI5DTXZqnDO0wQpGx"
fluff, id= csv_link.split('=')
print(id)

downloaded= drive.CreateFile({'id' : id})
downloaded.GetContentFile('Nifty50.csv')

#to import the csv files of stocks and save it as a dataframe 
data_Nifty50= pd.read_csv('Nifty50.csv')
print("Data sucessfully loaded")

data_corr= pd.DataFrame(columns= ['data Laxmi', 'data_Adani', 'data_Raymond', 'data_Voltas', 'data_idbi', 'data_Nifty50'])

data_corr['data_Laxmi']= data['Close Price']
data_corr['data_Adani']= data_adani['Close Price']
data_corr['data_Raymond']= data_raymond['Close Price']
data_corr['data_Voltas']= data_voltas['Close Price']
data_corr['data_idbi']= data_idbi['Close Price']
data_corr['data_Nifty50']= data_Nifty50['Close']

data_corr.head()

data_corr.describe()

data_corr_change= (data_corr.pct_change() * 100).fillna(0)

data_corr_change.describe()

sns.pairplot(data_corr_change)

"""---


## Query 2.8
    
    Calculate the volatility for the Nifty index and compare the 2. This leads us to a useful indicator known as 'Beta' ( We'll be covering this in length in Module 3)
"""

data_corr_change['MA_7_Laxmi']= data_corr_change['data_Laxmi'].rolling(window= 7).std() *   np.sqrt(7)
data_corr_change['MA_7_Nifty']= data_corr_change['data_Nifty50'].rolling(window= 7).std() * np.sqrt(7)
data_corr_change['MA_7_Voltas']= data_corr_change['data_Voltas'].rolling(window= 7).std() * np.sqrt(7)

data.describe()

plt.figure(figsize=(20, 8))
ax1= plt.plot(data_corr_change['MA_7_Nifty'], label='Nifty 50', lw= 2)
ax2= plt.plot(data_corr_change['MA_7_Laxmi'], label='Laxmi', lw=1)
ax3= plt.plot(data_corr_change['MA_7_Voltas'], label='Voltas', lw=1)
plt.legend(loc=1)

"""---


## Query 2.9 

    Trade Calls - Using Simple Moving Averages. Study about moving averages here. 
 
    Plot the 21 day and 34 day Moving average with the average price and decide a Call ! 
    Call should be buy whenever the smaller moving average (21) crosses over longer moving average (34) AND the call should be sell whenever smaller moving average crosses under longer moving average. 
    One of the most widely used technical indicators.
"""

# Initialize the short and long windows
short_window = 21
long_window = 34

# Initialize the `signals` DataFrame with the `signal` column
signals = pd.DataFrame(index= data.index)
signals['signal'] = 0.0

# Create short simple moving average over the short window
signals['short_mavg'] = data['Close Price'].rolling(window=short_window, min_periods=1, center=False).mean()

# Create long simple moving average over the long window
signals['long_mavg'] = data['Close Price'].rolling(window=long_window, min_periods=1, center=False).mean()

# Create signals
signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
                                            > signals['long_mavg'][short_window:], 1.0, 0.0)   

# Generate trading orders
signals['positions'] = signals['signal'].diff()

# Initialize the plot figure
fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111,  ylabel='Price in Rupees')

# Plot the closing price
data['Close Price'].plot(ax=ax1, color='r', lw=1.4)

# Plot the short and long moving averages
signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=1)

# Plot the buy signals
ax1.plot(signals.loc[signals.positions == 1.0].index, 
         signals.short_mavg[signals.positions == 1.0],
         '^', markersize=8, color='g')
         
# Plot the sell signals
ax1.plot(signals.loc[signals.positions == -1.0].index, 
         signals.short_mavg[signals.positions == -1.0],
         'v', markersize=8, color='k')
         
# Show the plot
plt.show()

"""---


## Query 2.10 

    Trade Calls - Using Bollinger Bands 
    Plot the bollinger bands for this stock - the duration of 14 days and 2 standard deviations away from the average 
    The bollinger bands comprise the following data points- 
    
    -- The 14 day rolling mean of the closing price (we call it the average) 
    -- Upper band which is the rolling mean + 2 standard deviations away from the average. 
    -- Lower band which is the rolling mean - 2 standard deviations away from the average. 
    -- Average Daily stock price.
    
    Bollinger bands are extremely reliable , with a 95% accuracy at 2 standard deviations , and especially useful in sideways moving market. 
    Observe the bands yourself , and analyse the accuracy of all the trade signals provided by the bollinger bands. 
    Save to a new csv file.
"""

band_dur= 14
no_of_std= 2

bollinger_data = pd.DataFrame(index= data.index)

rolling_mean = data['Close Price'].rolling(window= band_dur).mean()
rolling_std = data['Close Price'].rolling(window= band_dur).std()

bollinger_data['Rolling_Avg']= rolling_mean

bollinger_data['High'] = rolling_mean + (rolling_std * no_of_std)
bollinger_data['Low'] = rolling_mean - (rolling_std * no_of_std) 

bollinger_data['avg'] = data['Average Price']

bollinger_data= bollinger_data.dropna(0)

fig = plt.figure()
f
# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111)

# Plot the closing price
data['Average Price'].plot(ax=ax1, color='k', lw=1.7)

# Plot the short and long moving averages
bollinger_data[['High', 'Low', 'Rolling_Avg']].plot(ax=ax1, lw=1)