import pandas as pd


# In[3]:


df = pd.read_csv('C:\\Users\\Me\\Documents\\File.csv', low_memory = False, index_col = False)


# In[4]:


df.head()


# In[25]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


# In[48]:


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['prior_cases'])
ax1.set_title("Prior Cases by Month")

ax2.plot(df['call_month'], df['n_a'])
ax2.set_title("NA by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]=20,5


# In[38]:


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['ach_expedite'])
ax1.set_title("ACH Expedite by Month")

ax2.plot(df['call_month'], df['ach_transfer'])
ax2.set_title("ACH Transfer by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]= 20,5


# In[29]:


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['address_verification'])
ax1.set_title("Address Verification by Month")

ax2.plot(df['call_month'], df['check_stop_payment'])
ax2.set_title("Check Stop by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]= 20,5


# In[30]:


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['check_withdrawal'])
ax1.set_title("Check Withdrawal by Month")

ax2.plot(df['call_month'], df['close_account'])
ax2.set_title("Close Account by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]= 20,5


# In[31]:


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['drip_request'])
ax1.set_title("Drip Request by Month")

ax2.plot(df['call_month'], df['form_request'])
ax2.set_title("Form Request by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]= 20,5


# In[32]:



fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['phone_number_update'])
ax1.set_title("Phone Number Update by Month")

ax2.plot(df['call_month'], df['promotions_inquiry'])
ax2.set_title("Promotions Inquiry by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]= 20,5


# In[33]:




fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['refund_request'])
ax1.set_title("Refund Request by Month")

ax2.plot(df['call_month'], df['statement_request'])
ax2.set_title("Statement Request by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]= 20,5


# In[34]:


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['tax_doc_issue'])
ax1.set_title("Tax Doc Issue by Month")

ax2.plot(df['call_month'], df['trade_ticket'])
ax2.set_title("Trade Ticket by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]= 20,5


# In[35]:


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(df['call_month'], df['unatuhorized_access'])
ax1.set_title("Unauthorized Access by Month")

ax2.plot(df['call_month'], df['make_inquiry'])
ax2.set_title("Make Inquiry by Month")

ax1.invert_xaxis()
ax2.invert_xaxis()

plt.rcParams["figure.figsize"]= 20,5


# In[23]:


df1 = df.iloc[:,2:19]
corrMatrix = df1.corr()
print (corrMatrix)


# In[215]:


sns.heatmap(corrMatrix, annot=True)
plt.rcParams["figure.figsize"]= 15,10
plt.rcParams.update({'font.size': 12})


# In[120]:


df2 = pd.read_csv('C:\\Users\\Me\\Documents\\File.csv', low_memory = False, index_col = False)


# In[123]:


df3 = df2.iloc[:,2:12]


# In[124]:


corrMatrix2 = df3.corr()
print (corrMatrix2)


# In[194]:


sns.heatmap(corrMatrix2, annot=True)
plt.rcParams["figure.figsize"]= 15,10
plt.rcParams.update({'font.size': 12})
