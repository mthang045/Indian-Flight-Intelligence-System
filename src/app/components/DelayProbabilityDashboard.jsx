import { useState } from 'react';
import { AlertCircle, Cloud, Clock, Search } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useLanguage } from '../context/LanguageContext';

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

export function DelayProbabilityDashboard() {
  const { t } = useLanguage();
  const [flightInput, setFlightInput] = useState('');
  const [analysis, setAnalysis] = useState(null);

  const handleAnalyze = (e) => {
    e.preventDefault();
    
    // Mock analysis logic
    const probability = 15 + Math.random() * 60;
    const weatherOptions = [
      { impact: t('clearSkies'), severity: 'low' },
      { impact: t('lightRain'), severity: 'medium' },
      { impact: t('heavyMonsoon'), severity: 'high' },
      { impact: t('fogConditions'), severity: 'medium' },
      { impact: t('strongWinds'), severity: 'high' },
    ];
    
    const weather = weatherOptions[Math.floor(Math.random() * weatherOptions.length)];

    setAnalysis({
      delayProbability: Math.round(probability),
      weatherImpact: weather.impact,
      weatherSeverity: weather.severity,
    });
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

  const getWeatherColor = (severity) => {
    if (severity === 'low') return 'text-green-600';
    if (severity === 'medium') return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-blue-100">
      <div className="flex items-center gap-3 mb-6">
        <div className="bg-sky-500 p-2 rounded-lg">
          <Clock className="w-6 h-6 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-blue-900">{t('delayDashboard')}</h2>
      </div>

      <form onSubmit={handleAnalyze} className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {t('flightNumberRoute')}
        </label>
        <div className="flex gap-3">
          <input
            type="text"
            value={flightInput}
            onChange={(e) => setFlightInput(e.target.value)}
            placeholder="e.g., AI101 or DEL-BOM"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
            required
          />
          <button
            type="submit"
            className="bg-sky-500 hover:bg-sky-600 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
          >
            <Search className="w-5 h-5" />
            {t('analyze')}
          </button>
        </div>
      </form>

      {analysis && (
        <div className="space-y-6">
          {/* Delay Probability */}
          <div className="bg-gradient-to-br from-sky-50 to-blue-50 rounded-xl p-6 border border-sky-200">
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle className="w-5 h-5 text-sky-600" />
              <h3 className="text-lg font-semibold text-blue-900">{t('likelihoodDelay')}</h3>
            </div>
            
            <div className="text-center">
              <div className={`text-6xl font-bold mb-2 ${getDelayColor(analysis.delayProbability)}`}>
                {analysis.delayProbability}%
              </div>
              <p className="text-gray-600 mb-4">{t('probabilityDelay')}</p>
              
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className={`h-3 rounded-full transition-all duration-500 ${getDelayBgColor(analysis.delayProbability)}`}
                  style={{ width: `${analysis.delayProbability}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Weather Impact */}
          <div className="bg-white rounded-xl p-5 border border-gray-200">
            <div className="flex items-center gap-2 mb-3">
              <Cloud className="w-5 h-5 text-sky-600" />
              <h3 className="font-semibold text-blue-900">{t('weatherImpact')}</h3>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <span className="text-gray-700">{analysis.weatherImpact}</span>
              <span className={`font-semibold ${getWeatherColor(analysis.weatherSeverity)}`}>
                {t(analysis.weatherSeverity)}
              </span>
            </div>
          </div>

          {/* Historical Delay Trends */}
          <div className="bg-white rounded-xl p-5 border border-gray-200">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-sky-600" />
              <h3 className="font-semibold text-blue-900">{t('historicalTrends')}</h3>
            </div>
            
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={historicalData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="month" 
                  tick={{ fill: '#6b7280', fontSize: 12 }}
                />
                <YAxis 
                  tick={{ fill: '#6b7280', fontSize: 12 }}
                  label={{ value: t('delayRate') + ' (%)', angle: -90, position: 'insideLeft', fill: '#6b7280' }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
                  }}
                  formatter={(value) => [`${value}%`, t('delayRate')]}
                />
                <Bar dataKey="delays" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
            
            <p className="text-sm text-gray-500 mt-3 text-center">
              {t('averageDelay')}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
