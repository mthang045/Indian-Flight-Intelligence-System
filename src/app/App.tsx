import { Plane } from 'lucide-react';
import { FlightPricePredictor } from './components/FlightPricePredictor';
import { DelayProbabilityDashboard } from './components/DelayProbabilityDashboard';
import { LanguageProvider, useLanguage } from './context/LanguageContext';
import { LanguageSwitcher } from './components/LanguageSwitcher';

function AppContent() {
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
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Flight Price Predictor */}
          <div className="w-full">
            <FlightPricePredictor />
          </div>

          {/* Delay Probability Dashboard */}
          <div className="w-full">
            <DelayProbabilityDashboard />
          </div>
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
              <div className="text-3xl font-bold text-green-600 mb-1">85%+</div>
              <div className="text-gray-600 text-sm">{t('predictionAccuracy')}</div>
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
      <AppContent />
    </LanguageProvider>
  );
}
