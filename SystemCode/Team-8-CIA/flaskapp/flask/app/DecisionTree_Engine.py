import pandas as pd
import pickle
from sklearn import tree
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn import metrics

col_names = ['Trade Name', 'RIC','Sector','Size', 'P/E','Yield', 'GTI', 'Net Profit', 'ROE', 'Debt/Equity','Price/Book', '52W Pr','Yield-Perf','Target']
# load dataset, dataset updated where 0 = LowYield, 1 = HighYield
SGX_v5 = pd.read_csv("app/SGX Data v4.csv", header=0, names=col_names)
#SGX_v5.head()

#split dataset in features and target variable
feature_cols = ['P/E', 'GTI', 'Net Profit', 'ROE', 'Debt/Equity','Price/Book', '52W Pr']

X = SGX_v5[feature_cols] # Features
y = SGX_v5.Target # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

# Create Decision Tree classifer object
#clf = tree.DecisionTreeClassifier(random_state=1)

clf_XGB = XGBClassifier()

# Train Decision Tree Classifer
#clf = clf.fit(X_train,y_train)
clf_XGB = clf_XGB.fit(X_train,y_train)

# save the trained model to disk
import pickle
filename = 'CIA_Pred_XGBoost.sav'
pickle.dump(clf_XGB, open(filename, 'wb'))

# load the trained model from disk - Performance Metrics
clf_XGB_trained = pickle.load(open(filename, 'rb'))
y_pred = clf_XGB_trained.predict(X_test)
print(metrics.accuracy_score(y_test, y_pred))
print(metrics.confusion_matrix(y_test,y_pred))
print(metrics.classification_report(y_test,y_pred))