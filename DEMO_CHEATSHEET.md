# 🎯 CHEAT SHEET - DEMO NHANH

## 📋 CHUẨN BỊ 5 PHÚT TRƯỚC

```powershell
# Terminal 1: Backend
cd C:\Users\buimi\OneDrive\Documents\Khai Thác Dữ Liệu\api
uvicorn app:app --reload --port 8000

# Terminal 2: Frontend
cd C:\Users\buimi\OneDrive\Documents\Khai Thác Dữ Liệu
npm run dev
```

**Mở sẵn:**
- 🌐 Frontend: http://localhost:5173
- 📚 API Docs: http://localhost:8000/docs
- 💻 VS Code (code để show nếu hỏi)

---

## 🎬 SCRIPT DEMO 15 PHÚT

### 1️⃣ MỞ ĐẦU (2 phút)

**📢 Nói:**
> "Em xin trình bày: **Dự đoán giá vé và delay máy bay bằng ML**
> 
> **Vấn đề**: Khách đặt vé không biết giá có hợp lý, lo delay
> 
> **Giải pháp**: Hệ thống dự đoán thông minh giúp quyết định tốt hơn"

---

### 2️⃣ KIẾN TRÚC (3 phút)

**📊 Giải thích:**
> "Hệ thống Full-Stack:
> - **Frontend**: React + Vite - UI đẹp
> - **Backend**: FastAPI - API handling
> - **ML Models**: 
>   - RandomForestRegressor - Giá vé (98.14% R²)
>   - RandomForestClassifier - Delay (90.22% accuracy)
> - **Database**: MongoDB - Lưu predictions"

---

### 3️⃣ DEMO (8 phút)

#### Test Case 1: Chuyến đắt, ít delay
```
Vistara | Delhi → Mumbai | +30 days | 0 stops | Business | 135 min
```
**Expected**: ₹15K-18K, delay 20-30% 🟢

**📢 Giải thích kết quả:**
> "Business class, book trước, hãng premium → giá cao, ít delay"

---

#### Test Case 2: Chuyến rẻ, dễ delay
```
SpiceJet | Kolkata → Bangalore | +3 days | 2 stops | Economy | 185 min
```
**Expected**: ₹3K-4K, delay 70-80% 🔴

**📢 Giải thích:**
> "Budget airline, book gần, nhiều dừng → giá thấp, risk cao"

---

#### Show API Docs
**Mở**: http://localhost:8000/docs

**📢 Nói:**
> "FastAPI auto-generate docs. Click Try it out để test API trực tiếp"

---

### 4️⃣ KỸ THUẬT ML (5 phút)

**📊 Numbers quan trọng:**
- Dataset: **300,153 flights** thực tế
- Features: **30 features** (8 numeric + 22 one-hot)
- Price Model: **R² = 98.14%**, MAE = ₹421
- Delay Model: **Accuracy = 90.22%**
- Training time: **3-5 phút**
- Prediction time: **~100ms**

**📢 Giải thích tại sao chọn RandomForest:**
> "Ensemble method, high accuracy, không overfit, handle non-linear data tốt"

---

### 5️⃣ ĐIỂM NỔI BẬT (2 phút)

**✨ Highlights:**
- ✅ Full-stack complete (Frontend + Backend + ML + DB)
- ✅ High accuracy (98.14%, 90.22%)
- ✅ Production-ready (có validation, error handling)
- ✅ Fast response (~200ms)
- ✅ Professional UI/UX

---

## 💬 QUICK ANSWERS

### Q: "Tại sao R² = 98.14%?"
**A:** "Model giải thích được 98.14% variance của giá vé. Trung bình sai lệch chỉ ₹421 (~3%). Rất tốt cho production."

### Q: "Tại sao chọn RandomForest?"
**A:** "Ensemble method, accuracy cao, robust, không cần scaling. So với Linear: 72%, XGBoost: tương đương nhưng phức tạp hơn."

### Q: "Dataset từ đâu?"
**A:** "Kaggle - Indian Airlines Flight Data. 300K+ records thực tế 2022-2024."

### Q: "Training mất bao lâu?"
**A:** "3-5 phút trên Core i5. Load data 10s, preprocessing 20s, train 2-3 phút."

### Q: "Có thể deploy không?"
**A:** "Có! Backend → Heroku/AWS, Frontend → Vercel, DB → MongoDB Atlas. Chi phí ~$5-10/tháng."

---

## 🎯 TEST SCENARIOS

| # | Airline | Route | Days | Stops | Class | Expected Price | Expected Delay |
|---|---------|-------|------|-------|-------|----------------|----------------|
| 1 | Vistara | DEL-BOM | 30 | 0 | Business | ₹15-18K | 20-30% 🟢 |
| 2 | SpiceJet | CCU-BLR | 3 | 2 | Economy | ₹3-4K | 70-80% 🔴 |
| 3 | IndiGo | DEL-BOM | 15 | 0 | Economy | ₹4.5-5.5K | 35-45% 🟡 |

---

## ⏱️ TIMING

```
0:00 - 2:00   → Giới thiệu vấn đề
2:00 - 5:00   → Kiến trúc hệ thống
5:00 - 13:00  → Demo (UI + API + Logs)
13:00 - 18:00 → Kỹ thuật ML
18:00 - 20:00 → Tổng kết điểm mạnh
```

---

## 🔢 NUMBERS PHẢI NHỚ

- **98.14%** - R² score price model
- **90.22%** - Accuracy delay model
- **300,153** - Records trong dataset
- **30** - Number of features
- **₹421** - Mean Absolute Error
- **~200ms** - Response time
- **354 MB** - Flight model size
- **29 MB** - Delay model size

---

## 🚨 NẾU CÓ LỖI

### MongoDB không chạy:
**📢 Nói:** "MongoDB không cần thiết để dự đoán. Chỉ để lưu history. Model vẫn chạy bình thường."

### Frontend lỗi:
```powershell
rm -rf node_modules/.vite
npm run dev
```

### Backend lỗi:
```powershell
cd api
pip install -r requirements.txt
uvicorn app:app --reload
```

---

## ✅ CHECKLIST TRƯỚC KHI DEMO

- [ ] Backend chạy: http://localhost:8000/health
- [ ] Frontend chạy: http://localhost:5173
- [ ] Models load OK (check terminal)
- [ ] Test 2-3 cases
- [ ] Đọc qua script demo
- [ ] Nhớ numbers quan trọng
- [ ] Chuẩn bị trả lời câu hỏi

---

## 💡 TIPS CUỐI CÙNG

**DO:**
- ✅ Tự tin, nhìn vào giáo viên
- ✅ Nói chậm rãi, rõ ràng
- ✅ Show numbers cụ thể
- ✅ Giải thích logic: Problem → Solution → Result
- ✅ Để giáo viên hỏi, tương tác

**DON'T:**
- ❌ Đọc slide
- ❌ Nói quá nhanh
- ❌ Giấu lỗi
- ❌ Quá kỹ thuật không giải thích
- ❌ Không chuẩn bị cho câu hỏi

---

**🎓 TỰ TIN LÊN! BẠN ĐÃ BUILD ĐƯỢC HỆ THỐNG HOÀN CHỈNH! 🎓**

*Print sheet này ra để xem nhanh khi demo!*
