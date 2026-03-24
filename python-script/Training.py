import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
import joblib

df = pd.read_csv("f1_ai_ready_data.csv")

if 'TyreAge' not in df.columns:
    print("TyreAge column missing. Calculating it now...")

    if 'Stint' in df.columns:
        df['TyreAge'] = df.groupby(['Driver', 'Stint']).cumcount() + 1
    else:
        df['TyreAge'] = df['LapNumber'] 

le_compound = LabelEncoder()
df['Compound_Encoded'] = le_compound.fit_transform(df['Compound'].astype(str))

features = ['Compound_Encoded', 'TyreAge', 'TrackTemp', 'LapNumber']
X = df[features]
y = df['LapTime_s']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Model Training Complete! MAE: {mean_absolute_error(y_test, predictions):.3f}s")

joblib.dump(model, 'f1_undercut_model.pkl')
joblib.dump(le_compound, 'compound_encoder.pkl')
print("Model saved as f1_undercut_model.pkl")