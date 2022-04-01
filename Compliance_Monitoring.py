
# coding: utf-8

# In[1]:


import pyodbc 
import psycopg2 
import numpy as np 
import getpass 
import pandas as pd  
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn import preprocessing  
import matplotlib.pyplot as plt 
pyodbc.autocommit=True 
conn=pyodbc.connect('HUE', autocommit=True) 
#pd.read_sql('SHOW TABLES IN consume_invest', conn)

#import keyword file from your local machine
kw = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")


#takes keyword file, THEN converts to list to check against complaints

kw = kw['KW'].astype(str).values.tolist()

#lowercases each word in the list
for i in range(len(kw)):
    kw[i] = kw[i].lower()
    
    
#querry from AAP to pull in complaint data
query1 = """
SELECT a.conversationid, latestagentfullname, latestskillname, text, messageid, sentby, time     
From consume_voc.vw_le_msg_int_info  A
LEFT JOIN consume_voc.vw_le_msg_int_msgrecords B
ON A.conversationid=B.conversationid
Where (lower(a.latestskillname) LIKE '%account services wm%'
or lower(a.latestskillname) LIKE '%funding my account wm%'
or lower(a.latestskillname) LIKE '%invest wm%'
or lower(a.latestskillname) LIKE '%managed portfolios wm%'
or lower(a.latestskillname) LIKE '%new account concierge wm%'
or lower(a.latestskillname) LIKE '%options related question wm%'
or lower(a.latestskillname) LIKE '%trading wm%'
)
and source not LIKE 'NULL'
and time >= ADDDATE(TRUNC(NOW(),'DD'), -31)
 
;
"""

"""
Notes for future DB:
Skillnames to be changed to:

Account Services (Invest) to Account Services WM
Funding My Account to Funding My Account WM
Invest to Invest WM
Managed Portfolios to Managed Portfolios WM
New Account Concierge to New Account Concierge WM
Options Related Question to Options Related Question WM
Trading to Trading WM
"""

#Future area: consume_voc.vw_le_msg_int_msgrecords

df = pd.read_sql(sql = query1, con = conn, index_col=None)

#and to_date(time)>='2021-09-01'
#and time >= ADDDATE(TRUNC(NOW(),'DD'), -14);


# In[3]:


df.head(2)


# In[4]:


len(df)


# In[5]:


#takes the complaint text field and converts to string, and lowercases
df["text"] = df["text"].str.lower()


# In[6]:


agent_filter = (df['sentby'] == 'Agent')
df1 = df[agent_filter]


# In[7]:


df1['concat'] = df1['sentby'] + ': ' + df1['text'] + ' -- '
df1 = df1[['conversationid', 'latestagentfullname', 'time', 'concat' ]]


# In[8]:


visitor_filter = (df['sentby'] == 'Consumer')
df2 = df[visitor_filter]


# In[9]:


df2['concat'] = df2['sentby'] + ': ' + df2['text'] + ' -- '
df2 = df2[['conversationid', 'latestagentfullname', 'time', 'concat' ]]


# In[10]:


query = '\\b|\\b'.join(kw)

df2['query_match'] = df2['concat'].str.contains(query, case=False)
df2['word'] = df2['concat'].str.extract( '({})'.format(query) )


# In[11]:


df3 = df1.append(df2 , sort=False)


# In[12]:


df3 = df3.sort_values(['conversationid', 'time'], ascending = [True, True])


# In[13]:


df3.head(2)


# In[14]:


#data df
df4 = df3[['conversationid', 'latestagentfullname', 'time', 'concat' ]]
df4['conversationid'] = df4['conversationid'].astype(str)


# In[15]:


#index flag df
df5 = df3[['conversationid', 'query_match', 'word', 'time' ]]
filt = (df5['query_match'] == True)
df5 = df5[filt]
df5 = df5.drop_duplicates(['conversationid'])
df5['conversationid'] = df5['conversationid'].astype(str)


# In[16]:


# If a cell has an engagementid but a no text, THEN the text will be the same as the engagementid 
#- to handle nulls being treated as a float
df4['concat'] = np.where(df4['concat'].isnull(),df4['conversationid'],df4['concat'])
#df1['concat2'] = df1.groupby(['engagementid'])['concat'].apply(','.join).reset_index()
df6 = df4.groupby(['conversationid', 'latestagentfullname'])['concat'].apply(lambda x: ' '.join(x)).reset_index()


# In[17]:


merge = pd.merge(df5, df6, on= 'conversationid', how='outer')
merge['Manager'] = ""
merge['Case #'] = ""
merge['Case Date'] = ""
#merge['messageid'] = merge['conversationid'].str[8:]


# In[23]:


final = merge.drop_duplicates('conversationid', keep='last')


# In[19]:


final = final.drop(columns=['concat'])


# In[24]:


final.head(2)


# In[21]:


len(final)




#filter the dataframe to just where the rows were found with keywords 
#(Don't run if you want the whole file)
filt = (final['query_match'] == True)
output = final[filt]
output.to_csv("C:\\Users\\Me\\Documents\\File.csv", index = False)


# In[46]:


filt.head()


# In[38]:


#final["concat"]=final["concat"].str.replace(',',';')


# In[39]:


#final.head()


# In[103]:


#df3 = df1.append(df2 , sort=False)


# In[104]:


#df3 = df3.sort_values(['engagementid', 'time'], ascending = [True, True])


# In[105]:


#df4 = df3[['engagementid', 'query_match' , 'word']]
#df4.head()


# In[106]:


# If a cell has an engagementid but a no text, THEN the text will be the same as the engagementid - to handle nulls being treated as a float
#df3['concat'] = np.where(df3['concat'].isnull(),df3['engagementid'],df3['concat'])
#df1['concat2'] = df1.groupby(['engagementid'])['concat'].apply(','.join).reset_index()
#df4 = df3.groupby(['engagementid', 'agentfullname', 'query_match', 'time'])['concat'].apply(lambda x: ' '.join(x)).reset_index()


# In[107]:


#df5 = df4[['engagementid', 'query_match' ]]


# In[44]:


#SELECT certain columns
#df1 = df1[['','']]

#run if you want the output WITHOUT the filter
final.to_csv("C:\\Users\\Me\\Documents\\File.csv", index = False)




