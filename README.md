# 🛫 Flight Price Prediction System

Complete full-stack application for predicting Indian flight prices and delay probabilities using Machine Learning.

## 📁 Project Structure

```
Khai Thác Dữ Liệu/
│
├── 📊 data/                          # Data files
│   ├── airlines_flights_data.csv    # Raw flight data (300K+ records)
│   └── cleaned_flights.csv          # Processed training data
│
├── 🤖 models/                        # Trained ML models
│   ├── flight_model.pkl             # Price prediction model (354 MB)
│   ├── delay_model.pkl              # Delay prediction model (29 MB)
│   ├── label_encoders.pkl           # Categorical encoders
│   ├── feature_names.pkl            # Feature list
│   └── model_metadata.pkl           # Model metadata
│
├── 🌐 api/                           # FastAPI Backend
│   ├── app.py                       # Main API application
│   ├── models.py                    # Pydantic models
│   ├── database.py                  # MongoDB connection
│   ├── requirements.txt             # Python dependencies
│   └── [model copies]               # Local model files for API
│
├── 🎨 src/                           # React Frontend
│   ├── app/
│   │   ├── components/              # React components
│   │   │   ├── FlightPricePredictor.jsx
│   │   │   └── DelayProbabilityDashboard.jsx
│   │   └── context/                 # React context
│   └── styles/                      # CSS styles
│
├── 🐍 scripts/                       # Training & testing scripts
│   ├── train.py                     # Main training pipeline
│   └── test_predict_endpoint.py     # API testing script
│
├── 📚 docs/                          # Documentation
│   ├── API_USAGE.md                 # API documentation
│   ├── FULLSTACK_SETUP.md           # Setup guide
│   ├── COMPLETED.md                 # Features completed
│   └── LABEL_ENCODERS_GUIDE.md      # Encoder guide
│
└── ⚙️ Config files
    ├── package.json                 # Node.js dependencies
    ├── vite.config.ts               # Vite configuration
    └── postcss.config.mjs           # PostCSS config
```

---

## 🚀 Quick Start

### 1️⃣ Prerequisites

- Python 3.12+
- Node.js 18+
- MongoDB (localhost:27017)

### 2️⃣ Backend Setup

```powershell
# Install Python dependencies
cd api
pip install -r requirements.txt

# Start FastAPI server
uvicorn app:app --reload --port 8000
```

**Backend running at**: http://localhost:8000

### 3️⃣ Frontend Setup

```powershell
# Install Node.js dependencies
npm install

# Start React dev server
npm run dev
```

**Frontend running at**: http://localhost:5173

---

## 📊 Features

### ✨ Price Prediction
- 🎯 **98.14% R² accuracy** using RandomForestRegressor
- 💰 Predicts ticket prices in INR
- 💵 Auto-converts to VND (1 INR ≈ 300 VND)
- 📈 Shows confidence score and price range

### ⏰ Delay Prediction
- 🎯 **90.22% accuracy** using RandomForestClassifier
- 🚦 Color-coded risk levels:
  - 🟢 **Low Risk** (< 40%): Safe, on-time
  - 🟡 **Medium Risk** (40-70%): May be delayed
  - 🔴 **High Risk** (> 70%): Likely delayed

### 🗄️ MongoDB Integration
- 💾 Saves all predictions to database
- 📝 Tracks prediction history
- 🔍 Query past predictions

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Scikit-learn** - Machine Learning
- **Pandas** - Data processing
- **Joblib** - Model serialization

### Frontend
- **React 18.3.1** - UI library
- **Vite** - Build tool & dev server
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### ML Pipeline
- **RandomForestRegressor** - Price prediction
- **RandomForestClassifier** - Delay prediction
- **LabelEncoder** - 9 categorical encoders
- **One-hot Encoding** - 30 features

### Database
- **MongoDB** - Document database
- Collections: `flights`, `predictions`

---

## 📊 Dataset

- **Source**: Indian Airlines Flight Data
- **Records**: 300,153 flights
- **Airlines**: IndiGo, Air India, SpiceJet, Vistara, AirAsia, GO_FIRST
- **Cities**: Delhi, Mumbai, Bangalore, Chennai, Kolkata, Hyderabad
- **Features**: 30 (8 numeric + 22 one-hot encoded)

---

## 🔗 API Endpoints

### POST `/predict`
Unified endpoint for price and delay predictions.

**Request:**
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

**Response:**
```json
{
  "predicted_price": 4850.75,
  "confidence_score": 87.5,
  "price_range": {"min": 4268.66, "max": 5432.84},
  "delay_probability": 35.20,
  "delay_status": "On-time",
  "delay_risk": "Low",
  "saved_id": "665a...",
  "timestamp": "2026-03-10T10:30:00Z"
}
```

---

## 📖 Documentation

- [API Usage Guide](docs/API_USAGE.md) - Complete API documentation
- [Full-Stack Setup](docs/FULLSTACK_SETUP.md) - Detailed setup instructions
- [Label Encoders Guide](docs/LABEL_ENCODERS_GUIDE.md) - How encoders work
- [Completed Features](docs/COMPLETED.md) - What's been implemented

---

## 🧪 Testing

### Test API Endpoint
```powershell
cd scripts
python test_predict_endpoint.py
```

### Test in Browser
1. Open http://localhost:5173
2. Fill in flight details
3. Click "Dự đoán" (Predict)
4. View results with price and delay info

---

## 🎯 Model Performance

### Price Prediction Model
- **Algorithm**: RandomForestRegressor
- **Training samples**: 240,122
- **Test samples**: 60,031
- **R² Score**: 98.14%
- **MAE**: ₹421.50
- **RMSE**: ₹742.30

### Delay Prediction Model
- **Algorithm**: RandomForestClassifier
- **Accuracy**: 90.22%
- **Features**: 9 categorical + 3 numeric

---

## 🔧 Training Models

To retrain models from scratch:

```powershell
cd scripts
python train.py
```

This will:
1. Load raw data from `data/airlines_flights_data.csv`
2. Engineer features
3. Create and save label encoders
4. Train RandomForest models
5. Save models to `models/` and `api/`

---

## 🌟 Key Features

- ✅ Real-time predictions using ML models
- ✅ Automatic currency conversion (INR ↔ VND)
- ✅ Visual delay risk indicators with colors
- ✅ Loading states and error handling
- ✅ MongoDB tracking of all predictions
- ✅ Bilingual support (Vietnamese + English)
- ✅ Responsive design with Tailwind CSS
- ✅ RESTful API with FastAPI
- ✅ Async database operations with Motor

---

## 📝 Environment Variables

Create `.env` file in `api/` directory:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=flight_price_prediction
```

---

## 🚦 Development Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface                           │
│              React (localhost:5173)                         │
│    [Form] → [Submit] → [Loading] → [Results]               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ axios.post()
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend                            │
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

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check if MongoDB is running
mongosh

# Verify models exist
ls api/*.pkl

# Reinstall dependencies
pip install -r api/requirements.txt
```

### Frontend errors
```powershell
# Reinstall node modules
rm -r node_modules
npm install

# Check axios is installed
npm list axios
```

### API connection errors
- Ensure backend is running on port 8000
- Check CORS settings in `api/app.py`
- Verify MongoDB connection

---

## 📈 Future Improvements

- [ ] Add authentication (JWT)
- [ ] Implement Redis caching
- [ ] Deploy to cloud (AWS/Heroku)
- [ ] Add WebSocket for real-time updates
- [ ] Mobile app (React Native)
- [ ] A/B testing for models
- [ ] Analytics dashboard
- [ ] Email notifications

---

## 👥 Contributors

Flight Price Prediction Team

---

## 📄 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- Data source: Indian Airlines
- ML frameworks: Scikit-learn
- Web frameworks: FastAPI, React
- Database: MongoDB

---

**⚡ Status**: Production Ready  
**📅 Last Updated**: March 10, 2026  
**🎯 Version**: 1.0.0
