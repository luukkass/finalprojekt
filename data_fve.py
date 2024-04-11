import pandas as pd

dataraw = pd.read_csv("data\datacsvnaexport.csv", sep = ";")

dataraw['timestamp'] = pd.to_datetime(dataraw['update time'])
dataraw["rounded_timestamp"] = dataraw["timestamp"].dt.round("5min")
dataraw.to_csv("fve.csv")