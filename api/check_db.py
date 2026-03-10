#!/usr/bin/env python3
"""Check MongoDB database for saved predictions"""

from pymongo import MongoClient
from datetime import datetime

try:
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['flight_price_prediction']
    
    print("=" * 80)
    print("📊 MONGODB DATABASE CHECK")
    print("=" * 80)
    
    # List all collections
    collections = db.list_collection_names()
    print(f"\n📦 Collections in database: {collections}")
    
    # Check predictions collection
    predictions = db['predictions']
    count = predictions.count_documents({})
    print(f"\n✨ Predictions collection has {count} documents")
    
    if count > 0:
        print("\n📋 Last 5 predictions:")
        print("-" * 80)
        for doc in predictions.find().sort("created_at", -1).limit(5):
            created = doc.get('created_at', 'N/A')
            price = doc.get('predicted_price', 'N/A')
            delay = doc.get('delay_probability', 'N/A')
            input_data = doc.get('input_data', {})
            route = f"{input_data.get('source', '?')} → {input_data.get('destination', '?')}"
            
            print(f"  • {created} | {route} | ₹{price:.0f} | Delay: {delay:.1f}%")
    else:
        print("\n❌ No predictions found in database!")
        print("   Make a prediction on the frontend to test saving.")
    
    print("\n" + "=" * 80)
    
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    import traceback
    traceback.print_exc()
