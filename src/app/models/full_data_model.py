from jsbeautifier import main
from sklearn.linear_model import LogisticRegression
import pickle 
import pandas as pd
import os
def save_model(dataset):
    from sklearn.model_selection import train_test_split
    X=dataset[['gender','height','weight','ap_hi','ap_lo','gluc','cholesterol','smoke','alco','active','age in yrs']]
    y=dataset.cardio
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.10, random_state=42)
    from sklearn.linear_model import LogisticRegression
    logreg = LogisticRegression(class_weight='balanced',max_iter=10000)
    logreg.fit(X_train,y_train)
    filename = 'full_finalized_model.sav'
    pickle.dump(logreg, open(filename, 'wb'))

    
    

if __name__=='__main__':
    path=os.getcwd()
    print(path)
    dataset=pd.read_csv("models/kaggle_cleaned.csv")
    save_model(dataset)