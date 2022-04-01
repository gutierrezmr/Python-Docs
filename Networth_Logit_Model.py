#Split from client profitability random forest - networth was most important factor

logit = df[['networth','profit_bucket']]
logit = logit.dropna()
logit.head(2)


# In[23]:


cat_vars = logit[['networth']]
for var in cat_vars:
    cat_list='var'+'_'+var
    cat_list = pd.get_dummies(logit[var], prefix=var)
    data1=logit.join(cat_list)
    logit=data1


# In[24]:


cat_vars=['networth']
data_vars=logit.columns.values.tolist()
to_keep=[i for i in data_vars if i not in cat_vars]


# In[25]:


data_final=logit[to_keep]
data_final.columns.values


# In[26]:


X = data_final.loc[:, data_final.columns != 'profit_bucket']
y = data_final.loc[:, data_final.columns == 'profit_bucket']
from imblearn.over_sampling import SMOTE
os = SMOTE(random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
columns = X_train.columns


os_data_X,os_data_y=os.fit_resample(X_train, y_train)


os_data_X = pd.DataFrame(data=os_data_X,columns=columns )
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of no subscription in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of subscription",len(os_data_y[os_data_y['y']==1]))
print("Proportion of no subscription data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of subscription data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[27]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())

#bring in regression output, so what on coefs


# In[28]:


from sklearn.linear_model import LogisticRegression
from sklearn import metrics
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)


# In[29]:


y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))


# In[30]:


from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)


# In[31]:


from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


# In[39]:


from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()


# In[33]:


pop = data_final.pop("profit_bucket")
data_final["profit_bucket"]= pop
data_final.head(2)


# In[34]:


X_train, X_test, y_train, y_test = train_test_split(data_final.iloc[:, :-1], data_final.iloc[:, -1:], test_size = 0.3, random_state=1)

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)


cols = ['networth_$1,000,001 or more', 'networth_ 100,001−100,001− 500,000',
        'networth_ 25,001−25,001− 50,000','networth_ 50,001−50,001− 100,000', 
        'networth_ 500,001−500,001− 1,000,000', 'networth_Under $25,000']

#cols = ['option_cut_<100', 'option_cut_<200', 'option_cut_<500','option_cut_<1000']
X_train_std = pd.DataFrame(X_train_std, columns=cols)
X_test_std = pd.DataFrame(X_test_std, columns=cols)


# In[35]:


#
# Training / Test Dataframe
#
cols = ['networth_$1,000,001 or more', 'networth_ 100,001−100,001− 500,000',
        'networth_ 25,001−25,001− 50,000','networth_ 50,001−50,001− 100,000', 
        'networth_ 500,001−500,001− 1,000,000', 'networth_Under $25,000']
X_train_std = pd.DataFrame(X_train_std, columns=cols)
X_test_std = pd.DataFrame(X_test_std, columns=cols)


# In[36]:


from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(random_state=1)
forest.fit(X_train_std, y_train.values.ravel())


# In[37]:


import numpy as np
importances = forest.feature_importances_

#sort vars in descending order

sorted_indices = np.argsort(importances)[::-1]


# In[38]:


#plot feature importance 
import matplotlib.pyplot as plt
 
plt.title('Feature Importance')
plt.bar(range(X_train.shape[1]), importances[sorted_indices], align='center')
plt.xticks(range(X_train.shape[1]), X_train.columns[sorted_indices], rotation=90)
plt.tight_layout()
plt.show()
