from jsbeautifier import main
from sklearn.neural_network import MLPClassifier

import pickle 
import pandas as pd
import os
def save_model(dataset):
    X=dataset[['gender','height','weight','ap_hi','ap_lo','smoke','alco','active','age in yrs','cholesterol=1','cholesterol=2','cholesterol=3','gluc=1','gluc=2','gluc=3']]
    y=dataset.cardio
    clf = MLPClassifier(hidden_layer_sizes=(32,64,128),alpha=0.001,random_state=1,solver='adam', max_iter=5000).fit(X, y)

    filename = r'src\app\models\full_finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))

    
    

if __name__=='__main__':
    path=os.getcwd()
    print(path)
    dataset=pd.read_csv(r"src\app\models\Kagglecleaned3.csv")
    save_model(dataset)