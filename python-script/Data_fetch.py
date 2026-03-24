import fastf1
import pandas as pd
import os

if not os.path.exists('f1_cache'):
    os.makedirs('f1_cache')
fastf1.Cache.enable_cache('f1_cache')

years = [2021, 2022, 2023, 2024]
all_data = []

for year in years:
    for round_num in range(1, 25): 
        try:
            print(f"--- Attempting: {year} Round {round_num} ---")
            
            session = fastf1.get_session(year, round_num, 'R')
            
            session.load(laps=True, telemetry=False, weather=True)
            
            if not session.laps.empty:
                df = session.laps.copy()
            
                weather = session.weather_data[['Time', 'TrackTemp']].sort_values('Time')
                df = df.sort_values('Time')
                df = pd.merge_asof(df, weather, on='Time')
                
                df['Year'] = year
                df['Round'] = round_num
                df['LapTime_s'] = df['LapTime'].dt.total_seconds()
                
                all_data.append(df)
                print(f"Successfully loaded {year} Round {round_num}")
            
        except Exception as e:
            if "Session not found" in str(e):
                break 
            print(f"Skipping {year} R{round_num}: {e}")

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("f1_master_data_21_24.csv", index=False)
    print(f"\nDONE! Saved {len(final_df)} laps to CSV.")
else:
    print("Failed to collect any data. Please check your internet connection.")