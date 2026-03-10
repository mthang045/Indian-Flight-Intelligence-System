import { useState } from 'react';
import { Search, TrendingUp, Target, AlertCircle, Clock, Loader2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import axios from 'axios';

const indianCities = [
  'Delhi',
  'Mumbai',
  'Bangalore',
  'Chennai',
  'Kolkata',
  'Hyderabad',
  'Pune',
  'Ahmedabad',
  'Jaipur',
  'Kochi',
  'Goa',
  'Lucknow',
];

const airlines = [
  'Air India',
  'IndiGo',
  'SpiceJet',
  'Vistara',
  'AirAsia India',
  'Go First',
];

// Default flight durations and stops based on common routes (in minutes)
const routeDefaults = {
  // Delhi routes
  'Delhi->Mumbai': { duration: 135, stops: 0 },
  'Delhi->Bangalore': { duration: 165, stops: 0 },
  'Delhi->Chennai': { duration: 165, stops: 0 },
  'Delhi->Kolkata': { duration: 135, stops: 0 },
  'Delhi->Hyderabad': { duration: 150, stops: 0 },
  'Delhi->Pune': { duration: 135, stops: 0 },
  'Delhi->Ahmedabad': { duration: 105, stops: 0 },
  'Delhi->Jaipur': { duration: 60, stops: 0 },
  'Delhi->Kochi': { duration: 195, stops: 0 },
  'Delhi->Goa': { duration: 150, stops: 0 },
  'Delhi->Lucknow': { duration: 75, stops: 0 },
  
  // Mumbai routes
  'Mumbai->Delhi': { duration: 135, stops: 0 },
  'Mumbai->Bangalore': { duration: 105, stops: 0 },
  'Mumbai->Chennai': { duration: 120, stops: 0 },
  'Mumbai->Kolkata': { duration: 150, stops: 0 },
  'Mumbai->Hyderabad': { duration: 90, stops: 0 },
  'Mumbai->Pune': { duration: 45, stops: 0 },
  'Mumbai->Ahmedabad': { duration: 75, stops: 0 },
  'Mumbai->Jaipur': { duration: 105, stops: 0 },
  'Mumbai->Kochi': { duration: 115, stops: 0 },
  'Mumbai->Goa': { duration: 70, stops: 0 },
  
  // Bangalore routes
  'Bangalore->Delhi': { duration: 165, stops: 0 },
  'Bangalore->Mumbai': { duration: 105, stops: 0 },
  'Bangalore->Chennai': { duration: 60, stops: 0 },
  'Bangalore->Kolkata': { duration: 165, stops: 0 },
  'Bangalore->Hyderabad': { duration: 60, stops: 0 },
  'Bangalore->Pune': { duration: 90, stops: 0 },
  'Bangalore->Kochi': { duration: 75, stops: 0 },
  'Bangalore->Goa': { duration: 75, stops: 0 },
  
  // Chennai routes
  'Chennai->Delhi': { duration: 165, stops: 0 },
  'Chennai->Mumbai': { duration: 120, stops: 0 },
  'Chennai->Bangalore': { duration: 60, stops: 0 },
  'Chennai->Kolkata': { duration: 135, stops: 0 },
  'Chennai->Hyderabad': { duration: 75, stops: 0 },
  'Chennai->Kochi': { duration: 75, stops: 0 },
  
  // Kolkata routes
  'Kolkata->Delhi': { duration: 135, stops: 0 },
  'Kolkata->Mumbai': { duration: 150, stops: 0 },
  'Kolkata->Bangalore': { duration: 165, stops: 0 },
  'Kolkata->Chennai': { duration: 135, stops: 0 },
  'Kolkata->Hyderabad': { duration: 120, stops: 0 },
  
  // Hyderabad routes
  'Hyderabad->Delhi': { duration: 150, stops: 0 },
  'Hyderabad->Mumbai': { duration: 90, stops: 0 },
  'Hyderabad->Bangalore': { duration: 60, stops: 0 },
  'Hyderabad->Chennai': { duration: 75, stops: 0 },
  'Hyderabad->Kolkata': { duration: 120, stops: 0 },
};

const API_BASE_URL = 'http://localhost:8000';

export function FlightPricePredictor() {
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    departure: '',
    destination: '',
    date: '',
    airline: '',
    class: '',
    stops: 0,
    duration: 135,
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-update duration and stops when route changes
  const updateRouteDefaults = (departure, destination) => {
    if (departure && destination && departure !== destination) {
      const routeKey = `${departure}->${destination}`;
      const defaults = routeDefaults[routeKey];
      
      if (defaults) {
        setFormData(prev => ({
          ...prev,
          duration: defaults.duration,
          stops: defaults.stops
        }));
      } else {
        // Fallback: estimate based on distance tier
        // Short routes: 60-90 min, Medium: 90-150 min, Long: 150+ min
        const estimatedDuration = 120; // Default medium distance
        setFormData(prev => ({
          ...prev,
          duration: estimatedDuration,
          stops: 0 // Most flights are non-stop
        }));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    // Validate departure and destination are different
    if (formData.departure === formData.destination) {
      setError('Sân bay đi và đến phải khác nhau! / Departure and destination must be different!');
      setLoading(false);
      return;
    }
    
    try {
      // Calculate days_left from date
      const journeyDate = new Date(formData.date);
      const today = new Date();
      const daysLeft = Math.ceil((journeyDate - today) / (1000 * 60 * 60 * 24));

      // Map class names to English
      const classMapping = {
        [t('economy')]: 'Economy',
        [t('premiumEconomy')]: 'Economy',
        [t('business')]: 'Business',
        [t('firstClass')]: 'Business',
      };

      const requestData = {
        airline: formData.airline,
        source: formData.departure,  // SimplePredictionRequest uses 'source' not 'source_city'
        destination: formData.destination,  // SimplePredictionRequest uses 'destination' not 'destination_city'
        date: formData.date,
        departure_time: 'Morning',
        arrival_time: 'Afternoon',
        stops: formData.stops,
        flight_class: classMapping[formData.class] || 'Economy',
        duration_minutes: formData.duration,
        days_left: Math.max(1, daysLeft),
      };

      const response = await axios.post(`${API_BASE_URL}/predict`, requestData);
      
      setPrediction({
        price: response.data.predicted_price,
        confidence: response.data.confidence_score,
        priceRange: response.data.price_range,
        delayProbability: response.data.delay_probability,
        delayStatus: response.data.delay_status,
        delayRisk: response.data.delay_risk,
      });
    } catch (err) {
      console.error('Prediction error:', err);
      let errorMsg = 'Không thể kết nối API. Vui lòng kiểm tra backend đang chạy.';
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail);
      } else if (err.message) {
        errorMsg = err.message;
      }
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const classes = [
    t('economy'),
    t('premiumEconomy'),
    t('business'),
    t('firstClass'),
  ];

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-blue-100">
      <div className="flex items-center gap-3 mb-6">
        <div className="bg-blue-600 p-2 rounded-lg">
          <TrendingUp className="w-6 h-6 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-blue-900">{t('pricePredictor')}</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Departure City */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t('departureCity')}
            </label>
            <select
              value={formData.departure}
              onChange={(e) => {
                const newDeparture = e.target.value;
                const newDestination = newDeparture === formData.destination ? '' : formData.destination;
                setFormData({ 
                  ...formData, 
                  departure: newDeparture,
                  destination: newDestination
                });
                // Auto-update duration and stops
                if (newDestination) {
                  updateRouteDefaults(newDeparture, newDestination);
                }
                setError(null);
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
              required
            >
              <option value="">{t('selectCity')}</option>
              {indianCities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>

          {/* Destination City */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t('destinationCity')}
            </label>
            <select
              value={formData.destination}
              onChange={(e) => {
                const newDestination = e.target.value;
                setFormData({ ...formData, destination: newDestination });
                // Auto-update duration and stops based on route
                if (formData.departure) {
                  updateRouteDefaults(formData.departure, newDestination);
                }
                setError(null);
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
              required
            >
              <option value="">{t('selectCity')}</option>
              {indianCities.map((city) => (
                <option 
                  key={city} 
                  value={city}
                  disabled={city === formData.departure}
                >
                  {city}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Travel Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t('travelDate')}
            </label>
            <input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
              min={new Date().toISOString().split('T')[0]}
            />
          </div>

          {/* Airline */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t('airline')}
            </label>
            <select
              value={formData.airline}
              onChange={(e) => setFormData({ ...formData, airline: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
              required
            >
              <option value="">{t('selectAirline')}</option>
              {airlines.map((airline) => (
                <option key={airline} value={airline}>
                  {airline}
                </option>
              ))}
            </select>
          </div>

          {/* Class */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t('class')}
            </label>
            <select
              value={formData.class}
              onChange={(e) => setFormData({ ...formData, class: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
              required
            >
              <option value="">{t('selectClass')}</option>
              {classes.map((cls) => (
                <option key={cls} value={cls}>
                  {cls}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Hidden: Stops and Duration - Auto-calculated based on route */}
        <input type="hidden" value={formData.stops} />
        <input type="hidden" value={formData.duration} />
        
        {/* Optional: Show calculated values as info */}
        {formData.departure && formData.destination && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-sm text-blue-700">
              <span className="font-medium">Thông tin chuyến bay / Flight Info:</span>
              {' '}
              <span className="font-semibold">{formData.stops === 0 ? 'Bay thẳng' : `${formData.stops} điểm dừng`}</span>
              {' • '}
              <span className="font-semibold">~{formData.duration} phút</span>
              {' '}(tự động tính)
            </p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-red-800">Lỗi dự đoán</p>
              <p className="text-sm text-red-600 mt-1">{error}</p>
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white py-3 px-6 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Đang dự đoán...
            </>
          ) : (
            <>
              <Search className="w-5 h-5" />
              {t('predictPrice')}
            </>
          )}
        </button>
      </form>

      {/* Prediction Result */}
      {prediction && (
        <div className="mt-6 space-y-4">
          {/* Price Prediction */}
          <div className="bg-gradient-to-br from-blue-50 to-sky-50 rounded-xl p-6 border border-blue-200">
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-blue-600" />
              <h3 className="text-lg font-semibold text-blue-900">{t('predictedPrice')}</h3>
            </div>
            
            <div className="text-center">
              <div className="text-5xl font-bold text-blue-600 mb-2">
                ₹{prediction.price.toLocaleString('en-IN')}
              </div>
              <div className="text-sm text-gray-600 mb-4">
                Khoảng giá: ₹{Math.round(prediction.priceRange.min).toLocaleString('en-IN')} 
                {' - '}
                ₹{Math.round(prediction.priceRange.max).toLocaleString('en-IN')}
              </div>
              <div className="flex items-center justify-center gap-2 text-gray-600">
                <div className="flex items-center gap-1">
                  <span className="text-sm">{t('confidenceScore')}</span>
                  <span className="font-semibold text-green-600">{Math.round(prediction.confidence)}%</span>
                </div>
              </div>
              <div className="mt-4 bg-white rounded-lg p-3">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">{t('confidenceLevel')}</span>
                  <span className="text-gray-900 font-medium">{Math.round(prediction.confidence)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${prediction.confidence}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Delay Probability */}
          <div className={`rounded-xl p-6 border-2 ${
            prediction.delayRisk === 'Low' 
              ? 'bg-gradient-to-br from-green-50 to-emerald-50 border-green-300' 
              : prediction.delayRisk === 'Medium'
              ? 'bg-gradient-to-br from-yellow-50 to-amber-50 border-yellow-300'
              : 'bg-gradient-to-br from-red-50 to-rose-50 border-red-300'
          }`}>
            <div className="flex items-center gap-2 mb-4">
              <Clock className={`w-5 h-5 ${
                prediction.delayRisk === 'Low' 
                  ? 'text-green-600' 
                  : prediction.delayRisk === 'Medium'
                  ? 'text-yellow-600'
                  : 'text-red-600'
              }`} />
              <h3 className="text-lg font-semibold text-gray-900">Xác Suất Delay</h3>
            </div>
            
            <div className="text-center">
              <div className={`text-5xl font-bold mb-2 ${
                prediction.delayRisk === 'Low' 
                  ? 'text-green-600' 
                  : prediction.delayRisk === 'Medium'
                  ? 'text-yellow-600'
                  : 'text-red-600'
              }`}>
                {Math.round(prediction.delayProbability)}%
              </div>
              <div className="flex items-center justify-center gap-4 mb-4">
                <div className="text-sm">
                  <span className="text-gray-600">Trạng thái: </span>
                  <span className={`font-semibold ${
                    prediction.delayStatus === 'On-time' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {prediction.delayStatus === 'On-time' ? '✓ Đúng giờ' : '⚠ Có thể trễ'}
                  </span>
                </div>
                <div className="text-sm">
                  <span className="text-gray-600">Risk: </span>
                  <span className={`font-semibold px-2 py-1 rounded ${
                    prediction.delayRisk === 'Low' 
                      ? 'bg-green-100 text-green-700' 
                      : prediction.delayRisk === 'Medium'
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-red-100 text-red-700'
                  }`}>
                    {prediction.delayRisk}
                  </span>
                </div>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-500 ${
                    prediction.delayRisk === 'Low' 
                      ? 'bg-green-500' 
                      : prediction.delayRisk === 'Medium'
                      ? 'bg-yellow-500'
                      : 'bg-red-500'
                  }`}
                  style={{ width: `${prediction.delayProbability}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
