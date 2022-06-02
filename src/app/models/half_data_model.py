from jsbeautifier import main
from sklearn.neural_network import MLPClassifier
import pickle 
import pandas as pd
import os
def save_model(dataset):
    from sklearn.model_selection import train_test_split
    X=dataset[['gender','height','weight','smoke','alco','active','age in yrs']]
    y=dataset.cardio
    clf = MLPClassifier(hidden_layer_sizes=(32,64,128),alpha=0.001,random_state=1,solver='adam', max_iter=5000).fit(X, y)
    filename = r'src\app\models\half_finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))


    
    

if __name__=='__main__':
    path=os.getcwd()
    print(path)
    dataset=pd.read_csv(r"src\app\models\Kagglecleaned3.csv")
    save_model(dataset)