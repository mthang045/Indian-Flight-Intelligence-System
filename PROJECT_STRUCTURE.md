# 📁 Project Structure

```
Khai Thác Dữ Liệu/
│
├── 📊 data/                              # Dataset files
│   ├── airlines_flights_data.csv        # Raw Indian flights data (300K records)
│   └── cleaned_flights.csv              # Processed training data (30 features)
│
├── 🤖 models/                            # Trained machine learning models
│   ├── flight_model.pkl                 # RandomForest price predictor (354 MB)
│   ├── delay_model.pkl                  # RandomForest delay classifier (29 MB)
│   ├── label_encoders.pkl               # Encoders for 9 categorical features (2.6 KB)
│   ├── feature_names.pkl                # List of 30 feature names
│   └── model_metadata.pkl               # Training metadata & metrics
│
├── 🌐 api/                               # FastAPI Backend Server
│   ├── app.py                           # Main API application
│   ├── models.py                        # Pydantic request/response models
│   ├── database.py                      # MongoDB async connection
│   ├── requirements.txt                 # Python dependencies
│   ├── .env                             # Environment variables (MongoDB URI)
│   ├── flight_model.pkl                 # Copy of price model
│   ├── delay_model.pkl                  # Copy of delay model
│   ├── label_encoders.pkl               # Copy of encoders
│   ├── feature_names.pkl                # Copy of feature names
│   ├── model_metadata.pkl               # Copy of metadata
│   ├── README.md                        # API-specific readme
│   └── ML_INTEGRATION_GUIDE.md          # ML integration guide
│
├── 🎨 src/                               # React Frontend
│   ├── app/
│   │   ├── App.tsx                      # Main app component
│   │   ├── components/
│   │   │   ├── FlightPricePredictor.jsx # Price prediction form & results
│   │   │   ├── DelayProbabilityDashboard.jsx # Delay analysis dashboard
│   │   │   ├── LanguageSwitcher.jsx     # Vietnamese/English toggle
│   │   │   ├── ui/                      # Shadcn UI components
│   │   │   └── figma/                   # Figma exported components
│   │   └── context/
│   │       └── LanguageContext.jsx      # i18n context provider
│   └── styles/
│       ├── index.css                    # Main styles
│       ├── tailwind.css                 # Tailwind imports
│       ├── theme.css                    # Color theme variables
│       └── fonts.css                    # Font definitions
│

├── 🐍 scripts/                           # Training & Testing Scripts
│   ├── train.py                         # Complete training pipeline
│   │                                    # • Loads data from data/
│   │                                    # • Engineers features
│   │                                    # • Creates label encoders
│   │                                    # • Trains RandomForest models
│   │                                    # • Saves to models/ and api/
│   │
│   └── test_predict_endpoint.py         # API endpoint testing
│                                        # • Tests /predict endpoint
│                                        # • Multiple test cases
│                                        # • Validates responses
│
├── 📚 docs/                              # Documentation
│   ├── API_USAGE.md                     # Complete API documentation
│   │                                    # • All endpoints
│   │                                    # • Request/response examples
│   │                                    # • cURL examples
│   │                                    # • Python examples
│   │
│   ├── FULLSTACK_SETUP.md               # Full setup guide
│   │                                    # • Prerequisites
│   │                                    # • Backend setup
│   │                                    # • Frontend setup
│   │                                    # • Troubleshooting
│   │
│   ├── COMPLETED.md                     # Features completed
│   │                                    # • Implementation details
│   │                                    # • React integration
│   │                                    # • API integration
│   │
│   └── LABEL_ENCODERS_GUIDE.md          # Encoder usage guide
│                                        # • What are encoders
│                                        # • How to use them
│                                        # • Integration examples
│
├── 📖 guidelines/                        # Development guidelines
│   └── Guidelines.md                    # Coding standards
│
├── ⚙️ Configuration Files (Root)
│   ├── README.md                        # 🌟 START HERE - Project overview
│   ├── start.ps1                        # 🚀 Quick start script
│   ├── .gitignore                       # Git ignore rules
│   ├── package.json                     # Node.js dependencies
│   ├── package-lock.json                # Lock file
│   ├── vite.config.ts                   # Vite build config
│   ├── postcss.config.mjs               # PostCSS config
│   ├── ATTRIBUTIONS.md                  # Third-party attributions
│   └── PROJECT_STRUCTURE.md             # This file
│
└── 🗂️ Other Folders
    ├── node_modules/                    # Node.js packages (git-ignored)
    └── __pycache__/                     # Python cache (git-ignored)
```

---

## 🎯 Quick Navigation

### For Users
1. **Getting Started**: Read [README.md](../README.md)
2. **Setup Guide**: See [docs/FULLSTACK_SETUP.md](docs/FULLSTACK_SETUP.md)
3. **Quick Start**: Run `.\start.ps1` from root

### For Developers
1. **Backend API**: [api/app.py](../api/app.py)
2. **Frontend Components**: [src/app/components/](../src/app/components/)
3. **Training Pipeline**: [scripts/train.py](../scripts/train.py)
4. **Pydantic Models**: [api/models.py](../api/models.py)

### For Documentation
1. **API Docs**: [docs/API_USAGE.md](docs/API_USAGE.md)
2. **Setup Guide**: [docs/FULLSTACK_SETUP.md](docs/FULLSTACK_SETUP.md)
3. **Encoders Guide**: [docs/LABEL_ENCODERS_GUIDE.md](docs/LABEL_ENCODERS_GUIDE.md)

---

## 📊 Data Flow

```
1. Training Phase:
   data/airlines_flights_data.csv 
      ↓ scripts/train.py
      ↓
   models/*.pkl (saved)
      ↓ (copied to)
   api/*.pkl

2. Prediction Phase:
   User Input (React Form)
      ↓ axios POST
   FastAPI Backend (api/app.py)
      ↓ loads
   api/*.pkl models
      ↓ predicts
   Response JSON
      ↓
   React UI displays results
      ↓
   MongoDB saves prediction
```

---

## 🔧 File Purposes

### Data Files
- **airlines_flights_data.csv**: Original dataset, never modified
- **cleaned_flights.csv**: Preprocessed with one-hot encoding for training

### Model Files
- **flight_model.pkl**: Trained RandomForestRegressor for price prediction
- **delay_model.pkl**: Trained RandomForestClassifier for delay prediction
- **label_encoders.pkl**: Dictionary of 9 LabelEncoders for categorical variables
- **feature_names.pkl**: List of 30 feature names in correct order
- **model_metadata.pkl**: Training metrics, R², MAE, RMSE, timestamps

### Why Models in Both Folders?
- **models/**: Source of truth, version controlled
- **api/**: Working copies for FastAPI server to load

---

## 🚀 Common Commands

### Training
```powershell
cd scripts
python train.py
```

### Testing Backend
```powershell
cd scripts
python test_predict_endpoint.py
```

### Starting Servers
```powershell
# Option 1: Automatic (recommended)
.\start.ps1

# Option 2: Manual
# Terminal 1:
cd api
uvicorn app:app --reload --port 8000

# Terminal 2:
npm run dev
```

---

## 📦 Key Dependencies

### Python (Backend)
- fastapi - Web framework
- motor - Async MongoDB driver
- scikit-learn - ML models
- pandas - Data processing
- joblib - Model serialization

### Node.js (Frontend)
- react - UI framework
- axios - HTTP client
- vite - Build tool
- tailwindcss - Styling
- lucide-react - Icons

---

## 🔐 Environment Variables

Create `.env` in `api/`:
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=flight_price_prediction
```

---

## 📈 Model Performance

**Price Prediction (flight_model.pkl)**
- R² Score: 98.14%
- MAE: ₹421.50
- RMSE: ₹742.30

**Delay Prediction (delay_model.pkl)**  
- Accuracy: 90.22%
- Low/Medium/High risk classification

---

## 💡 Tips

1. **Always start MongoDB first** before backend
2. **Models must exist** in both `models/` and `api/`
3. **Run train.py** if models are missing
4. **Check docs/** for detailed guides
5. **Use start.ps1** for quick development

---

**Last Updated**: March 10, 2026  
**Maintained by**: Flight Price Prediction Team
