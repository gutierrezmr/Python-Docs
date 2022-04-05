
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import matplotlib.pyplot as plt 


# In[3]:


df = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")



# In[4]:


#df = df.iloc[1:]
df.head(2)


# In[5]:


len(df)


# In[6]:


#split balance and trade fields into range categoricals
df['balance_cut'] = pd.cut(df.balance,bins=[0,100,1000,10000,100000,1000000,10000000],labels=['<100','<1000','<10000','<100000','<1000000','<10000000' ])
df['cashbalance_cut'] = pd.cut(df.cashbalance,bins=[0,100,1000,10000,100000,1000000,10000000],labels=['<100','<1000','<10000','<100000','<1000000','<10000000' ])
df['trade_cut'] = pd.cut(df.trades,bins=[0,100,200,500,1000],labels=['<100','<200','<500','<1000'])
df['equity_cut'] = pd.cut(df.equity_trades,bins=[0,10,20,50,100],labels=['<10','<20','<50','<100'])
df['option_cut'] = pd.cut(df.option_trades,bins=[0,10,20,50,100],labels=['<10','<20','<50','<100'])


# In[7]:


df = df.drop(columns=['trades','equity_trades','option_trades','accountnumber', 'firstfundeddate', 'cashbalance', 'balance', 'still_funded_flag'])
df.head(2)


# In[8]:


#need to encode categoricals to ints
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()

# Assigning numerical values and storing in another column

df['profit_bucket'] = pd.to_numeric(df['profit_bucket'])
df['employment_num'] = labelencoder.fit_transform(df['employmentstatus'])
df['income_num'] = labelencoder.fit_transform(df['annualincome'])
df['networth_num'] = labelencoder.fit_transform(df['networth'])
df['objective_num'] = labelencoder.fit_transform(df['investmentobjective'])
df['risk_num'] = labelencoder.fit_transform(df['risktolerance'])
df['time_num'] = labelencoder.fit_transform(df['timehorizon'])
df['liquidity_num'] = labelencoder.fit_transform(df['liquidityneeds'])
df['balance_num'] = labelencoder.fit_transform(df['balance_cut'])
df['cash_num'] = labelencoder.fit_transform(df['cashbalance_cut'])
df['trade_num'] = labelencoder.fit_transform(df['trade_cut'])
df['equity_num'] = labelencoder.fit_transform(df['equity_cut'])
df['option_num'] = labelencoder.fit_transform(df['option_cut'])


df.head(2)


# In[9]:


df.profit_bucket.unique()


# In[10]:


len(df)


# In[11]:


#drop all columns that are not categorical ints
df_cat = df.drop(columns=['employmentstatus','annualincome', 'networth', 'investmentobjective',
                              'risktolerance', 'timehorizon', 'liquidityneeds'
                          , 'balance_cut', 'cashbalance_cut',
                          'trade_cut','option_cut', 'equity_cut'])


# In[12]:


df_cat.head(2)


# In[42]:


df_cat.employment_num.unique()


# In[14]:


#create test and train split, target var is profit_bucket, last column, can use iloc indexing

import pandas as pd
from sklearn.model_SELECTion import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import datasets

df_cat = df[['employment_num','income_num','networth_num','objective_num'
              ,'risk_num','time_num','liquidity_num','balance_num','cash_num','trade_num',
             'option_num','equity_num','profit_bucket']]

#leave out option and equity and take out trade


# In[15]:


df_cat.profit_bucket.unique()


# In[16]:


X_train, X_test, y_train, y_test = train_test_split(df_cat.iloc[:, :-1], df_cat.iloc[:, -1:], test_size = 0.3, random_state=1)

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)
#
# Training / Test Dataframe
#
cols = ['employment_num','income_num','networth_num','objective_num'
              ,'risk_num','time_num','liquidity_num','balance_num','cash_num','trade_num','option_num','equity_num']
X_train_std = pd.DataFrame(X_train_std, columns=cols)
X_test_std = pd.DataFrame(X_test_std, columns=cols)


# In[ ]:


#bring in new unfiltered data to new test set


# In[17]:


from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(random_state=1)
forest.fit(X_train_std, y_train.values.ravel())


# In[18]:


import numpy as np
importances = forest.feature_importances_

#sort vars in descending order

sorted_indices = np.argsort(importances)[::-1]


# In[19]:


#plot feature importance 
import matplotlib.pyplot as plt
 
plt.title('Feature Importance')
plt.bar(range(X_train.shape[1]), importances[sorted_indices], align='center')
plt.xticks(range(X_train.shape[1]), X_train.columns[sorted_indices], rotation=90)
plt.tight_layout()
plt.show()
