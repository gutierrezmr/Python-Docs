
# coding: utf-8

# In[1]:


import pandas as pd
import string
import re
string.punctuation


# In[2]:


df = pd.read_csv('C:\\Users\\Me\\Documents\\File.csv')
stop = pd.read_csv('C:\\Users\\Me\\Documents\\File.csv')
df['DESCRIPTION'] = df['DESCRIPTION'].astype(str)


# In[4]:


df.head(5)


# In[3]:


stop_words = stop['fixed_stop'].tolist()
#print(stop_words)


# In[4]:


def clean_text_1(text):
    text = text.lower()#make lower
    text = re.sub('\[.*?\]','',text) #remove brackets
    text = re.sub('[%s]' % re.escape(string.punctuation),'',text) #remove punctuations
    text = re.sub('\w*\d\w*','',text) #removes digits
    text = re.sub('[''""...]','',text) #removes digits
    text = re.sub('\n', '', text)
    return text
round1 = lambda x: clean_text_1(x)


# In[5]:


clean_description = pd.DataFrame(df.DESCRIPTION.apply(round1))
clean_description.head()


# In[6]:


df['CLEAN_DESCRIPTION'] = clean_description['DESCRIPTION'].str.split(' ').apply(lambda x: ' '.join(k for k in x if k not in stop_words))


# In[7]:


df.head()


# In[8]:


#remove punc,stopwords and to lower
def remove_punctuation(text):
    no_punct=[words for words in text if words not in string.punctuation]
    words_wo_punct=''.join(no_punct)
    return words_wo_punct
df['no_punc_desc']=df['DESCRIPTION'].apply(lambda x: remove_punctuation(x))


# In[10]:


def tokenize(text):
    split=re.split("\W+",text) 
    return split
df['split_desc']=df['no_punc_desc'].apply(lambda x: tokenize(x.lower()))
df.head(1)


# In[11]:


def remove_stopwords(text):
    text=[word for word in text if word not in stop_words]
    return text
df['Clean_Desc'] = df['no_punc_desc'].apply(lambda x: remove_stopwords(x))
df.head(5)


# In[14]:


#df.DESCRIPTION.str.split(expand=True).stack().value_counts()


# In[12]:


s = df['CLEAN_DESCRIPTION'].value_counts()


# In[14]:


s = df['CLEAN_DESCRIPTION'].groupby(df['CONTACT_REASON']).value_counts()


# In[15]:


s.to_csv("C:\\Users\\Me\\Documents\\File.csv.csv")

