import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn import metrics 
from sklearn.metrics import confusion_matrix
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import statsmodels.api as sa
import scikit_posthocs as sp
import statsmodels.formula.api as sfa
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import seaborn as sns
import plotly.express as px
#select data in H1B 2017
def read_csv_file(fp):
    df = pd.read_csv(fp)
    df_2017_sucess=df[(df['pw_unit'] != "H") & (df["case_year"] == 2017) & (df["case_status"] != "D") & (df["case_status"] != "W") ]
    return df_2017_sucess
#convert soc_name into integer
df_wage_occup = df_2017_sucess[['case_status','prevailing_wage','emp_h1b_dependent']]
H1B_dependent=df_wage_occup['emp_h1b_dependent'].value_counts()
H1B_dependent

def Classification(emp_h1b_dependent):
    if emp_h1b_dependent == 'N':
        return 0
    elif emp_h1b_dependent == 'Y':
        return 1
df_wage_occup['size_emp_h1b_dependent']=df_wage_occup['emp_h1b_dependent'].apply(Classification)
df_wage_occup

#plot the logistic regression
a=df_wage_occup['prevailing_wage']
b=df_wage_occup['size_emp_h1b_dependent']
sns.regplot(x=a, y=b, data=df_wage_occup, logistic=True, ci=None)

#the prevailing wage state in USA
import plotly.express as px
import pandas as pd
average_state = pd.DataFrame(df_2017_sucess.groupby('emp_state').agg({'prevailing_wage':'mean'}))
fig=px.choropleth(average_state,
              locations=average_state.index,
              locationmode='USA-states',
              scope='usa',
              color='prevailing_wage',
              color_discrete_map=['red', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow'])
fig.update_layout(
    title_text = 'The Distribution of Prevailing Wage from H1B Approved Aplications in 2017')




#%%
data = pd.read_csv('h1b_data.csv')

 
data.dropna(inplace=True)


data['case_status'] = data['case_status'].replace(['C', 'CW'], [0, 1])
data = data.loc[data['case_status'].isin([0, 1]), ['prevailing_wage', 'wage_from', 'case_status','job_title', 'work_state']]

model = LogisticRegression()


X = data[['prevailing_wage']]
y = data['case_status'].astype('int')


model = LogisticRegression()


model.fit(X, y)

params = model.coef_
for i in range(len(X.columns)):
    print(f'{X.columns[i]}: {params[0, i]}')

print('Approved prevailing_wage mean: ', data[data['case_status']==1]['prevailing_wage'].mean())
print('Denied prevailing_wage mean: ', data[data['case_status']==0]['prevailing_wage'].mean())

#%%
plt.figure(figsize=(25, 13))

sns.histplot(data=data[data['case_status']==1], x='prevailing_wage')
plt.show()
plt.figure(figsize=(25, 13))


sns.histplot(data=data[data['case_status']==0], x='prevailing_wage')
plt.show()

corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True)
plt.show()

#%%
counts = data['job_title'].value_counts()

valid_jobs = counts[counts >= 5000].index.tolist()

df = data[data['job_title'].isin(valid_jobs)]
dummy_job_title = pd.get_dummies(df['job_title'])
dummy_job_title

dtc = DecisionTreeClassifier()
dtc.fit(dummy_job_title, df['case_status'].astype('int'))
plt.figure(figsize=(20,20))


importance = dtc.feature_importances_
for i in range(len(dummy_job_title.columns)):
    print(f'{dummy_job_title.columns[i]}: {importance[i]}')
    

fig, ax = plt.subplots(figsize=(40, 20))
plot_tree(dtc, fontsize=10, ax=ax, filled=True, rounded=True, class_names=['Approved', 'Denied'])
plt.show()



counts = data['work_state'].value_counts()

valid_jobs = counts[counts >= 500].index.tolist()

df = data[data['work_state'].isin(valid_jobs)]
dummy_job_title = pd.get_dummies(df['work_state'])
dummy_job_title

model.fit(dummy_job_title, df['case_status'].astype('int'))
params = model.coef_
list_para = []
for i in range(len(dummy_job_title.columns)):
    list_para.append((dummy_job_title.columns[i],params[0, i]))

sorted_list = sorted(list_para, key=lambda x: x[1])
for i in sorted_list:
    print(i[0], ':', i[1])



plt.figure(figsize=(25, 13))


sns.countplot(data=df, y='work_state')
plt.show()
    
#%%
X = data[['prevailing_wage']]
y = data['wage_from'].astype('int')

reg = LinearRegression().fit(X, y)
print('coef: ', reg.coef_[0])
print('r2_score: ', r2_score(X, y))


y_pred = reg.predict(X)


plt.figure(figsize=(25, 13))

plt.scatter(X, y)
plt.plot(X, y_pred, color='red', linewidth=2)
plt.xlabel('prevailing_wage')
plt.ylabel('wage_from')
plt.show()

#%%
data = pd.read_csv('h1b_data.csv')

 
data.dropna(inplace=True)


data['case_status'] = data['case_status'].replace(['C', 'CW'], [0, 1])
data = data.loc[data['case_status'].isin([0, 1]), ['prevailing_wage', 'wage_from', 'case_status','job_title', 'work_state']]

model = LogisticRegression()


X = data[['prevailing_wage']]
y = data['case_status'].astype('int')


model = LogisticRegression()


model.fit(X, y)

params = model.coef_
for i in range(len(X.columns)):
    print(f'{X.columns[i]}: {params[0, i]}')

print('Approved prevailing_wage mean: ', data[data['case_status']==1]['prevailing_wage'].mean())
print('Denied prevailing_wage mean: ', data[data['case_status']==0]['prevailing_wage'].mean())

#%%
plt.figure(figsize=(25, 13))

sns.histplot(data=data[data['case_status']==1], x='prevailing_wage')
plt.show()
plt.figure(figsize=(25, 13))


sns.histplot(data=data[data['case_status']==0], x='prevailing_wage')
plt.show()

corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True)
plt.show()

#%%
counts = data['job_title'].value_counts()

valid_jobs = counts[counts >= 5000].index.tolist()

df = data[data['job_title'].isin(valid_jobs)]
dummy_job_title = pd.get_dummies(df['job_title'])
dummy_job_title

dtc = DecisionTreeClassifier()
dtc.fit(dummy_job_title, df['case_status'].astype('int'))
plt.figure(figsize=(20,20))


importance = dtc.feature_importances_
for i in range(len(dummy_job_title.columns)):
    print(f'{dummy_job_title.columns[i]}: {importance[i]}')
    

fig, ax = plt.subplots(figsize=(40, 20))
plot_tree(dtc, fontsize=10, ax=ax, filled=True, rounded=True, class_names=['Approved', 'Denied'])
plt.show()



counts = data['work_state'].value_counts()

valid_jobs = counts[counts >= 500].index.tolist()

df = data[data['work_state'].isin(valid_jobs)]
dummy_job_title = pd.get_dummies(df['work_state'])
dummy_job_title

model.fit(dummy_job_title, df['case_status'].astype('int'))
params = model.coef_
list_para = []
for i in range(len(dummy_job_title.columns)):
    list_para.append((dummy_job_title.columns[i],params[0, i]))

sorted_list = sorted(list_para, key=lambda x: x[1])
for i in sorted_list:
    print(i[0], ':', i[1])



plt.figure(figsize=(25, 13))


sns.countplot(data=df, y='work_state')
plt.show()
    
#%%
X = data[['prevailing_wage']]
y = data['wage_from'].astype('int')

reg = LinearRegression().fit(X, y)
print('coef: ', reg.coef_[0])
print('r2_score: ', r2_score(X, y))


y_pred = reg.predict(X)


plt.figure(figsize=(25, 13))

plt.scatter(X, y)
plt.plot(X, y_pred, color='red', linewidth=2)
plt.xlabel('prevailing_wage')
plt.ylabel('wage_from')
plt.show()

if __name__ == '__main__':
    print(read_csv_file('/Users/teresa930206/Downloads/h1b_data.csv'))
















