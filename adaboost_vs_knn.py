# -*- coding: utf-8 -*-
"""AdaBoost vs KNN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Fr8JqP685rx-5Nd7iTORIpx5y1t1jHZi
"""

import pandas as pd
import numpy as np

df = pd.read_csv("heart_attack_prediction_dataset.csv")
df.head()

df.info()

df = df.drop(columns = ["Patient ID", "Continent", "Hemisphere"])

df[['systolic', 'diastolic']] = df['Blood Pressure'].str.split('/', expand=True).astype(int)

df = df.drop(columns = ["Blood Pressure"])

df.info()

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

columns_to_encode = ["Sex", "Diet", "Country"]
for col in columns_to_encode:
  df[col] = encoder.fit_transform(df[col])

df.info()

X = df.drop(columns = ["Heart Attack Risk"])
y = df["Heart Attack Risk"]

"""**TRAINING AND ADABOOST CLASSIFIER**"""

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from scipy.stats import randint, uniform

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, stratify = y, random_state = 43)

dt = DecisionTreeClassifier(random_state=42)
adaboost = AdaBoostClassifier(base_estimator=dt, random_state=43)

param_dist = {
    'base_estimator__max_depth': randint(1, 21),
    'n_estimators': randint(50, 501),
    'learning_rate': uniform(0.01, 1.0)
}

adaboost_rs = RandomizedSearchCV(estimator=adaboost, param_distributions=param_dist, n_iter=50, cv=5, random_state=42, verbose = 2, n_jobs=-1)

adaboost_rs.fit(X_train, y_train)

print("Best Parameters:", adaboost_rs.best_params_)
print("Best Cross-validation Accuracy:", adaboost_rs.best_score_)

y_pred = adaboost_rs.predict(X_test)

from sklearn.metrics import accuracy_score
print(f"AdaBoost accuracy score {accuracy_score(y_pred, y_test)}")

y_pred_proba = adaboost_rs.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_pred_proba)
print(f"ROC AUC Score: {roc_auc}")

"""**TRAINING A K NEIGHBORS CLASSIFIER**

"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

from sklearn.metrics import roc_auc_score
neighbors = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
best_roc_auc_score = 0
best_n_neighbors = 0
for n in neighbors:
    knn = KNeighborsClassifier(n_neighbors=n)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn.fit(X_train, y_train)

    y_pred_knn = knn.predict(X_test)

    current_roc_auc_score = roc_auc_score(y_test, y_pred_knn)

    if current_roc_auc_score > best_roc_auc_score:
        best_roc_auc_score = current_roc_auc_score
        best_n_neighbors = n

print(f"Neighbors: {best_n_neighbors}, roc_auc_score: {best_roc_auc_score:.4f}")

print(f"KNN accuracy score {accuracy_score(y_pred_knn, y_test)}")

"""*AdaBoost has a slightly higher accuracy compared to kNN. While AdaBoost performs better in terms of accuracy, both models performed poorly due to class imbalance.***"""

