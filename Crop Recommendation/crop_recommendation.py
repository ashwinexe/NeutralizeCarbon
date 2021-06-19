import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle 

l = LabelEncoder()
filename = 'crop_model.sav'

# Reading in the data
df = pd.read_csv("data/Crop_recommendation.csv")


# Splitting the data
X = df.drop("label",axis = 1)
df['label'] = l.fit_transform(df['label'])
y = df['label']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2, random_state=42)

# Training the classifier
decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train,y_train)

# Save model
pickle.dump(decision_tree, open(filename, 'wb'))