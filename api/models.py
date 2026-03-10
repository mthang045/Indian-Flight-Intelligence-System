from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    """Custom ObjectId type for Pydantic v2"""
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ])
    
    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return v
        raise ValueError("Invalid ObjectId")

# ============================================================================
# FLIGHT MODELS
# ============================================================================

class Flight(BaseModel):
    """
    Core Flight model matching Indian flight market data.
    Essential fields for flight price prediction.
    """
    airline: str = Field(..., description="Airline name (IndiGo, Air India, SpiceJet, Vistara, AirAsia, GO_FIRST)")
    source: str = Field(..., alias="source_city", description="Origin city code (DEL, BOM, BLR, MAA, CCU, HYD)")
    destination: str = Field(..., alias="destination_city", description="Destination city code")
    departure_time: str = Field(..., description="Departure time (HH:MM:SS format)")
    duration_minutes: int = Field(..., gt=0, le=3000, description="Flight duration in minutes")
    stops: int = Field(0, ge=0, le=5, description="Number of stops (0=direct, 1=one stop, etc.)")
    price: float = Field(..., gt=0, description="Ticket price in INR (Indian Rupees)")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "airline": "IndiGo",
                "source": "DEL",
                "destination": "BOM",
                "departure_time": "06:30:00",
                "duration_minutes": 135,
                "stops": 0,
                "price": 4500.0
            }
        }

class FlightBase(BaseModel):
    """Extended Flight schema with additional fields"""
    airline: str = Field(..., description="Airline name (e.g., IndiGo, Air India)")
    flight_number: str = Field(..., description="Flight number (e.g., 6E-2045)")
    source_city: str = Field(..., description="Origin city (e.g., DEL, BOM)")
    destination_city: str = Field(..., description="Destination city")
    departure_time: str = Field(..., description="Departure time (HH:MM:SS)")
    arrival_time: str = Field(..., description="Arrival time (HH:MM:SS)")
    duration_minutes: int = Field(..., gt=0, description="Flight duration in minutes")
    stops: int = Field(0, ge=0, description="Number of stops")
    flight_class: str = Field(..., description="Flight class (Economy, Business)")
    days_left: int = Field(..., ge=1, le=365, description="Days until departure")
    price: float = Field(..., gt=0, description="Ticket price in INR")
    
    class Config:
        json_schema_extra = {
            "example": {
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
                "price": 4500.0
            }
        }

class FlightCreate(FlightBase):
    """Schema for creating a new flight"""
    pass

class FlightInDB(FlightBase):
    """Schema for flight stored in database"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

class FlightResponse(BaseModel):
    """Schema for flight response"""
    id: str = Field(..., alias="_id")
    airline: str
    flight_number: str
    source_city: str
    destination_city: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    stops: int
    flight_class: str
    days_left: int
    price: float
    created_at: datetime
    
    class Config:
        populate_by_name = True

# ============================================================================
# PREDICTION MODELS
# ============================================================================

class PredictionRequest(BaseModel):
    """Request model for Indian flight price prediction with all required features"""
    # Core flight details
    airline: str = Field(..., description="Airline name (IndiGo, Air India, SpiceJet, Vistara, AirAsia, GO_FIRST)")
    source: str = Field(..., description="Origin city code (DEL, BOM, BLR, MAA, CCU, HYD)")
    destination: str = Field(..., description="Destination city code")
    
    # Time-related features
    departure_time: str = Field(..., description="Departure time in HH:MM:SS format")
    arrival_time: str = Field(..., description="Arrival time in HH:MM:SS format")
    duration_minutes: int = Field(..., gt=0, le=3000, description="Flight duration in minutes")
    
    # Journey date features
    day: int = Field(..., ge=1, le=31, description="Day of journey (1-31)")
    month: int = Field(..., ge=1, le=12, description="Month of journey (1-12)")
    year: int = Field(2024, ge=2023, le=2030, description="Year of journey")
    
    # Time of day features
    departure_hour: int = Field(..., ge=0, le=23, description="Departure hour (0-23)")
    arrival_hour: int = Field(..., ge=0, le=23, description="Arrival hour (0-23)")
    
    # Additional features
    stops: int = Field(0, ge=0, le=5, description="Number of stops (0=non-stop)")
    flight_class: str = Field("Economy", description="Flight class (Economy/Business)")
    days_left: int = Field(..., ge=1, le=365, description="Days until departure date")
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }

class PredictionInput(BaseModel):
    """Input schema for price prediction (legacy compatibility)"""
    airline: str = Field(..., description="Airline name")
    source_city: str = Field(..., description="Origin city")
    destination_city: str = Field(..., description="Destination city")
    departure_time: str = Field(..., description="Departure time (HH:MM:SS)")
    arrival_time: str = Field(..., description="Arrival time (HH:MM:SS)")
    duration_minutes: int = Field(..., gt=0, description="Flight duration in minutes")
    stops: int = Field(0, ge=0, description="Number of stops")
    flight_class: str = Field(..., description="Flight class")
    days_left: int = Field(..., ge=1, le=365, description="Days until departure")
    
    # Additional fields for better prediction
    day: Optional[int] = Field(None, ge=1, le=31, description="Day of month")
    month: Optional[int] = Field(None, ge=1, le=12, description="Month")
    departure_hour: Optional[int] = Field(None, ge=0, le=23, description="Departure hour")
    
    class Config:
        json_schema_extra = {
            "example": {
                "airline": "IndiGo",
                "source_city": "DEL",
                "destination_city": "BOM",
                "departure_time": "06:30:00",
                "arrival_time": "08:45:00",
                "duration_minutes": 135,
                "stops": 0,
                "flight_class": "Economy",
                "days_left": 14,
                "day": 25,
                "month": 3,
                "departure_hour": 6
            }
        }

class PredictionResult(BaseModel):
    """Schema for prediction result"""
    predicted_price: float = Field(..., description="Predicted ticket price in INR")
    confidence_score: float = Field(..., ge=0, le=100, description="Prediction confidence (0-100%)")
    delay_risk: str = Field(..., description="Delay risk level (Low/Medium/High)")
    price_range: Dict[str, float] = Field(..., description="Min and max price range")
    features_used: Optional[Dict[str, Any]] = Field(None, description="Features used for prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_price": 4850.0,
                "confidence_score": 87.5,
                "delay_risk": "Low",
                "price_range": {
                    "min": 4300.0,
                    "max": 5400.0
                },
                "features_used": {
                    "airline": "IndiGo",
                    "route": "DEL-BOM",
                    "duration": 135
                }
            }
        }

class PredictionInDB(BaseModel):
    """Schema for prediction stored in database"""
    input_data: Dict[str, Any] = Field(..., description="Input features")
    predicted_price: float = Field(..., description="Predicted price")
    confidence_score: float = Field(..., description="Confidence score")
    delay_risk: str = Field(..., description="Delay risk level")
    user_id: Optional[str] = Field(None, description="User ID if authenticated")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

class PredictionResponse(BaseModel):
    """Schema for prediction response with saved data"""
    prediction: PredictionResult
    saved_id: str = Field(..., description="ID of saved prediction")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# DELAY PREDICTION MODELS
# ============================================================================

class DelayPredictionRequest(BaseModel):
    """Request model for flight delay prediction"""
    airline: str = Field(..., description="Airline name (IndiGo, SpiceJet, Vistara, etc.)")
    source_city: str = Field(..., description="Origin city (Delhi, Mumbai, Bangalore, etc.)")
    destination_city: str = Field(..., description="Destination city")
    departure_time: str = Field(..., description="Departure period (Morning, Afternoon, Evening, Night, etc.)")
    arrival_time: str = Field(..., description="Arrival period")
    stops_numeric: int = Field(..., ge=0, le=5, description="Number of stops (0=non-stop)")
    duration_minutes: float = Field(..., gt=0, description="Flight duration in minutes")
    days_left: int = Field(..., ge=1, le=365, description="Days until departure")
    flight_class: str = Field("Economy", description="Flight class (Economy/Business)")
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }

class DelayPredictionResult(BaseModel):
    """Result of delay prediction"""
    delay_probability: float = Field(..., ge=0, le=100, description="Probability of delay (0-100%)")
    prediction: str = Field(..., description="Predicted status (On-time or Delayed)")
    risk_level: str = Field(..., description="Risk level (Low, Medium, High)")
    factors: Optional[Dict[str, Any]] = Field(None, description="Contributing factors")
    
    class Config:
        json_schema_extra = {
            "example": {
                "delay_probability": 48.5,
                "prediction": "On-time",
                "risk_level": "Medium",
                "factors": {
                    "stops": 1,
                    "departure_time": "Evening",
                    "airline": "IndiGo"
                }
            }
        }

# ============================================================================
# SIMPLE PREDICTION MODELS (with Label Encoders)
# ============================================================================

class SimplePredictionRequest(BaseModel):
    """
    Simplified prediction request - only essential fields.
    Uses label encoders to transform categorical inputs automatically.
    """
    airline: str = Field(..., description="Airline name (IndiGo, Air India, SpiceJet, Vistara, AirAsia, GO_FIRST)")
    source: str = Field(..., description="Origin city name (Delhi, Mumbai, Bangalore, Chennai, Kolkata, Hyderabad)")
    destination: str = Field(..., description="Destination city name")
    date: str = Field(..., description="Journey date (YYYY-MM-DD format)")
    departure_time: Optional[str] = Field("Morning", description="Departure time period (Morning, Afternoon, Evening, Night)")
    arrival_time: Optional[str] = Field("Afternoon", description="Arrival time period")
    stops: Optional[int] = Field(0, ge=0, le=5, description="Number of stops (0=non-stop)")
    flight_class: Optional[str] = Field("Economy", description="Flight class (Economy/Business)")
    duration_minutes: Optional[int] = Field(120, gt=0, description="Estimated flight duration in minutes")
    days_left: Optional[int] = Field(30, ge=1, le=365, description="Days until departure")
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }

class SimplePredictionResponse(BaseModel):
    """Unified prediction response with both price and delay predictions"""
    # Price prediction
    predicted_price: float = Field(..., description="Predicted ticket price in INR")
    confidence_score: float = Field(..., ge=0, le=100, description="Prediction confidence (0-100%)")
    price_range: Dict[str, float] = Field(..., description="Min and max price range")
    
    # Delay prediction
    delay_probability: float = Field(..., ge=0, le=100, description="Probability of delay (0-100%)")
    delay_status: str = Field(..., description="Predicted delay status (On-time/Delayed)")
    delay_risk: str = Field(..., description="Delay risk level (Low/Medium/High)")
    
    # Metadata
    saved_id: str = Field(..., description="ID of saved prediction in MongoDB")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Input echo
    input_data: Dict[str, Any] = Field(..., description="Echo of input data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_price": 4850.0,
                "confidence_score": 87.5,
                "price_range": {"min": 4300.0, "max": 5400.0},
                "delay_probability": 35.2,
                "delay_status": "On-time",
                "delay_risk": "Low",
                "saved_id": "507f1f77bcf86cd799439011",
                "timestamp": "2024-06-01T10:30:00",
                "input_data": {
                    "airline": "IndiGo",
                    "source": "Delhi",
                    "destination": "Mumbai"
                }
            }
        }

# ============================================================================
# STATISTICS & ANALYSIS MODELS
# ============================================================================

class FlightStatistics(BaseModel):
    """Statistics for flight data"""
    total_flights: int
    airlines: list[str]
    routes: list[Dict[str, Any]]
    avg_price: float
    price_range: Dict[str, float]
    avg_duration: float
    
class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    database: str
    model_loaded: bool = False
    model_path: str = ""
    delay_model_loaded: bool = False
    delay_model_path: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
