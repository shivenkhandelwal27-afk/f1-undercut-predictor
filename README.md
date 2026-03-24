# 🏎️ F1 Undercut Predictor AI

A machine learning tool designed to predict the success probability of a pit-stop "undercut" strategy. This AI analyzes historical race data (2021–2024) to determine if pitting for fresh tires will allow a driver to emerge ahead of a rival who stays out.

## How it Works
The project uses a **Random Forest Regressor** trained on millions of data points from the FastF1 API. It calculates tire degradation curves based on:
* **Compound Type** (Soft, Medium, Hard)
* **Tyre Age** (Laps since the last pit stop)
* **Track Temperature** (°C)
* **Fuel Load** (Estimated by current Lap Number)



---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/shivenkhandelwal27-afk/f1-undercut-predictor.git](https://github.com/shivenkhandelwal27-afk/f1-undercut-predictor.git)
cd f1-undercut-predictor
```

### 2. Install Dependencies
Ensure you have Python 3.8+ installed. Run:
```bash
pip install fastf1 pandas scikit-learn joblib
```

### 3. Initialize Git LFS
Since the trained model is >100MB, you need Git LFS to pull the actual brain of the AI:
```bash
git lfs install
git lfs pull
```

## Usage

### Step 1: Data Fetching (Optional)
If you want to update the model with new 2026 data, run the fetching script:
```bash
python fetching.py
```

### Step 2: Run the Predictor
To test a real-world scenario, run the interactive prediction script:
```bash
python prediction.py
```

The script will ask for inputs like:
* Track Temp: e.g., 25
* Current Lap: e.g., 20
* Rival Tyre Age: e.g., 18
* Pit Loss: e.g., 20.5 (seconds)

## Model Performance

* Algorithm: Random Forest Regressor (100 estimators)
* Accuracy: Mean Absolute Error (MAE) of ~0.28s per lap.
* Data Source: Official F1 Timing Data via FastF1.

## Credits
* Made by - Shiven Khandelwal
* Reg No. - 25BCE10271
