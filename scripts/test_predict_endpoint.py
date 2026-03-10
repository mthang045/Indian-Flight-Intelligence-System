"""
Test script for the unified /predict endpoint

This script tests the complete FastAPI application that:
1. Loads flight_model.pkl and label_encoders.pkl
2. Transforms input using encoders
3. Predicts price & delay probability
4. Saves to MongoDB
5. Returns unified JSON response

Usage:
    python test_predict_endpoint.py

Make sure the FastAPI server is running: uvicorn app:app --reload
"""

import requests
import json
from datetime import datetime, timedelta

# API endpoint
BASE_URL = "http://localhost:8000"
PREDICT_ENDPOINT = f"{BASE_URL}/predict"

# Test cases
test_cases = [
    {
        "name": "IndiGo Delhi to Mumbai - Economy",
        "data": {
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
    },
    {
        "name": "Air India Bangalore to Delhi - Business",
        "data": {
            "airline": "Air India",
            "source": "Bangalore",
            "destination": "Delhi",
            "date": "2024-07-10",
            "departure_time": "Evening",
            "arrival_time": "Night",
            "stops": 0,
            "flight_class": "Business",
            "duration_minutes": 165,
            "days_left": 45
        }
    },
    {
        "name": "SpiceJet Chennai to Kolkata - with 1 stop",
        "data": {
            "airline": "SpiceJet",
            "source": "Chennai",
            "destination": "Kolkata",
            "date": "2024-06-20",
            "departure_time": "Afternoon",
            "arrival_time": "Evening",
            "stops": 1,
            "flight_class": "Economy",
            "duration_minutes": 180,
            "days_left": 15
        }
    },
    {
        "name": "Vistara Mumbai to Hyderabad - Last minute",
        "data": {
            "airline": "Vistara",
            "source": "Mumbai",
            "destination": "Hyderabad",
            "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "departure_time": "Night",
            "arrival_time": "Night",
            "stops": 0,
            "flight_class": "Economy",
            "duration_minutes": 90,
            "days_left": 3
        }
    }
]

def test_health_check():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("=" * 80)
        print("🏥 HEALTH CHECK")
        print("=" * 80)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data.get('status')}")
            print(f"✅ Database: {data.get('database')}")
            print(f"✅ Price Model Loaded: {data.get('model_loaded')}")
            print(f"✅ Delay Model Loaded: {data.get('delay_model_loaded')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {str(e)}")
        print("   Make sure FastAPI server is running: uvicorn app:app --reload")
        return False

def test_predict_endpoint(test_case):
    """Test the /predict endpoint"""
    print("\n" + "=" * 80)
    print(f"🧪 TEST: {test_case['name']}")
    print("=" * 80)
    
    try:
        # Make POST request
        response = requests.post(PREDICT_ENDPOINT, json=test_case['data'])
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ REQUEST SUCCESSFUL")
            print("\n📥 Input Data:")
            print(json.dumps(test_case['data'], indent=2))
            
            print("\n📊 PREDICTION RESULTS:")
            print(f"   💰 Predicted Price: ₹{result['predicted_price']:,.2f}")
            print(f"   📈 Confidence: {result['confidence_score']}%")
            print(f"   💵 Price Range: ₹{result['price_range']['min']:,.2f} - ₹{result['price_range']['max']:,.2f}")
            print(f"\n   ⏰ Delay Probability: {result['delay_probability']}%")
            print(f"   📌 Delay Status: {result['delay_status']}")
            print(f"   ⚠️  Delay Risk: {result['delay_risk']}")
            print(f"\n   💾 Saved to MongoDB: {result['saved_id']}")
            print(f"   🕐 Timestamp: {result['timestamp']}")
            
            return True
        else:
            print(f"❌ PREDICTION FAILED")
            print(f"   Status Code: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("🚀 " + "=" * 78)
    print("🚀 TESTING UNIFIED /predict ENDPOINT")
    print("🚀 " + "=" * 78)
    
    # Test health check first
    if not test_health_check():
        print("\n⚠️  Cannot proceed with tests. Please start the FastAPI server first.")
        print("   Run: cd api && uvicorn app:app --reload")
        return
    
    # Run all test cases
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        if test_predict_endpoint(test_case):
            passed += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📝 Total: {len(test_cases)}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
