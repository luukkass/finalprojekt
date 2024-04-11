import pandas as pd

# Load the primary and secondary datasets
primary_df = pd.read_csv('data\wunderground\IVELKO9.csv')
secondary_df = pd.read_csv('data\wunderground\IPODBR33.csv')

# add a column marking the name of the station 
primary_df = primary_df.assign(dataset='IVELKO9')
secondary_df = secondary_df.assign(dataset='IPODBR33')

# Combine the 'Date' and 'Time' columns into a new 'timestamp' column
primary_df['timestamp'] = primary_df['Date'] + ' ' + primary_df['Time']
secondary_df['timestamp'] = secondary_df['Date'] + ' ' + secondary_df['Time']

# Convert the 'timestamp' column to datetime format, skipping invalid values
primary_df['timestamp'] = pd.to_datetime(primary_df['timestamp'], format='%Y/%m/%d %I:%M %p', errors='coerce')
secondary_df['timestamp'] = pd.to_datetime(secondary_df['timestamp'], format='%Y/%m/%d %I:%M %p', errors='coerce')

# Drop rows with NaT (Not a Time) values
primary_df = primary_df.dropna(subset=['timestamp'])
secondary_df = secondary_df.dropna(subset=['timestamp'])

primary_df["rounded_timestamp"] = primary_df["timestamp"].dt.round("5min")
secondary_df["rounded_timestamp"] = secondary_df["timestamp"].dt.round("5min")

# Create a boolean mask for rows in the primary dataset where 'temperature' is missing
primary_mask = primary_df['Temperature_C'].isna()

# Get the 'rounded_timestamp' values in the primary dataset where 'temperature' is missing
missing_timestamps = primary_df.loc[primary_mask, 'rounded_timestamp']

# Create a new dataframe that only includes the rows from 'secondary_df' where the 'rounded_timestamp' matches 'missing_timestamps'
secondary_subset = secondary_df[secondary_df['rounded_timestamp'].isin(missing_timestamps)]

# Concatenate the primary dataset with 'secondary_subset'
merged_df = pd.concat([primary_df, secondary_subset], ignore_index=True)


# Sort the merged DataFrame by the timestamp column
merged_df = merged_df.sort_values('rounded_timestamp')

# Drop rows where 'Temperature_C' is NaN
merged_df_dropped = merged_df.dropna(subset=['Temperature_C'])
# To drop columns, you can use the 'drop' function. Let's say you want to drop columns named 'col1', 'col2', and 'col3'
merged_df_dropped = merged_df_dropped.drop(columns=['Date','Time',])

# To move the 'rounded_timestamp' column to the first position, you can do:
cols = list(merged_df_dropped.columns)
cols.insert(0, cols.pop(cols.index('rounded_timestamp')))
merged_df_dropped = merged_df.loc[:, cols]



merged_df_dropped.to_csv("robustmeteo.csv")
