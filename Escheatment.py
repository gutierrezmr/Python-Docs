
# coding: utf-8

# In[14]:


import psycopg2 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_SELECTion import train_test_split
sns.set_style("whitegrid")
sns.set(style="whitegrid", color_codes=True)
rs_dbhost = 'redshift.amazonaws.com' 
rs_dbport = 'port' 
rs_dbname = 'name' 
rs_dbuser = 'username' 
rs_dbpassword = 'pswd' 
rs_conn = psycopg2.connect( 
    host=rs_dbhost, 
    user=rs_dbuser, 
    port=rs_dbport, 
    password=rs_dbpassword, 
    dbname=rs_dbname
) 
rs_cursor = rs_conn.cursor()
#------------------------------------------------------------------
import pyodbc
pyodbc.autocommit=True
conn=pyodbc.connect('HUE', autocommit=True)
#pd.read_sql('SHOW TABLES IN consume_invest', conn)


# In[17]:


#REDSHIFT QUERY
#Worthless securities period

query = """

drop table if exists z_mgutierrez.reps;
create table z_mgutierrez.reps as ( 
SELECT registeredrepcode, accountnumber From securities.accounts
Union all
SELECT registeredrepcode, accountnumber From advisor.accounts);

SELECT
distinct a.AccountNumber
,LoginName, c.registeredrepcode, emailaddress,
CASE WHEN total_market_value = 0 and positions >= 1 THEN 'Y'
else 'N' end as worthless_securities
FROM lookup.accountloginmap a LEFT JOIN ai.balance_dailyflow b on a.accountnumber = b.accountnumber
LEFT JOIN z_mgutierrez.reps c on a.accountnumber = c.accountnumber
LEFT JOIN apex_ext.ext989_ecommunication_preference d on a.accountnumber = d.accountnumber
WHERE LoginName IS NOT NULL
AND a.AccountNumber IN (



) and processdate LIKE '2022-03-22';
"""
################################## ^DATE OF REQUEST^

df = pd.read_sql(sql = query, con =rs_conn, index_col=None)


# In[6]:


#NORMAL QUERY
query = """
SELECT
AccountNumber
,LoginName
FROM lookup.accountloginmap
WHERE LoginName IS NOT NULL
AND AccountNumber IN ();
"""


df = pd.read_sql(sql = query, con =rs_conn, index_col=None)


# In[11]:


len(df)


# In[12]:


print(list(df.loginname))


# In[15]:


query1 = """SELECT
    pty.tk_ceqv_admin_client_id,
--  login.uid,
--  pty.last_update_dt,
--  pty.party_id,
    login.last_login  
FROM (SELECT sub.uid, MAX(sub.aap_rsa_date_time) as last_login FROM (
SELECT uid, aap_rsa_date_time, substr(to_date(aap_rsa_date_time),1,7) as tm,
CASE WHEN action='ALLOW' THEN 1 WHEN action='CHALLENGE' and challenge_success='Y' THEN 1 else 0 end as login_success
FROM consume_deposits.vw_rsa_event_details where transaction_type='SESSION_SIGNIN'
and rule_fired<>'IPONGoldList' and rule_fired not LIKE '%Alexa%') sub
group by sub.uid) login inner join(SELECT a.last_update_dt, a.party_id, a.dep_ceqv_admin_client_id,
a.idm_ceqv_admin_client_id, a.tk_ceqv_admin_client_id, a.primary_addr_prov_state_name
FROM consume_acm.vw_acm_customer_view a inner join(SELECT MAX(last_update_dt) as mx_date,
idm_ceqv_admin_client_id FROM consume_acm.vw_acm_customer_view group by 2 ) x
on a.last_update_dt=x.mx_date and a.idm_ceqv_admin_client_id=x.idm_ceqv_admin_client_id
) pty on login.uid=pty.idm_ceqv_admin_client_id where pty.tk_ceqv_admin_client_id is not null
AND pty.tk_ceqv_admin_client_id IN 

( 

)
"""


df1 = pd.read_sql(sql = query1, con = conn, index_col=None)


# In[18]:


df1 = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[19]:


#will only return rows with last_login
df1.columns = ['loginname', 'last_login']
df1.head(10)


# In[20]:


len(df1)


# In[21]:


Left_join = pd.merge(df, 
                     df1, 
                     on ='loginname', 
                     how ='left')


# In[22]:


Left_join.head(2)


# In[24]:


df2 = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[25]:


df2.head(2)


# In[26]:


Final_join = pd.merge(df2, 
                     Left_join, 
                     on ='accountnumber', 
                     how ='left')


# In[27]:


Final_join.head(2)


# In[28]:


Final_join.to_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[29]:


#MB
#REDSHIFT QUERY
#Worthless securities period

query = """

drop table if exists z_mgutierrez.reps;
create table z_mgutierrez.reps as ( 
SELECT registeredrepcode, accountnumber From securities.accounts
Union all
SELECT registeredrepcode, accountnumber From advisor.accounts);

SELECT
distinct a.AccountNumber
,LoginName, c.registeredrepcode, emailaddress,
CASE WHEN total_market_value = 0 and positions >= 1 THEN 'Y'
else 'N' end as worthless_securities
FROM lookup.accountloginmap a LEFT JOIN ai.balance_dailyflow b on a.accountnumber = b.accountnumber
LEFT JOIN z_mgutierrez.reps c on a.accountnumber = c.accountnumber
LEFT JOIN apex_ext.ext989_ecommunication_preference d on a.accountnumber = d.accountnumber
WHERE LoginName IS NOT NULL
AND a.AccountNumber IN (


) and processdate LIKE '2022-03-22';
"""
################################## ^DATE OF REQUEST^

mb_df = pd.read_sql(sql = query, con =rs_conn, index_col=None)


# In[30]:


mb_df.head(2)


# In[32]:


mb_file = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[33]:


mb_file.head(2)


# In[40]:


mb_join = pd.merge(mb_file, 
                     mb_df, 
                     on ='accountnumber', 
                     how ='left')


# In[41]:


mb_join.head(10)


# In[42]:


mb_join.to_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[43]:


df3 = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")
df4 = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[44]:


Final_join = pd.merge(df3, 
                     df4, 
                     on ='loginname', 
                     how ='left')


# In[45]:


Final_join.head(2)


# In[46]:


Final_join.to_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[4]:


#REDSHIFT QUERY
#Worthless securities period

query = """

SELECT
scivantage, cif from ai.ally_acm where processdate LIKE '2022-03-03' and scivantage in
(
)

;
"""
################################## ^DATE OF REQUEST^

cif = pd.read_sql(sql = query, con =rs_conn, index_col=None)


# In[8]:


cif.columns = ['loginname', 'cif']
cif.head()


# In[24]:


import numpy as np
cif.replace('', np.nan).COUNT()


# In[6]:


cif2 = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[13]:


len(cif2)


# In[16]:


cif_join = pd.merge(cif2, 
                     cif, 
                     on ='loginname', 
                     how ='left')


# In[17]:


len(cif_join)


# In[18]:


cif_join.to_csv("C:\\Users\\Me\\Documents\\File.csv")

