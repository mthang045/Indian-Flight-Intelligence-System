"""
Script Huấn Luyện Model Dự Đoán Giá Vé Máy Bay
Tạo flight_model.pkl và lưu encoder để sử dụng trong backend
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("🚀 HUẤN LUYỆN MODEL Dự ĐOÁN GIÁ VÉ MÁY BAY")
print("=" * 80)
print()

# ============================================================================
# BƯỚC 1: TẢI VÀ CHUẨN BỊ DỮ LIỆU
# ============================================================================
print("📊 BƯỚC 1: Tải dữ liệu...")
df = pd.read_csv('../data/airlines_flights_data.csv')
print(f"   ✅ Đã tải: {df.shape[0]:,} dòng, {df.shape[1]} cột")
print(f"   📋 Các cột: {df.columns.tolist()}")
print()

# Kiểm tra missing values
missing = df.isnull().sum()
if missing.sum() > 0:
    print(f"   ⚠️  Có {missing.sum()} giá trị thiếu")
    df = df.dropna()
    print(f"   ✅ Đã xóa, còn lại: {df.shape[0]:,} dòng")
else:
    print("   ✅ Không có giá trị thiếu")
print()

# ============================================================================
# BƯỚC 2: XỬ LÝ VÀ TẠO FEATURES
# ============================================================================
print("🔧 BƯỚC 2: Xử lý và tạo features...")

# 2.1 Tạo thông tin ngày tháng từ days_left
current_date = datetime.now()
df['journey_date'] = pd.to_datetime(current_date) + pd.to_timedelta(df['days_left'], unit='D')
df['day'] = df['journey_date'].dt.day
df['month'] = df['journey_date'].dt.month
df['year'] = df['journey_date'].dt.year
print("   ✅ Đã tạo: day, month, year")

# 2.2 Chuyển duration sang phút
df['duration_minutes'] = (df['duration'] * 60).round().astype(int)
print(f"   ✅ Duration: {df['duration_minutes'].min()} - {df['duration_minutes'].max()} phút")

# 2.3 Xử lý price
df['price_clean'] = pd.to_numeric(df['price'], errors='coerce')
print(f"   ✅ Price: ₹{df['price_clean'].min():,.0f} - ₹{df['price_clean'].max():,.0f}")

# 2.4 Xử lý stops
if df['stops'].dtype == 'object':
    df['stops_numeric'] = df['stops'].str.extract(r'(\d+)').fillna(0).astype(int)
else:
    df['stops_numeric'] = df['stops']
print("   ✅ Đã xử lý stops")

# 2.5 Trích xuất giờ khởi hành và đến
df['departure_hour'] = pd.to_datetime(df['departure_time'], format='%H:%M:%S', errors='coerce').dt.hour
df['arrival_hour'] = pd.to_datetime(df['arrival_time'], format='%H:%M:%S', errors='coerce').dt.hour

# Phân loại khung giờ
def get_time_category(hour):
    if pd.isna(hour):
        return 'Unknown'
    elif hour < 6:
        return 'Night'
    elif hour < 12:
        return 'Morning'
    elif hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'

df['departure_period'] = df['departure_hour'].apply(get_time_category)
df['arrival_period'] = df['arrival_hour'].apply(get_time_category)
print("   ✅ Đã tạo: departure_hour, arrival_hour, departure_period, arrival_period")
print()

# ============================================================================
# BƯỚC 3: TẠO VÀ LƯU ENCODERS (QUAN TRỌNG CHO BACKEND!)
# ============================================================================
print("🔐 BƯỚC 3: Tạo và lưu Label Encoders (Cho Backend)...")
print()

# Dictionary lưu tất cả encoders
encoders = {}

# Các cột cần encode
categorical_columns = ['airline', 'source_city', 'destination_city', 'class', 
                       'departure_time', 'arrival_time', 'departure_period', 'arrival_period']

for col in categorical_columns:
    if col in df.columns:
        le = LabelEncoder()
        le.fit(df[col].astype(str))
        encoders[col] = le
        print(f"   ✅ {col:20s} → {len(le.classes_)} giá trị: {le.classes_[:3].tolist()}...")

# Encoder cho stops
le_stops = LabelEncoder()
le_stops.fit(df['stops'].astype(str))
encoders['stops'] = le_stops
print(f"   ✅ {'stops':20s} → {len(le_stops.classes_)} giá trị: {le_stops.classes_.tolist()}")

# Lưu encoders
models_dir = Path('../models')
api_dir = Path('../api')
models_dir.mkdir(exist_ok=True)
api_dir.mkdir(exist_ok=True)

# Lưu tất cả encoders vào một file
joblib.dump(encoders, models_dir / 'label_encoders.pkl')
joblib.dump(encoders, api_dir / 'label_encoders.pkl')
print()
print(f"   💾 Đã lưu: models/label_encoders.pkl")
print(f"   💾 Đã lưu: api/label_encoders.pkl")
print()

# ============================================================================
# BƯỚC 4: ONE-HOT ENCODING
# ============================================================================
print("🎯 BƯỚC 4: Thực hiện One-Hot Encoding...")

# Select columns for encoding
encode_cols = ['airline', 'source_city', 'destination_city', 'class', 
               'departure_period', 'arrival_period']

df_encoded = pd.get_dummies(df, columns=encode_cols, prefix=encode_cols)
print(f"   ✅ Shape sau encoding: {df_encoded.shape}")
print()

# ============================================================================
# BƯỚC 5: CHUẨN BỊ FEATURES VÀ TARGET
# ============================================================================
print("📋 BƯỚC 5: Chuẩn bị features và target...")

# Các cột cần drop
drop_columns = ['index', 'flight', 'departure_time', 'arrival_time', 
                'stops', 'duration', 'price', 'journey_date']

# Features: tất cả trừ price_clean và các cột không cần thiết
X = df_encoded.drop(columns=drop_columns + ['price_clean'], errors='ignore')
y = df_encoded['price_clean']

print(f"   ✅ Số features: {X.shape[1]}")
print(f"   ✅ Số samples: {X.shape[0]:,}")
print(f"   ✅ Target range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
print(f"   ✅ Target mean: ₹{y.mean():,.2f}")
print()

# Lưu tên cột features để sử dụng sau
feature_names = X.columns.tolist()
joblib.dump(feature_names, models_dir / 'feature_names.pkl')
joblib.dump(feature_names, api_dir / 'feature_names.pkl')
print(f"   💾 Đã lưu: models/feature_names.pkl & api/feature_names.pkl")
print()

# ============================================================================
# BƯỚC 6: CHIA DỮ LIỆU TRAIN/TEST
# ============================================================================
print("✂️  BƯỚC 6: Chia dữ liệu train/test (80-20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"   ✅ Train: {X_train.shape[0]:,} samples")
print(f"   ✅ Test:  {X_test.shape[0]:,} samples")
print()

# ============================================================================
# BƯỚC 7: HUẤN LUYỆN MODEL
# ============================================================================
print("🤖 BƯỚC 7: Huấn luyện RandomForestRegressor...")
print()

# Tạo model với hyperparameters tối ưu
model = RandomForestRegressor(
    n_estimators=150,        # Từ kết quả optimization
    max_depth=None,          # Không giới hạn độ sâu
    min_samples_split=2,
    min_samples_leaf=6,
    max_features=None,       # Sử dụng tất cả features
    bootstrap=True,
    random_state=42,
    n_jobs=-1,               # Sử dụng tất cả CPU cores
    verbose=1
)

print("   ⚙️  Hyperparameters:")
print(f"      • n_estimators: {model.n_estimators}")
print(f"      • max_depth: {model.max_depth}")
print(f"      • min_samples_split: {model.min_samples_split}")
print(f"      • min_samples_leaf: {model.min_samples_leaf}")
print()

# Huấn luyện
print("   🔄 Đang huấn luyện...")
import time
start_time = time.time()
model.fit(X_train, y_train)
training_time = time.time() - start_time
print(f"   ✅ Hoàn thành trong {training_time:.2f} giây")
print()

# ============================================================================
# BƯỚC 8: ĐÁNH GIÁ MODEL
# ============================================================================
print("=" * 80)
print("📊 BƯỚC 8: ĐÁNH GIÁ MODEL")
print("=" * 80)
print()

# Dự đoán
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Metrics cho training set
train_r2 = r2_score(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))

# Metrics cho test set
test_r2 = r2_score(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

print("📈 KẾT QUẢ HUẤN LUYỆN:")
print()
print("   Training Set:")
print(f"      • R² Score:  {train_r2:.6f} ({train_r2*100:.2f}%)")
print(f"      • MAE:       ₹{train_mae:,.2f}")
print(f"      • RMSE:      ₹{train_rmse:,.2f}")
print()
print("   Test Set:")
print(f"      • R² Score:  {test_r2:.6f} ({test_r2*100:.2f}%)")
print(f"      • MAE:       ₹{test_mae:,.2f}")
print(f"      • RMSE:      ₹{test_rmse:,.2f}")
print()

# Kiểm tra overfitting
diff = abs(train_r2 - test_r2)
if diff < 0.05:
    print(f"   ✅ Model không bị overfitting (Diff: {diff:.4f})")
else:
    print(f"   ⚠️  Có thể bị overfitting (Diff: {diff:.4f})")
print()

# Top features
print("🏆 TOP 10 FEATURES QUAN TRỌNG NHẤT:")
print()
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for i, (idx, row) in enumerate(feature_importance.head(10).iterrows(), 1):
    percentage = row['importance'] * 100
    bar = '█' * int(percentage / 2)
    print(f"   {i:2d}. {row['feature']:35s} {bar:30s} {percentage:5.2f}%")
print()

# ============================================================================
# BƯỚC 9: LƯU MODEL
# ============================================================================
print("=" * 80)
print("💾 BƯỚC 9: LƯU MODEL")
print("=" * 80)
print()

# Lưu vào thư mục models
model_path = models_dir / 'flight_model.pkl'
joblib.dump(model, model_path)
print(f"   ✅ Đã lưu: models/flight_model.pkl")

# Lưu vào thư mục api
api_model_path = api_dir / 'flight_model.pkl'
joblib.dump(model, api_model_path)
print(f"   ✅ Đã lưu: api/flight_model.pkl")
print()

# Lưu thông tin metadata
metadata = {
    'model_type': 'RandomForestRegressor',
    'n_estimators': model.n_estimators,
    'train_samples': len(X_train),
    'test_samples': len(X_test),
    'n_features': len(feature_names),
    'train_r2': train_r2,
    'test_r2': test_r2,
    'train_mae': train_mae,
    'test_mae': test_mae,
    'training_time_seconds': training_time,
    'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

metadata_path = models_dir / 'model_metadata.pkl'
joblib.dump(metadata, metadata_path)
joblib.dump(metadata, api_dir / 'model_metadata.pkl')
print(f"   💾 Đã lưu: models/model_metadata.pkl & api/model_metadata.pkl")
print()

# ============================================================================
# BƯỚC 10: KIỂM TRA VÍ DỤ
# ============================================================================
print("=" * 80)
print("🧪 BƯỚC 10: KIỂM TRA VÍ DỤ")
print("=" * 80)
print()

# Lấy 3 mẫu ngẫu nhiên từ test set
sample_indices = np.random.choice(len(X_test), 3, replace=False)

print("Dự đoán giá vé cho 3 chuyến bay mẫu:")
print()

for i, idx in enumerate(sample_indices, 1):
    actual = y_test.iloc[idx]
    predicted = y_test_pred[idx]
    error = abs(actual - predicted)
    error_pct = (error / actual) * 100
    
    print(f"   Mẫu {i}:")
    print(f"      • Giá thực tế:  ₹{actual:,.2f}")
    print(f"      • Giá dự đoán:  ₹{predicted:,.2f}")
    print(f"      • Sai số:       ₹{error:,.2f} ({error_pct:.2f}%)")
    print()

# ============================================================================
# KẾT THÚC
# ============================================================================
print("=" * 80)
print("✅ HOÀN THÀNH!")
print("=" * 80)
print()
print("📁 CÁC FILE ĐÃ TẠO:")
print()
print("   Thư mục gốc:")
print(f"      ✓ flight_model.pkl          - Model đã huấn luyện")
print(f"      ✓ label_encoders.pkl        - Encoders cho categorical data")
print(f"      ✓ feature_names.pkl         - Danh sách tên features")
print(f"      ✓ model_metadata.pkl        - Thông tin metadata")
print()
print("   Thư mục api/:")
print(f"      ✓ api/flight_model.pkl      - Model (cho backend)")
print(f"      ✓ api/label_encoders.pkl    - Encoders (cho backend)")
print(f"      ✓ api/feature_names.pkl     - Features (cho backend)")
print(f"      ✓ api/model_metadata.pkl    - Metadata (cho backend)")
print()
print("📊 KẾT QUẢ TÓM TẮT:")
print(f"   • Độ chính xác test: {test_r2*100:.2f}%")
print(f"   • Sai số trung bình: ₹{test_mae:,.2f}")
print(f"   • Số features: {len(feature_names)}")
print(f"   • Số encoders: {len(encoders)}")
print()
print("💡 QUAN TRỌNG:")
print("   Backend CẦN cả 3 file để hoạt động:")
print("   1. flight_model.pkl     → Dự đoán giá")
print("   2. label_encoders.pkl   → Chuyển 'IndiGo', 'Delhi' thành số")
print("   3. feature_names.pkl    → Đảm bảo đúng thứ tự features")
print()
print("🚀 SẴN SÀNG TÍCH HỢP VÀO FASTAPI!")
print("=" * 80)
