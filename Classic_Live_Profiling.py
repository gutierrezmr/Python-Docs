
#Connection string - Hue AAP
query = """ SELECT * from
analytics.classic_live_profiling;
"""
df = pd.read_sql(sql = query, con =rs_conn, index_col=None)

df.head()


# In[90]:


len(df)


# In[121]:


df.groupby(['source','generation']).size()


# In[118]:


df.groupby(['source'])['classic_option_trades','classic_equity_trades','mobile_option_trades','mobile_equity_trades',
                       'live_option_trades','live_equity_trades','api_option_trades','api_equity_trades'].mean()


# In[59]:


query2 = '''With things as
(SELECT
channel,
app_or_browser,
pty.party_id,
pty.tk_ceqv_admin_client_id,
login_dt,
login_success
from (
sELECT
uid,
substr(to_date(aap_rsa_date_time),1,7) as tm,
to_date(aap_rsa_date_time) as login_dt,
case 
WHEN action='ALLOW' THEN 1 
WHEN action='CHALLENGE' and challenge_success='Y' THEN 1 else 0 end as login_success,
channel,
channel_desc,
app_or_browser
FROM consume_deposits.vw_rsa_event_details
where transaction_type='SESSION_SIGNIN' and rule_fired<>'IPONGoldList' and 
rule_fired not LIKE '%Alexa%' and to_date(aap_rsa_date_time)>='2021-11-01' 
and to_date(aap_rsa_date_time)<='2022-01-08'
) login inner join (
SELECT 
a.last_update_dt,
a.party_id,
a.dep_ceqv_admin_client_id,
a.idm_ceqv_admin_client_id,
a.tk_ceqv_admin_client_id
from consume_acm.vw_acm_customer_view a
inner join (
SELECT 
MAX(last_update_dt) as mx_date,
idm_ceqv_admin_client_id
from consume_acm.vw_acm_customer_view
group by 2
) x
on a.last_update_dt=x.mx_date and a.idm_ceqv_admin_client_id=x.idm_ceqv_admin_client_id) pty

on login.uid=pty.idm_ceqv_admin_client_id
where pty.tk_ceqv_admin_client_id is not null
and login_success=1 
)

SELECT  tk_ceqv_admin_client_id, channel, app_or_browser, SUM(login_success)
From things
Group by 1,2,3'''   
df2 = pd.read_sql(sql = query2, con =conn, index_col=None)


# In[116]:


df2.columns = ['loginname','channel', 'app_or_browser', 'total_logins']
df2.head()


# In[61]:


merge = pd.merge(df, 
                     df2, 
                     on ='loginname', 
                     how ='left')


# In[92]:


merge.head()


# In[93]:


#LOGINS are as of 3 Months ago
len(merge)


# In[105]:


df4 = merge[['loginname','source','trades','total_logins','channel',
          'total_commissions','generation','total_equity',
          'cash','first_balance','firstfundedyear']]


# In[119]:


df4.groupby(['source','channel'])['trades'].mean()


# In[25]:


#df3 = merge.columns = ['source','trades', 'channel', 'total_logins']
df3 = merge[['source', 'channel', 'total_logins']]
df3.head()


# In[26]:


len(df3)


# In[27]:


df3.groupby(['source','channel']).SUM()


# In[44]:


df4 = merge[['login_id', 'generation', 'channel', 'total_logins']]
df4 = df4.drop_duplicates(subset=['login_id'])
df4.head()


# In[45]:


len(df4)


# In[48]:


df4.groupby(['channel','generation']).mean()


# In[61]:


# clients in each source segment
#merge.groupby(['source']).size()
merge.groupby('source')['accountnumber'].nunique()


# In[62]:


merge.groupby('generation')['accountnumber'].nunique()


# In[63]:


merge.groupby('channel')['total_logins'].mean()


# In[34]:


merge.groupby('channel')['trades'].SUM()


# In[38]:


merge_unique.groupby('generation')['trades'].SUM()


# In[64]:


merge_unique.groupby(['source']).mean()


# In[43]:


merge.groupby('channel').SUM()


# In[45]:


merge_unique.groupby(['source']).mean()


# In[44]:


merge.groupby('channel').mean()


# In[ ]:


merge_unique()


# In[51]:


merge['total_commissions'].mean()


# In[49]:


merge['total_equity'].mean()


# In[59]:


merge.groupby(['source'])['total_equity'].mean()


# In[58]:


merge.groupby(['source'])['first_balance'].mean()


# In[50]:


merge['first_balance'].mean()


# In[7]:


df.to_csv("C:\\Users\\rzfggz\\Documents\\channel.csv")

