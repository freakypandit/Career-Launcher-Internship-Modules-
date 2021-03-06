# -*- coding: utf-8 -*-
"""Module 6 -  Clustering for Diverse portfolio analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d1ngBOeyPOcVzBp9JZiJdx_Va52jTLxe

# Module 6
### Welcome to the Answer notebook for Module 6 !
"""

from google.colab import drive
drive.mount('/content/drive', force_remount= True)

"""---


##Query 6.1 

    Create a table/data frame with the closing prices of 30 different stocks, with 10 from each of the caps
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import glob 
import pandas as pd
import sklearn
import numpy as np

from sklearn.cluster import KMeans
import seaborn as sns
# %matplotlib inline
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (20,8)    #to fix the size of our graph for better visualization.
import seaborn as sn

"""**The first task to perform is to get closing prices for 30 different stocks, 10 from each cap, in a single data frame. I have already cleaned up all the datasets and put them together in a folder data_module_6. We will get this folder from Google Drive.**

**Link : https://drive.google.com/open?id=1fhZUEHiWkmdZeiLQIeYnzRifcS_i_7d5**
"""

os.chdir('drive/My Drive/data_module_6')

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

"""**Now we have all the 30 stock files from our folder, next task would be get closing_prices for each stock, since closing_price is 8th column in each file, we would just get that column from each. A helper function read_8th_col does that job.**"""

def read_8th_col(file):
    return pd.read_csv(file, usecols=[8])

combined_data = pd.concat([read_8th_col(file) for file in all_filenames], axis=1)

combined_data.head()

"""**Now we have closing prices for each of the stock in our dataframe, combined_data. The next task would be rename each of the column head with name of the stock. So that each column represents a new stock.**"""

names=[]
for name in all_filenames:
  names.append(name.split('.')[0])

combined_data.columns = combined_data.columns[:0].tolist() + names

combined_data.head()

"""**We now have a neat and clean dataframe to continue with.**

---


##Query 6.2 

    Calculate average annual percentage return and volatility of all 30 stocks over a theoretical one year period
"""

len(combined_data)

"""**We can see that for each stock we have records for last 494 days(each row represent a different day).  Since we need to calculate the the returns over the last theoratical year, we would get the latest 252  rows from our dataset.**

**252 days : Ideally 1 year in Stock Market.**
"""

yearly_combined_data= combined_data[242:]

yearly_combined_data.info()

"""**We now have the data for last year, we can calculate returns and volatility on it.**

**Mean avg. Return =  daily mean * 252**

**Volatility = std(daily mean) * sqrt(252)**
"""

import math
returns = yearly_combined_data.pct_change().mean() * 252
volatility = yearly_combined_data.pct_change().std() * math.sqrt(252)


returns.columns = ["Returns"]
volatility.columns = ["Variance"]

"""**We now have the annual returns and volatility for each stock, next task would be concatenate them in a single dataframe against stock.**"""

#Concatenating the returns and variances into a single data-frame
ret_vol = pd.concat([returns, volatility], axis = 1).dropna()
ret_vol.columns = ["Returns","Volatility"]

ret_vol.info()

ret_vol

"""---


##Query 6.3 
    
    Cluster the 30 stocks according to their mean annual Volatilities and Returns using K-means clustering. Identify the optimum number of clusters using the Elbow curve method.

**We are going to perform the elbow curve method on our dataframe to find the optimum number of clusters for our K-Means algorithm.**

**We will use inertia and distortion to decides the number of clusters.**

**The point after which the distortion/inertia start decreasing in a linear fashion, tell us the optimum number of clusters.**
"""

from sklearn import metrics 
from scipy.spatial.distance import cdist

"""**The first task is to find out the values for inertia and distortion for clusters in range of 1 to 10.**"""

X =  ret_vol.values #Converting ret_vol into nummpy array
distortions = [] 
inertias = [] 
mapping1 = {} 
mapping2 = {} 
K = range(1,10) 
  
for k in K: 
    #Building and fitting the model 
    kmeanModel = KMeans(n_clusters=k).fit(X) 
    kmeanModel.fit(X)     
      
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 
                      'euclidean'),axis=1)) / X.shape[0]) 
    inertias.append(kmeanModel.inertia_) 
  
    mapping1[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_, 
                 'euclidean'),axis=1)) / X.shape[0] 
    mapping2[k] = kmeanModel.inertia_

"""**Now we will use the dictonaries : mapping1{} and mapping2{} in to find and plot the key-value pairs.**"""

for key,val in mapping1.items(): 
    print(str(key)+' : '+str(val))

fig = plt.figure()
sns.set_style("darkgrid")
# Add a subplot and label for y-axis
ax = fig.add_subplot(111, title='The Elbow Method using Distortion', xlabel= 'Values of K', ylabel='Distortion')
plt.plot(K, distortions, 'kx-') 
plt.legend(['No. of Clusters'])
plt.show()

for key,val in mapping2.items(): 
    print(str(key)+' : '+str(val))

fig = plt.figure()
sns.set_style("darkgrid")
# Add a subplot and label for y-axis
ax = fig.add_subplot(111, title='The Elbow Method using Inertia', xlabel= 'Values of K', ylabel='Inertia')
ax = plt.plot(K, inertias, 'kx-') 
plt.legend(['No. of Clusters'])
plt.plot()

"""**We can analyze the graphs and understand that after point 6 we have a straight line, so 6 is the optimum number of clusters for our data.**

**Thus, Optimum Number of Clusters = 6**

---


##Query 6.4 

    Prepare a separate Data frame to show which stocks belong to the same cluster

**We will first make a copy of our dataframe, find out clusters for each stock, add cluster column to copy of our data, and perform groupby operation.**
"""

kmeans = KMeans(n_clusters = 6).fit(X)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

cluster_data= ret_vol

cluster_data['clusters'] = labels

#Lets analyze the clusters
print(cluster_data.groupby(['clusters']))

cluster_data

"""**We now have our required data to continue plotting a scatterplot, but to add the stock name to each of the data point, we would create another column with the names for a stock.**"""

cluster_data['names']= cluster_data.index

plt.figure()
fig.add_subplot(111, title='Clustering Stocks using Returns and Volatility', ylabel='Volatility', xlabel='Returns')

ax = sns.lmplot('Returns', # Horizontal axis
           'Volatility', # Vertical axis
           data=cluster_data, # Data source
           fit_reg=False, # Don't fix a regression line
           hue= "clusters",
           aspect= 2,
           height= 8
           ) # size and dimension

plt.title('Clustering Stocks using Returns and Volatility')
def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

label_point(cluster_data.Returns, cluster_data.Volatility, cluster_data.names, plt.gca())

"""**We have sucessfully plotted all the stocks in a Returns VS volatility plot and also clustered them.**


---



---


**END.**

**THANKS Career Launcher for giving an opportunity to work on such a wonderful Project.**
"""