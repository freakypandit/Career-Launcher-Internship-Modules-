# -*- coding: utf-8 -*-
"""Module 4 - Algo Trading using Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ouA3zu_Dtr_4RhWXYANJlU0npt0f23ft

##Module 4 -

### Solution notebook for module 4
"""

# Run this cell to mount your Google Drive.
from google.colab import drive
drive.mount('/content/drive')

"""---


##Query 4.1

    -- Import the csv file of the stock which contained the Bollinger columns as well.
    Create a new column 'Call' , whose entries are - 
      - 'Buy' if the stock price is below the lower Bollinger band 
      - 'Hold Buy/ Liquidate Short' if the stock price is between the lower and middle Bollinger band 
      - 'Hold Short/ Liquidate Buy' if the stock price is between the middle and upper Bollinger band 
      - 'Short' if the stock price is above the upper Bollinger band
    
    -- Now train a classification model with the 3 bollinger columns and the stock price as inputs and 'Calls' as output. Check the accuracy on a test set. (There are many classifier models to choose from, try each one out and compare the accuracy for each)
    
    -- Import another stock data and create the bollinger columns. Using the already defined model, predict the daily calls for this new stock.
"""

# Commented out IPython magic to ensure Python compatibility.
#imports for our notebook

import numpy as np
import pandas as pd
import sklearn

import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
# %config InlineBackend.figure_format='retina'
plt.rcParams['figure.figsize'] = (20,8)

#load our data
data= pd.read_csv('drive/My Drive/LAXMIMACH.csv')
data.info()

"""**The next task would be to add bollinger bands to this dataframe, we will add 3 bollinger bands, an upper band, a lower band and a moving average as a middle band.**

**Edit 1: I did not save bollinger values with data earlier (saved them in different file), so instead of importing that data , i'll add the column to this file as well.**
"""

#the piece of code here is same as that used earlier to build bollinger bands.
band_dur= 14
no_of_std= 2

rolling_mean = data['Close Price'].rolling(window= band_dur).mean()
rolling_std = data['Close Price'].rolling(window= band_dur).std()

#middle band
data['Rolling_Avg']= rolling_mean

#upper band
data['Upper Band'] = rolling_mean + (rolling_std * no_of_std)

#lower band
data['Lower Band'] = rolling_mean - (rolling_std * no_of_std)

data.describe()

missing_data= data.isnull().sum()/len(data)
missing_data= missing_data[missing_data > 0]

missing_data=missing_data.sort_values()

print(missing_data)

"""**We can see that we added three columns but we have some missing values in these columns. So we need to handle these missing values before further operation.**

**We will remove these rows, as filling these with 0 might result in unwanted outliers.**
"""

#removing all rows with NULL values in any column
data= data.dropna()

#to reset the index back to 0.
data.index -= 13

data.index

"""**The first task is to create a new column 'call', below given code does that.**"""

data['call']= 'Call'

for i in range(0, 480):
  
  #we will use conditional statements to fill values in the new column
  if (data['Close Price'][i] < data['Lower Band'][i]):
    data['call'][i]= 'Buy'
    
  elif (data['Close Price'][i] > data['Lower Band'][i] and data['Close Price'][i] < data['Rolling_Avg'][i]):
    data['call'][i]= 'Hold Buy/ Liquidate Short'
    
  elif (data['Close Price'][i] < data['Upper Band'][i] and data['Close Price'][i] > data['Rolling_Avg'][i]):
    data['call'][i]= 'Hold Short/ Liquidate Buy'
      
  elif (data['Close Price'][i] > data['Upper Band'][i]):
    data['call'][i]= 'Short'
  
  else:
    data['call'][i]= None

"""**Now that we have sucessfully created the call column we can proceed further.**"""

#to check first 5 rows of dataframe.
data.head(5)

#to chek our dataframe
data.info()

"""**The next task is to build a classification model with the 3 bollinger bands and stock price as input and call as output, to do so we would first create a new dataframe which would contain only those columns which are relevent to us for building a classification model.**"""

#data_trade is a new column with all the relevant values.
data_trade = pd.concat([data['Close Price'], data['Rolling_Avg'], data['Lower Band'], data['Upper Band'], data['call']], axis=1)
data_trade.columns = ['Price', 'Rolling Avg', 'Lower Band', 'Upper Band', 'call']

"""**Now that we have created the new dataframe, we would extract our features and label from it, and seperate it in training and testing set.**"""

data_trade.info()

#features for our model.
X = data_trade.iloc[:, 0: 4].values

#our label
y = data_trade.iloc[:, 4: 5].values

#just to check
print("The features are -- \n {0}\n\nThe labels are -- \n {1}".format(data_trade.iloc[:, 0: 4].head(), data_trade.iloc[:, 4:5].head()))

"""**We can see that we have our features and labels, now we can build a model.**"""

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state=0)
classifier.fit(X_train, y_train)

# Fitting naive bayse to the Training set
from sklearn.naive_bayes import GaussianNB
classifier_gauss = GaussianNB()
classifier_gauss.fit(X_train, y_train)

# Fitting support vector classification to the Training set
from sklearn.svm import SVC
classifier_svc = SVC(kernel='linear', random_state=0)
classifier_svc.fit(X_train, y_train)

# Fitting decision tree to Training set
from sklearn.tree import DecisionTreeClassifier
classifier_tree= DecisionTreeClassifier(random_state=0, max_depth=2)
classifier_tree.fit(X_train, y_train)

# Fitting random forest to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier_rf = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
classifier_rf.fit(X_train, y_train)

# Predicting the Test set result for logistic regression
print("The test accuracy for logistic regression is {}".format(classifier.score(X_test, y_test) * 100))

# Predicting the Test set result for naive bayes
print("The test accuracy for naive bayes is {}".format(classifier_gauss.score(X_test, y_test) * 100))

# Predicting the Test set result for support vector machine
print("The test accuracy for support vector classification is {}".format(classifier_svc.score(X_test, y_test) * 100))

# Predicting the Test set result for decision tree
print("The test accuracy for decision tree classifier is {}".format(classifier_tree.score(X_test, y_test) * 100))

# Predicting the Test set result for random forest
print("The test accuracy for random forest classifier is {}".format(classifier_rf.score(X_test, y_test) * 100))

"""**We can see that we are getting the most accuracy on test set for support vector machine, 99% accuracy, thus we can say that support vector classifier is the optimal model here.**

**To understand the mislabelling between classes, we can plot confusion matrices for each of the classifier as well.**
"""

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
mat = confusion_matrix(y_test, classifier.predict(X_test))
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=True)
plt.xlabel('true label')
plt.ylabel('predicted label')

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
mat = confusion_matrix(y_test, classifier_gauss.predict(X_test))
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=True)
plt.xlabel('true label')
plt.ylabel('predicted label')

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
mat = confusion_matrix(y_test, classifier_svc.predict(X_test))
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=True)
plt.xlabel('true label')
plt.ylabel('predicted label')

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
mat = confusion_matrix(y_test, classifier_rf.predict(X_test))
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=True)
plt.xlabel('true label')
plt.ylabel('predicted label')

"""**We can see that support vector classifier infact had the least number of mislabelling, only 1. Thus we can say it is the best performing classifier on our data, and thus we will use this classifier to predict the call for our next data, which is also our next task.**"""

#importing a new data
data_raymond= pd.read_csv('drive/My Drive/RAYMOND.csv')
data_raymond.head()

"""**Once our new data is imported the next task would be to generate bollinger bands for it.**"""

band_dur= 14
no_of_std= 2

rolling_mean = data_raymond['Close Price'].rolling(window= band_dur).mean()
rolling_std = data_raymond['Close Price'].rolling(window= band_dur).std()

data_raymond['Rolling_Avg']= rolling_mean

data_raymond['Upper Band'] = rolling_mean + (rolling_std * no_of_std)
data_raymond['Lower Band'] = rolling_mean - (rolling_std * no_of_std)

#drop all the null values
data_raymond= data_raymond.dropna()

#reset the index to 0
data_raymond.index -= 13

#create a new column named call
data_raymond['call']= None

"""**We will create a new dataframe with only necessary columns.**"""

data_trade_raymond = pd.concat([data_raymond['Close Price'], data_raymond['Rolling_Avg'], 
                                data_raymond['Lower Band'], data_raymond['Upper Band'], data_raymond['call']], axis=1)

data_trade_raymond.columns = ['Price', 'Rolling Avg', 'Lower Band', 'Upper Band', 'call']

data_trade_raymond.head()

#features for our model.
X = data_trade_raymond.iloc[:, 0: 4].values

#our label
y = data_trade_raymond.iloc[:, 4:5].values

#just to check
print("The features are -- \n {0}\n\nThe labels are -- \n {1}".format(data_trade_raymond.iloc[:, 0: 4].head(), data_trade_raymond.iloc[:, 4:5].head()))

#we would use SVC to predict the call
y= classifier_svc.predict(X)

data_trade_raymond['call']= y

data_trade_raymond['call'].unique()

"""---


##Query 4.2 
    
    Now, we'll again utilize classification to make a trade call, and measure the efficiency of our trading algorithm over the past two years. For this assignment , we will use RandomForest classifier.
    
    -- Import the stock data file of your choice
       Define 4 new columns , whose values are: 
        - % change between Open and Close price for the day 
        - % change between Low and High price for the day 
        - 5 day rolling mean of the day to day % change in Close Price 
        - 5 day rolling std of the day to day % change in Close Price

    -- Create a new column 'Action' whose values are: 
        - 1 if next day's price(Close) is greater than present day's. 
        - (-1) if next day's price(Close) is less than present day's. 
                        i.e. Action [ i ] = 1 if Close[ i+1 ] > Close[ i ] 
                        i.e. Action [ i ] = (-1) if Close[ i+1 ] < Close[ i ]

    -- Construct a classification model with the 4 new inputs and 'Action' as target

    -- Check the accuracy of this model , also , plot the net cumulative returns (in %) if we were to follow this algorithmic model

**We will create the four new columns with the code given below.**
"""

data['%change open-close']= (((data['Close Price'] - data['Open Price']) / data['Open Price']) * 100 ).fillna(0)
data['%change high-low']= (((data['High Price'] - data['Low Price']) / data['Low Price']) * 100 ).fillna(0)

data['%Rolling Mean Close'] = data['Close Price'].rolling(window = 5).mean()
data['%Rolling Std Close']  = data['Close Price'].rolling(window  = 5).std()

"""**A new column action will be added to the dataframe.**

**NOTE : Instead of using 'Close Price' for previous day, we will be using 'Prev Close' for a given day, both contain the same values.**
"""

data['Action']= 0

for i in range(0, 480):
  if (data['Close Price'][i] > data['Prev Close'][i]):
    data['Action'][i]= 1
  
  elif (data['Close Price'][i] < data['Prev Close'][i]):
    data['Action'][i]= -1

"""**We have sucessfully filled the column Action with appropriate values, the next step would be to check for missing values, and cleaning our data before treating it against a classifier.**"""

missing_data= data.isnull().sum()/len(data)
missing_data= missing_data[missing_data > 0]

missing_data=missing_data.sort_values()

print(missing_data)

#to tdrop the null values
data= data.dropna()

#to reset the index to 0
data.index -= 4

data.index

data.head(2)

"""**We would create a new dataframe with only relevant colums to build our classifier, as mentined in the query it will be a rando forest classifier.**"""

# input for model
X= data.iloc[:, 19: 23].values

#label 
y= data.iloc[:, 23: ].values

#just to check
print("The features are -- \n {0}\n\nThe labels are -- \n {1}".format(data.iloc[:, 19: 23].head(), data.iloc[:, 23:].head()))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

from sklearn.ensemble import RandomForestClassifier
classifier_rf2 = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
classifier_rf2.fit(X_train, y_train)

print('The accuracy on test data is {}'.format(classifier_rf2.score(X_test, y_test) * 100))

"""**We can see that our classifier is able to predict correctly about 84 % times the outcome for given inputs.**

**The last step is to plot out net commulative returns for the given stock for entire time period.**
"""

# daily return:
data['daily_return'] = data['Close Price'].pct_change()

# calculate cumluative return
data['net_comm_returns'] = np.exp(np.log1p(data['daily_return']).cumsum()) -1

import matplotlib.pyplot as plt
fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111, title='Net Commulative Returns', ylabel='Strategy Returns')
week['comm_returns'].plot(ax=ax1, color='r', lw=1.3, grid= True)