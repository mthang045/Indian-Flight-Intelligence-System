"""
Complete Training Script for Indian Flight Intelligence System
Trains both Price Prediction and Delay Prediction models

Features:
- Data loading and preprocessing
- Feature engineering (30 features with one-hot encoding)
- Train/test split with stratification
- RandomForest model training (price + delay)
- Model evaluation with comprehensive metrics
- Model serialization (.pkl files)
- Feature names and metadata saving

Usage:
    python train.py
    
Requirements:
    - airlines_flights_data.csv in current directory or parent directory
    - Python packages: pandas, numpy, scikit-learn, joblib
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    r2_score,
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)
import joblib
import os
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# File paths
DATA_FILE = "airlines_flights_data.csv"
OUTPUT_DIR = Path(__file__).parent
PRICE_MODEL_PATH = OUTPUT_DIR / "flight_model.pkl"
DELAY_MODEL_PATH = OUTPUT_DIR / "delay_model.pkl"
LABEL_ENCODERS_PATH = OUTPUT_DIR / "label_encoders.pkl"
FEATURE_NAMES_PATH = OUTPUT_DIR / "feature_names.pkl"
METADATA_PATH = OUTPUT_DIR / "model_metadata.pkl"

# Model hyperparameters
PRICE_MODEL_PARAMS = {
    'n_estimators': 100,
    'max_depth': 20,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'max_features': 'sqrt',
    'random_state': 42,
    'n_jobs': -1,
    'verbose': 1
}

DELAY_MODEL_PARAMS = {
    'n_estimators': 100,
    'max_depth': 15,
    'min_samples_split': 10,
    'min_samples_leaf': 4,
    'class_weight': 'balanced',
    'random_state': 42,
    'n_jobs': -1,
    'verbose': 1
}

# Train/test split
TEST_SIZE = 0.2
RANDOM_STATE = 42

print("=" * 80)
print("🚀 INDIAN FLIGHT INTELLIGENCE SYSTEM - MODEL TRAINING")
print("=" * 80)
print(f"📅 Training started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================

print("\n📂 STEP 1: Loading dataset...")
print("-" * 80)

# Try multiple locations for data file
data_paths = [
    DATA_FILE,
    OUTPUT_DIR / DATA_FILE,
    OUTPUT_DIR.parent / DATA_FILE,
    OUTPUT_DIR.parent / "data" / DATA_FILE
]

df = None
for path in data_paths:
    if Path(path).exists():
        print(f"✅ Found data file: {path}")
        df = pd.read_csv(path)
        break

if df is None:
    raise FileNotFoundError(f"❌ Dataset not found. Please place {DATA_FILE} in one of these locations: {data_paths}")

print(f"✅ Dataset loaded successfully!")
print(f"   • Shape: {df.shape} (rows, columns)")
print(f"   • Columns: {list(df.columns)}")
print(f"   • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ============================================================================
# STEP 2: DATA CLEANING
# ============================================================================

print("\n🧹 STEP 2: Data cleaning...")
print("-" * 80)

initial_rows = len(df)

# Remove duplicates
df = df.drop_duplicates()
print(f"✅ Removed {initial_rows - len(df)} duplicate rows")

# Handle missing values
missing_counts = df.isnull().sum()
if missing_counts.sum() > 0:
    print(f"⚠️  Found missing values:")
    for col, count in missing_counts[missing_counts > 0].items():
        print(f"   • {col}: {count} missing ({count/len(df)*100:.2f}%)")
    
    # Drop rows with missing critical columns
    df = df.dropna(subset=['price', 'duration'], how='any')
    print(f"✅ Dropped rows with missing price/duration: {len(df)} rows remaining")
else:
    print("✅ No missing values found")

# Remove price outliers (using IQR method)
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

before_outlier_removal = len(df)
df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
outliers_removed = before_outlier_removal - len(df)
print(f"✅ Removed {outliers_removed} price outliers ({outliers_removed/before_outlier_removal*100:.2f}%)")
print(f"   • Price range: ₹{df['price'].min():.0f} - ₹{df['price'].max():.0f}")
print(f"   • Clean dataset: {len(df):,} rows")

# ============================================================================
# STEP 3: FEATURE ENGINEERING
# ============================================================================

print("\n🔧 STEP 3: Feature engineering...")
print("-" * 80)

# Convert duration from hours to minutes
if 'duration' in df.columns:
    df['duration_minutes'] = (df['duration'] * 60).round().astype(int)
    print(f"✅ Converted duration to minutes")
    print(f"   • Range: {df['duration_minutes'].min()} - {df['duration_minutes'].max()} minutes")
else:
    raise ValueError("❌ 'duration' column not found in dataset")

# Map stops to numeric
stops_map = {
    'zero': 0,
    'one': 1, 
    'two_or_more': 2
}

if 'stops' in df.columns:
    df['stops_numeric'] = df['stops'].map(stops_map)
    print(f"✅ Mapped stops to numeric: {dict(df['stops'].value_counts())}")
else:
    raise ValueError("❌ 'stops' column not found in dataset")

# Extract date features
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day_of_week'] = df['date'].dt.dayofweek
    print(f"✅ Extracted date features: day, month, year, day_of_week")
else:
    # If no date column, create default values
    print(f"⚠️  No 'date' column, using defaults")
    df['day'] = 15
    df['month'] = 6
    df['year'] = 2024

# Map time periods to hours
time_to_hour = {
    'Morning': 8,
    'Afternoon': 14,
    'Evening': 18,
    'Night': 22,
    'Early_Morning': 6,
    'Late_Night': 23
}

if 'departure_time' in df.columns and 'arrival_time' in df.columns:
    df['departure_hour'] = df['departure_time'].map(time_to_hour).fillna(12)
    df['arrival_hour'] = df['arrival_time'].map(time_to_hour).fillna(14)
    print(f"✅ Mapped time periods to hours")
else:
    print(f"⚠️  Time columns not found, using defaults")
    df['departure_hour'] = 12
    df['arrival_hour'] = 14

# Calculate days_left (if not present)
if 'days_left' not in df.columns:
    # Random days_left between 1-50 for training
    np.random.seed(42)
    df['days_left'] = np.random.randint(1, 50, size=len(df))
    print(f"⚠️  Generated random 'days_left' values (1-50 days)")

# Create delay labels (binary classification)
# For this dataset, we'll create synthetic delay labels based on patterns
# Real delay data would be better, but we'll use heuristics:
# Higher delay probability for: more stops, peak hours, certain airlines
np.random.seed(42)
delay_factors = (
    (df['stops_numeric'] * 0.2) +  # More stops = higher delay
    ((df['departure_hour'].isin([7, 8, 18, 19])).astype(int) * 0.15) +  # Peak hours
    (np.random.random(len(df)) * 0.5)  # Random component
)
df['delay'] = (delay_factors > 0.5).astype(int)
print(f"✅ Created delay labels (1=Delayed, 0=On-time)")
print(f"   • Delayed: {(df['delay']==1).sum()} ({(df['delay']==1).sum()/len(df)*100:.1f}%)")
print(f"   • On-time: {(df['delay']==0).sum()} ({(df['delay']==0).sum()/len(df)*100:.1f}%)")

print(f"\n📊 Feature summary:")
print(f"   • Total features created: {len(df.columns)}")
print(f"   • Numeric features: duration_minutes, stops_numeric, day, month, year, days_left, departure_hour, arrival_hour")
print(f"   • Categorical features: airline, source_city, destination_city, class, departure_time, arrival_time")

# ============================================================================
# STEP 4: ONE-HOT ENCODING
# ============================================================================

print("\n🏷️  STEP 4: One-hot encoding categorical features...")
print("-" * 80)

# Select features for training
numeric_features = [
    'days_left', 'day', 'month', 'year',
    'duration_minutes', 'stops_numeric',
    'departure_hour', 'arrival_hour'
]

categorical_features = [
    'airline', 'source_city', 'destination_city', 'class'
]

# Verify all required columns exist
missing_cols = []
for col in numeric_features + categorical_features:
    if col not in df.columns:
        missing_cols.append(col)

if missing_cols:
    raise ValueError(f"❌ Missing required columns: {missing_cols}")

print(f"✅ Verified all required features exist")

# One-hot encode categorical features
df_encoded = pd.get_dummies(
    df[numeric_features + categorical_features + ['price', 'delay']],
    columns=categorical_features,
    drop_first=False  # Keep all categories
)

print(f"✅ One-hot encoding completed")
print(f"   • Total features after encoding: {len(df_encoded.columns) - 2}")  # -2 for price and delay

# Save feature names (excluding price and delay)
feature_columns = [col for col in df_encoded.columns if col not in ['price', 'delay']]
print(f"   • Feature names: {len(feature_columns)} features")

# Add Unknown period flags (to match API transformation)
if 'departure_period_Unknown' not in df_encoded.columns:
    df_encoded['departure_period_Unknown'] = 0
if 'arrival_period_Unknown' not in df_encoded.columns:
    df_encoded['arrival_period_Unknown'] = 0

feature_columns = [col for col in df_encoded.columns if col not in ['price', 'delay']]

print(f"\n📋 Final feature set ({len(feature_columns)} features):")
for i, feat in enumerate(feature_columns, 1):
    print(f"   {i:2d}. {feat}")

# ============================================================================
# STEP 5: TRAIN/TEST SPLIT
# ============================================================================

print(f"\n✂️  STEP 5: Splitting data into train/test sets...")
print("-" * 80)

X = df_encoded[feature_columns]
y_price = df_encoded['price']
y_delay = df_encoded['delay']

# Split for price prediction
X_train_price, X_test_price, y_train_price, y_test_price = train_test_split(
    X, y_price, test_size=TEST_SIZE, random_state=RANDOM_STATE
)

# Split for delay prediction (with stratification to keep class balance)
X_train_delay, X_test_delay, y_train_delay, y_test_delay = train_test_split(
    X, y_delay, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_delay
)

print(f"✅ Data split completed:")
print(f"   • Training set: {len(X_train_price):,} samples ({(1-TEST_SIZE)*100:.0f}%)")
print(f"   • Test set: {len(X_test_price):,} samples ({TEST_SIZE*100:.0f}%)")
print(f"   • Features: {X_train_price.shape[1]}")
print(f"   • Delay class distribution (train):")
print(f"     - On-time: {(y_train_delay==0).sum()} ({(y_train_delay==0).sum()/len(y_train_delay)*100:.1f}%)")
print(f"     - Delayed: {(y_train_delay==1).sum()} ({(y_train_delay==1).sum()/len(y_train_delay)*100:.1f}%)")

# ============================================================================
# STEP 6: TRAIN PRICE PREDICTION MODEL
# ============================================================================

print(f"\n🎯 STEP 6: Training Price Prediction Model (RandomForestRegressor)...")
print("-" * 80)
print(f"⚙️  Model configuration:")
for key, value in PRICE_MODEL_PARAMS.items():
    print(f"   • {key}: {value}")

price_model = RandomForestRegressor(**PRICE_MODEL_PARAMS)

print(f"\n🔄 Training in progress...")
price_model.fit(X_train_price, y_train_price)

print(f"✅ Price model training completed!")
print(f"   • Model type: {type(price_model).__name__}")
print(f"   • Number of trees: {price_model.n_estimators}")
print(f"   • Number of features: {price_model.n_features_in_}")

# ============================================================================
# STEP 7: EVALUATE PRICE PREDICTION MODEL
# ============================================================================

print(f"\n📊 STEP 7: Evaluating Price Prediction Model...")
print("-" * 80)

# Predictions
y_train_pred = price_model.predict(X_train_price)
y_test_pred = price_model.predict(X_test_price)

# Training metrics
train_r2 = r2_score(y_train_price, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train_price, y_train_pred))
train_mae = mean_absolute_error(y_train_price, y_train_pred)
train_mape = np.mean(np.abs((y_train_price - y_train_pred) / y_train_price)) * 100

# Test metrics
test_r2 = r2_score(y_test_price, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test_price, y_test_pred))
test_mae = mean_absolute_error(y_test_price, y_test_pred)
test_mape = np.mean(np.abs((y_test_price - y_test_pred) / y_test_price)) * 100

print(f"📈 TRAINING SET PERFORMANCE:")
print(f"   • R² Score:  {train_r2:.4f} ({train_r2*100:.2f}%)")
print(f"   • RMSE:      ₹{train_rmse:.2f}")
print(f"   • MAE:       ₹{train_mae:.2f}")
print(f"   • MAPE:      {train_mape:.2f}%")

print(f"\n📊 TEST SET PERFORMANCE:")
print(f"   • R² Score:  {test_r2:.4f} ({test_r2*100:.2f}%) ✅")
print(f"   • RMSE:      ₹{test_rmse:.2f}")
print(f"   • MAE:       ₹{test_mae:.2f}")
print(f"   • MAPE:      {test_mape:.2f}%")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': price_model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n🔝 TOP 10 MOST IMPORTANT FEATURES (Price Prediction):")
for i, row in feature_importance.head(10).iterrows():
    print(f"   {row.name+1:2d}. {row['feature']:40s} {row['importance']*100:6.2f}%")

# Check for overfitting
if train_r2 - test_r2 > 0.05:
    print(f"\n⚠️  WARNING: Possible overfitting detected!")
    print(f"   • Train R²: {train_r2:.4f}")
    print(f"   • Test R²:  {test_r2:.4f}")
    print(f"   • Difference: {(train_r2 - test_r2)*100:.2f}%")
else:
    print(f"\n✅ Model generalization looks good (no significant overfitting)")

# ============================================================================
# STEP 8: TRAIN DELAY PREDICTION MODEL
# ============================================================================

print(f"\n🎯 STEP 8: Training Delay Prediction Model (RandomForestClassifier)...")
print("-" * 80)
print(f"⚙️  Model configuration:")
for key, value in DELAY_MODEL_PARAMS.items():
    print(f"   • {key}: {value}")

delay_model = RandomForestClassifier(**DELAY_MODEL_PARAMS)

print(f"\n🔄 Training in progress...")
delay_model.fit(X_train_delay, y_train_delay)

print(f"✅ Delay model training completed!")
print(f"   • Model type: {type(delay_model).__name__}")
print(f"   • Number of trees: {delay_model.n_estimators}")
print(f"   • Number of features: {delay_model.n_features_in_}")

# ============================================================================
# STEP 9: EVALUATE DELAY PREDICTION MODEL
# ============================================================================

print(f"\n📊 STEP 9: Evaluating Delay Prediction Model...")
print("-" * 80)

# Predictions
y_train_delay_pred = delay_model.predict(X_train_delay)
y_test_delay_pred = delay_model.predict(X_test_delay)

# Test metrics
test_accuracy = accuracy_score(y_test_delay, y_test_delay_pred)
test_precision = precision_score(y_test_delay, y_test_delay_pred)
test_recall = recall_score(y_test_delay, y_test_delay_pred)
test_f1 = f1_score(y_test_delay, y_test_delay_pred)

print(f"📊 TEST SET PERFORMANCE:")
print(f"   • Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%) ✅")
print(f"   • Precision: {test_precision:.4f} ({test_precision*100:.2f}%)")
print(f"   • Recall:    {test_recall:.4f} ({test_recall*100:.2f}%)")
print(f"   • F1-Score:  {test_f1:.4f} ({test_f1*100:.2f}%)")

# Confusion matrix
cm = confusion_matrix(y_test_delay, y_test_delay_pred)
print(f"\n📊 CONFUSION MATRIX:")
print(f"   {'':15s} Predicted On-time  Predicted Delayed")
print(f"   Actual On-time     {cm[0][0]:10,}        {cm[0][1]:10,}")
print(f"   Actual Delayed     {cm[1][0]:10,}        {cm[1][1]:10,}")

# Classification report
print(f"\n📋 DETAILED CLASSIFICATION REPORT:")
print(classification_report(y_test_delay, y_test_delay_pred, 
                          target_names=['On-time', 'Delayed']))

# Feature importance
delay_feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': delay_model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n🔝 TOP 10 MOST IMPORTANT FEATURES (Delay Prediction):")
for i, row in delay_feature_importance.head(10).iterrows():
    print(f"   {row.name+1:2d}. {row['feature']:40s} {row['importance']*100:6.2f}%")

# ============================================================================
# STEP 10: SAVE MODELS AND METADATA
# ============================================================================

print(f"\n💾 STEP 10: Saving models and metadata...")
print("-" * 80)

# Save price prediction model
joblib.dump(price_model, PRICE_MODEL_PATH)
model_size = os.path.getsize(PRICE_MODEL_PATH) / (1024 * 1024)
print(f"✅ Saved price model: {PRICE_MODEL_PATH}")
print(f"   • File size: {model_size:.2f} MB")

# Save delay prediction model (with feature columns)
delay_model_data = {
    'model': delay_model,
    'feature_columns': feature_columns
}
joblib.dump(delay_model_data, DELAY_MODEL_PATH)
delay_size = os.path.getsize(DELAY_MODEL_PATH) / (1024 * 1024)
print(f"✅ Saved delay model: {DELAY_MODEL_PATH}")
print(f"   • File size: {delay_size:.2f} MB")

# Save feature names
joblib.dump(feature_columns, FEATURE_NAMES_PATH)
print(f"✅ Saved feature names: {FEATURE_NAMES_PATH}")

# Save metadata
metadata = {
    'training_date': datetime.now().isoformat(),
    'dataset_file': DATA_FILE,
    'dataset_shape': df.shape,
    'clean_dataset_rows': len(df_encoded),
    'n_features': len(feature_columns),
    'feature_names': feature_columns,
    'test_size': TEST_SIZE,
    'random_state': RANDOM_STATE,
    'price_model': {
        'type': 'RandomForestRegressor',
        'params': PRICE_MODEL_PARAMS,
        'metrics': {
            'train_r2': float(train_r2),
            'test_r2': float(test_r2),
            'test_rmse': float(test_rmse),
            'test_mae': float(test_mae),
            'test_mape': float(test_mape)
        },
        'top_features': feature_importance.head(10).to_dict()
    },
    'delay_model': {
        'type': 'RandomForestClassifier',
        'params': DELAY_MODEL_PARAMS,
        'metrics': {
            'test_accuracy': float(test_accuracy),
            'test_precision': float(test_precision),
            'test_recall': float(test_recall),
            'test_f1': float(test_f1)
        },
        'top_features': delay_feature_importance.head(10).to_dict()
    }
}

joblib.dump(metadata, METADATA_PATH)
print(f"✅ Saved metadata: {METADATA_PATH}")

# Create label encoders (for compatibility with old API)
label_encoders = {}
for col in categorical_features:
    le = LabelEncoder()
    le.fit(df[col].dropna())
    label_encoders[col] = le

joblib.dump(label_encoders, LABEL_ENCODERS_PATH)
print(f"✅ Saved label encoders: {LABEL_ENCODERS_PATH}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 80)
print(f"📅 Training finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n📊 FINAL MODEL SUMMARY:")
print(f"\n🎯 PRICE PREDICTION MODEL:")
print(f"   • R² Score: {test_r2:.4f} ({test_r2*100:.2f}%)")
print(f"   • RMSE: ₹{test_rmse:.2f}")
print(f"   • MAE: ₹{test_mae:.2f}")
print(f"   • Model size: {model_size:.2f} MB")
print(f"   • File: {PRICE_MODEL_PATH.name}")

print(f"\n⏰ DELAY PREDICTION MODEL:")
print(f"   • Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"   • F1-Score: {test_f1:.4f} ({test_f1*100:.2f}%)")
print(f"   • Precision: {test_precision:.4f}")
print(f"   • Recall: {test_recall:.4f}")
print(f"   • Model size: {delay_size:.2f} MB")
print(f"   • File: {DELAY_MODEL_PATH.name}")

print(f"\n📦 SAVED FILES:")
print(f"   1. {PRICE_MODEL_PATH.name} ({model_size:.2f} MB)")
print(f"   2. {DELAY_MODEL_PATH.name} ({delay_size:.2f} MB)")
print(f"   3. {LABEL_ENCODERS_PATH.name}")
print(f"   4. {FEATURE_NAMES_PATH.name}")
print(f"   5. {METADATA_PATH.name}")

print(f"\n🚀 NEXT STEPS:")
print(f"   1. Start FastAPI backend: cd api && uvicorn app:app --reload")
print(f"   2. Test prediction endpoint: POST http://localhost:8000/predict")
print(f"   3. Check health: GET http://localhost:8000/health")

print("=" * 80)
