import pandas as pd

# load
primary_df = pd.read_csv('data\wunderground\IVELKO9.csv')
secondary_df = pd.read_csv('data\wunderground\IPODBR33.csv')

# pridan nazev stanice
primary_df = primary_df.assign(dataset='IVELKO9')
secondary_df = secondary_df.assign(dataset='IPODBR33')

# vytvoren timestamp sloupec
primary_df['timestamp'] = primary_df['Date'] + ' ' + primary_df['Time']
secondary_df['timestamp'] = secondary_df['Date'] + ' ' + secondary_df['Time']
# konvert
primary_df['timestamp'] = pd.to_datetime(primary_df['timestamp'], format='%Y/%m/%d %I:%M %p', errors='coerce')
secondary_df['timestamp'] = pd.to_datetime(secondary_df['timestamp'], format='%Y/%m/%d %I:%M %p', errors='coerce')
# drop NAT
primary_df = primary_df.dropna(subset=['timestamp'])
secondary_df = secondary_df.dropna(subset=['timestamp'])
# zaokrouhleno
primary_df["rounded_timestamp"] = primary_df["timestamp"].dt.round("5min")
secondary_df["rounded_timestamp"] = secondary_df["timestamp"].dt.round("5min")

# reseni missing values vypadku stanic a concat
primary_mask = primary_df['Temperature_C'].isna()
missing_timestamps = primary_df.loc[primary_mask, 'rounded_timestamp']
secondary_subset = secondary_df[secondary_df['rounded_timestamp'].isin(missing_timestamps)]
merged_df = pd.concat([primary_df, secondary_subset], ignore_index=True)

# seřadit podle rounded_timestamp pro časovou posloupnost
merged_df = merged_df.sort_values('rounded_timestamp')

#drop zbytečné sloupce
merged_df_dropped = merged_df.drop(columns=['Date','Time',])

# rounded_timestamp na index0 pro přehlednost
cols = list(merged_df_dropped.columns)
cols.insert(0, cols.pop(cols.index('rounded_timestamp')))
merged_df_dropped = merged_df.loc[:, cols]

print("Before dropna, null values in 'Temperature_C':", merged_df_dropped['Temperature_C'].isnull().sum())

merged_df_dropped = merged_df_dropped.dropna(subset=['Temperature_C'])

print("After dropna, null values in 'Temperature_C':", merged_df_dropped['Temperature_C'].isnull().sum())

merged_df_dropped.to_csv("robustmeteo.csv")