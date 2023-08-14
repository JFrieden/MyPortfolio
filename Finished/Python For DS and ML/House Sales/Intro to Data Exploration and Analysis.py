#!/usr/bin/env python
# coding: utf-8

# # Intro To Data Analysis On Housing Sale Data. 

# ## Important Libraries: Pandas (Dataframes), Numpy (Numeric calculations), Scipy (statistical analysis), Scikit-learn (Predictive Modeling), Matplotlib (Basic Graphing/ Visualization), Seaborn (Advanced Data Visualization Based On Matplotlib)

# ### Intro to Pandas

# In[23]:


#Pandas is an essential Python Library that allows the user
#To create and operate extensively on objects known as dataframes
#Dataframes are python objects organized to allow powerful
#Manipulation and representation of large data, like that found in CSV files
import pandas as pd

#use the read_csv(filename) method to create a df object populated with the contents of House Sales Values
df = pd.read_csv('/House Sales Values.csv')


print("Printing First 10 Rows of Data")
print(df.head(10))

print()

#Looking at the shape (row x col) of our dataset
print("Dataset Shape")
print(df.shape)

print()

#Looking at the data types of the dataset
print("Data types in the set")
print(df.dtypes)

print()

#Describing our dataset (with stats)
print("Describing dataset")
print(df.describe())

print()

#Cleaning Data. Finding Null Values and Removing Them

total_count = df.isnull().sum().sort_values(ascending = False) #Finding Total Count of Data

#Finding % of missing data relative to full set

percent_missing = (df.isnull().sum() / df.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total_count, percent_missing], axis = 1, keys=['Total','Percent'])
missing_data.head(20) #No longer prints if anything is written under it?!

print()
print("Oh No! It appears 5 of our categories have a few missing pieces of Data!")
print("Let's clean the dataset so we only consider fully known data.")
print()


#Removing Null Values
df.dropna(axis=0, inplace=True)

#Updated shape of our dataframe
print(df.shape)


# ### Using Scikit-learn (sklearn) to convert Categorical Data into Numeric Data

# In[30]:


#Numpy is a library used to perform numeric operations
#on data structures like lists and matrices

#Scipy is alibrary that uses Numpy data structures
#for advanced algebra and calculus operations

#Scikit-learn (aka sklearn) is a foundational library for building 
#predictive models

from sklearn.preprocessing import LabelEncoder

#get all categorical features
categorical_cols = ['HouseType', 'Fireplaces', 'Pool']
print("Names of Categorical Features")
print(categorical_cols)
print("Number of categorical features:",len(categorical_cols))

#Preparing to convert categorical variables into labels...
labelEncoder = LabelEncoder()

#applying LabelEncoder to categorical features

for categorical_item in categorical_cols:
    df[categorical_item] = labelEncoder.fit_transform(df[categorical_item])
    
print("Features successfully converted")
print()

#Checking first 10 rows of dataset
print("Showing first 10 rows of dataset post-conversion")
print(df.head(10))
print()

#Checking for updated Datatypes in dataset
print("Checking Updated Datatypes")
print(df.dtypes)


# ### Using Numpy and Scipy.stats to Remove +3 Z-Score Outliers

# In[41]:


import numpy as np
from scipy import stats

#Calcuation of Z-Scores
z_scores = np.abs(stats.zscore(df))

#Cleaning up any data with z-score >= 3
df = df[(z_scores < 3).all(axis = 1)]
print("Shape of dataframe without outliers", df.shape)
print()
print("Description of dataframe without outliers\n", df.describe())
print()

print("Our data had and has no outliers!")


# ### Visualizing Our Data with Matplotlib and Seaborn

# In[44]:


#Visualizing distribution of Sale Price
import matplotlib.pyplot as plt
import seaborn as sns

print("Overall Sale-Price Distribution")
sns.distplot(df['SalePrice']);

#Visualizing Price-by-type (Detached = 0, Semi = 1, Townhome = 2)

var = 'HouseType'
data = pd.concat([df['SalePrice'], df[var]], axis=1)
f, ax = plt.subplots(figsize=(14,8))
fig = sns.boxplot(x=var, y="SalePrice", data = data)
fig.axis(ymin = 300000, ymax = 2000000)

#Above plots are good for absolute visualization of single variable impact
#We can achieve relative impact of all variables using correlation matrices and heatmap visualization

correlation_matrix = df.corr()
f, ax = plt.subplots(figsize=(20, 10))
sns.heatmap(correlation_matrix, cmap="YlGnBu", vmax =.9, square=True) #Big boy, but easy enough to understand


# # Building Predictive Models

# ### Linear Regression                                                                                                                                                              
# #### Multiple-Linear Regression defines a linear relationship between a dependent variable Y and n number of independent variables X0 through Xn as Y = Intercept + c0X0 + c1X1 + ... + cnXn where cn is a coefficient determined by the linear regression model

# In[49]:


#Regression is a term coined in the 1870's by a statitician who noticed
#That genetic traits like height do not typically increase or decrease
#Over time, but instead "Regress" towards a mean which varies slightly
#With the Introduction of each new piece of data

from sklearn.model_selection import train_test_split 
        # method returns a split of x and y data 
        # into x-axis train and test data, and y-axis train
        # and test data respectively. (X = independent variables, y = dependent variable)
        # params(x-data, y-data, test_size = % of data to test 0.0-1.0, 
        #        random_state = seed for RNG, shuffle = Boolean option: pre-shuffle data?)

        
#Let's begin By Splitting the data into training and testing sets

X = df.drop('SalePrice', axis = 1) #Everything but salePrice data
y =df['SalePrice'] #Only salePrice Data

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.50,random_state=80, shuffle = True)
print("Data split successfully into training and testing data sets...\n")



#Building and testing a linear regression model
from sklearn.linear_model import LinearRegression

#Initializing the Linear Regression Model
LR = LinearRegression(copy_X = True)
LR.fit(X_train,y_train)
print("Linear Regression Model Trained Successfully...\n")

#Making a predicion using the test data in the LRM
yhat = LR.predict(X_test)

#Two ways to measure accuracy of the LRM

#1) Mean Squared Error (MSE) that calculates the difference between actual and predicted values as follows
from sklearn.metrics import mean_squared_error
print("Mean squared error of the linear regression model:", mean_squared_error(y_test, yhat))

#2) R-squared A.K.A. coefficient of determination that calculates how close the data is to the fitted regression line
print("R-Squared error of the LRM on the Training Data:", LR.score(X_train, y_train))
print("R-Squared error of the LRM on the Test Data:", LR.score(X_test, y_test))
print()
print("This indicates that ~39% of the variation of sale prices can be linearly related to our independent variables\n\n")


# ### Decision Tree Regression
# 
# #### Tree Structure breaks data set into smaller subsets and traverses down different possibility-nodes (boolean options) to arrive at a prediction

# In[51]:


from sklearn.tree import DecisionTreeRegressor

#Initializing the Decision Tree Regression Model
saleTree = DecisionTreeRegressor(random_state = 100)

#fit the regressor with X and y data
saleTree.fit(X_train, y_train)
print("Decision tree regression model trained successfully")

#Making a prediction using the test data in the decision Tree Regression Model
predTree = saleTree.predict(X_test)

from sklearn import metrics
print("Decision Tree Accuracy:", metrics.accuracy_score(y_test, predTree))


# #### We are now finished with the coding portion of Daneyal Anis' first machine learning manual. Some closing conceptual notes that are not well conveyed by the code follow:
#     There are three types of machine learning models:
#         1) Supervised Machine Learning
#                 -Model is provided direction in terms of how to classify data
#                  Uses this direction to learn before making predictions
#                  (Broadly, independent vs. dependent is identified)
#                  Examples include regression and classification analysis
#                  regression for numbers, classification for type/categorizing
#                  
#         2) Unsupervised Machine Learning
#                 -Model is given data without direction or labels, and
#                  has to make its own "decisions" about what seems to be
#                  related and how. Includes methods like clustering, 
#                  dimension reduction, and association learning.
#                  
#                      -Clustering: creates clusters of objects deemed "similar" by the program
#                                   with the most similar being the most close together. Think
#                                   fraud-detection via feeding a UnSupe ML model investment
#                                   portfolios with and without fraudulent activity. K-means is 
#                                   a popular python clustering method. 
#                                   
#                      -Dimension Reduction: Different things are grouped together based on shared
#                                            features, like categorizing movies into the genres
#                                            
#                      -Association Learning: More sophisticated. Associate behaviors with clusters 
#                                             or future events. Think a streaming algorithm. Associates
#                                             clusters of media with profile viewing behavior to recommend
#                                             new content.
#         
#         3) Deep Learning
#                 - Several learning models are combined into a network that
#                   is capable of "decision making" because the network employs
#                   multiple different learning models. Different "nodes", or 
#                   decision-point learning models, can have different weights
#                   to the significance of their decisions. Popular Python
#                   libraries include: TensorFlow, Keras, & PyTorch 
