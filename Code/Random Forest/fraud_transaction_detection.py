# -*- coding: utf-8 -*-
"""credit_card_random_forest.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yIALMEo7C3v5M-1uw2wNPtcSwU8uC6Uw

##Importing Libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

"""##Data Exploration"""

df=pd.read_csv('/content/drive/MyDrive/Dataset/creditcard.csv')
df.head()

df['Class'].value_counts()

fraud_percent = 100*df['Class'].value_counts()[1]/df.shape[0]
print(f'fraud transaction percentage : {round(fraud_percent,3)}%')

df.drop(columns=['Time'],inplace=True)
X=df.drop(columns=['Class'])
y=df['Class']

X.shape, y.shape

#Confusion Matrix Visualization
from sklearn.metrics import confusion_matrix
def heatmap_confusion_matrix(y_true, y_pred, statement):
    print(statement)
    cm=confusion_matrix(y_true,y_pred)
    group_names = ['True Neg','False Pos','False Neg','True Pos']
    group_counts = ['{0:0.0f}'.format(value) for value in cm.flatten()]
    labels = [f'{v1}\n{v2}' for v1, v2 in zip(group_names,group_counts)]
    labels = np.asarray(labels).reshape(2,2)
    plt.figure(figsize=(6,4))
    sns.set(font_scale=1.2)
    sns.heatmap(cm,annot=labels,fmt='',cmap='Blues')
    plt.xlabel("Predicted Value")
    plt.ylabel("Actual Value")
    plt.show()

#Classification Metrics
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
def classification_metrics(y_true,y_predict,y_probability):
    print("Accuracy Score  : ",round(accuracy_score(y_true,y_predict),3))
    print("Precision Score : ",round(precision_score(y_true,y_predict),3))
    print("Recall Score    : ",round(recall_score(y_true,y_predict),3))
    print("F1 Score        : ",round(f1_score(y_true,y_predict),3))
    print("roc_auc_score   : ",round(roc_auc_score(y_true,y_probability),3))

#Evaluate Binary Classification Model
def evaluate_model(model,train_X,test_X,train_y,test_y,name):
    print(name)
    model.fit(train_X,train_y)
    m_pred=model.predict(test_X)
    m_prob=model.predict_proba(test_X)[:,1]
    # heatmap_confusion_matrix(train_y, model.predict(train_X), 'Result on train data')
    heatmap_confusion_matrix(test_y,m_pred, 'Result on test data')
    classification_metrics(test_y,m_pred,m_prob)

"""##Random Forest on actual data"""

def train_evaluate_random_forest(X, y, name, X_org, y_org, eval_original):
    
    #Splitting data into train and test
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)
    print(x_train.shape, x_test.shape)
    
    #Normalization of data
    scale = StandardScaler()
    x_train = scale.fit_transform(x_train)
    x_test = scale.transform(x_test)
    
    #Training on Random Forest
    model = RandomForestClassifier(n_estimators=50, random_state=100)
    evaluate_model(model, x_train, x_test, y_train, y_test, name)

    #Evaluation of Model on Original data
    if eval_original:
        heatmap_confusion_matrix(y_org, model.predict(scale.transform(X_org)), 'Result on Original Dataset')

train_evaluate_random_forest(X, y, 'Random Forest', X, y, False)

"""##UnderSampling"""

from sklearn.utils import shuffle
fraud = df[df['Class']==1].copy()
non_fraud = df[df['Class']==0].copy()
non_fraud = shuffle(non_fraud, random_state=42)
non_fraud = non_fraud[0:fraud.shape[0]*9].copy()
non_fraud.shape

data = pd.concat([non_fraud, fraud])
data = shuffle(data, random_state=42)
X_under = data.drop(columns=['Class'])
y_under = data['Class']
y_under.value_counts()

train_evaluate_random_forest(X_under, y_under, 'Random forest with UnderSampling', X, y, True)

"""##OverSampling using Smote"""

X = df.drop(columns=['Class'])
y = df['Class']

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_over, y_over = smote.fit_resample(X, y)

data = pd.concat([X_over, y_over], axis=1)
data = shuffle(data, random_state=42)
X_over = data.drop(columns=['Class'])
y_over = data['Class']
y_over.value_counts()

train_evaluate_random_forest(X_over, y_over, 'Random forest with OverSampling using SMOTE', X, y, True)