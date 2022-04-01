"""
 

We took a look at this item and here is what we are seeing overall:
  
When forecasting the growth of total users – assuming the proportion of pro vs non-pro users remains constant 
– we don’t seem to hit the magic number that would equate to finding it necessary for the $50,000 license tag 
until at least October 21 given the best possible conditions (ie, the value of the upper confidence interval). 
That key number is an average user count of ~ 163K total users (1.4X increase on the average user count over the 
past 18 months) – of course this could be different if we have a significant swing in the ratio between 
pro vs non-pro users, but LIKE I said, this is assumed to remain constant in the forecast.
  
In addition to this, it seems as the most strongly correlated variable to total user counts are accounts trading:
  
When plotted against each other, we show this:
  
This confirms the correlation matrix findings above. So what? It means that we have another variable that could be measured to determine if the $50,000 licenses make sense. For example:  Total user counts measured -- on average -- to about 74% of accounts trading. Holding all things equal, we can assume that if the number of accounts trading approaches around 230K, we can revisit the $50,000 license purchase again. That 230K sweet spot for accounts trading also is not forecasted until the end of September – assuming the best possible conditions. Also, if finance has monthly trader forecasted already we can also apply that 74% to that as well and get an idea what it’d look LIKE based on those projections.
  
"""
  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import statsmodels.api as sm
import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'
  
df = pd.read_csv('C:\\Users\\Me\\Downloads\\File.csv', low_memory = False, index_col = False)
df.head()
  
corrMatrix = df.corr(method ='kendall')
print (corrMatrix)
  
sns.heatmap(corrMatrix, annot=True)
plt.rcParams["figure.figsize"]= 15,10
plt.rcParams.update({'font.size': 12})
  
df['Month']=pd.to_datetime(df['Month'])
  
types = df.dtypes
print(types)
  
df.head(10)
  
df['Month'].head()
  
df.plot(x='Month', y=['Total Users', 'Accounts Trading'], figsize=(15, 6))
plt.show()
  
df.set_index('Month', inplace=True)
  
df.index
  
#convert to time series:
ts = df['Total Users']
ts.head(20)
  
ts.plot(figsize=(15, 6))
plt.show()
