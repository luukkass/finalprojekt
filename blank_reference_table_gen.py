import pandas as pd
from datetime import datetime, timedelta

# Define start and end datetime
start = datetime(2023, 3, 16, 0, 0, 0)
end = datetime(2024, 4, 16, 23, 55, 0)

# Generate date range
date_range = pd.date_range(start, end, freq='5min')

# Create DataFrame
df = pd.DataFrame(date_range, columns=['datetime'])

# Save to CSV
df.to_csv('reference_table.csv', index=False)
