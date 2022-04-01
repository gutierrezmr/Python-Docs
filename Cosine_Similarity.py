
# coding: utf-8

# In[24]:


import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math
import re
from collections import Counter
import pandas as pd


# In[25]:


#reading in csv file to a pandas data frame
df = pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")


# In[23]:


df.head(2)


# In[17]:


#saving the regex expression to find word characters
WORD = re.compile(r"\w+")

def cos(vec1, vec2):
    '''
    1st dictionary {‘the’: 5, ‘quick’: 10, ‘brown’: 1, ‘fox’: 15}
    2nd dictionary {‘brown’: 1, ‘jumped’: 56, ‘fox’: 15}
    final dictionary {‘brown’: 1, ‘fox’: 15}
    '''
    intersection = set(vec1.keys()) & set(vec2.keys())
    
    '''
    basic calculation: 
    In any right triangle, the cosine of an angle is the length of the 
    adjacent side (A) divided by the length of the hypotenuse (H). 
    In a formula, it is written simply as 'cos'. cos x = A / H
    '''
    numerator = SUM([vec1[x] * vec2[x] for x in intersection])
    sum1 = SUM([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = SUM([vec2[x] ** 2 for x in list(vec2.keys())])    
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    '''
    Cosine similarity measures the similarity between two vectors by calculating the cosine of the angle
    between the two vectors. Cosine similarity is one of the most widely used and powerful similarity 
    measure in Data Science. It is used in multiple applications such as finding similar documents 
    in NLP, information retrieval, finding similar sequence to a DNA in bioinformatics, 
    detecting plagiarism and may more
    '''
    
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
    '''
    As an example, let's say we want to find the cosine of angle C. From the formula above we know that the cosine 
    of an angle is the adjacent side divided by the hypotenuse. 
    The adjacent side is BC and has a length of 26. The hypotenuse is AC with a length of 30. So we can write
    cos c = 26 / 30
  
    This comes out to 0.866. So we can say "The cosine of C is 0.866 "
    Similarly, we can apply this to our text fields to gauge between two vectors (emails)
    'how close/acute the angle is' or
    'how similar the text is'. Higher the cosine = stronger similarity 
    '''
    
def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)
    
#read in csv with two columns: one being original emails and the other being follow up emails
df=pd.read_csv("C:\\Users\\Me\\Documents\\File.csv")
'''
Apply the function created to the df and find the similarity of both columns, for each row and
return the similarity score
'''    
df['vector1']=df['EMAIL1'].apply(lambda x: text_to_vector(x)) 
df['vector2']=df['EMAIL2'].apply(lambda x: text_to_vector(x)) 
df['simscore']=df.apply(lambda x: cos(x['vector1'],x['vector2']),axis=1)


# In[21]:


df.head(2)


# In[19]:


df.to_csv("C:\\Users\\Me\\Documents\\File.csv.csv")

--spark nlp

