import pandas as pd
#load
meteo = pd.read_csv("robustmeteo.csv")
fve = pd.read_csv("data\datacsvnaexport.csv", sep = ";")

print(fve.head())
print(meteo.head())