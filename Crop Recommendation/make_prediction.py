import pandas as pd 
import pickle 

filename = "Crop Recommendation/crop_model.sav"

# Load model
loaded_model = pickle.load(open(filename, 'rb'))

# Take inputs
colm_names = ["N","P","K","temperature","humidity","ph","rainfall"]
d = {}
for i in range(len(colm_names)):
    print("Enter the value for " + colm_names[i])
    ipt = float(input())
    d[colm_names[i]] = ipt 

# Convert to Series object for prediction
x = pd.Series(d)
x = x.values.reshape(1, -1)

# Make prediction 
print(loaded_model.predict(x))