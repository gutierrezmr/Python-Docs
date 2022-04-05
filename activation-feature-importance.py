import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import matplotlib.pyplot as plt 


# In[2]:


df = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[3]:


#df = df.iloc[1:]
df.head(2)


# In[4]:


len(df)


# In[5]:


#split balance and trade fields into range categoricals
df['balance_cut'] = pd.cut(df.balance,bins=[0,100,1000,10000,100000,1000000,10000000],labels=['<100','<1000','<10000','<100000','<1000000','<10000000' ])
df['cashbalance_cut'] = pd.cut(df.cashbalance,bins=[0,100,1000,10000,100000,1000000,10000000],labels=['<100','<1000','<10000','<100000','<1000000','<10000000' ])


# In[6]:


df = df.drop(columns=['accountnumber','cashbalance', 'balance'])
df.head(2)


# In[7]:


#need to encode categoricals to ints
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()

# Assigning numerical values and storing in another column

df['traded_bucket'] = pd.to_numeric(df['traded_bucket'])
df['employment_num'] = labelencoder.fit_transform(df['employmentstatus'])
df['income_num'] = labelencoder.fit_transform(df['annualincome'])
df['networth_num'] = labelencoder.fit_transform(df['networth'])
df['objective_num'] = labelencoder.fit_transform(df['investmentobjective'])
df['risk_num'] = labelencoder.fit_transform(df['risktolerance'])
df['time_num'] = labelencoder.fit_transform(df['timehorizon'])
df['liquidity_num'] = labelencoder.fit_transform(df['liquidityneeds'])
df['balance_num'] = labelencoder.fit_transform(df['balance_cut'])
df['cash_num'] = labelencoder.fit_transform(df['cashbalance_cut'])

df.head(2)


# In[9]:


df.traded_bucket.unique()


# In[10]:


len(df)


# In[11]:


#drop all columns that are not categorical ints
df_cat = df.drop(columns=['employmentstatus','annualincome', 'networth', 'investmentobjective',
                              'risktolerance', 'timehorizon', 'liquidityneeds', 'balance_cut', 'cashbalance_cut'])


# In[12]:


df_cat.head(2)


# In[14]:


df_cat.traded_bucket.unique()


# In[15]:


#create test and train split, target var is profit_bucket, last column, can use iloc indexing

import pandas as pd
from sklearn.model_SELECTion import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import datasets

df_cat = df[['employment_num','income_num','networth_num','objective_num'
              ,'risk_num','time_num','liquidity_num','balance_num','cash_num','traded_bucket']]


# In[17]:


df_cat.traded_bucket.unique()


# In[20]:


X_train, X_test, y_train, y_test = train_test_split(df_cat.iloc[:, :-1], df_cat.iloc[:, -1:], test_size = 0.3, random_state=1)

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)
#
# Training / Test Dataframe
#
cols = ['employment_num','income_num','networth_num','objective_num'
              ,'risk_num','time_num','liquidity_num','balance_num','cash_num']
X_train_std = pd.DataFrame(X_train_std, columns=cols)
X_test_std = pd.DataFrame(X_test_std, columns=cols)


# In[21]:


from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(random_state=1)
forest.fit(X_train_std, y_train.values.ravel())


# In[22]:


import numpy as np
importances = forest.feature_importances_

#sort vars in descending order

sorted_indices = np.argsort(importances)[::-1]


# In[23]:


#plot feature importance 
import matplotlib.pyplot as plt
 
plt.title('Feature Importance')
plt.bar(range(X_train.shape[1]), importances[sorted_indices], align='center')
plt.xticks(range(X_train.shape[1]), X_train.columns[sorted_indices], rotation=90)
plt.tight_layout()
plt.show()
