import pandas as pd


dataraw = pd.read_csv("data\datacsvnaexport_final.csv", sep = ";")
dataraw['update time'] = dataraw['update time'].str.rstrip('.')
dataraw['timestamp'] = pd.to_datetime(dataraw['update time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
dataraw["rounded_timestamp"] = dataraw["timestamp"].dt.round("5min")

dataraw.to_csv("fve_final.csv")
