# Quick Start Script - Flight Price Prediction System
# Run this to start both backend and frontend

Write-Host "`n🚀 Starting Flight Price Prediction System...`n" -ForegroundColor Cyan

# Check if MongoDB is running
Write-Host "1️⃣ Checking MongoDB..." -ForegroundColor Yellow
try {
    $mongoCheck = mongosh --eval "db.version()" --quiet
    Write-Host "   ✅ MongoDB is running: $mongoCheck" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  MongoDB not running! Starting MongoDB..." -ForegroundColor Red
    Write-Host "   → Please start MongoDB manually or run: Start-Service MongoDB" -ForegroundColor Yellow
    exit 1
}

# Check if models exist
Write-Host "`n2️⃣ Checking ML models..." -ForegroundColor Yellow
if (Test-Path "models/flight_model.pkl") {
    Write-Host "   ✅ models/flight_model.pkl exists" -ForegroundColor Green
} else {
    Write-Host "   ❌ models/flight_model.pkl not found!" -ForegroundColor Red
    Write-Host "   → Run: cd scripts && python train.py" -ForegroundColor Yellow
    exit 1
}

if (Test-Path "api/flight_model.pkl") {
    Write-Host "   ✅ api/flight_model.pkl exists" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Copying models to api/..." -ForegroundColor Yellow
    Copy-Item "models/*.pkl" "api/" -Force
    Write-Host "   ✅ Models copied" -ForegroundColor Green
}

# Check Python dependencies
Write-Host "`n3️⃣ Checking Python dependencies..." -ForegroundColor Yellow
try {
    python -c "import fastapi, motor, sklearn, pandas, joblib" 2>$null
    Write-Host "   ✅ Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r api/requirements.txt
}

# Check Node dependencies
Write-Host "`n4️⃣ Checking Node.js dependencies..." -ForegroundColor Yellow
if (Test-Path "node_modules/axios") {
    Write-Host "   ✅ Node.js dependencies installed" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Installing Node.js dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "   ✅ ALL CHECKS PASSED - READY TO START!" -ForegroundColor Green  
Write-Host "═══════════════════════════════════════════════════════════`n" -ForegroundColor Green

Write-Host "📌 Opening terminals..." -ForegroundColor Cyan
Write-Host "`n🌐 Backend will start on: http://localhost:8000" -ForegroundColor Yellow
Write-Host "🎨 Frontend will start on: http://localhost:5173`n" -ForegroundColor Yellow

# Start Backend in new terminal
Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; cd api; Write-Host '🌐 Starting FastAPI Backend...' -ForegroundColor Green; uvicorn app:app --reload --port 8000"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend in new terminal  
Write-Host "Starting Frontend (React)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host '🎨 Starting React Frontend...' -ForegroundColor Green; npm run dev"

Write-Host "`n✅ Both servers are starting in separate terminals!" -ForegroundColor Green
Write-Host "`n📖 Documentation:" -ForegroundColor Cyan
Write-Host "   • README.md - Project overview" -ForegroundColor White
Write-Host "   • docs/FULLSTACK_SETUP.md - Setup guide" -ForegroundColor White
Write-Host "   • docs/API_USAGE.md - API documentation`n" -ForegroundColor White

Write-Host "🎯 Quick Links:" -ForegroundColor Magenta
Write-Host "   • Backend API: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   • Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "   • Health Check: http://localhost:8000/health`n" -ForegroundColor White

Write-Host "Press Ctrl+C in each terminal to stop the servers.`n" -ForegroundColor Yellow
