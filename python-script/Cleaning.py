import pandas as pd
import numpy as np

df = pd.read_csv("f1_master_data_21_24.csv")

print("Columns found in CSV:", df.columns.tolist())

df['LapTime_s'] = pd.to_numeric(df['LapTime_s'], errors='coerce')
df = df.dropna(subset=['LapTime_s'])


race_col = None
for col in ['EventName', 'GP', 'Race', 'event_name']:
    if col in df.columns:
        race_col = col
        break

if not race_col:
    race_col = 'RoundNumber' if 'RoundNumber' in df.columns else 'Round'

print(f"Using '{race_col}' to group races.")

def filter_outliers(group):
    fastest_lap = group['LapTime_s'].min()
    return group[group['LapTime_s'] <= (fastest_lap * 1.07)]

df_clean = df.groupby(['Year', race_col], group_keys=False).apply(filter_outliers)

if 'PitInTime' in df_clean.columns:
    df_clean = df_clean[df_clean['PitInTime'].isna()]
if 'PitOutTime' in df_clean.columns:
    df_clean = df_clean[df_clean['PitOutTime'].isna()]

df_clean.to_csv("f1_ai_ready_data.csv", index=False)
print(f"Done! Cleaned data saved. Total laps: {len(df_clean)}")