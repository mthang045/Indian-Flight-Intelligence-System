from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime
import random
import joblib
import pandas as pd
import numpy as np
import os
from pathlib import Path

from database import Database, get_database, FLIGHTS_COLLECTION, PREDICTIONS_COLLECTION
from models import (
    FlightCreate, FlightResponse, FlightStatistics,
    PredictionInput, PredictionRequest, PredictionResult, PredictionResponse, PredictionInDB,
    DelayPredictionRequest, DelayPredictionResult,
    SimplePredictionRequest, SimplePredictionResponse,
    HealthCheck
)

# Global variables to store ML models and encoders
ml_model = None
delay_model_data = None
label_encoders = None
MODEL_PATH = Path(__file__).parent / "flight_model.pkl"
DELAY_MODEL_PATH = Path(__file__).parent / "delay_model.pkl"
ENCODERS_PATH = Path(__file__).parent / "label_encoders.pkl"

# Initialize FastAPI app
app = FastAPI(
    title="Flight Price Prediction API",
    description="FastAPI backend for Indian Flight Price Prediction with MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_db_client():
    """Connect to MongoDB and load ML models on startup"""
    global ml_model, delay_model_data, label_encoders
    
    print("=" * 80)
    print("🚀 STARTING FASTAPI SERVER")
    print("=" * 80)
    
    # Connect to MongoDB
    await Database.connect_db()
    print("✅ MongoDB connected!")
    
    # Load Price Prediction ML model
    try:
        if MODEL_PATH.exists():
            ml_model = joblib.load(MODEL_PATH)
            print(f"✅ Price prediction model loaded from {MODEL_PATH}")
            if hasattr(ml_model, 'n_estimators'):
                print(f"   • Model type: {type(ml_model).__name__}")
                print(f"   • n_estimators: {ml_model.n_estimators}")
                print(f"   • n_features: {ml_model.n_features_in_}")
        else:
            print(f"⚠️  Warning: Price model not found at {MODEL_PATH}")
            print("   Using mock predictions until model is trained and saved.")
    except Exception as e:
        print(f"❌ Error loading price model: {str(e)}")
        print("   Using mock predictions.")
    
    # Load Label Encoders
    try:
        if ENCODERS_PATH.exists():
            label_encoders = joblib.load(ENCODERS_PATH)
            print(f"✅ Label encoders loaded from {ENCODERS_PATH}")
            print(f"   • Number of encoders: {len(label_encoders)}")
            print(f"   • Available encoders: {list(label_encoders.keys())}")
        else:
            print(f"⚠️  Warning: Label encoders not found at {ENCODERS_PATH}")
            print("   Some features may not work correctly.")
    except Exception as e:
        print(f"❌ Error loading label encoders: {str(e)}")
    
    # Load Delay Prediction model
    try:
        if DELAY_MODEL_PATH.exists():
            delay_model_data = joblib.load(DELAY_MODEL_PATH)
            print(f"✅ Delay prediction model loaded from {DELAY_MODEL_PATH}")
        else:
            print(f"⚠️  Warning: Delay model not found at {DELAY_MODEL_PATH}")
    except Exception as e:
        print(f"❌ Error loading delay model: {str(e)}")
    
    print("=" * 80)
    print("✅ FastAPI server ready!")
    print("=" * 80)

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB connection on shutdown"""
    await Database.close_db()
    print("👋 FastAPI server stopped!")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def get_flights_collection():
    """Get flights collection"""
    return Database.get_collection(FLIGHTS_COLLECTION)

async def get_predictions_collection():
    """Get predictions collection"""
    return Database.get_collection(PREDICTIONS_COLLECTION)

def transform_simple_input_with_encoders(request: SimplePredictionRequest) -> pd.DataFrame:
    """
    Transform SimplePredictionRequest to match the exact training data structure.
    
    Must produce 30 features matching the trained model:
    - Numeric: days_left, day, month, year, duration_minutes, stops_numeric, departure_hour, arrival_hour
    - One-hot: airline_*, source_city_*, destination_city_*, class_*, *_period_Unknown
    
    Returns:
        pd.DataFrame with exactly 30 features matching the trained model
    """
    from datetime import datetime as dt
    
    # Parse date
    try:
        journey_date = dt.strptime(request.date, "%Y-%m-%d")
        day = journey_date.day
        month = journey_date.month
        year = journey_date.year
    except:
        now = dt.now()
        day = now.day
        month = now.month
        year = now.year
    
    # Map time period strings to hours
    time_to_hour = {
        'Morning': 8,
        'Afternoon': 14,
        'Evening': 18,
        'Night': 22,
        'Early_Morning': 6,
        'Late_Night': 23
    }
    
    departure_hour = time_to_hour.get(request.departure_time, 8)
    arrival_hour = time_to_hour.get(request.arrival_time, 14)
    
    # Initialize all 30 features with 0
    data = {
        # Numeric features (8)
        'days_left': request.days_left,
        'day': day,
        'month': month,
        'year': year,
        'duration_minutes': request.duration_minutes,
        'stops_numeric': request.stops,
        'departure_hour': departure_hour,
        'arrival_hour': arrival_hour,
        
        # One-hot: Airlines (6)
        'airline_AirAsia': 0,
        'airline_Air_India': 0,
        'airline_GO_FIRST': 0,
        'airline_Indigo': 0,
        'airline_SpiceJet': 0,
        'airline_Vistara': 0,
        
        # One-hot: Source cities (6)
        'source_city_Bangalore': 0,
        'source_city_Chennai': 0,
        'source_city_Delhi': 0,
        'source_city_Hyderabad': 0,
        'source_city_Kolkata': 0,
        'source_city_Mumbai': 0,
        
        # One-hot: Destination cities (6)
        'destination_city_Bangalore': 0,
        'destination_city_Chennai': 0,
        'destination_city_Delhi': 0,
        'destination_city_Hyderabad': 0,
        'destination_city_Kolkata': 0,
        'destination_city_Mumbai': 0,
        
        # One-hot: Class (2)
        'class_Business': 0,
        'class_Economy': 0,
        
        # Time period flags (2)
        'departure_period_Unknown': 0,
        'arrival_period_Unknown': 0
    }
    
    # Set airline (normalize names)
    airline_map = {
        'AirAsia': 'airline_AirAsia',
        'AirAsia India': 'airline_AirAsia',
        'Air India': 'airline_Air_India',
        'Air_India': 'airline_Air_India',
        'GO_FIRST': 'airline_GO_FIRST',
        'Go First': 'airline_GO_FIRST',
        'IndiGo': 'airline_Indigo',
        'Indigo': 'airline_Indigo',
        'SpiceJet': 'airline_SpiceJet',
        'Vistara': 'airline_Vistara'
    }
    airline_col = airline_map.get(request.airline, None)
    if airline_col and airline_col in data:
        data[airline_col] = 1
    
    # Set source city
    city_names = {
        'BLR': 'Bangalore', 'Bangalore': 'Bangalore',
        'MAA': 'Chennai', 'Chennai': 'Chennai',
        'DEL': 'Delhi', 'Delhi': 'Delhi',
        'HYD': 'Hyderabad', 'Hyderabad': 'Hyderabad',
        'CCU': 'Kolkata', 'Kolkata': 'Kolkata',
        'BOM': 'Mumbai', 'Mumbai': 'Mumbai'
    }
    source_name = city_names.get(request.source, request.source)
    source_col = f'source_city_{source_name}'
    if source_col in data:
        data[source_col] = 1
    
    # Set destination city
    dest_name = city_names.get(request.destination, request.destination)
    dest_col = f'destination_city_{dest_name}'
    if dest_col in data:
        data[dest_col] = 1
    
    # Set class
    if request.flight_class == 'Business':
        data['class_Business'] = 1
    else:
        data['class_Economy'] = 1
    
    # Create DataFrame
    df = pd.DataFrame([data])
    
    return df

def prepare_prediction_dataframe(request: PredictionRequest) -> pd.DataFrame:
    """
    Convert PredictionRequest to pandas DataFrame with ONE-HOT ENCODED features.
    Must match the exact training data structure from cleaned_flights.csv:
    
    Features (30 columns):
    - Numeric: days_left, day, month, year, duration_minutes, stops_numeric, departure_hour, arrival_hour
    - One-hot: airline_*, source_city_*, destination_city_*, class_*, *_period_Unknown
    """
    
    # Initialize all features with 0 (for one-hot encoding)
    data = {
        # Numeric features
        'days_left': request.days_left,
        'day': request.day,
        'month': request.month,
        'year': request.year,
        'duration_minutes': request.duration_minutes,
        'stops_numeric': request.stops,
        'departure_hour': request.departure_hour,
        'arrival_hour': request.arrival_hour,
        
        # One-hot encoded: Airlines
        'airline_AirAsia': 0,
        'airline_Air_India': 0,
        'airline_GO_FIRST': 0,
        'airline_Indigo': 0,
        'airline_SpiceJet': 0,
        'airline_Vistara': 0,
        
        # One-hot encoded: Source cities
        'source_city_Bangalore': 0,
        'source_city_Chennai': 0,
        'source_city_Delhi': 0,
        'source_city_Hyderabad': 0,
        'source_city_Kolkata': 0,
        'source_city_Mumbai': 0,
        
        # One-hot encoded: Destination cities
        'destination_city_Bangalore': 0,
        'destination_city_Chennai': 0,
        'destination_city_Delhi': 0,
        'destination_city_Hyderabad': 0,
        'destination_city_Kolkata': 0,
        'destination_city_Mumbai': 0,
        
        # One-hot encoded: Class
        'class_Business': 0,
        'class_Economy': 0,
        
        # One-hot encoded: Time periods (Unknown flags)
        'departure_period_Unknown': 0,
        'arrival_period_Unknown': 0
    }
    
    # Set the appropriate one-hot encoded values
    
    # Airline mapping
    airline_map = {
        'AirAsia': 'airline_AirAsia',
        'Air India': 'airline_Air_India',
        'Air_India': 'airline_Air_India',
        'GO_FIRST': 'airline_GO_FIRST',
        'IndiGo': 'airline_Indigo',
        'Indigo': 'airline_Indigo',
        'SpiceJet': 'airline_SpiceJet',
        'Vistara': 'airline_Vistara'
    }
    airline_col = airline_map.get(request.airline, f'airline_{request.airline}')
    if airline_col in data:
        data[airline_col] = 1
    
    # Source city mapping
    city_names = {
        'BLR': 'Bangalore',
        'MAA': 'Chennai',
        'DEL': 'Delhi',
        'HYD': 'Hyderabad',
        'CCU': 'Kolkata',
        'BOM': 'Mumbai'
    }
    source_city_name = city_names.get(request.source, request.source)
    source_col = f'source_city_{source_city_name}'
    if source_col in data:
        data[source_col] = 1
    
    # Destination city mapping
    dest_city_name = city_names.get(request.destination, request.destination)
    dest_col = f'destination_city_{dest_city_name}'
    if dest_col in data:
        data[dest_col] = 1
    
    # Flight class
    if request.flight_class == 'Business':
        data['class_Business'] = 1
    else:  # Economy
        data['class_Economy'] = 1
    
    # Time periods - set to 0 (not Unknown)
    # In the training data, departure_period_Unknown and arrival_period_Unknown 
    # are flags for unknown time periods. Since we have valid hours, set to 0.
    data['departure_period_Unknown'] = 0
    data['arrival_period_Unknown'] = 0
    
    # Create DataFrame with single row
    df = pd.DataFrame([data])
    
    return df

def ml_model_prediction(request: PredictionRequest) -> PredictionResult:
    """
    Use the trained ML model to predict flight price.
    Falls back to mock prediction if model is not available.
    """
    global ml_model
    
    if ml_model is None:
        # Fallback to mock prediction
        print("⚠️  Warning: Using mock prediction (model not loaded)")
        legacy_input = PredictionInput(
            airline=request.airline,
            source_city=request.source,
            destination_city=request.destination,
            departure_time=request.departure_time,
            arrival_time=request.arrival_time,
            duration_minutes=request.duration_minutes,
            stops=request.stops,
            flight_class=request.flight_class,
            days_left=request.days_left,
            day=request.day,
            month=request.month,
            departure_hour=request.departure_hour
        )
        return mock_ml_prediction(legacy_input)
    
    try:
        # Prepare input DataFrame
        input_df = prepare_prediction_dataframe(request)
        
        # Make prediction
        predicted_price = ml_model.predict(input_df)[0]
        predicted_price = float(round(predicted_price, 2))
        
        # Calculate confidence score (you can enhance this based on model metrics)
        confidence = 85.0  # Default confidence
        
        # Determine delay risk based on stops
        if request.stops > 1:
            delay_risk = "High"
        elif request.stops == 1:
            delay_risk = "Medium"
        else:
            delay_risk = "Low"
        
        # Calculate price range (±15%)
        price_range = {
            "min": round(predicted_price * 0.85, 2),
            "max": round(predicted_price * 1.15, 2)
        }
        
        return PredictionResult(
            predicted_price=predicted_price,
            confidence_score=confidence,
            delay_risk=delay_risk,
            price_range=price_range,
            features_used={
                "airline": request.airline,
                "route": f"{request.source}-{request.destination}",
                "duration_minutes": request.duration_minutes,
                "class": request.flight_class,
                "days_left": request.days_left
            }
        )
    except Exception as e:
        print(f"❌ Error during ML prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"ML prediction failed: {str(e)}")

def mock_ml_prediction(input_data: PredictionInput) -> PredictionResult:
    """
    Mock ML prediction function.
    TODO: Replace this with actual ML model inference.
    """
    # Base price calculation based on duration
    base_price = 2000 + (input_data.duration_minutes * 15)
    
    # Airline multiplier
    airline_multipliers = {
        "Vistara": 2.5,
        "Air_India": 2.0,
        "Air India": 2.0,
        "IndiGo": 1.0,
        "Indigo": 1.0,
        "SpiceJet": 0.9,
        "GO_FIRST": 0.85,
        "AirAsia": 0.8
    }
    airline_mult = airline_multipliers.get(input_data.airline, 1.0)
    
    # Class multiplier
    class_mult = 3.5 if input_data.flight_class == "Business" else 1.0
    
    # Days left adjustment (early booking discount)
    days_mult = 1.0 - (input_data.days_left / 365) * 0.2
    
    # Calculate predicted price
    predicted_price = base_price * airline_mult * class_mult * days_mult
    predicted_price = round(predicted_price, 2)
    
    # Calculate confidence score (higher for common routes)
    confidence = random.uniform(75, 95)
    
    # Determine delay risk (simple logic)
    if input_data.stops > 1:
        delay_risk = "High"
    elif input_data.stops == 1:
        delay_risk = "Medium"
    else:
        delay_risk = "Low"
    
    # Price range (±20%)
    price_range = {
        "min": round(predicted_price * 0.8, 2),
        "max": round(predicted_price * 1.2, 2)
    }
    
    return PredictionResult(
        predicted_price=predicted_price,
        confidence_score=round(confidence, 2),
        delay_risk=delay_risk,
        price_range=price_range,
        features_used={
            "airline": input_data.airline,
            "route": f"{input_data.source_city}-{input_data.destination_city}",
            "duration_minutes": input_data.duration_minutes,
            "class": input_data.flight_class
        }
    )

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "✈️ Flight Price Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthCheck, tags=["Root"])
async def health_check():
    """Health check endpoint - includes database and ML models status"""
    global ml_model, delay_model_data
    
    try:
        # Test database connection
        db = Database.get_database()
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return HealthCheck(
        status="healthy" if db_status == "connected" else "unhealthy",
        database=db_status,
        model_loaded=(ml_model is not None),
        model_path=str(MODEL_PATH),
        delay_model_loaded=(delay_model_data is not None),
        delay_model_path=str(DELAY_MODEL_PATH)
    )

# ============================================================================
# FLIGHT ENDPOINTS
# ============================================================================

@app.post("/flights", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Flights"])
async def add_flight(flight: FlightCreate, collection=Depends(get_flights_collection)):
    """
    Add a new flight to the database.
    
    - **airline**: Airline name (e.g., IndiGo, Air India)
    - **flight_number**: Flight number (e.g., 6E-2045)
    - **source_city**: Origin city code (e.g., DEL)
    - **destination_city**: Destination city code (e.g., BOM)
    - **price**: Ticket price in INR
    """
    try:
        flight_dict = flight.model_dump()
        flight_dict["created_at"] = datetime.utcnow()
        flight_dict["updated_at"] = datetime.utcnow()
        
        result = await collection.insert_one(flight_dict)
        
        return {
            "message": "Flight added successfully",
            "flight_id": str(result.inserted_id),
            "flight": flight_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding flight: {str(e)}")

@app.get("/flights", response_model=List[dict], tags=["Flights"])
async def get_all_flights(
    limit: int = 100,
    skip: int = 0,
    airline: Optional[str] = None,
    source_city: Optional[str] = None,
    destination_city: Optional[str] = None,
    collection=Depends(get_flights_collection)
):
    """
    Get all flights with optional filtering.
    
    - **limit**: Maximum number of flights to return (default: 100)
    - **skip**: Number of flights to skip (pagination)
    - **airline**: Filter by airline
    - **source_city**: Filter by origin city
    - **destination_city**: Filter by destination city
    """
    try:
        # Build query filter
        query = {}
        if airline:
            query["airline"] = airline
        if source_city:
            query["source_city"] = source_city
        if destination_city:
            query["destination_city"] = destination_city
        
        # Query database
        cursor = collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
        flights = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for flight in flights:
            flight["_id"] = str(flight["_id"])
        
        return flights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching flights: {str(e)}")

@app.get("/flights/{flight_id}", response_model=dict, tags=["Flights"])
async def get_flight_by_id(flight_id: str, collection=Depends(get_flights_collection)):
    """Get a specific flight by ID"""
    try:
        from bson import ObjectId
        flight = await collection.find_one({"_id": ObjectId(flight_id)})
        
        if not flight:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        flight["_id"] = str(flight["_id"])
        return flight
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching flight: {str(e)}")

@app.delete("/flights/{flight_id}", tags=["Flights"])
async def delete_flight(flight_id: str, collection=Depends(get_flights_collection)):
    """Delete a flight by ID"""
    try:
        from bson import ObjectId
        result = await collection.delete_one({"_id": ObjectId(flight_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        return {"message": "Flight deleted successfully", "flight_id": flight_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting flight: {str(e)}")

@app.get("/flights/statistics", response_model=FlightStatistics, tags=["Flights"])
async def get_flight_statistics(collection=Depends(get_flights_collection)):
    """Get statistics about flights in the database"""
    try:
        total_flights = await collection.count_documents({})
        
        # Get unique airlines
        airlines = await collection.distinct("airline")
        
        # Get popular routes
        pipeline = [
            {"$group": {
                "_id": {"source": "$source_city", "destination": "$destination_city"},
                "count": {"$sum": 1},
                "avg_price": {"$avg": "$price"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        routes_cursor = collection.aggregate(pipeline)
        routes = await routes_cursor.to_list(length=10)
        
        # Calculate average price
        price_pipeline = [
            {"$group": {
                "_id": None,
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "avg_duration": {"$avg": "$duration_minutes"}
            }}
        ]
        stats_cursor = collection.aggregate(price_pipeline)
        stats = await stats_cursor.to_list(length=1)
        
        if stats:
            stat = stats[0]
            return FlightStatistics(
                total_flights=total_flights,
                airlines=airlines,
                routes=routes,
                avg_price=round(stat["avg_price"], 2),
                price_range={"min": stat["min_price"], "max": stat["max_price"]},
                avg_duration=round(stat["avg_duration"], 2)
            )
        else:
            return FlightStatistics(
                total_flights=0,
                airlines=[],
                routes=[],
                avg_price=0,
                price_range={"min": 0, "max": 0},
                avg_duration=0
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

# ============================================================================
# PREDICTION ENDPOINTS
# ============================================================================

# OLD ENDPOINT - COMMENTED OUT (causes conflict with unified /predict endpoint)
# @app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
# async def predict_price(
#     input_data: PredictionInput,
#     collection=Depends(get_predictions_collection)
# ):
#     """
#     Predict flight price based on input features.
#     
#     This endpoint will call the ML model to predict flight prices.
#     Currently using a mock prediction function.
#     """
#     try:
#         # Get prediction from ML model (currently mock)
#         prediction = mock_ml_prediction(input_data)
#         
#         # Save prediction to database
#         prediction_doc = PredictionInDB(
#             input_data=input_data.model_dump(),
#             predicted_price=prediction.predicted_price,
#             confidence_score=prediction.confidence_score,
#             delay_risk=prediction.delay_risk
#         )
#         
#         result = await collection.insert_one(prediction_doc.model_dump(by_alias=True))
#         
#         return PredictionResponse(
#             prediction=prediction,
#             saved_id=str(result.inserted_id),
#             timestamp=datetime.utcnow()
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/api/v2/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_price_v2(
    request: PredictionRequest,
    collection=Depends(get_predictions_collection)
):
    """
    Predict Indian flight price using comprehensive features.
    
    This endpoint uses the full feature set including:
    - Journey date features (day, month, year)
    - Time of day features (departure_hour, arrival_hour)
    - Flight details (airline, source, destination, duration, stops, class)
    - Booking timing (days_left)
    
    Example request:
    ```json
    {
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
    ```
    """
    try:
        # Use real ML model for prediction
        prediction = ml_model_prediction(request)
        
        # Save prediction to database with full feature set
        prediction_doc = PredictionInDB(
            input_data=request.model_dump(),
            predicted_price=prediction.predicted_price,
            confidence_score=prediction.confidence_score,
            delay_risk=prediction.delay_risk
        )
        
        result = await collection.insert_one(prediction_doc.model_dump(by_alias=True))
        
        return PredictionResponse(
            prediction=prediction,
            saved_id=str(result.inserted_id),
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/predictions", response_model=List[dict], tags=["Predictions"])
async def get_predictions_history(
    limit: int = 50,
    skip: int = 0,
    collection=Depends(get_predictions_collection)
):
    """Get prediction history"""
    try:
        cursor = collection.find().skip(skip).limit(limit).sort("created_at", -1)
        predictions = await cursor.to_list(length=limit)
        
        for pred in predictions:
            pred["_id"] = str(pred["_id"])
        
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching predictions: {str(e)}")

# ============================================================================
# DELAY PREDICTION ENDPOINTS
# ============================================================================

@app.post("/predict-delay", response_model=DelayPredictionResult, tags=["Delay Prediction"])
async def predict_delay(request: DelayPredictionRequest):
    """
    Predict the probability of flight delay.
    
    Returns delay probability (0-100%), prediction status (On-time/Delayed),
    and risk level (Low/Medium/High).
    
    Example request:
    ```json
    {
        "airline": "IndiGo",
        "source_city": "Delhi",
        "destination_city": "Mumbai",
        "departure_time": "Evening",
        "arrival_time": "Night",
        "stops_numeric": 1,
        "duration_minutes": 150,
        "days_left": 7,
        "flight_class": "Economy"
    }
    ```
    """
    global delay_model_data
    
    if delay_model_data is None:
        raise HTTPException(
            status_code=503,
            detail="Delay prediction model not loaded. Please train the model first."
        )
    
    try:
        model = delay_model_data['model']
        feature_columns = delay_model_data['feature_columns']
        
        # Prepare input features
        flight_features = {
            'stops_numeric': request.stops_numeric,
            'days_left': request.days_left,
            'duration_minutes': request.duration_minutes,
            'airline': request.airline,
            'source_city': request.source_city,
            'destination_city': request.destination_city,
            'departure_time': request.departure_time,
            'arrival_time': request.arrival_time,
            'class': request.flight_class
        }
        
        # Create DataFrame and encode
        input_df = pd.DataFrame([flight_features])
        input_encoded = pd.get_dummies(input_df, columns=[
            'airline', 'source_city', 'destination_city',
            'departure_time', 'arrival_time', 'class'
        ], drop_first=True)
        
        # Ensure all training features are present
        for col in feature_columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        
        # Select only the features used in training (in correct order)
        input_encoded = input_encoded[feature_columns]
        
        # Predict probability (probability of class 1 = Delayed)
        delay_probability = model.predict_proba(input_encoded)[0][1]
        
        # Predict class
        prediction = model.predict(input_encoded)[0]
        
        # Determine risk level
        if delay_probability > 0.7:
            risk_level = "High"
        elif delay_probability > 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return DelayPredictionResult(
            delay_probability=round(delay_probability * 100, 2),
            prediction='Delayed' if prediction == 1 else 'On-time',
            risk_level=risk_level,
            factors={
                'stops': request.stops_numeric,
                'departure_time': request.departure_time,
                'airline': request.airline,
                'days_left': request.days_left,
                'duration': request.duration_minutes
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Delay prediction error: {str(e)}"
        )

# ============================================================================
# UNIFIED PREDICTION ENDPOINT (with Label Encoders)
# ============================================================================

@app.post("/predict", response_model=SimplePredictionResponse, tags=["Unified Prediction"])
async def unified_predict(
    request: SimplePredictionRequest,
    collection=Depends(get_predictions_collection)
):
    """
    🚀 Complete FastAPI endpoint that:
    - Connects to MongoDB using motor
    - Loads flight_model.pkl and label_encoders.pkl
    - Takes JSON input (airline, source, destination, date)
    - Transforms input using encoders
    - Predicts price & delay probability
    - Saves prediction result to MongoDB (for tracking)
    - Returns result as JSON
    
    Example request:
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
    """
    global ml_model, delay_model_data, label_encoders
    
    # Validate models are loaded
    if ml_model is None:
        raise HTTPException(
            status_code=503,
            detail="Price prediction model not loaded. Please ensure flight_model.pkl exists."
        )
    
    if label_encoders is None:
        raise HTTPException(
            status_code=503,
            detail="Label encoders not loaded. Please ensure label_encoders.pkl exists."
        )
    
    try:
        # ========================================
        # STEP 1: Transform input using encoders
        # ========================================
        input_df = transform_simple_input_with_encoders(request)
        
        # ========================================
        # STEP 2: Predict PRICE using flight_model
        # ========================================
        predicted_price = ml_model.predict(input_df)[0]
        predicted_price = float(round(predicted_price, 2))
        
        # Calculate confidence score
        confidence = 87.5  # You can enhance this based on model's actual confidence metrics
        
        # Calculate price range (±12%)
        price_range = {
            "min": round(predicted_price * 0.88, 2),
            "max": round(predicted_price * 1.12, 2)
        }
        
        # ========================================
        # STEP 3: Predict DELAY using delay_model
        # ========================================
        delay_probability = 0.0
        delay_status = "On-time"
        delay_risk = "Low"
        
        if delay_model_data is not None:
            try:
                model = delay_model_data['model']
                feature_columns = delay_model_data['feature_columns']
                
                # Prepare delay prediction features
                delay_features = {
                    'stops_numeric': request.stops,
                    'days_left': request.days_left,
                    'duration_minutes': request.duration_minutes,
                    'airline': request.airline,
                    'source_city': request.source,
                    'destination_city': request.destination,
                    'departure_time': request.departure_time,
                    'arrival_time': request.arrival_time,
                    'class': request.flight_class
                }
                
                # Create DataFrame and one-hot encode
                delay_df = pd.DataFrame([delay_features])
                delay_encoded = pd.get_dummies(delay_df, columns=[
                    'airline', 'source_city', 'destination_city',
                    'departure_time', 'arrival_time', 'class'
                ], drop_first=True)
                
                # Ensure all training features are present
                for col in feature_columns:
                    if col not in delay_encoded.columns:
                        delay_encoded[col] = 0
                
                # Select only the features used in training (in correct order)
                delay_encoded = delay_encoded[feature_columns]
                
                # Predict delay probability
                delay_prob = model.predict_proba(delay_encoded)[0][1]
                delay_probability = round(delay_prob * 100, 2)
                
                # Predict delay class
                delay_pred = model.predict(delay_encoded)[0]
                delay_status = 'Delayed' if delay_pred == 1 else 'On-time'
                
                # Determine risk level
                if delay_probability > 70:
                    delay_risk = "High"
                elif delay_probability > 40:
                    delay_risk = "Medium"
                else:
                    delay_risk = "Low"
            
            except Exception as delay_error:
                print(f"⚠️  Delay prediction failed: {delay_error}")
                # Continue with default delay values
        
        # ========================================
        # STEP 4: Save to MongoDB
        # ========================================
        try:
            prediction_doc = {
                "input_data": request.model_dump(),
                "predicted_price": predicted_price,
                "confidence_score": confidence,
                "price_range": price_range,
                "delay_probability": delay_probability,
                "delay_status": delay_status,
                "delay_risk": delay_risk,
                "created_at": datetime.utcnow(),
                "model_version": "1.0",
                "encoder_version": "1.0"
            }
            
            print(f"💾 Attempting to save prediction to MongoDB...")
            print(f"   Collection: {collection.name if hasattr(collection, 'name') else 'predictions'}")
            print(f"   Document keys: {list(prediction_doc.keys())}")
            
            result = await collection.insert_one(prediction_doc)
            saved_id = str(result.inserted_id)
            
            print(f"✅ Successfully saved to MongoDB with ID: {saved_id}")
            
        except Exception as save_error:
            print(f"⚠️  MongoDB save failed: {str(save_error)}")
            import traceback
            traceback.print_exc()
            # Continue without failing the prediction
            saved_id = "not_saved"
        
        # ========================================
        # STEP 5: Return unified response
        # ========================================
        return SimplePredictionResponse(
            predicted_price=predicted_price,
            confidence_score=confidence,
            price_range=price_range,
            delay_probability=delay_probability,
            delay_status=delay_status,
            delay_risk=delay_risk,
            saved_id=saved_id,
            timestamp=datetime.utcnow(),
            input_data=request.model_dump()
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log and raise detailed error
        print(f"❌ Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Unified prediction error: {str(e)}"
        )

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
