# 🚀 Full Stack Setup Guide - Flight Price Predictor

Hướng dẫn chi tiết để chạy toàn bộ ứng dụng dự đoán giá vé máy bay, bao gồm cả Backend (FastAPI) và Frontend (React + Vite).

---

## 📋 Mục lục

1. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
2. [Setup Backend (FastAPI)](#setup-backend-fastapi)
3. [Setup Frontend (React)](#setup-frontend-react)
4. [Chạy ứng dụng](#chạy-ứng-dụng)
5. [Kiểm tra kết nối](#kiểm-tra-kết-nối)
6. [Troubleshooting](#troubleshooting)

---

## 🛠️ Yêu cầu hệ thống

### Backend
- ✅ Python 3.12
- ✅ MongoDB (localhost:27017)
- ✅ Các file models: `flight_model.pkl`, `label_encoders.pkl`, `delay_model.pkl`

### Frontend
- ✅ Node.js 18+ (hoặc pnpm)
- ✅ npm/pnpm
- ✅ React 18.3.1

---

## 🔧 Setup Backend (FastAPI)

### Bước 1: Kiểm tra MongoDB

```powershell
# Mở MongoDB Shell để kiểm tra
mongosh

# Kiểm tra database
> show databases
> use flight_price_prediction
> show collections

# Thoát
> exit
```

### Bước 2: Cài đặt dependencies

```powershell
cd api
pip install -r requirements.txt
```

**requirements.txt** cần có:
```
fastapi==0.110.0
uvicorn==0.27.0
motor==3.3.2
pymongo==4.6.1
pandas==2.2.0
scikit-learn==1.4.0
joblib==1.3.2
pydantic==2.6.0
python-multipart==0.0.7
```

### Bước 3: Kiểm tra models tồn tại

```powershell
# Liệt kê tất cả files .pkl
ls *.pkl
```

Bạn cần có:
- ✅ `flight_model.pkl` (277 MB) - Price prediction model
- ✅ `label_encoders.pkl` (2.6 KB) - Label encoders
- ✅ `delay_model.pkl` (150 KB) - Delay prediction model

Nếu thiếu, chạy training script:
```powershell
cd ..
python train.py
```

### Bước 4: Khởi động FastAPI Server

```powershell
cd api
uvicorn app:app --reload --port 8000
```

**Output thành công:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
================================================================================
🚀 STARTING FASTAPI SERVER
================================================================================
✅ MongoDB connected!
✅ Price prediction model loaded from ...\flight_model.pkl
   • Model type: RandomForestRegressor
   • n_estimators: 150
   • n_features: 30
✅ Label encoders loaded from ...\label_encoders.pkl
   • Number of encoders: 9
   • Available encoders: ['airline', 'source_city', 'destination_city', ...]
✅ Delay prediction model loaded from ...\delay_model.pkl
================================================================================
✅ FastAPI server ready!
================================================================================
```

**API Endpoints:**
- 🌐 Swagger Docs: http://localhost:8000/docs
- 📝 ReDoc: http://localhost:8000/redoc
- ❤️ Health Check: http://localhost:8000/health
- 🎯 Predict Endpoint: http://localhost:8000/predict (POST)

---

## 🎨 Setup Frontend (React)

### Bước 1: Cài đặt dependencies

```powershell
# Mở terminal mới (giữ FastAPI chạy ở terminal cũ)
cd "C:\Users\buimi\OneDrive\Documents\Khai Thác Dữ Liệu"

# Cài đặt dependencies (bao gồm axios mới thêm)
npm install

# Hoặc nếu dùng pnpm
pnpm install
```

### Bước 2: Kiểm tra axios đã được cài

```powershell
# Kiểm tra package.json
cat package.json | Select-String "axios"
```

Output:
```
"axios": "^1.7.2",
```

### Bước 3: Khởi động React Dev Server

```powershell
npm run dev

# Hoặc
pnpm dev
```

**Output thành công:**
```
  VITE v6.3.5  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

Frontend sẽ chạy tại: http://localhost:5173

---

## 🚀 Chạy ứng dụng

### Terminal 1: Backend (FastAPI)
```powershell
cd api
uvicorn app:app --reload --port 8000
```

### Terminal 2: Frontend (React)
```powershell
npm run dev
```

### Terminal 3: Test API (Optional)
```powershell
python test_predict_endpoint.py
```

---

## ✅ Kiểm tra kết nối

### Test 1: Health Check

```powershell
curl http://localhost:8000/health
```

Hoặc mở browser: http://localhost:8000/health

### Test 2: API Prediction

```powershell
curl -X POST http://localhost:8000/predict `
  -H "Content-Type: application/json" `
  -d '{
    "airline": "IndiGo",
    "source": "Delhi",
    "destination": "Mumbai",
    "date": "2026-06-15",
    "stops": 0,
    "flight_class": "Economy",
    "duration_minutes": 135,
    "days_left": 30
  }'
```

### Test 3: Frontend Form

1. Mở http://localhost:5173
2. Điền form:
   - **Departure City**: Delhi
   - **Destination City**: Mumbai
   - **Travel Date**: Chọn ngày tương lai
   - **Airline**: IndiGo
   - **Class**: Economy
3. Click nút **"Dự đoán"** (Predict)

**Kết quả mong đợi:**

✅ **Price Prediction:**
- Giá vé INR: ₹4,850
- Giá VND: ≈ 1,455,000 ₫
- Price Range: Min - Max
- Confidence Score: 87.5%

✅ **Delay Prediction:**
- Delay Probability: 35.2%
- Status: On-time
- Risk Level: 🟢 Low Risk - Safe (màu xanh)

---

## 🐛 Troubleshooting

### ❌ Problem 1: "Cannot connect to server"

**Triệu chứng:**
```
Lỗi dự đoán
Không thể kết nối tới server. Vui lòng kiểm tra FastAPI đang chạy.
💡 Đảm bảo FastAPI đang chạy: cd api && uvicorn app:app --reload
```

**Giải pháp:**
1. Kiểm tra FastAPI có đang chạy không:
   ```powershell
   curl http://localhost:8000/health
   ```
2. Nếu không chạy, start lại:
   ```powershell
   cd api
   uvicorn app:app --reload --port 8000
   ```

---

### ❌ Problem 2: "Price prediction model not loaded"

**Triệu chứng:**
```json
{
  "detail": "Price prediction model not loaded. Please ensure flight_model.pkl exists."
}
```

**Giải pháp:**
```powershell
# Kiểm tra file tồn tại
ls api/flight_model.pkl

# Nếu không có, chạy training
python train.py
```

---

### ❌ Problem 3: "Label encoders not loaded"

**Triệu chứng:**
```json
{
  "detail": "Label encoders not loaded. Please ensure label_encoders.pkl exists."
}
```

**Giải pháp:**
```powershell
# Kiểm tra file
ls api/label_encoders.pkl

# Nếu không có, train lại
python train.py
```

---

### ❌ Problem 4: MongoDB Connection Error

**Triệu chứng:**
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017
```

**Giải pháp:**
```powershell
# Kiểm tra MongoDB service
Get-Service MongoDB

# Start MongoDB service
Start-Service MongoDB

# Hoặc dùng GUI: Services -> MongoDB Server -> Start
```

---

### ❌ Problem 5: CORS Error trong browser

**Triệu chứng:**
```
Access to XMLHttpRequest at 'http://localhost:8000/predict' from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Giải pháp:**
Đảm bảo `api/app.py` có CORS middleware:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production, chỉ định cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### ❌ Problem 6: Axios not found

**Triệu chứng:**
```
Module not found: Can't resolve 'axios'
```

**Giải pháp:**
```powershell
npm install axios

# Hoặc
pnpm add axios
```

---

### ❌ Problem 7: FastAPI startup errors

**Triệu chứng:**
```python
ImportError: cannot import name 'SimplePredictionRequest' from 'models'
```

**Giải pháp:**
Kiểm tra `api/models.py` có class `SimplePredictionRequest` và `SimplePredictionResponse`.

---

## 📊 API Response Format

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
  "timestamp": "2026-03-10T10:30:00.000Z",
  "input_data": {
    "airline": "IndiGo",
    "source": "Delhi",
    "destination": "Mumbai",
    ...
  }
}
```

---

## 🎯 Component Features

### FlightPricePredictor.jsx

**New Features:**
- ✅ Real API integration với axios
- ✅ Loading state với spinner animation
- ✅ Error handling với chi tiết error message
- ✅ Hiển thị giá vé INR
- ✅ Quy đổi sang VND (1 INR ≈ 300 VND)
- ✅ Price range (min-max)
- ✅ Confidence score với progress bar
- ✅ Delay probability với màu sắc:
  - 🟢 **Green (Low Risk)**: < 40% - An toàn, ít trễ
  - 🟡 **Yellow (Medium Risk)**: 40-70% - Có thể trễ
  - 🔴 **Red (High Risk)**: > 70% - Dễ trễ
- ✅ Delay status badge
- ✅ MongoDB save confirmation

---

## 🔑 Key Technologies

### Backend Stack
- **FastAPI**: Modern Python web framework
- **Motor**: Async MongoDB driver
- **Scikit-learn**: Machine Learning models
- **Pandas**: Data processing
- **Joblib**: Model serialization

### Frontend Stack
- **React 18.3.1**: UI library
- **Vite**: Build tool & dev server
- **Axios**: HTTP client
- **Lucide React**: Icons
- **Tailwind CSS**: Styling

### ML Pipeline
- **RandomForestRegressor**: Price prediction (98.14% R²)
- **RandomForestClassifier**: Delay prediction (90.22% accuracy)
- **LabelEncoder**: 9 categorical encoders
- **One-hot Encoding**: 30 features

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **API Usage Guide**: [API_USAGE.md](API_USAGE.md)
- **Label Encoders Guide**: [LABEL_ENCODERS_GUIDE_VI.md](LABEL_ENCODERS_GUIDE_VI.md)
- **Training Script**: [train.py](train.py)
- **Test Script**: [test_predict_endpoint.py](test_predict_endpoint.py)

---

## 🎓 Development Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                         │
│              React (localhost:5173)                         │
│    [Form] → [Submit] → [Loading] → [Results]               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ axios.post()
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│              (localhost:8000/predict)                       │
│    [Validate] → [Transform] → [Predict] → [Save]           │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌─────────┐  ┌──────────┐  ┌──────────┐
   │ ML Model│  │ Encoders │  │ MongoDB  │
   │flight.pkl│  │label.pkl │  │  :27017  │
   └─────────┘  └──────────┘  └──────────┘
```

---

## 💡 Pro Tips

1. **Luôn chạy Backend trước Frontend** để tránh connection errors
2. **Kiểm tra MongoDB** đang chạy trước khi start FastAPI
3. **Dùng Swagger UI** (http://localhost:8000/docs) để test API trước khi test UI
4. **Check Browser DevTools Console** để debug axios requests
5. **Dùng Network tab** để xem API request/response details

---

## ✨ Next Steps

- [ ] Add authentication (JWT tokens)
- [ ] Implement caching với Redis
- [ ] Deploy backend lên cloud (AWS/Heroku)
- [ ] Deploy frontend lên Vercel/Netlify
- [ ] Add real-time updates với WebSocket
- [ ] Implement A/B testing cho models
- [ ] Add analytics dashboard
- [ ] Mobile responsive optimization

---

**Created by**: Flight Price Prediction Team  
**Version**: 1.0  
**Last Updated**: March 10, 2026  
**Status**: ✅ Production Ready
