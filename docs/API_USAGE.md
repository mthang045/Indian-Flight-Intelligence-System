# API Usage Guide - Unified /predict Endpoint

## 🎯 Overview

Đây là API hoàn chỉnh cho dự đoán giá vé máy bay và xác suất delay, sử dụng FastAPI + MongoDB + Machine Learning Models với Label Encoders.

## ✨ Features

✅ **Complete FastAPI Integration**
- Kết nối MongoDB bằng Motor (async driver)
- Load `flight_model.pkl` và `label_encoders.pkl` khi khởi động
- Endpoint `/predict` nhận JSON input đơn giản
- Transform input tự động bằng label encoders
- Predict cả **giá vé** và **xác suất delay**
- Lưu kết quả prediction vào MongoDB để tracking
- Trả về kết quả dạng JSON

## 🚀 Quick Start

### 1. Khởi động MongoDB (nếu chưa chạy)

```powershell
# Kiểm tra MongoDB đang chạy
mongosh

# Nếu chưa có, start MongoDB service
# Windows: Services -> MongoDB Server -> Start
```

### 2. Khởi động FastAPI Server

```powershell
cd api
uvicorn app:app --reload --port 8000
```

Server sẽ chạy tại: http://localhost:8000

### 3. Kiểm tra Health

```powershell
curl http://localhost:8000/health
```

Hoặc mở browser: http://localhost:8000/docs

### 4. Test Endpoint

```powershell
python test_predict_endpoint.py
```

## 📡 API Endpoints

### POST /predict - Unified Prediction Endpoint

**URL**: `http://localhost:8000/predict`

**Method**: `POST`

**Headers**: `Content-Type: application/json`

**Request Body**:
```json
{
  "airline": "IndiGo",
  "source": "Delhi",
  "destination": "Mumbai",
  "date": "2024-06-15",
  "departure_time": "Morning",
  "arrival_time": "Afternoon",
  "stops": 0,
  "flight_class": "Economy",
  "duration_minutes": 135,
  "days_left": 30
}
```

**Response**:
```json
{
  "predicted_price": 4850.75,
  "confidence_score": 87.5,
  "price_range": {
    "min": 4268.66,
    "max": 5432.84
  },
  "delay_probability": 35.20,
  "delay_status": "On-time",
  "delay_risk": "Low",
  "saved_id": "665a1b2c3d4e5f6g7h8i9j0k",
  "timestamp": "2024-06-01T10:30:00.000Z",
  "input_data": {
    "airline": "IndiGo",
    "source": "Delhi",
    "destination": "Mumbai",
    ...
  }
}
```

## 📋 Request Parameters

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `airline` | `string` | ✅ Yes | Airline name | `"IndiGo"`, `"Air India"`, `"SpiceJet"`, `"Vistara"`, `"AirAsia"`, `"GO_FIRST"` |
| `source` | `string` | ✅ Yes | Origin city | `"Delhi"`, `"Mumbai"`, `"Bangalore"`, `"Chennai"`, `"Kolkata"`, `"Hyderabad"` |
| `destination` | `string` | ✅ Yes | Destination city | Same as source cities |
| `date` | `string` | ✅ Yes | Journey date (YYYY-MM-DD) | `"2024-06-15"` |
| `departure_time` | `string` | ❌ No | Departure period | `"Morning"`, `"Afternoon"`, `"Evening"`, `"Night"` (default: `"Morning"`) |
| `arrival_time` | `string` | ❌ No | Arrival period | Same as departure_time (default: `"Afternoon"`) |
| `stops` | `integer` | ❌ No | Number of stops | `0` (non-stop), `1`, `2` (default: `0`) |
| `flight_class` | `string` | ❌ No | Flight class | `"Economy"`, `"Business"` (default: `"Economy"`) |
| `duration_minutes` | `integer` | ❌ No | Flight duration | `135` (default: `120`) |
| `days_left` | `integer` | ❌ No | Days until departure | `30` (default: `30`) |

## 📊 Response Fields

### Price Prediction
- `predicted_price`: Giá vé dự đoán (INR)
- `confidence_score`: Độ tin cậy của dự đoán (0-100%)
- `price_range`: Khoảng giá tối thiểu và tối đa

### Delay Prediction
- `delay_probability`: Xác suất bị delay (0-100%)
- `delay_status`: Trạng thái dự đoán (`"On-time"` hoặc `"Delayed"`)
- `delay_risk`: Mức độ rủi ro delay (`"Low"`, `"Medium"`, `"High"`)

### Metadata
- `saved_id`: ID của prediction đã lưu trong MongoDB
- `timestamp`: Thời gian thực hiện prediction
- `input_data`: Echo lại input data

## 🧪 cURL Examples

### Example 1: IndiGo Delhi → Mumbai (Economy)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "IndiGo",
    "source": "Delhi",
    "destination": "Mumbai",
    "date": "2024-06-15",
    "departure_time": "Morning",
    "arrival_time": "Afternoon",
    "stops": 0,
    "flight_class": "Economy",
    "duration_minutes": 135,
    "days_left": 30
  }'
```

### Example 2: Air India Bangalore → Delhi (Business)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "Air India",
    "source": "Bangalore",
    "destination": "Delhi",
    "date": "2024-07-10",
    "departure_time": "Evening",
    "arrival_time": "Night",
    "stops": 0,
    "flight_class": "Business",
    "duration_minutes": 165,
    "days_left": 45
  }'
```

### Example 3: SpiceJet with 1 stop (Budget)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "SpiceJet",
    "source": "Chennai",
    "destination": "Kolkata",
    "date": "2024-06-20",
    "departure_time": "Afternoon",
    "arrival_time": "Evening",
    "stops": 1,
    "flight_class": "Economy",
    "duration_minutes": 180,
    "days_left": 15
  }'
```

## 🐍 Python Example

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "airline": "IndiGo",
    "source": "Delhi",
    "destination": "Mumbai",
    "date": "2024-06-15",
    "departure_time": "Morning",
    "arrival_time": "Afternoon",
    "stops": 0,
    "flight_class": "Economy",
    "duration_minutes": 135,
    "days_left": 30
}

response = requests.post(url, json=data)
result = response.json()

print(f"💰 Predicted Price: ₹{result['predicted_price']:,.2f}")
print(f"⏰ Delay Probability: {result['delay_probability']}%")
print(f"📌 Delay Risk: {result['delay_risk']}")
print(f"💾 Saved ID: {result['saved_id']}")
```

## 📁 File Structure

```
Khai Thác Dữ Liệu/
├── api/
│   ├── app.py                    # Main FastAPI application
│   ├── models.py                 # Pydantic models
│   ├── database.py               # MongoDB connection
│   ├── flight_model.pkl          # Trained price prediction model
│   ├── label_encoders.pkl        # Label encoders for categorical variables
│   └── delay_model.pkl           # Trained delay prediction model
├── airlines_flights_data.csv     # Raw training data
├── train.py                      # Model training script
├── test_predict_endpoint.py      # Endpoint testing script
└── API_USAGE.md                  # This file
```

## 🔍 How It Works

### 1. **Model Loading (Startup)**
```python
@app.on_event("startup")
async def startup_db_client():
    # Load models và encoders
    ml_model = joblib.load("flight_model.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    delay_model_data = joblib.load("delay_model.pkl")
```

### 2. **Input Transformation**
```python
def transform_simple_input_with_encoders(request):
    # Parse date
    day, month, year = parse_date(request.date)
    
    # Create features DataFrame
    df = pd.DataFrame([{
        'airline': request.airline,
        'source_city': request.source,
        'destination_city': request.destination,
        'days_left': request.days_left,
        ...
    }])
    
    # One-hot encoding
    df_encoded = pd.get_dummies(df, columns=['airline', 'source_city', ...])
    
    return df_encoded
```

### 3. **Price Prediction**
```python
predicted_price = ml_model.predict(input_df)[0]
```

### 4. **Delay Prediction**
```python
delay_probability = delay_model.predict_proba(input_df)[0][1]
delay_status = 'Delayed' if delay_probability > 0.5 else 'On-time'
```

### 5. **MongoDB Storage**
```python
prediction_doc = {
    "input_data": request.model_dump(),
    "predicted_price": predicted_price,
    "delay_probability": delay_probability,
    ...
}
await collection.insert_one(prediction_doc)
```

## 🎯 Key Features

### ✅ Label Encoders Integration
- **Automatic transformation**: Không cần hardcode mappings
- **Dynamic encoding**: airlines, cities, times tự động được encode
- **Production-ready**: Backend hiểu được "IndiGo", "Delhi" mà không cần tra cứu dictionary

### ✅ Unified Response
- **Single endpoint** cho cả price và delay prediction
- **Complete information** trong một API call
- **MongoDB tracking** của mọi prediction

### ✅ Error Handling
- Model not loaded → HTTP 503
- Invalid input → HTTP 422 (Pydantic validation)
- Prediction errors → HTTP 500 với chi tiết

## 🛠️ Troubleshooting

### Error: "Price prediction model not loaded"
```
Solution: Đảm bảo file flight_model.pkl tồn tại trong thư mục api/
Check: ls api/flight_model.pkl
```

### Error: "Label encoders not loaded"
```
Solution: Chạy train.py để tạo label_encoders.pkl
Command: python train.py
```

### Error: "MongoDB connection failed"
```
Solution: Đảm bảo MongoDB đang chạy
Check: mongosh
Start: Services -> MongoDB Server -> Start
```

### Error: Import errors
```
Solution: Install dependencies
Command: pip install fastapi motor pymongo scikit-learn pandas joblib
```

## 📚 Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🎓 Training Models

Nếu muốn train lại models:

```powershell
python train.py
```

Script này sẽ:
1. Load `airlines_flights_data.csv`
2. Feature engineering
3. Tạo và lưu `label_encoders.pkl`
4. Train RandomForestRegressor
5. Lưu `flight_model.pkl`, `label_encoders.pkl`, metadata

## 💡 Tips

1. **Booking Timing**: `days_left` càng nhỏ → giá càng cao
2. **Airline Choice**: IndiGo và SpiceJet thường rẻ hơn Air India và Vistara
3. **Flight Class**: Business có thể đắt gấp 2-3 lần Economy
4. **Stops**: Non-stop flights thường đắt hơn nhưng delay ít hơn
5. **Time Period**: Morning flights thường đúng giờ hơn Evening/Night

## 📞 Support

Nếu gặp vấn đề:
1. Check logs khi start FastAPI server
2. Verify models exist: `ls api/*.pkl`
3. Test MongoDB: `mongosh`
4. Check API docs: http://localhost:8000/docs

---

**Created by**: Flight Price Prediction Team  
**Version**: 1.0  
**Last Updated**: June 2024
