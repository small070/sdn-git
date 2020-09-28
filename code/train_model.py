from sklearn import svm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import ensemble, preprocessing, metrics
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
import joblib

#   顯示所有columns
pd.set_option('display.max_columns', None)
#   顯示所有rows
pd.set_option('display.max_rows', None)
#   設定colwidth為100，預設為50
pd.set_option('max_colwidth', 100)


df = pd.read_csv('test.csv')

# df = shuffle(df)

# print(df)
X = pd.DataFrame(df, columns=['packet_time', 'average_priority', 'average_hard_timeout', 'packet_ratio'])

std = StandardScaler()
# X = std.fit_transform(X)
# X = scale(X) # 標準化
# X['packet_time'] = pd.to_numeric(X['packet_time'], errors='coerce') 
# x = x.drop(columns=['packet_time'], axis=1)

# 歸一化
minMax = MinMaxScaler()

#將資料進行歸一化
X = minMax.fit_transform(X)

y = df.label


model = joblib.load('train_KNN_model.m')
model = model.predict(X)
print(model)


# 預測
# clf_predict = clf.predict(X_test)
# print('SVC_train: ', clf.score(X_train,y_train))
# print('SVC_test: ', clf.score(X_test, y_test)) # acc
# print(len(clf_predict), len(y_test))
# from sklearn.metrics import cohen_kappa_score
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import roc_curve
# print(cohen_kappa_score(y_test, clf_predict))
# print(confusion_matrix(y_test, clf_predict))
# fpr, tpr, thresholds = roc_curve(y_test,clf_predict,pos_label=None,sample_weight=None,drop_intermediate=True)
# from sklearn.metrics import auc
# AUC = auc(fpr, tpr)
# print("AUC: ", AUC)
# plt.plot(fpr,tpr,marker = 'o')
# plt.show()
# print('')


# save model




