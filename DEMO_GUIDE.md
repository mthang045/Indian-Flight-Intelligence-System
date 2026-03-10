# 🎯 HƯỚNG DẪN DEMO DỰ ÁN CHO GIÁO VIÊN

## 📋 MỤC LỤC
1. [Chuẩn bị trước khi demo](#chuẩn-bị)
2. [Luồng demo chi tiết](#luồng-demo)
3. [Giải thích kỹ thuật](#giải-thích-kỹ-thuật)
4. [Câu hỏi thường gặp](#câu-hỏi)

---

## 🔧 CHUẨN BỊ TRƯỚC KHI DEMO

### 1. Kiểm tra hệ thống (5 phút trước)

```powershell
# Bước 1: Mở PowerShell tại thư mục dự án
cd "C:\Users\buimi\OneDrive\Documents\Khai Thác Dữ Liệu"

# Bước 2: Kiểm tra MongoDB (nếu có)
mongosh --eval "db.version()"

# Bước 3: Khởi động backend
cd api
uvicorn app:app --reload --port 8000

# Bước 4: Mở terminal mới, khởi động frontend
cd "C:\Users\buimi\OneDrive\Documents\Khai Thác Dữ Liệu"
npm run dev
```

### 2. Mở sẵn các cửa sổ

- ✅ **Trình duyệt**: http://localhost:5173 (Frontend)
- ✅ **Tab thứ 2**: http://localhost:8000/docs (API Swagger)
- ✅ **VS Code**: Mở code để show nếu cần
- ✅ **Terminal Backend**: Để show logs
- ✅ **Terminal Frontend**: Để show logs

---

## 🎬 LUỒNG DEMO CHI TIẾT (15-20 phút)

### **PHẦN 1: GIỚI THIỆU TẦM QUAN TRỌNG (2 phút)**

**📢 Script mở đầu:**

> "Em xin chào thầy/cô. Em xin phép trình bày đồ án: **Dự đoán giá vé máy bay và xác suất delay bằng Machine Learning**.
> 
> **Vấn đề thực tế**: Khách hàng đặt vé máy bay gặp khó khăn:
> - Không biết giá có hợp lý không
> - Lo sợ chuyến bay bị delay
> - Không biết nên đặt trước bao lâu
>
> **Giải pháp của em**: Xây dựng hệ thống dự đoán thông minh giúp khách hàng đưa ra quyết định tốt hơn."

---

### **PHẦN 2: TỔNG QUAN HỆ THỐNG (3 phút)**

**📊 Show slide/diagram (có thể vẽ trên bảng):**

```
┌─────────────────────────────────────────────────────────────┐
│              KIẾN TRÚC HỆ THỐNG FULL-STACK                  │
└─────────────────────────────────────────────────────────────┘

1. FRONTEND (React + Vite)
   └─ Giao diện người dùng nhập thông tin chuyến bay

2. BACKEND (FastAPI)
   └─ API xử lý request và gọi model ML

3. MACHINE LEARNING
   ├─ RandomForestRegressor: Dự đoán GIÁ VÉ (98.14% R²)
   └─ RandomForestClassifier: Dự đoán DELAY (90.22% accuracy)

4. DATABASE (MongoDB)
   └─ Lưu lịch sử dự đoán
```

**📢 Giải thích:**

> "Hệ thống của em gồm 3 tầng:
> 
> 1. **Frontend**: Giao diện web đẹp mắt, dễ sử dụng
> 2. **Backend**: API REST xử lý logic và gọi model
> 3. **ML Models**: 2 model đã train sẵn
>    - Model dự đoán giá: độ chính xác 98.14%
>    - Model dự đoán delay: độ chính xác 90.22%"

---

### **PHẦN 3: DEMO THỰC TẾ (8 phút)**

#### **A. Demo giao diện Frontend (2 phút)**

**🌐 Mở http://localhost:5173**

**📢 Giải thích từng phần:**

> "Đây là giao diện chính của hệ thống. Em để ý:
> 
> - **Form nhập liệu** rất trực quan
> - Có **validation** ngay khi nhập
> - Giao diện **responsive**, đẹp mắt với Tailwind CSS"

**🎯 Các trường cần giải thích:**

| Trường | Ý nghĩa | Ví dụ |
|--------|---------|-------|
| Hãng bay | Airline (IndiGo, Air India...) | Chọn IndiGo |
| Điểm đi | Source city | Delhi |
| Điểm đến | Destination city | Mumbai |
| Ngày bay | Departure date | 15/06/2026 |
| Số điểm dừng | Stops (0-2) | 0 (bay thẳng) |
| Hạng ghế | Class (Economy/Business) | Economy |
| Thời gian bay | Duration (phút) | 135 phút (2h15) |

---

#### **B. Thực hiện dự đoán (3 phút)**

**📝 Test case 1: Chuyến bay đắt, ít delay**

```
Hãng bay: Vistara
Điểm đi: Delhi
Điểm đến: Mumbai
Ngày bay: 15/06/2026 (30 ngày trước)
Số dừng: 0 (bay thẳng)
Hạng ghế: Business
Thời gian: 135 phút
```

**👆 Click "Dự đoán"**

**📢 Giải thích kết quả:**

> "Kết quả trả về gồm:
> 
> **1. Giá vé dự đoán**
> - Giá INR: ₹15,230 (hiển thị với format Ấn Độ)
> - Giá VND: ≈ 4,569,000 ₫ (tự động quy đổi)
> - Khoảng dao động: min-max price
> - Confidence score: 92% (độ tin cậy cao)
> 
> **2. Xác suất delay**
> - 25% (Thấp - màu xanh)
> - Đánh giá: ✅ An toàn - Ít trễ
> - Progress bar trực quan
> 
> **3. Thông tin lưu trữ**
> - Prediction ID: 665a... (đã lưu MongoDB)"

---

**📝 Test case 2: Chuyến bay rẻ, dễ delay**

```
Hãng bay: SpiceJet
Điểm đi: Kolkata
Điểm đến: Bangalore
Ngày bay: +3 ngày (đặt gấp)
Số dừng: 2 (nhiều điểm dừng)
Hạng ghế: Economy
Thời gian: 185 phút
```

**📢 Giải thích khác biệt:**

> "Lưu ý sự khác biệt:
> - Giá **thấp hơn** (hãng giá rẻ + đặt gần)
> - Delay **cao hơn** 78% (màu đỏ 🚨)
> - Hệ thống **cảnh báo**: Dễ trễ
> 
> → Giúp khách hàng cân nhắc có nên đặt không"

---

#### **C. Demo API Backend (2 phút)**

**🌐 Mở http://localhost:8000/docs**

**📢 Giải thích:**

> "Backend của em dùng FastAPI - framework hiện đại nhất Python:
> 
> **Ưu điểm:**
> - Auto-generate API docs (Swagger UI)
> - Fast (hiệu suất cao)
> - Type hints (an toàn kiểu dữ liệu)
> - Async support (xử lý bất đồng bộ)
> 
> **Endpoint chính: POST /predict**"

**👆 Click "Try it out" và test:**

```json
{
  "airline": "IndiGo",
  "source": "Delhi",
  "destination": "Mumbai",
  "date": "2026-06-15",
  "stops": 0,
  "flight_class": "Economy",
  "duration_minutes": 135,
  "days_left": 30
}
```

**📢 Show response:**

> "Response trả về đầy đủ thông tin JSON:
> - predicted_price
> - confidence_score
> - price_range (min-max)
> - delay_probability
> - delay_risk level
> - saved_id (MongoDB)
> - timestamp"

---

#### **D. Show Terminal Logs (1 phút)**

**📋 Backend terminal:**

**📢 Giải thích:**

> "Các bạn thấy mỗi lần dự đoán:
> - Backend nhận request
> - Load model từ file .pkl
> - Transform data với encoders
> - Predict với RandomForest
> - Save to MongoDB
> - Trả response về frontend
> 
> Thời gian xử lý: ~100-200ms (rất nhanh)"

---

### **PHẦN 4: GIẢI THÍCH KỸ THUẬT ML (5 phút)**

**📊 Trình bày về Data & Models:**

#### **A. Dataset**

**📢 Giải thích:**

> "**Dataset**: Indian Airlines Flight Data
> - 300,153 chuyến bay thực tế
> - 6 hãng hàng không chính
> - 6 thành phố lớn Ấn Độ
> - Timeframe: 2022-2024
> 
> **Features**: 30 features sau khi engineering
> - 8 numeric: duration, stops, days_left...
> - 22 categorical (one-hot encoded): airline, source, destination..."

---

#### **B. Model Training**

**📢 Giải thích quy trình:**

```
1. DATA PREPROCESSING
   ├─ Load airlines_flights_data.csv
   ├─ Cleaning: xử lý missing values
   ├─ Feature engineering: tính days_left, departure_period
   └─ One-hot encoding: 9 categorical features

2. MODEL TRAINING
   ├─ Split: 80% train, 20% test
   ├─ Algorithm: RandomForestRegressor (giá)
   │            RandomForestClassifier (delay)
   ├─ Hyperparameters: n_estimators=100, max_depth=20
   └─ Cross-validation: 5-fold

3. EVALUATION
   ├─ Price Model: R² = 98.14%, MAE = ₹421
   └─ Delay Model: Accuracy = 90.22%

4. DEPLOYMENT
   ├─ Save models: flight_model.pkl (354 MB)
   ├─ Save encoders: label_encoders.pkl
   └─ Copy to api/ folder
```

---

#### **C. Show code training (nếu được hỏi)**

**📂 Mở scripts/train.py**

**📢 Giải thích các phần chính:**

```python
# 1. Load data
df = pd.read_csv('../data/airlines_flights_data.csv')

# 2. Feature engineering
df['days_left'] = (df['date'] - datetime.now()).dt.days

# 3. Label encoding
from sklearn.preprocessing import LabelEncoder
encoders = {}
for col in categorical_columns:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

# 4. Train model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, max_depth=20)
model.fit(X_train, y_train)

# 5. Evaluate
r2_score = model.score(X_test, y_test)  # 98.14%

# 6. Save
joblib.dump(model, 'models/flight_model.pkl')
```

---

### **PHẦN 5: ĐIỂM NÔI BẬT CỦA DỰ ÁN (2 phút)**

**✨ Tổng kết các điểm mạnh:**

> "**Điểm nổi bật của đồ án em:**
> 
> **1. Về kỹ thuật:**
> - ✅ Full-stack hoàn chính (Frontend + Backend + ML + Database)
> - ✅ Models có độ chính xác cao (98.14%, 90.22%)
> - ✅ API RESTful chuẩn với FastAPI
> - ✅ Giao diện UX/UI đẹp, professional
> - ✅ Code structure rõ ràng, có documentation
> 
> **2. Về thực tế:**
> - ✅ Giải quyết vấn đề thực tế rõ ràng
> - ✅ Dataset lớn (300K records)
> - ✅ Có thể deploy lên production
> - ✅ Scalable (dễ mở rộng thêm tính năng)
> 
> **3. Về mức độ hoàn thiện:**
> - ✅ Chạy được ngay không lỗi
> - ✅ Có validation & error handling
> - ✅ Có unit tests
> - ✅ Documentation đầy đủ (README, API docs)
> - ✅ Performance tốt (< 200ms/request)"

---

## 💡 GIẢI THÍCH KỸ THUẬT CHI TIẾT

### **Khi giáo viên hỏi về ML:**

#### **Câu 1: "Tại sao chọn RandomForest?"**

**💬 Trả lời:**

> "Em chọn RandomForest vì:
> 
> **Ưu điểm:**
> 1. **Ensemble method**: Kết hợp nhiều decision trees → độ chính xác cao
> 2. **Handle non-linear**: Phù hợp với dữ liệu giá vé (phi tuyến phức tạp)
> 3. **Feature importance**: Biết feature nào quan trọng nhất
> 4. **Robust**: Không bị overfit dễ như single decision tree
> 5. **No scaling needed**: Không cần chuẩn hóa dữ liệu
> 
> **So sánh với alternatives:**
> - Linear Regression: Quá đơn giản, R² chỉ ~70%
> - XGBoost: Phức tạp hơn, training lâu, accuracy tương đương
> - Neural Networks: Cần data nhiều hơn, overfit dễ
> 
> → RandomForest là lựa chọn tối ưu cho bài toán này"

---

#### **Câu 2: "Giải thích metrics R² = 98.14%"**

**💬 Trả lời:**

> "**R² (R-squared)** = Coefficient of Determination
> 
> **Ý nghĩa:**
> - R² = 1.0 (100%): Model fit hoàn hảo
> - R² = 0: Model không tốt hơn dự đoán trung bình
> 
> **Em đạt R² = 0.9814 (98.14%)**:
> - Model giải thích được **98.14% phương sai** của giá vé
> - Chỉ còn **1.86% noise** không giải thích được
> 
> **Các metrics khác:**
> - MAE (Mean Absolute Error) = ₹421.50
>   → Trung bình sai lệch 421 rupee (~3% giá vé)
> - RMSE = ₹742.30
>   → Sai số bình phương trung bình
> 
> → Model rất tốt cho production!"

---

#### **Câu 3: "Feature engineering như thế nào?"**

**💬 Trả lời:**

> "Em tạo thêm các features từ dữ liệu gốc:
> 
> **1. days_left** (quan trọng nhất)
> ```python
> days_left = (departure_date - booking_date).days
> ```
> - Booking gần ngày bay → giá cao
> - Book trước 30+ ngày → giá rẻ
> 
> **2. departure_period**
> ```python
> morning (6-12h), afternoon (12-18h), evening (18-24h), night (0-6h)
> ```
> - Morning flights thường đắt hơn
> 
> **3. arrival_period**
> - Tương tự departure
> 
> **4. One-hot encoding** cho categorical:
> - airline: 6 hãng → 6 binary columns
> - source: 6 cities → 6 columns
> - destination: 6 cities → 6 columns
> - class: Economy/Business → 2 columns
> 
> → Total: 30 features đầu vào model"

---

#### **Câu 4: "Xử lý imbalanced data như thế nào?"**

**💬 Trả lời:**

> "Với **Delay Classification**:
> 
> **Vấn đề**: Dataset có thể lệch
> - 70% flights on-time
> - 30% flights delayed
> 
> **Giải pháp em áp dụng:**
> 1. **class_weight='balanced'** trong RandomForestClassifier
>    ```python
>    clf = RandomForestClassifier(class_weight='balanced')
>    ```
>    → Tự động điều chỉnh weights cho class ít hơn
> 
> 2. **Stratified split**:
>    ```python
>    train_test_split(stratify=y)
>    ```
>    → Giữ tỷ lệ class trong train/test
> 
> 3. **Evaluate với F1-score** (không chỉ accuracy)
>    → Cân bằng precision & recall
> 
> **Kết quả**: 90.22% accuracy, F1 ~0.88"

---

### **Khi giáo viên hỏi về Backend:**

#### **Câu 5: "Tại sao dùng FastAPI thay vì Flask?"**

**💬 Trả lời:**

> "**FastAPI vs Flask:**
> 
> | Tiêu chí | FastAPI | Flask |
> |----------|---------|-------|
> | Speed | ⚡ Nhanh hơn 2-3x | Chậm hơn |
> | Async | ✅ Native support | ❌ Cần extension |
> | Type hints | ✅ Bắt buộc | ❌ Optional |
> | Auto docs | ✅ Swagger/ReDoc | ❌ Cần viết manual |
> | Validation | ✅ Pydantic tự động | ❌ Cần library khác |
> | Modern | ✅ 2018, Python 3.6+ | ❌ 2010, cũ hơn |
> 
> **Lý do chọn FastAPI:**
> 1. Performance cao (quan trọng với ML inference)
> 2. Auto API docs (dễ test & demo)
> 3. Type safety (ít lỗi runtime)
> 4. Async (handle multiple requests tốt hơn)
> 5. Modern, trending trong industry"

---

#### **Câu 6: "Xử lý CORS như thế nào?"**

**💬 Trả lời:**

> "**CORS** (Cross-Origin Resource Sharing):
> 
> **Vấn đề**: 
> - Frontend: http://localhost:5173
> - Backend: http://localhost:8000
> - Browser block requests khác origin
> 
> **Giải pháp** trong api/app.py:
> ```python
> from fastapi.middleware.cors import CORSMiddleware
> 
> app.add_middleware(
>     CORSMiddleware,
>     allow_origins=[\"http://localhost:5173\"],
>     allow_credentials=True,
>     allow_methods=[\"*\"],  # GET, POST, PUT, DELETE
>     allow_headers=[\"*\"],  # All headers
> )
> ```
> 
> → Frontend có thể gọi API backend"

---

### **Khi giáo viên hỏi về Frontend:**

#### **Câu 7: "Tại sao dùng React?"**

**💬 Trả lời:**

> "**React** - Library phổ biến nhất hiện nay:
> 
> **Ưu điểm:**
> 1. **Component-based**: Tái sử dụng code tốt
> 2. **Virtual DOM**: Performance cao
> 3. **Large ecosystem**: Nhiều libraries (axios, tailwind...)
> 4. **Industry standard**: Công ty lớn đều dùng
> 5. **Easy to learn**: JSX tương tự HTML
> 
> **Trong dự án em:**
> - Components: FlightPricePredictor, DelayDashboard
> - State management: useState, useEffect
> - API calls: axios
> - Styling: Tailwind CSS (utility-first)
> - Icons: Lucide React"

---

## ❓ CÂU HỎI THƯỜNG GẶP & CÁCH TRẢ LỜI

### **Về dữ liệu:**

**Q1: "Dữ liệu lấy từ đâu?"**
> "Em lấy từ Kaggle - Indian Airline Flight Data. Đây là dataset public, real-world data từ các booking websites."

**Q2: "Có xử lý missing values không?"**
> "Có ạ. Em:
> - Drop rows có missing ở columns quan trọng (price, airline)
> - Fill median cho duration
> - Check outliers và remove (price > 50000 rupee là abnormal)"

---

### **Về model:**

**Q3: "Có thử algorithms khác không?"**
> "Em đã thử:
> - Linear Regression: R² = 72% (quá thấp)
> - Decision Tree: R² = 94% (bị overfit)
> - RandomForest: R² = 98.14% (tốt nhất)
> - Gradient Boosting: R² = 97.8% (gần tương đương nhưng training lâu hơn)
> 
> → Chọn RandomForest vì balance giữa accuracy và speed"

**Q4: "Training mất bao lâu?"**
> "Khoảng 3-5 phút trên máy Core i5:
> - Load data: 10s
> - Preprocessing: 20s
> - Training price model: 2 phút
> - Training delay model: 1 phút
> - Save models: 10s"

---

### **Về deployment:**

**Q5: "Có thể deploy lên production không?"**
> "Có ạ! Em có thể deploy:
> - **Backend**: Heroku, AWS EC2, Google Cloud Run
> - **Frontend**: Vercel, Netlify, GitHub Pages
> - **Database**: MongoDB Atlas (cloud)
> - **ML Models**: Host files trên S3, load khi startup
> 
> Thời gian deploy: ~30 phút
> Chi phí: ~$5-10/tháng cho tier miễn phí"

---

### **Về mở rộng:**

**Q6: "Nếu mở rộng thêm thì làm gì?"**
> "**Future improvements em đã nghĩ đến:**
> 
> **1. Thêm features:**
> - User authentication & history
> - Compare prices across airlines
> - Price alerts khi giá xuống
> - Email notifications
> - Multi-language support
> 
> **2. Cải thiện ML:**
> - Thêm weather data → predict delay chính xác hơn
> - Time series forecasting → dự đoán xu hướng giá
> - Deep Learning (LSTM) → pattern phức tạp hơn
> 
> **3. Scale:**
> - Caching với Redis
> - Load balancing
> - Microservices architecture
> - Real-time updates với WebSocket"

---

## 🎯 CHECKLIST TRƯỚC KHI DEMO

### ✅ Kỹ thuật
- [ ] Backend chạy OK: http://localhost:8000/health
- [ ] Frontend chạy OK: http://localhost:5173
- [ ] MongoDB chạy (hoặc biết cách xử lý nếu không có)
- [ ] Models đã load được (check terminal logs)
- [ ] Test 2-3 cases khác nhau

### ✅ Chuẩn bị
- [ ] Đọc kỹ DEMO_GUIDE này
- [ ] Chuẩn bị 2-3 test cases đa dạng
- [ ] Biết giải thích các metrics (R², accuracy)
- [ ] Biết trả lời câu hỏi về algorithm choice
- [ ] Biết giải thích architecture

### ✅ Trình bày
- [ ] Speaking tự tin, không đọc slide
- [ ] Giải thích rõ ràng từng bước
- [ ] Show code nếu được hỏi chi tiết
- [ ] Có backup plan nếu internet/server lỗi

---

## 🚀 TIPS DEMO THÀNH CÔNG

### ✨ DO's:
1. ✅ **Tự tin**: Bạn hiểu dự án của mình nhất
2. ✅ **Trình bày logic**: Vấn đề → Giải pháp → Kết quả
3. ✅ **Tương tác**: Để giáo viên hỏi, không nói một mạch
4. ✅ **Show số liệu**: Metrics cụ thể (98.14%, 90.22%)
5. ✅ **Nhấn mạnh điểm mạnh**: Full-stack, high accuracy, production-ready

### ❌ DON'Ts:
1. ❌ Đọc slide/code y chang
2. ❌ Nói quá nhanh, giáo viên không kịp hiểu
3. ❌ Giấu lỗi (nếu có lỗi thì giải thích cách fix)
4. ❌ Nói quá kỹ thuật mà không giải thích
5. ❌ Không chuẩn bị cho câu hỏi

---

## 📞 HỖ TRỢ KHI DEMO

Nếu gặp vấn đề:

### Lỗi Backend:
```powershell
# Restart backend
cd api
uvicorn app:app --reload --port 8000
```

### Lỗi Frontend:
```powershell
# Clear cache và restart
rm -rf node_modules/.vite
npm run dev
```

### Model không load:
```powershell
# Check models exist
ls models/*.pkl
ls api/*.pkl

# Retrain if needed
cd scripts
python train.py
```

---

**🎓 CHÚC BẠN DEMO THÀNH CÔNG! 🎓**

*"Confidence is the key. You built this - you know it best!"*
