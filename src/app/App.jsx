import { Plane, BarChart3, ChevronRight } from 'lucide-react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { FlightPricePredictor } from './components/FlightPricePredictor';
import { DelayAnalysis } from './pages/DelayAnalysis';
import { LanguageProvider, useLanguage } from './context/LanguageContext';
import { LanguageSwitcher } from './components/LanguageSwitcher';

function HomePage() {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-sky-50 to-white">
      {/* Header */}
      <header className="bg-blue-900 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-sky-500 p-3 rounded-lg">
                <Plane className="w-8 h-8" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">{t('appTitle')}</h1>
                <p className="text-blue-200 text-sm mt-1">
                  {t('appSubtitle')}
                </p>
              </div>
            </div>
            <LanguageSwitcher />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Access Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Price Predictor Card */}
          <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 text-white shadow-lg">
            <div className="flex items-center gap-3 mb-3">
              <Plane className="w-8 h-8" />
              <h3 className="text-xl font-bold">Dự Đoán Giá Vé</h3>
            </div>
            <p className="text-blue-100 text-sm mb-4">
              Dự đoán giá vé và xác suất delay ngay trong 1 lần tra cứu
            </p>
            <div className="flex items-center text-blue-100 text-sm">
              <span className="bg-blue-800 px-2 py-1 rounded">Đang ở đây</span>
            </div>
          </div>

          {/* Delay Analysis Card */}
          <Link 
            to="/delay-analysis"
            className="bg-gradient-to-br from-sky-500 to-sky-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl transition-all hover:scale-105"
          >
            <div className="flex items-center gap-3 mb-3">
              <BarChart3 className="w-8 h-8" />
              <h3 className="text-xl font-bold">Phân Tích Delay Chi Tiết</h3>
            </div>
            <p className="text-sky-100 text-sm mb-4">
              Tra cứu theo số hiệu chuyến bay hoặc tuyến bay cụ thể
            </p>
            <div className="flex items-center gap-1 text-white font-medium">
              <span>Xem chi tiết</span>
              <ChevronRight className="w-5 h-5" />
            </div>
          </Link>
        </div>

        {/* Flight Price Predictor */}
        <div className="w-full max-w-4xl mx-auto">
          <FlightPricePredictor />
        </div>

        {/* Footer Info */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-6 border border-blue-100">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-1">12+</div>
              <div className="text-gray-600 text-sm">{t('citiesCovered')}</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-sky-500 mb-1">6+</div>
              <div className="text-gray-600 text-sm">{t('airlinesTracked')}</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-600 mb-1">98%+</div>
              <div className="text-gray-600 text-sm">Model Accuracy (R²)</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/delay-analysis" element={<DelayAnalysis />} />
        </Routes>
      </BrowserRouter>
    </LanguageProvider>
  );
}
