import { useState } from 'react';
import { AlertCircle, Cloud, Clock, Search, ArrowLeft, Loader2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Link } from 'react-router-dom';
import axios from 'axios';

const historicalData = [
  { id: 'jan', month: 'Jan', delays: 15 },
  { id: 'feb', month: 'Feb', delays: 12 },
  { id: 'mar', month: 'Mar', delays: 18 },
  { id: 'apr', month: 'Apr', delays: 22 },
  { id: 'may', month: 'May', delays: 28 },
  { id: 'jun', month: 'Jun', delays: 35 },
  { id: 'jul', month: 'Jul', delays: 40 },
  { id: 'aug', month: 'Aug', delays: 38 },
  { id: 'sep', month: 'Sep', delays: 25 },
  { id: 'oct', month: 'Oct', delays: 20 },
  { id: 'nov', month: 'Nov', delays: 16 },
  { id: 'dec', month: 'Dec', delays: 19 },
];

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

export function DelayAnalysis() {
  const [searchType, setSearchType] = useState('route'); // 'route' or 'flight'
  const [formData, setFormData] = useState({
    flightNumber: '',
    airline: '',
    source: '',
    destination: '',
    date: '',
    stops: 0,
    duration: 135,
  });
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-update duration and stops when route changes
  const updateRouteDefaults = (source, destination) => {
    if (source && destination && source !== destination) {
      const routeKey = `${source}->${destination}`;
      const defaults = routeDefaults[routeKey];
      
      if (defaults) {
        setFormData(prev => ({
          ...prev,
          duration: defaults.duration,
          stops: defaults.stops
        }));
      } else {
        // Fallback: estimate based on distance tier
        const estimatedDuration = 120; // Default medium distance
        setFormData(prev => ({
          ...prev,
          duration: estimatedDuration,
          stops: 0 // Most flights are non-stop
        }));
      }
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Validate required fields
      if (!formData.airline || !formData.source || !formData.destination) {
        setError('Vui lòng điền đầy đủ thông tin: Hãng hàng không, Điểm đi, Điểm đến');
        setLoading(false);
        return;
      }
      
      // Validate departure and destination are different
      if (formData.source === formData.destination) {
        setError('Sân bay đi và đến phải khác nhau! / Departure and destination must be different!');
        setLoading(false);
        return;
      }

      const journeyDate = new Date(formData.date || Date.now());
      const today = new Date();
      const daysLeft = Math.ceil((journeyDate - today) / (1000 * 60 * 60 * 24));

      const requestData = {
        airline: formData.airline,
        source: formData.source,  // SimplePredictionRequest uses 'source' not 'source_city'
        destination: formData.destination,  // SimplePredictionRequest uses 'destination' not 'destination_city'
        date: formData.date || new Date().toISOString().split('T')[0],
        departure_time: 'Morning',
        arrival_time: 'Afternoon',
        stops: formData.stops,
        flight_class: 'Economy',
        duration_minutes: formData.duration,
        days_left: Math.max(1, daysLeft),
      };

      const response = await axios.post(`${API_BASE_URL}/predict`, requestData);

      // Generate flight number safely
      const airlineCode = formData.airline ? formData.airline.substring(0, 2).toUpperCase() : 'XX';
      const randomNum = Math.floor(Math.random() * 9000) + 1000;

      setAnalysis({
        delayProbability: response.data.delay_probability,
        delayStatus: response.data.delay_status,
        delayRisk: response.data.delay_risk,
        flightNumber: formData.flightNumber || `${airlineCode}-${randomNum}`,
        route: `${formData.source} → ${formData.destination}`,
      });
    } catch (err) {
      console.error('Analysis error:', err);
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

  const getDelayColor = (probability) => {
    if (probability < 30) return 'text-green-600';
    if (probability < 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getDelayBgColor = (probability) => {
    if (probability < 30) return 'bg-green-500';
    if (probability < 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getRiskBgColor = (risk) => {
    if (risk === 'Low') return 'bg-green-100 text-green-700 border-green-300';
    if (risk === 'Medium') return 'bg-yellow-100 text-yellow-700 border-yellow-300';
    return 'bg-red-100 text-red-700 border-red-300';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-sky-50 to-white">
      {/* Header */}
      <header className="bg-sky-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link 
                to="/" 
                className="bg-sky-700 hover:bg-sky-800 p-2 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-6 h-6" />
              </Link>
              <div>
                <h1 className="text-3xl font-bold">Phân Tích Trễ Chuyến Bay</h1>
                <p className="text-sky-200 text-sm mt-1">
                  Tra cứu xác suất delay theo tuyến hoặc số hiệu chuyến bay
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Search Form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6 border border-blue-100">
              <div className="flex items-center gap-3 mb-6">
                <div className="bg-sky-500 p-2 rounded-lg">
                  <Clock className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-blue-900">Tra Cứu Delay</h2>
              </div>

              {/* Search Type Toggle */}
              <div className="flex gap-2 mb-6">
                <button
                  type="button"
                  onClick={() => setSearchType('route')}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                    searchType === 'route'
                      ? 'bg-sky-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Theo Tuyến Bay
                </button>
                <button
                  type="button"
                  onClick={() => setSearchType('flight')}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                    searchType === 'flight'
                      ? 'bg-sky-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Theo Số Hiệu
                </button>
              </div>

              <form onSubmit={handleAnalyze} className="space-y-4">
                {searchType === 'flight' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Số Hiệu Chuyến Bay (e.g., 6E-2045, AI-101)
                    </label>
                    <input
                      type="text"
                      value={formData.flightNumber}
                      onChange={(e) => setFormData({ ...formData, flightNumber: e.target.value })}
                      placeholder="6E-2045"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                    />
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Hãng Hàng Không
                    </label>
                    <select
                      value={formData.airline}
                      onChange={(e) => setFormData({ ...formData, airline: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent bg-white"
                      required
                    >
                      <option value="">Chọn hãng</option>
                      {airlines.map((airline) => (
                        <option key={airline} value={airline}>
                          {airline}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Ngày Bay
                    </label>
                    <input
                      type="date"
                      value={formData.date}
                      onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                      min={new Date().toISOString().split('T')[0]}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Điểm Khởi Hành
                    </label>
                    <select
                      value={formData.source}
                      onChange={(e) => {
                        const newSource = e.target.value;
                        const newDestination = newSource === formData.destination ? '' : formData.destination;
                        setFormData({ 
                          ...formData, 
                          source: newSource,
                          destination: newDestination
                        });
                        // Auto-update duration and stops
                        if (newDestination) {
                          updateRouteDefaults(newSource, newDestination);
                        }
                        setError(null);
                      }}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent bg-white"
                      required
                    >
                      <option value="">Chọn thành phố</option>
                      {indianCities.map((city) => (
                        <option key={city} value={city}>
                          {city}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Điểm Đến
                    </label>
                    <select
                      value={formData.destination}
                      onChange={(e) => {
                        const newDestination = e.target.value;
                        setFormData({ ...formData, destination: newDestination });
                        // Auto-update duration and stops based on route
                        if (formData.source) {
                          updateRouteDefaults(formData.source, newDestination);
                        }
                        setError(null);
                      }}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent bg-white"
                      required
                    >
                      <option value="">Chọn thành phố</option>
                      {indianCities.map((city) => (
                        <option 
                          key={city} 
                          value={city}
                          disabled={city === formData.source}
                        >
                          {city}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Hidden: Stops and Duration - Auto-calculated based on route */}
                <input type="hidden" value={formData.stops} />
                <input type="hidden" value={formData.duration} />
                
                {/* Show calculated flight info */}
                {formData.source && formData.destination && (
                  <div className="bg-sky-50 border border-sky-200 rounded-lg p-3">
                    <p className="text-sm text-sky-700">
                      <span className="font-medium">Thông tin chuyến bay:</span>
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
                      <p className="text-sm font-medium text-red-800">Lỗi phân tích</p>
                      <p className="text-sm text-red-600 mt-1">{error}</p>
                    </div>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-sky-500 hover:bg-sky-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Đang phân tích...
                    </>
                  ) : (
                    <>
                      <Search className="w-5 h-5" />
                      Phân Tích Delay
                    </>
                  )}
                </button>
              </form>

              {analysis && (
                <div className="mt-6 space-y-4">
                  {/* Flight Info */}
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-600">Chuyến bay</p>
                        <p className="text-lg font-bold text-blue-900">{analysis.flightNumber}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Tuyến</p>
                        <p className="text-lg font-semibold text-gray-900">{analysis.route}</p>
                      </div>
                    </div>
                  </div>

                  {/* Delay Probability */}
                  <div className={`rounded-xl p-6 border-2 ${
                    analysis.delayRisk === 'Low' 
                      ? 'bg-gradient-to-br from-green-50 to-emerald-50 border-green-300' 
                      : analysis.delayRisk === 'Medium'
                      ? 'bg-gradient-to-br from-yellow-50 to-amber-50 border-yellow-300'
                      : 'bg-gradient-to-br from-red-50 to-rose-50 border-red-300'
                  }`}>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Kết Quả Phân Tích</h3>
                    
                    <div className="text-center mb-4">
                      <div className={`text-6xl font-bold mb-2 ${getDelayColor(analysis.delayProbability)}`}>
                        {Math.round(analysis.delayProbability)}%
                      </div>
                      <p className="text-sm text-gray-600">Xác suất delay</p>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div className="bg-white rounded-lg p-3 text-center">
                        <p className="text-sm text-gray-600 mb-1">Trạng thái</p>
                        <p className={`text-lg font-bold ${
                          analysis.delayStatus === 'On-time' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {analysis.delayStatus === 'On-time' ? 'Đúng giờ' : 'Có thể trễ'}
                        </p>
                      </div>
                      <div className="bg-white rounded-lg p-3 text-center">
                        <p className="text-sm text-gray-600 mb-1">Mức độ rủi ro</p>
                        <span className={`inline-block px-3 py-1 rounded-full text-lg font-bold border ${getRiskBgColor(analysis.delayRisk)}`}>
                          {analysis.delayRisk}
                        </span>
                      </div>
                    </div>

                    <div className="w-full bg-gray-300 rounded-full h-3">
                      <div
                        className={`h-3 rounded-full transition-all duration-500 ${getDelayBgColor(analysis.delayProbability)}`}
                        style={{ width: `${analysis.delayProbability}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Historical Data Chart */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6 border border-blue-100 sticky top-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Delay Trends Theo Tháng</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={historicalData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="delays" fill="#0ea5e9" />
                </BarChart>
              </ResponsiveContainer>

              <div className="mt-6 p-4 bg-sky-50 rounded-lg border border-sky-200">
                <div className="flex items-start gap-3">
                  <Cloud className="w-5 h-5 text-sky-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-sky-900">Tip</p>
                    <p className="text-xs text-sky-700 mt-1">
                      Tháng 6-8 (mùa mưa monsoon) thường có tỷ lệ delay cao nhất.
                      Book vé sớm và chọn chuyến sáng để giảm rủi ro.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
