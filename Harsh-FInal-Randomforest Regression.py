#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 17:46:41 2018

@author: harsh
"""

#Importing Required Libraries
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import explained_variance_score, mean_squared_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import os

#Setting up working directories
os.chdir(r'/Users/harsh/Desktop/Data sets')

#Importing The Dataset
sp=pd.read_csv('SolarPrediction.csv')
spw=sp[['Radiation', 'Temperature','Pressure', 'Humidity', 'Speed','WindDirection(Degrees)']]

#copy of dataset
spwc=spw.copy()

#checking basic information of data
spwc.shape
spwc.info()
desc=spwc.describe()
spwc.head()

#Checking for Missing values
plt.figure(figsize=(8,4))
sns.heatmap(spwc.isnull(),cbar=False,cmap='viridis',yticklabels=False)
plt.title('Missing value in the dataset')

#describing Feature distribution
selected_features=['Radiation', 'Temperature','Pressure', 'Humidity', 'Speed','WindDirection(Degrees)']
n_rows = 3
n_cols = 2
fig=plt.figure()
for i, var_name in enumerate(selected_features):
    ax=fig.add_subplot(n_rows,n_cols,i+1)
    spwc[var_name].hist(bins=10,ax=ax,color='green')
    ax.set_title(var_name+" Distribution")
fig.tight_layout()
fig.set_size_inches(10,10)
plt.show()

# For further visualise any realtionships between the features, 

sns.pairplot(spwc,diag_kind="kde",markers="+")

#Separating the Independent and Dependent Variables
x = spwc[['Temperature','Pressure', 'Humidity', 'Speed','WindDirection(Degrees)']]
y = spwc[['Radiation']]

#Splitting the Dataset
#The dataset was subsequently split into a training and test set, with an 80%, 20% split respectively.

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
print (x_train.shape, y_train.shape)
print (x_test.shape, y_test.shape)

#a pearson correlation heatmap (matrix) was plotted for correlation.
corr = x.corr()
plt.figure(figsize=(8,9))
sns.heatmap(corr, cmap = 'coolwarm', annot= True,square=True)
plt.title("Pearson correlation heatmap",fontsize=20,color="Blue",fontname='Console')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

#Feature selection (For backward selection if needed)

regressor = RandomForestRegressor(n_estimators = 100)
regressor.fit(x_train, y_train)
feature_importances = regressor.feature_importances_

x_train_opt = x_train.copy()
removed_columns = pd.DataFrame()
models = []
r2s_opt = []

for i in range(0,5):
    least_important = np.argmin(feature_importances)
    removed_columns = removed_columns.append(x_train_opt.pop(x_train_opt.columns[least_important]))
    regressor.fit(x_train_opt, y_train)
    feature_importances = regressor.feature_importances_
    accuracies = cross_val_score(estimator = regressor,X = x_train_opt,y = y_train, cv = 5,scoring = 'r2')
    r2s_opt = np.append(r2s_opt, accuracies.mean())
    models = np.append(models, ", ".join(list(x_train_opt)))
    
feature_selection = pd.DataFrame({'Features':models,'r2 Score':r2s_opt})
feature_selection.head()

#K-fold Cross Validation (with R2 value)
accuracies = cross_val_score(estimator = regressor, X = x_train,y = y_train, cv = 10, scoring = 'r2')
accuracy = accuracies.mean()
print('r2 = {}'.format(accuracy))
##.73

#Test Score
print('Accuracy:',regressor.score(x_test,y_test))

#Predicting the test set
y_pred = pd.DataFrame(regressor.predict(x_test))
y_pred.columns=['Radiation']
print(y_pred[0:5])

#validating model
# 1.
r_squared = r2_score(y_test, y_pred)
print('r2 = {}'.format(r_squared))
# 2.
sns.regplot(y_test, y=y_pred,scatter_kws={"color": "red"}, line_kws={"color": "blue"})
plt.title('Check for Linearity',fontsize=20,color="Blue")
plt.xlabel('Actual value')
plt.ylabel('Predicted value')

#R2,adjusted R2 and p value for each varibale.
#Ordinary Least Squares (OLS)
est=sm.OLS(y_test,x_test)
est=est.fit()
print(est.summary())
























