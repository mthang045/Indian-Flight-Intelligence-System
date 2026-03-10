# Hướng Dẫn Tích Hợp Label Encoders

## 📋 Tổng Quan

Hướng dẫn này trình bày cách sử dụng các label encoder đã được tạo và lưu bằng joblib. Các encoder này cho phép bạn mã hóa biến phân loại một cách nhất quán cho dự đoán thời gian thực trong backend FastAPI.

## 📁 Các File Đã Tạo

### Thư Mục Gốc:
- `save_label_encoders.py` - Script tạo và lưu encoders
- `label_encoders.pkl` - Tất cả encoders trong một file (2.59 KB)
- `airline_encoder.pkl` - Encoder hãng hàng không (0.52 KB)
- `source_city_encoder.pkl` - Encoder thành phố xuất phát (0.52 KB)
- `destination_city_encoder.pkl` - Encoder thành phố đích (0.52 KB)
- `class_encoder.pkl` - Encoder hạng vé (0.48 KB)
- `departure_time_encoder.pkl` - Encoder giờ khởi hành (0.53 KB)
- `arrival_time_encoder.pkl` - Encoder giờ đến (0.53 KB)
- `departure_period_encoder.pkl` - Encoder khung giờ khởi hành (0.47 KB)
- `arrival_period_encoder.pkl` - Encoder khung giờ đến (0.47 KB)
- `stops_encoder.pkl` - Encoder số điểm dừng (0.49 KB)

### Thư Mục API:
- `api/encoders.py` - Module hỗ trợ với các hàm tiện ích
- `api/app_with_encoders_example.py` - Ví dụ tích hợp FastAPI
- `api/label_encoders.pkl` - Tất cả encoders (bản sao cho API)
- `api/*_encoder.pkl` - Bản sao các encoder riêng lẻ

## 🔧 Bảng Ánh Xạ Encoder

### Hãng Hàng Không (6 giá trị):
```python
['AirAsia', 'Air_India', 'GO_FIRST', 'Indigo', 'SpiceJet', 'Vistara']
# Indigo → 3
# Vistara → 5
# AirAsia → 0
```

### Thành Phố (6 giá trị):
```python
['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai']
# Delhi → 2
# Mumbai → 5
# Bangalore → 0
```

### Hạng Vé (2 giá trị):
```python
['Business', 'Economy']
# Business → 0
# Economy → 1
```

### Khung Giờ (6 giá trị):
```python
['Afternoon', 'Early_Morning', 'Evening', 'Late_Night', 'Morning', 'Night']
```

### Điểm Dừng (3 giá trị):
```python
['one', 'two_or_more', 'zero']
```

## 🚀 Bắt Đầu Nhanh

### 1. Tải Tất Cả Encoders Cùng Lúc

```python
import joblib

# Tải tất cả encoders từ một file
encoders = joblib.load('api/label_encoders.pkl')

# Truy cập các encoder riêng lẻ
airline_encoder = encoders['airline']
source_encoder = encoders['source_city']
class_encoder = encoders['class']
```

### 2. Tải Encoder Riêng Lẻ

```python
import joblib

# Tải encoder cụ thể
airline_encoder = joblib.load('api/airline_encoder.pkl')

# Mã hóa một giá trị
encoded = airline_encoder.transform(['Indigo'])[0]  # Trả về: 3

# Giải mã ngược lại
decoded = airline_encoder.inverse_transform([3])[0]  # Trả về: 'Indigo'
```

### 3. Sử Dụng Module Hỗ Trợ

```python
from encoders import (
    load_encoders, 
    encode_categorical, 
    decode_categorical,
    validate_categorical_value,
    get_encoder_classes
)

# Tải encoders (tự động cache)
encoders = load_encoders()

# Mã hóa dữ liệu đầu vào
input_data = {
    'airline': 'Indigo',
    'source_city': 'Delhi',
    'destination_city': 'Mumbai',
    'class': 'Economy',
    'duration_minutes': 150
}

encoded = encode_categorical(input_data, ['airline', 'source_city', 'destination_city', 'class'])
# Kết quả: {'airline': 3, 'source_city': 2, 'destination_city': 5, 'class': 1, 'duration_minutes': 150}

# Kiểm tra trước khi mã hóa
is_valid = validate_categorical_value('airline', 'Indigo')  # True
is_valid = validate_categorical_value('airline', 'FakeAir')  # False

# Lấy tất cả giá trị có thể
airlines = get_encoder_classes('airline')
# Trả về: ['AirAsia', 'Air_India', 'GO_FIRST', 'Indigo', 'SpiceJet', 'Vistara']
```

## 🎯 Tích Hợp FastAPI

### Phương Án 1: Tích Hợp Cơ Bản trong app.py

```python
from fastapi import FastAPI, HTTPException
import joblib
from pathlib import Path

app = FastAPI()

# Biến toàn cục cho encoders
label_encoders = None

@app.on_event("startup")
async def startup_event():
    global label_encoders
    
    # Tải encoders
    encoder_path = Path(__file__).parent / 'label_encoders.pkl'
    label_encoders = joblib.load(encoder_path)
    print(f"✅ Đã tải {len(label_encoders)} encoders")

@app.post("/predict")
async def predict(airline: str, source_city: str, destination_city: str, flight_class: str):
    # Kiểm tra đầu vào
    if airline not in label_encoders['airline'].classes_:
        raise HTTPException(400, f"Hãng không hợp lệ. Hợp lệ: {label_encoders['airline'].classes_.tolist()}")
    
    # Mã hóa đầu vào
    airline_encoded = label_encoders['airline'].transform([airline])[0]
    source_encoded = label_encoders['source_city'].transform([source_city])[0]
    dest_encoded = label_encoders['destination_city'].transform([destination_city])[0]
    class_encoded = label_encoders['class'].transform([flight_class])[0]
    
    # Sử dụng giá trị đã mã hóa để dự đoán
    # ... logic dự đoán của bạn ở đây
    
    return {"encoded_airline": int(airline_encoded), "encoded_source": int(source_encoded)}
```

### Phương Án 2: Sử Dụng Module Hỗ Trợ

```python
from fastapi import FastAPI, HTTPException
from encoders import load_encoders, encode_categorical, validate_categorical_value

app = FastAPI()

# Tải encoders khi khởi động
label_encoders = None

@app.on_event("startup")
async def startup_event():
    global label_encoders
    label_encoders = load_encoders()

@app.post("/predict")
async def predict(
    airline: str, 
    source_city: str, 
    destination_city: str, 
    flight_class: str,
    duration_minutes: int,
    days_left: int
):
    # Kiểm tra đầu vào
    for field, value in [('airline', airline), ('source_city', source_city), 
                         ('destination_city', destination_city), ('class', flight_class)]:
        if not validate_categorical_value(field, value):
            raise HTTPException(
                400, 
                f"{field} không hợp lệ: '{value}'. Hợp lệ: {label_encoders[field].classes_.tolist()}"
            )
    
    # Mã hóa tất cả các trường phân loại
    input_data = {
        'airline': airline,
        'source_city': source_city,
        'destination_city': destination_city,
        'class': flight_class,
        'duration_minutes': duration_minutes,
        'days_left': days_left
    }
    
    encoded = encode_categorical(
        input_data, 
        ['airline', 'source_city', 'destination_city', 'class']
    )
    
    # Sử dụng giá trị đã mã hóa để dự đoán
    # ... dự đoán model ML của bạn ở đây
    
    return {"encoded_data": encoded}
```

## 📊 Ví Dụ Đầy Đủ Với Kiểm Tra

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from encoders import load_encoders, encode_categorical, get_encoder_classes
import joblib

app = FastAPI()

# Tải encoders và model khi khởi động
model = None
encoders = None

@app.on_event("startup")
async def startup():
    global model, encoders
    model = joblib.load('api/flight_model.pkl')
    encoders = load_encoders()

class PredictionRequest(BaseModel):
    airline: str
    source_city: str
    destination_city: str
    flight_class: str
    departure_time: str
    arrival_time: str
    stops: str
    duration_minutes: int
    days_left: int
    
    @validator('airline')
    def validate_airline(cls, v):
        valid = get_encoder_classes('airline')
        if v not in valid:
            raise ValueError(f"Hãng không hợp lệ. Hợp lệ: {valid}")
        return v
    
    @validator('source_city', 'destination_city')
    def validate_city(cls, v):
        valid = get_encoder_classes('source_city')
        if v not in valid:
            raise ValueError(f"Thành phố không hợp lệ. Hợp lệ: {valid}")
        return v
    
    @validator('flight_class')
    def validate_class(cls, v):
        valid = get_encoder_classes('class')
        if v not in valid:
            raise ValueError(f"Hạng không hợp lệ. Hợp lệ: {valid}")
        return v

@app.post("/predict")
async def predict(request: PredictionRequest):
    # Chuyển sang dict và mã hóa các trường phân loại
    data = request.dict()
    encoded = encode_categorical(
        data,
        ['airline', 'source_city', 'destination_city', 'flight_class', 
         'departure_time', 'arrival_time', 'stops']
    )
    
    # Chuẩn bị features cho model (điều chỉnh theo định dạng model của bạn)
    # ... chuẩn bị feature vector hoặc DataFrame
    
    # Thực hiện dự đoán
    # prediction = model.predict(features)[0]
    
    return {
        "predicted_price": 15000.00,  # Thay bằng dự đoán thực tế
        "encoded_values": encoded
    }

@app.get("/valid-values")
async def get_valid_values():
    """Lấy tất cả giá trị phân loại hợp lệ cho frontend"""
    return {
        "airlines": get_encoder_classes('airline'),
        "cities": get_encoder_classes('source_city'),
        "classes": get_encoder_classes('class'),
        "time_periods": get_encoder_classes('departure_time'),
        "stops": get_encoder_classes('stops')
    }
```

## ⚠️ Lưu Ý Quan Trọng

### 1. **Thứ Tự Mã Hóa**
- Luôn mã hóa giá trị theo cùng thứ tự như khi huấn luyện
- Sử dụng CÙNG instance encoder để đảm bảo tính nhất quán

### 2. **Xử Lý Giá Trị Không Xác Định**
```python
# Luôn kiểm tra trước khi mã hóa để tránh lỗi
if value not in encoder.classes_:
    raise ValueError(f"Giá trị không xác định: {value}")
```

### 3. **One-Hot Encoding vs Label Encoding**
- Model hiện tại của bạn sử dụng **one-hot encoding** (qua `pd.get_dummies()`)
- Label encoders hữu ích cho:
  - Kiểm tra đầu vào
  - Tiền xử lý dữ liệu trước khi one-hot encoding
  - Các model chấp nhận số nguyên phân loại (như XGBoost)

### 4. **Tích Hợp Với Model Hiện Tại**
`flight_model.pkl` của bạn yêu cầu features đã được one-hot encoded. Để sử dụng label encoders:

```python
# 1. Mã hóa giá trị phân loại
encoded = encode_categorical(input_data, categorical_cols)

# 2. Áp dụng one-hot encoding để khớp với dữ liệu huấn luyện
import pandas as pd
df = pd.DataFrame([encoded])
df_encoded = pd.get_dummies(df, columns=categorical_cols)

# 3. Đảm bảo thứ tự cột khớp với huấn luyện
df_encoded = df_encoded.reindex(columns=training_columns, fill_value=0)

# 4. Dự đoán
prediction = model.predict(df_encoded)
```

## 🔄 Tạo Lại Encoders

Nếu bạn cập nhật dữ liệu hoặc cần tạo lại encoders:

```bash
python save_label_encoders.py
```

Script này sẽ:
1. Tải `airlines_flights_data.csv`
2. Fit LabelEncoders trên tất cả cột phân loại
3. Lưu các encoder riêng lẻ (*.pkl files)
4. Lưu encoders tổng hợp (label_encoders.pkl)
5. Sao chép tất cả file vào thư mục api/

## 📈 Kiểm Tra

Kiểm tra module encoder hỗ trợ:

```bash
cd api
python encoders.py
```

Script này chạy các kịch bản ví dụ hiển thị:
- Mã hóa dữ liệu đầu vào
- Giải mã giá trị đã mã hóa
- Lấy các danh mục hợp lệ
- Kiểm tra đầu vào

## 🎓 Thực Hành Tốt Nhất

1. **Luôn kiểm tra** đầu vào người dùng trước khi mã hóa
2. **Tải encoders một lần** khi khởi động (không phải mỗi request)
3. **Cache các lớp encoder** để kiểm tra
4. **Cung cấp thông báo lỗi hữu ích** với các tùy chọn hợp lệ
5. **Quản lý phiên bản** các file encoder cùng với model
6. **Cập nhật encoders** khi huấn luyện lại model với dữ liệu mới

## 📚 Tài Nguyên Bổ Sung

- `save_label_encoders.py` - Mã nguồn script
- `api/encoders.py` - Mã nguồn hàm hỗ trợ
- `api/app_with_encoders_example.py` - Ví dụ FastAPI đầy đủ
- Tài liệu sklearn LabelEncoder: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
