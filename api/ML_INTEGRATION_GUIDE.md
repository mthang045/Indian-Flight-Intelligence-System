# FastAPI ML Model Integration - Complete Guide

## 🎯 Overview

Your FastAPI app now automatically loads the trained ML model (`flight_model.pkl`) on startup and uses it for real predictions in the `/api/v2/predict` endpoint.

## 📁 Files Updated

### 1. **api/app.py** - Main FastAPI Application
**Changes Made:**
- ✅ Added imports: `joblib`, `pandas`, `os`, `Path`
- ✅ Created global variable `ml_model` to store the loaded model
- ✅ Updated `@app.on_event("startup")` to load the model using `joblib.load()`
- ✅ Added `prepare_prediction_dataframe()` function to convert request data to DataFrame
- ✅ Added `ml_model_prediction()` function to use the real model
- ✅ Updated `/api/v2/predict` endpoint to use real ML predictions
- ✅ Updated `/health` endpoint to show model loading status

### 2. **api/models.py** - Pydantic Models
**Changes Made:**
- ✅ Updated `HealthCheck` model to include `model_loaded` and `model_path` fields

### 3. **api/requirements.txt** - Python Dependencies
**Changes Made:**
- ✅ Added `pandas==2.1.4`
- ✅ Added `joblib==1.3.2`
- ✅ Added `scikit-learn==1.3.2`

## 🚀 How It Works

### **1. Server Startup**
When you run `python app.py`, the server:

```python
# On startup:
@app.on_event("startup")
async def startup_db_client():
    global ml_model
    
    # Load the model from flight_model.pkl
    if MODEL_PATH.exists():
        ml_model = joblib.load(MODEL_PATH)  # ✅ Model loaded!
        print("✅ ML model loaded from flight_model.pkl")
    else:
        print("⚠️ Model file not found, using mock predictions")
```

### **2. Prediction Request**
When a POST request comes to `/api/v2/predict`:

```python
# Step 1: Receive PredictionRequest
request = {
    "airline": "IndiGo",
    "source": "DEL",
    "destination": "BOM",
    "departure_time": "06:30:00",
    "arrival_time": "08:45:00",
    "duration_minutes": 135,
    "day": 25,
    "month": 3,
    "year": 2024,
    "departure_hour": 6,
    "arrival_hour": 8,
    "stops": 0,
    "flight_class": "Economy",
    "days_left": 14
}

# Step 2: Convert to DataFrame
df = prepare_prediction_dataframe(request)
# DataFrame columns match training data:
# ['airline', 'arrival_hour', 'arrival_period', 'class', 'day', 
#  'days_left', 'departure_hour', 'departure_period', 'destination_city',
#  'duration_minutes', 'month', 'source_city', 'stops_numeric', 'year']

# Step 3: Predict using model
predicted_price = ml_model.predict(df)[0]  # Real ML prediction!

# Step 4: Return JSON response
return {
    "prediction": {
        "predicted_price": 4850.25,
        "confidence_score": 85.0,
        "delay_risk": "Low",
        "price_range": {"min": 4122.71, "max": 5577.79}
    },
    "saved_id": "507f191e810c19729de860ea",
    "timestamp": "2024-03-10T10:30:00Z"
}
```

### **3. DataFrame Column Mapping**

The `prepare_prediction_dataframe()` function ensures the DataFrame has the exact columns your model expects:

```python
def prepare_prediction_dataframe(request: PredictionRequest) -> pd.DataFrame:
    # Determine time periods
    def get_period(hour: int) -> str:
        if 5 <= hour < 12: return "Morning"
        elif 12 <= hour < 17: return "Afternoon"
        elif 17 <= hour < 21: return "Evening"
        else: return "Night"
    
    # Create DataFrame with exact column order
    data = {
        'airline': request.airline,                    # IndiGo, Air India, etc.
        'arrival_hour': request.arrival_hour,          # 0-23
        'arrival_period': get_period(request.arrival_hour),
        'class': request.flight_class,                 # Economy/Business
        'day': request.day,                            # 1-31
        'days_left': request.days_left,                # Days until departure
        'departure_hour': request.departure_hour,      # 0-23
        'departure_period': get_period(request.departure_hour),
        'destination_city': request.destination,       # DEL, BOM, etc.
        'duration_minutes': request.duration_minutes,  # Flight duration
        'month': request.month,                        # 1-12
        'source_city': request.source,                 # Origin city
        'stops_numeric': request.stops,                # 0, 1, 2...
        'year': request.year                           # 2024, 2025, etc.
    }
    
    return pd.DataFrame([data])  # Single row DataFrame
```

## 📋 Step-by-Step Usage

### **Step 1: Train and Save Your Model**

Run the example training script:

```bash
cd api
python train_model_example.py
```

This will:
- Load `cleaned_flights_simple.csv`
- Train a Random Forest model
- Save it as `flight_model.pkl`

### **Step 2: Start the FastAPI Server**

```bash
cd api
python app.py
```

You should see:
```
✅ MongoDB connected!
✅ ML model loaded from c:\...\api\flight_model.pkl
🚀 FastAPI server started!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **Step 3: Check Health Status**

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "model_loaded": true,
  "model_path": "c:\\...\\api\\flight_model.pkl",
  "timestamp": "2024-03-10T10:30:00Z"
}
```

### **Step 4: Make a Prediction**

```bash
curl -X POST http://localhost:8000/api/v2/predict \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "IndiGo",
    "source": "DEL",
    "destination": "BOM",
    "departure_time": "06:30:00",
    "arrival_time": "08:45:00",
    "duration_minutes": 135,
    "day": 25,
    "month": 3,
    "year": 2024,
    "departure_hour": 6,
    "arrival_hour": 8,
    "stops": 0,
    "flight_class": "Economy",
    "days_left": 14
  }'
```

Response:
```json
{
  "prediction": {
    "predicted_price": 4850.25,
    "confidence_score": 85.0,
    "delay_risk": "Low",
    "price_range": {
      "min": 4122.71,
      "max": 5577.79
    },
    "features_used": {
      "airline": "IndiGo",
      "route": "DEL-BOM",
      "duration_minutes": 135,
      "class": "Economy",
      "days_left": 14
    }
  },
  "saved_id": "507f191e810c19729de860ea",
  "timestamp": "2024-03-10T10:30:00Z"
}
```

### **Step 5: Test from React Frontend**

```javascript
// In your React component
const predictPrice = async (flightData) => {
  try {
    const response = await fetch('http://localhost:8000/api/v2/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        airline: "IndiGo",
        source: "DEL",
        destination: "BOM",
        departure_time: "06:30:00",
        arrival_time: "08:45:00",
        duration_minutes: 135,
        day: 25,
        month: 3,
        year: 2024,
        departure_hour: 6,
        arrival_hour: 8,
        stops: 0,
        flight_class: "Economy",
        days_left: 14
      })
    });
    
    const data = await response.json();
    console.log('Predicted Price:', data.prediction.predicted_price);
    console.log('Confidence:', data.prediction.confidence_score);
    
    return data;
  } catch (error) {
    console.error('Prediction error:', error);
  }
};
```

## 🧪 Testing

Run the automated test script:

```bash
cd api
python test_prediction_api.py
```

This will:
- ✅ Check health endpoint
- ✅ Test single prediction
- ✅ Test multiple scenarios (different airlines, routes, times)

## 🔄 Fallback Behavior

If the model file doesn't exist or fails to load:
- ⚠️ The API will use **mock predictions** (rule-based)
- ℹ️ Server logs will show: `"Using mock prediction (model not loaded)"`
- ✅ The API continues to work normally
- 💡 Train and save a model to enable real ML predictions

## 📊 Model Column Requirements

Your trained model **MUST** expect these columns in this order:

1. `airline` - Airline name (string)
2. `arrival_hour` - Arrival hour 0-23 (int)
3. `arrival_period` - Morning/Afternoon/Evening/Night (string)
4. `class` - Economy/Business (string)
5. `day` - Day of month 1-31 (int)
6. `days_left` - Days until departure (int)
7. `departure_hour` - Departure hour 0-23 (int)
8. `departure_period` - Morning/Afternoon/Evening/Night (string)
9. `destination_city` - Destination code (string)
10. `duration_minutes` - Flight duration (int)
11. `month` - Month 1-12 (int)
12. `source_city` - Origin code (string)
13. `stops_numeric` - Number of stops (int)
14. `year` - Year (int)

**Important:** If your model was trained with one-hot encoded categorical variables, you'll need to update the `prepare_prediction_dataframe()` function to match that encoding.

## 🛠️ Troubleshooting

### Problem: Model Not Loading
```
⚠️ Warning: Model file not found at c:\...\api\flight_model.pkl
```

**Solution:** Train and save the model first:
```bash
python train_model_example.py
```

### Problem: Prediction Error
```
❌ Error during ML prediction: could not convert string to float
```

**Solution:** Check that your model expects the same data types and encoding as the `prepare_prediction_dataframe()` function provides.

### Problem: Wrong Column Order
```
ValueError: Number of features of the model must match the input
```

**Solution:** Verify the column order in `prepare_prediction_dataframe()` matches your training data.

## 🎓 Next Steps

1. **Improve the Model**
   - Try XGBoost, LightGBM, or Neural Networks
   - Add hyperparameter tuning
   - Use cross-validation

2. **Add Model Versioning**
   - Save models with timestamps: `flight_model_v1_20240310.pkl`
   - Track model performance metrics
   - Allow model rollback

3. **Add Prediction Confidence**
   - Use model's `predict_proba()` or feature importance
   - Calculate prediction intervals
   - Show confidence scores to users

4. **Monitor Model Performance**
   - Log all predictions to database
   - Compare predictions vs actual prices
   - Retrain model periodically

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

✅ **Your FastAPI app is now integrated with ML model predictions!**
