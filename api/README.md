# FastAPI Backend - Flight Price Prediction

RESTful API backend for Indian Flight Price Prediction using FastAPI and MongoDB.

## 🚀 Features

- ✅ FastAPI with async/await support
- ✅ MongoDB with Motor (async driver)
- ✅ Pydantic models for data validation
- ✅ CORS enabled for frontend integration
- ✅ Interactive API documentation (Swagger UI)
- ✅ Environment-based configuration

## 📁 Project Structure

```
api/
├── app.py              # Main FastAPI application
├── database.py         # MongoDB connection
├── models.py           # Pydantic models
├── .env               # Environment variables
├── .env.example       # Example environment file
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## 🔧 Installation

1. **Install dependencies:**
```bash
cd api
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
copy .env.example .env
```

Edit `.env` and configure your MongoDB URI.

3. **Run the server:**
```bash
uvicorn app:app --reload
```

Or using Python:
```bash
python app.py
```

## 📡 API Endpoints

### Root & Health
- `GET /` - API information
- `GET /health` - Health check

### Flights
- `POST /flights` - Add new flight
- `GET /flights` - Get all flights (with filtering)
- `GET /flights/{id}` - Get flight by ID
- `DELETE /flights/{id}` - Delete flight
- `GET /flights/statistics` - Get flight statistics

### Predictions
- `POST /predict` - Predict flight price
- `GET /predictions` - Get prediction history

## 📚 Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 MongoDB Connection

The API uses Motor (async MongoDB driver) for database operations.

Default connection: `mongodb://localhost:27017`

## 🧪 Testing Endpoints

### Add a Flight
```bash
curl -X POST "http://localhost:8000/flights" \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "IndiGo",
    "flight_number": "6E-2045",
    "source_city": "DEL",
    "destination_city": "BOM",
    "departure_time": "06:30:00",
    "arrival_time": "08:45:00",
    "duration_minutes": 135,
    "stops": 0,
    "flight_class": "Economy",
    "days_left": 14,
    "price": 4500
  }'
```

### Predict Price
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "IndiGo",
    "source_city": "DEL",
    "destination_city": "BOM",
    "departure_time": "06:30:00",
    "arrival_time": "08:45:00",
    "duration_minutes": 135,
    "stops": 0,
    "flight_class": "Economy",
    "days_left": 14
  }'
```

## 🔄 Integration with ML Model

The `/predict` endpoint currently uses a mock prediction function. 

To integrate your actual ML model:
1. Train your model using the cleaned CSV data
2. Save the model (e.g., using joblib or pickle)
3. Replace `mock_ml_prediction()` in `app.py` with actual model inference

## 🛠 Tech Stack

- **FastAPI** - Modern web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 📝 License

MIT
