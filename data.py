import pandas as pd

# Load the primary and secondary datasets
primary_df = pd.read_csv('data\wunderground\IVELKO9.csv')
secondary_df = pd.read_csv('data\wunderground\IPODBR33.csv')

# Combine the 'Date' and 'Time' columns into a new 'timestamp' column
primary_df['timestamp'] = primary_df['Date'] + ' ' + primary_df['Time']
secondary_df['timestamp'] = secondary_df['Date'] + ' ' + secondary_df['Time']

# Convert the 'timestamp' column to datetime format, skipping invalid values
primary_df['timestamp'] = pd.to_datetime(primary_df['timestamp'], format='%Y/%m/%d %I:%M %p', errors='coerce')
secondary_df['timestamp'] = pd.to_datetime(secondary_df['timestamp'], format='%Y/%m/%d %I:%M %p', errors='coerce')

# Drop rows with NaT (Not a Time) values
primary_df = primary_df.dropna(subset=['timestamp'])
secondary_df = secondary_df.dropna(subset=['timestamp'])

# Create a boolean mask for rows in the secondary dataset that don't have a matching timestamp in the primary dataset
secondary_mask = ~secondary_df['timestamp'].isin(primary_df['timestamp'])

# Concatenate the primary dataset with the filtered secondary dataset
merged_df = pd.concat([primary_df, secondary_df[secondary_mask]], ignore_index=True)

# Sort the merged DataFrame by the timestamp column
merged_df = merged_df.sort_values('timestamp')

merged_df.to_csv('out.csv')