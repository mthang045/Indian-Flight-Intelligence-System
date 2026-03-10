# 📊 LUỒNG HOẠT ĐỘNG HỆ THỐNG

## 🔄 FLOW CHART TỔNG QUAN

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                    👤 NGƯỜI DÙNG (USER)                             │
│                                                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           │ 1. Truy cập http://localhost:5173
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     🎨 FRONTEND (React + Vite)                      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Form nhập liệu:                                            │  │
│  │  • Hãng bay (IndiGo, Air India...)                          │  │
│  │  • Điểm đi → Điểm đến (Delhi → Mumbai)                      │  │
│  │  • Ngày bay (15/06/2026)                                    │  │
│  │  • Số điểm dừng (0, 1, 2)                                   │  │
│  │  • Hạng ghế (Economy/Business)                              │  │
│  │  • Thời gian bay (135 phút)                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  [Button: Dự đoán] ← User click                                    │
│                                                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           │ 2. axios.post('/predict')
                           │    Gửi JSON request
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🌐 BACKEND (FastAPI)                             │
│                      http://localhost:8000                          │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  BƯỚC 1: Nhận request                                        │ │
│  │  ──────────────────────                                      │ │
│  │  → Validate dữ liệu với Pydantic                             │ │
│  │  → Check required fields                                     │ │
│  │  → Convert types (str → int, date...)                        │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                           │                                         │
│                           ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  BƯỚC 2: Transform data                                      │ │
│  │  ───────────────────────                                     │ │
│  │  → Calculate days_left = (date - today).days                 │ │
│  │  → Load label_encoders.pkl                                   │ │
│  │  → Encode categorical features:                              │ │
│  │    • airline: "IndiGo" → 2                                   │ │
│  │    • source: "Delhi" → 1                                     │ │
│  │    • destination: "Mumbai" → 4                               │ │
│  │    • class: "Economy" → 0                                    │ │
│  │    • ...9 features total                                     │ │
│  │  → Create feature vector [30 dimensions]                     │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                           │                                         │
│                           ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  BƯỚC 3: ML Prediction                                       │ │
│  │  ──────────────────────                                      │ │
│  │                                                              │ │
│  │  A. Dự đoán GIÁ VÉ:                                          │ │
│  │  ────────────────                                            │ │
│  │  → Load flight_model.pkl (RandomForestRegressor)            │ │
│  │  → model.predict(features)                                   │ │
│  │  → predicted_price = ₹4,850                                  │ │
│  │  → confidence_score = model.score() = 92%                    │ │
│  │  → price_range = (min: ₹4,268, max: ₹5,432)                 │ │
│  │                                                              │ │
│  │  B. Dự đoán DELAY:                                           │ │
│  │  ───────────────                                             │ │
│  │  → Load delay_model.pkl (RandomForestClassifier)            │ │
│  │  → delay_proba = model.predict_proba(features)              │ │
│  │  → delay_probability = 35.2%                                 │ │
│  │  → delay_risk = "Low" (< 40%)                                │ │
│  │  → delay_status = "On-time"                                  │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                           │                                         │
│                           ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  BƯỚC 4: Save to Database                                    │ │
│  │  ─────────────────────────                                   │ │
│  │  → Connect MongoDB (localhost:27017)                         │ │
│  │  → db.predictions.insert_one({                               │ │
│  │      "airline": "IndiGo",                                    │ │
│  │      "predicted_price": 4850,                                │ │
│  │      "delay_probability": 35.2,                              │ │
│  │      "timestamp": "2026-03-11T10:30:00Z",                    │ │
│  │      "user_input": {...}                                     │ │
│  │    })                                                        │ │
│  │  → Return saved_id = "665a1b2c..."                           │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                           │                                         │
│                           ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  BƯỚC 5: Return Response                                     │ │
│  │  ────────────────────────                                    │ │
│  │  {                                                           │ │
│  │    "predicted_price": 4850.75,                               │ │
│  │    "confidence_score": 92.5,                                 │ │
│  │    "price_range": {"min": 4268, "max": 5432},                │ │
│  │    "delay_probability": 35.2,                                │ │
│  │    "delay_status": "On-time",                                │ │
│  │    "delay_risk": "Low",                                      │ │
│  │    "saved_id": "665a1b2c...",                                │ │
│  │    "timestamp": "2026-03-11T10:30:00Z"                       │ │
│  │  }                                                           │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           │ 3. JSON Response trả về
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     🎨 FRONTEND (React)                             │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Hiển thị kết quả:                                           │ │
│  │                                                              │ │
│  │  ╔════════════════════════════════════════════════════════╗  │ │
│  │  ║            KẾT QUẢ DỰ ĐOÁN                            ║  │ │
│  │  ╚════════════════════════════════════════════════════════╝  │ │
│  │                                                              │ │
│  │  💰 GIÁ VÉ DỰ ĐOÁN                                           │ │
│  │  ─────────────────                                           │ │
│  │  • Giá INR: ₹4,850                                           │ │
│  │  • Giá VND: ≈ 1,455,000 ₫ (1 INR ≈ 300 VND)                │ │
│  │  • Khoảng giá: ₹4,268 - ₹5,432                              │ │
│  │  • Độ tin cậy: 92% ████████████████░░░░                     │ │
│  │                                                              │ │
│  │  ⏰ XÁC SUẤT DELAY                                           │ │
│  │  ──────────────────                                          │ │
│  │  • Xác suất: 35.2%                                           │ │
│  │  • Đánh giá: ✅ An toàn - Ít trễ                            │ │
│  │  • Risk level: 🟢 Low (Thấp)                                │ │
│  │  • Progress: ███████░░░░░░░░░░░░░ 35%                      │ │
│  │                                                              │ │
│  │  💾 Đã lưu vào database: 665a1b2c...                         │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           │ 4. User xem kết quả
                           ▼
                    ✅ HOÀN THÀNH!
```

---

## ⏱️ TIMELINE CHI TIẾT

### Request → Response: ~150-200ms

```
Time: 0ms
│
├─ 0-10ms    → Frontend: User click button
│              • Validate form data
│              • Show loading spinner
│              • axios.post() start
│
├─ 10-20ms   → Network: HTTP request
│              • Send JSON to backend
│              • Headers, body encoding
│
├─ 20-30ms   → Backend: Receive & validate
│              • FastAPI parse JSON
│              • Pydantic validation
│
├─ 30-60ms   → Backend: Transform data
│              • Load encoders (cached after first)
│              • Encode categorical features
│              • Build feature vector
│
├─ 60-120ms  → Backend: ML Prediction
│              • Load models (cached)
│              • flight_model.predict() - 40ms
│              • delay_model.predict_proba() - 20ms
│              • Calculate confidence & ranges
│
├─ 120-140ms → Backend: Save to MongoDB
│              • Insert document
│              • Get inserted_id
│
├─ 140-150ms → Backend: Build response JSON
│              • Format numbers
│              • Calculate VND conversion
│              • Add timestamp
│
├─ 150-160ms → Network: Return response
│              • JSON encoding
│              • HTTP response
│
└─ 160-200ms → Frontend: Render results
               • Parse JSON
               • Update React state
               • Animate display
               • Hide loading spinner
```

**Tổng: ~200ms (0.2 giây) - RẤT NHANH! ⚡**

---

## 🗂️ DATA FLOW

### INPUT → OUTPUT Chi tiết

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT FROM USER                                            │
└─────────────────────────────────────────────────────────────┘

  Raw Input (Frontend Form):
  ┌──────────────────────────────────────────┐
  │ airline: "IndiGo"                        │
  │ source: "Delhi"                          │
  │ destination: "Mumbai"                    │
  │ date: "2026-06-15"                       │
  │ stops: 0                                 │
  │ flight_class: "Economy"                  │
  │ duration_minutes: 135                    │
  └──────────────────────────────────────────┘
         │
         │ Frontend Processing
         ▼
  Calculated Fields:
  ┌──────────────────────────────────────────┐
  │ days_left: 96                            │
  │   (= June 15 - March 11)                 │
  └──────────────────────────────────────────┘
         │
         │ Send to Backend
         ▼
┌─────────────────────────────────────────────────────────────┐
│  BACKEND PROCESSING                                         │
└─────────────────────────────────────────────────────────────┘

  Step 1: Encode Categorical
  ┌──────────────────────────────────────────┐
  │ airline_encoded: 2                       │
  │ source_encoded: 1                        │
  │ destination_encoded: 4                   │
  │ class_encoded: 0                         │
  │ departure_time_encoded: 1                │
  │ arrival_time_encoded: 2                  │
  │ stops_encoded: 0                         │
  └──────────────────────────────────────────┘
         │
         │ Feature Engineering
         ▼
  Step 2: Build Feature Vector
  ┌──────────────────────────────────────────┐
  │ [2, 1, 4, 0, 1, 2, 0, 135, 96,           │
  │  0, 1, 0, 0, 0, 0,                       │
  │  0, 0, 1, 0, 0, 0,                       │
  │  0, 0, 0, 1, 0, 0,                       │
  │  1, 0]                                   │
  │                                          │
  │ ↑ Total: 30 features                     │
  └──────────────────────────────────────────┘
         │
         │ ML Inference
         ▼
  Step 3: Model Predictions
  ┌──────────────────────────────────────────┐
  │ Price Model Output:                      │
  │   predicted_price: 4850.75               │
  │   confidence: 0.925                      │
  │   price_range: [4268.66, 5432.84]        │
  │                                          │
  │ Delay Model Output:                      │
  │   delay_proba: [0.648, 0.352]            │
  │   delay_class: 0 (On-time)               │
  │   delay_probability: 35.2%               │
  └──────────────────────────────────────────┘
         │
         │ Post-processing
         ▼
  Step 4: Format Results
  ┌──────────────────────────────────────────┐
  │ predicted_price: 4850.75                 │
  │ price_vnd: 1,455,000 (×300)              │
  │ confidence_score: 92.5%                  │
  │ delay_probability: 35.2%                 │
  │ delay_risk: "Low"                        │
  │ delay_status: "On-time"                  │
  │ saved_id: "665a1b2c..."                  │
  │ timestamp: "2026-03-11T10:30:00Z"        │
  └──────────────────────────────────────────┘
         │
         │ Return to Frontend
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT TO USER                                             │
└─────────────────────────────────────────────────────────────┘

  Visual Display:
  ╔════════════════════════════════════════╗
  ║  💰 Giá vé: ₹4,850 (≈1,455,000 ₫)     ║
  ║  📊 Tin cậy: 92.5%                     ║
  ║  ⏰ Delay: 35.2% - 🟢 Thấp            ║
  ║  ✅ An toàn - Ít trễ                  ║
  ╚════════════════════════════════════════╝
```

---

## 🧠 ML MODEL INTERNALS

### RandomForest Decision Process

```
INPUT FEATURES [30 dimensions]
        │
        │ Split into 100 Decision Trees
        ▼
┌───────────────────────────────────────────────────────────┐
│                 DECISION TREE 1                           │
│                                                           │
│       days_left < 20?                                     │
│      ┌───YES───┐        ┌───NO────┐                      │
│      ▼         │        │         ▼                       │
│  class=Bus?   │        │    airline=Vistara?             │
│  ┌─YES→₹12000 │        │    ┌─YES→₹6000                 │
│  └─NO→₹8000   │        │    └─NO→₹4500                  │
│                                                           │
│  Prediction: ₹4,500                                       │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                 DECISION TREE 2                           │
│                                                           │
│       duration > 150?                                     │
│      ┌───YES───┐        ┌───NO────┐                      │
│      ▼         │        │         ▼                       │
│  stops=2?     │        │    source=Delhi?                │
│  ┌─YES→₹5200  │        │    ┌─YES→₹4800                 │
│  └─NO→₹4900   │        │    └─NO→₹5100                  │
│                                                           │
│  Prediction: ₹4,800                                       │
└───────────────────────────────────────────────────────────┘

        ...repeat for 98 more trees...

┌───────────────────────────────────────────────────────────┐
│                 DECISION TREE 100                         │
│  Prediction: ₹5,000                                       │
└───────────────────────────────────────────────────────────┘

        │
        │ Aggregate all predictions
        ▼
┌───────────────────────────────────────────────────────────┐
│              ENSEMBLE AVERAGE                             │
│                                                           │
│  Tree predictions:                                        │
│  [4500, 4800, 4750, 5000, 4900, 4850, ...]               │
│                                                           │
│  Mean = (4500 + 4800 + ... + 5000) / 100                 │
│       = 4,850.75                                          │
│                                                           │
│  Std Dev = 412.5                                          │
│  Confidence = 1 - (std_dev / mean)                       │
│             = 1 - (412.5 / 4850.75)                      │
│             = 0.915 (91.5%)                              │
│                                                           │
│  Price Range:                                            │
│    min = mean - 1.5*std_dev = 4,268.66                   │
│    max = mean + 1.5*std_dev = 5,432.84                   │
└───────────────────────────────────────────────────────────┘

FINAL OUTPUT: ₹4,850.75 ± ₹582.09 (91.5% confidence)
```

---

## 🎯 DEMO SCENARIOS

### Scenario 1: Chuyến bay đắt, ít delay

```
INPUT:
  Airline: Vistara
  Route: Delhi → Mumbai
  Date: +30 days (book trước)
  Stops: 0 (direct)
  Class: Business
  Duration: 135 min

EXPECTED OUTPUT:
  Price: ₹15,000-18,000 (cao vì Business + Vistara premium)
  Delay: 20-30% (thấp vì Vistara tốt)
  Risk: 🟢 Low

EXPLAIN TO TEACHER:
"Vistara là hãng cao cấp, Business class, book trước 30 ngày
nên giá cao nhưng chất lượng tốt, ít delay"
```

### Scenario 2: Chuyến bay rẻ, dễ delay

```
INPUT:
  Airline: SpiceJet
  Route: Kolkata → Bangalore
  Date: +3 days (book gấp)
  Stops: 2 (nhiều dừng)
  Class: Economy
  Duration: 185 min

EXPECTED OUTPUT:
  Price: ₹3,000-4,000 (thấp vì SpiceJet budget + book gần)
  Delay: 70-80% (cao vì budget airline + nhiều dừng)
  Risk: 🔴 High

EXPLAIN TO TEACHER:
"SpiceJet là hãng giá rẻ, book gần ngày bay, 2 điểm dừng
nên giá thấp nhưng risk delay cao"
```

### Scenario 3: Chuyến bay cân bằng

```
INPUT:
  Airline: IndiGo
  Route: Delhi → Mumbai
  Date: +15 days
  Stops: 0
  Class: Economy
  Duration: 135 min

EXPECTED OUTPUT:
  Price: ₹4,500-5,500 (trung bình)
  Delay: 35-45% (trung bình)
  Risk: 🟡 Medium

EXPLAIN TO TEACHER:
"IndiGo là hãng phổ biến nhất Ấn Độ, balance giữa giá
và quality, delay ở mức chấp nhận được"
```

---

## 📱 USER JOURNEY MAP

```
TIME: 0s
│
│ USER opens http://localhost:5173
├─ Loading page... (Vite dev server: 50-100ms)
│
TIME: 0.1s
│
│ ✅ Page displayed
│
├─ User sees:
│  • Form nhập liệu rõ ràng
│  • Placeholders hướng dẫn
│  • UI đẹp với Tailwind
│
├─ User fills form: (30-60 seconds)
│  1. Select airline: IndiGo
│  2. Select source: Delhi
│  3. Select destination: Mumbai
│  4. Pick date: 15/06/2026
│  5. Select stops: 0
│  6. Select class: Economy
│  7. Input duration: 135
│
TIME: 1 minute
│
│ ✅ Form filled
│
├─ User clicks [Dự đoán] button
│
├─ Frontend:
│  • Validate inputs ✓
│  • Show loading spinner 🔄
│  • Disable button (prevent double-click)
│
TIME: 1 min 0.1s
│
│ ⏳ Loading... (200ms)
│
├─ Backend processing...
│  • Transform data
│  • ML prediction
│  • Save MongoDB
│
TIME: 1 min 0.3s
│
│ ✅ Got results!
│
├─ Frontend:
│  • Hide loading spinner
│  • Animate results (fade in)
│  • Show price with color
│  • Show delay with icon
│
├─ User sees:
│  ╔════════════════════════════════╗
│  ║  💰 ₹4,850 (≈1,455,000 ₫)     ║
│  ║  📊 92% confidence             ║
│  ║  ⏰ 35% delay - 🟢 Low         ║
│  ║  ✅ An toàn - Ít trễ          ║
│  ╚════════════════════════════════╝
│
├─ User reads results (10-20 seconds)
│  • Compares price with expectations
│  • Checks delay risk
│  • Decides: book or not
│
TIME: 1 min 30s
│
│ 🎯 DECISION MADE!
│
└─ User may:
   Option A: Try different inputs (loop back)
   Option B: Use info to book flight
   Option C: Close app
```

---

## 🎓 TEACHING POINTS

### Khi giải thích cho giáo viên:

**Point 1: Real-world Problem**
> "Đây không phải bài toán giả lập. Đây là vấn đề thực tế
> mà hàng triệu người booking vé máy bay gặp phải mỗi ngày"

**Point 2: End-to-end Solution**
> "Em không chỉ train model. Em build complete system:
> từ UI → API → ML → Database. Production-ready!"

**Point 3: High Accuracy**
> "R² = 98.14% là con số rất cao trong regression.
> Papers trên Kaggle chỉ đạt 95-96%"

**Point 4: Multiple Models**
> "Em không chỉ dự đoán giá. Em còn dự đoán delay
> để giúp user decision making tốt hơn"

**Point 5: Scalability**
> "Code structure cho phép dễ dàng:
> - Add thêm airlines
> - Add thêm routes
> - Retrain với data mới
> - Deploy lên cloud"

---

**📚 File này giải thích CHI TIẾT luồng hoạt động của toàn bộ hệ thống!**

*Đọc kỹ để hiểu rõ từng bước khi demo cho giáo viên!* 🎯
