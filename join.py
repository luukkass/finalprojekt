import pandas as pd
from datetime import timedelta

# Load your datasets
df_reference = pd.read_csv('data_final/reference_table.csv')
df_generation = pd.read_csv('data_final/fve_final.csv', sep = ",")
df_weather = pd.read_csv('data_final/robustmeteo.csv', sep = ",")
df_consumption = pd.read_csv('data/cez_data_elektromer/pnd_spotreba3.csv',sep = ";", encoding='ISO-8859-1')

df_generation.drop(['update time','rounded_timestamp','Unnamed: 0'], axis=1, inplace=True)
df_weather.drop(['rounded_timestamp','Unnamed: 0'], axis=1, inplace=True)
df_consumption.drop(["Status", "Datum.1", "Status.1", "Datum.2", "Status.2",'Unnamed: 9'], axis=1, inplace=True)


# Custom rounding function
def custom_rounding(timestamp, interval):
    """
    Custom rounding function that rounds timestamps to the nearest interval and sets seconds to zero.
    Breaks ties by rounding down.
    
    :param timestamp: The original timestamp.
    :param interval: The interval to round to, in minutes.
    :return: The rounded timestamp with seconds set to zero.
    """
    # Convert interval to a timedelta
    delta = timedelta(minutes=interval)
    
    # Find the remainder when dividing the timestamp by the interval
    remainder = timestamp.minute % interval
    
    # If the remainder is less than half the interval, round down
    if remainder < interval / 2:
        rounded = timestamp - timedelta(minutes=remainder)
    # If the remainder is exactly half the interval, also round down
    elif remainder == interval / 2:
        rounded = timestamp - timedelta(minutes=remainder)
    # Otherwise, round up
    else:
        rounded = timestamp + (delta - timedelta(minutes=remainder))
    
    # Set seconds (and microseconds) to zero
    return rounded.replace(second=0, microsecond=0)

# Convert timestamps to datetime and set as index
df_reference['timestamp'] = pd.to_datetime(df_reference['datetime'])
df_generation['timestamp'] = pd.to_datetime(df_generation['timestamp'])
df_weather['timestamp'] = pd.to_datetime(df_weather['timestamp'])
df_consumption['timestamp'] = pd.to_datetime(df_consumption['Datum'], dayfirst=True)

df_generation['timestamp_rounded'] = df_generation['timestamp'].apply(lambda x: custom_rounding(x, 5))
df_weather['timestamp_rounded'] = df_weather['timestamp'].apply(lambda x: custom_rounding(x, 5))

df_reference.set_index('timestamp', inplace=True)
df_generation.set_index('timestamp_rounded', inplace=True)
df_weather.set_index('timestamp_rounded', inplace=True)
df_consumption.set_index('timestamp', inplace=True)

print(df_generation[df_generation.index.duplicated(keep=False)])
print(df_weather[df_weather.index.duplicated(keep=False)])

df_merged_with_reference = pd.merge(df_reference, df_generation, how='left', left_index=True, right_index=True)
df_final_merged = pd.merge(df_merged_with_reference, df_weather, how='left', left_index=True, right_index=True)

df_final_merged.drop(['EPS active power R(W)','EPS active power S(W)','EPS active power T(W)','EPS apparent power R(VA)','EPS apparent power S(VA)','EPS apparent power T(VA)'], axis=1, inplace=True)

df_final_merged.to_csv("final_merge_5min_1.csv")