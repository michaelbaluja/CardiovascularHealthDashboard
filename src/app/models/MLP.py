import pickle
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
#result = loaded_model.predict(X_test)
