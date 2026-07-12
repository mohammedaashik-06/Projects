import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

from sklearn.metrics import r2_score

df = pd.read_csv("student_history.csv")

X = df[["attendance","internal_marks","assignment_score","study_hours","participation"]]
y = df["final_score"]

X_train,X_test,y_train,y_test = train_test_split(
X,y,test_size=0.2,random_state=42
)

# Linear Regression
lr = LinearRegression()
lr.fit(X_train,y_train)
lr_pred = lr.predict(X_test)
lr_acc = round(r2_score(y_test,lr_pred)*100,2)

# Random Forest
rf = RandomForestRegressor()
rf.fit(X_train,y_train)
rf_pred = rf.predict(X_test)
rf_acc = round(r2_score(y_test,rf_pred)*100,2)

# SVM
svm = SVR()
svm.fit(X_train,y_train)
svm_pred = svm.predict(X_test)
svm_acc = round(r2_score(y_test,svm_pred)*100,2)

accuracy = {
"linear":lr_acc,
"rf":rf_acc,
"svm":svm_acc
}

# ⭐ Use Random Forest as main prediction model
model = rf
