import pandas as pd
import joblib
import numpy as np

model = joblib.load('f1_undercut_model.pkl')
le_compound = joblib.load('compound_encoder.pkl')

def predict_stint_pace(compound, start_age, current_lap, track_temp, num_laps):
    compound_enc = le_compound.transform([compound])[0]
    total_time = 0
    
    for i in range(num_laps):
        features = pd.DataFrame([[compound_enc, start_age + i, track_temp, current_lap + i]], 
                                columns=['Compound_Encoded', 'TyreAge', 'TrackTemp', 'LapNumber'])
        pred_time = model.predict(features)[0]
        total_time += pred_time
        
    return total_time

print("\n--- F1 UNDERCUT STRATEGY ENGINE ---")
gp_name = input("Which GP are you simulating? (e.g. Silverstone, Monza): ")
t_temp = float(input("Current Track Temperature (°C): "))
curr_lap = int(input("Current Lap Number: "))
pit_loss = float(input("Time lost in Pits at this track (seconds): "))

print("\n--- RIVAL STATUS ---")
rival_tyre = input("Rival's current tyre (HARD/MEDIUM/SOFT): ").upper()
rival_age = int(input("How old are the rival's tyres? (Laps): "))

print("\n--- YOUR POTENTIAL PIT ---")
your_new_tyre = input("Which tyre will YOU switch to? (HARD/MEDIUM/SOFT): ").upper()


print(f"\nAnalyzing strategy for {gp_name}...")

found_payback = False
for laps_ahead in range(1, 21):
    time_stay_out = predict_stint_pace(rival_tyre, rival_age, curr_lap, t_temp, laps_ahead)
    time_undercut = predict_stint_pace(your_new_tyre, 1, curr_lap + 1, t_temp, laps_ahead) + pit_loss
    
    if time_undercut < time_stay_out and not found_payback:
        print(f"MATCH! At Lap {curr_lap + laps_ahead}, you will officially be ahead.")
        print(f"Target Window: {laps_ahead} laps after pitting.")
        found_payback = True
        break

if not found_payback:
    print("STRATEGY: Do not pit. Fresh tyres will not catch the rival before the race ends.")