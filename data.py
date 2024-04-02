import pandas as pd

# Load the primary and secondary datasets
primary_df = pd.read_csv('primary_station.csv')
secondary_df = pd.read_csv('secondary_station.csv')

# Convert the timestamp column to datetime
primary_df['timestamp'] = pd.to_datetime(primary_df['timestamp'])
secondary_df['timestamp'] = pd.to_datetime(secondary_df['timestamp'])

# Create a boolean mask for rows in the secondary dataset that don't have a matching timestamp in the primary dataset
secondary_mask = ~secondary_df['timestamp'].isin(primary_df['timestamp'])

# Concatenate the primary dataset with the filtered secondary dataset
merged_df = pd.concat([primary_df, secondary_df[secondary_mask]], ignore_index=True)

# Sort the merged DataFrame by the timestamp column
merged_df = merged_df.sort_values('timestamp')