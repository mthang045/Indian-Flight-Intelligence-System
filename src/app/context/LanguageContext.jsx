import { createContext, useContext, useState } from 'react';

const translations = {
  vi: {
    // Header
    appTitle: 'Hệ Thống Thông Tin Chuyến Bay Ấn Độ',
    appSubtitle: 'Dự Đoán Giá Vé & Phân Tích Trễ Chuyến Bay Bằng AI',
    
    // Flight Price Predictor
    pricePredictor: 'Dự Đoán Giá Vé Máy Bay',
    departureCity: 'Thành Phố Khởi Hành',
    destinationCity: 'Thành Phố Đến',
    selectCity: 'Chọn thành phố',
    travelDate: 'Ngày Bay',
    airline: 'Hãng Hàng Không',
    selectAirline: 'Chọn hãng',
    class: 'Hạng Ghế',
    selectClass: 'Chọn hạng',
    predictPrice: 'Dự Đoán Giá',
    predictedPrice: 'Giá Dự Đoán',
    confidenceScore: 'Độ Tin Cậy:',
    confidenceLevel: 'Mức Độ Tin Cậy',
    
    // Delay Dashboard
    delayDashboard: 'Bảng Điều Khiển Dự Đoán Trễ',
    flightNumberRoute: 'Số Hiệu Chuyến Bay hoặc Tuyến',
    analyze: 'Phân Tích',
    likelihoodDelay: 'Khả Năng Trễ Chuyến',
    probabilityDelay: 'Xác Suất Trễ Chuyến',
    weatherImpact: 'Ảnh Hưởng Thời Tiết',
    historicalTrends: 'Xu Hướng Lịch Sử Trễ Chuyến',
    delayRate: 'Tỷ Lệ Trễ',
    averageDelay: 'Tỷ lệ trung bình trễ chuyến trong 12 tháng qua',
    
    // Weather conditions
    clearSkies: 'Trời Quang - Ảnh Hưởng Tối Thiểu',
    lightRain: 'Mưa Nhẹ - Ảnh Hưởng Trung Bình',
    heavyMonsoon: 'Mưa Lớn - Ảnh Hưởng Cao',
    fogConditions: 'Sương Mù - Ảnh Hưởng Trung Bình',
    strongWinds: 'Gió Mạnh - Ảnh Hưởng Cao',
    
    // Severity
    low: 'THẤP',
    medium: 'TRUNG BÌNH',
    high: 'CAO',
    
    // Classes
    economy: 'Phổ Thông',
    premiumEconomy: 'Phổ Thông Cao Cấp',
    business: 'Thương Gia',
    firstClass: 'Hạng Nhất',
    
    // Footer
    citiesCovered: 'Thành Phố Phủ Sóng',
    airlinesTracked: 'Hãng Hàng Không Theo Dõi',
    predictionAccuracy: 'Độ Chính Xác Dự Đoán',
  },
  en: {
    // Header
    appTitle: 'Indian Flight Intelligence System',
    appSubtitle: 'AI-Powered Flight Price Prediction & Delay Analysis',
    
    // Flight Price Predictor
    pricePredictor: 'Flight Price Predictor',
    departureCity: 'Departure City',
    destinationCity: 'Destination City',
    selectCity: 'Select city',
    travelDate: 'Travel Date',
    airline: 'Airline',
    selectAirline: 'Select airline',
    class: 'Class',
    selectClass: 'Select class',
    predictPrice: 'Predict Price',
    predictedPrice: 'Predicted Price',
    confidenceScore: 'Confidence Score:',
    confidenceLevel: 'Confidence Level',
    
    // Delay Dashboard
    delayDashboard: 'Delay Probability Dashboard',
    flightNumberRoute: 'Flight Number or Route',
    analyze: 'Analyze',
    likelihoodDelay: 'Likelihood of Delay',
    probabilityDelay: 'Probability of Delay',
    weatherImpact: 'Weather Impact',
    historicalTrends: 'Historical Delay Trends',
    delayRate: 'Delay Rate',
    averageDelay: 'Average delay percentage over the past 12 months',
    
    // Weather conditions
    clearSkies: 'Clear Skies - Minimal Impact',
    lightRain: 'Light Rain - Moderate Impact',
    heavyMonsoon: 'Heavy Monsoon - High Impact',
    fogConditions: 'Fog Conditions - Moderate Impact',
    strongWinds: 'Strong Winds - High Impact',
    
    // Severity
    low: 'LOW',
    medium: 'MEDIUM',
    high: 'HIGH',
    
    // Classes
    economy: 'Economy',
    premiumEconomy: 'Premium Economy',
    business: 'Business',
    firstClass: 'First Class',
    
    // Footer
    citiesCovered: 'Indian Cities Covered',
    airlinesTracked: 'Major Airlines Tracked',
    predictionAccuracy: 'Prediction Accuracy',
  },
  hi: {
    // Header
    appTitle: 'भारतीय विमान सूचना प्रणाली',
    appSubtitle: 'एआई-संचालित विमान मूल्य पूर्वानुमान और विलंब विश्लेषण',
    
    // Flight Price Predictor
    pricePredictor: 'विमान मूल्य पूर्वानुमानक',
    departureCity: 'प्रस्थान शहर',
    destinationCity: 'गंतव्य शहर',
    selectCity: 'शहर चुनें',
    travelDate: 'यात्रा तिथि',
    airline: 'एयरलाइन',
    selectAirline: 'एयरलाइन चुनें',
    class: 'श्रेणी',
    selectClass: 'श्रेणी चुनें',
    predictPrice: 'मूल्य पूर्वानुमान',
    predictedPrice: 'अनुमानित मूल्य',
    confidenceScore: 'विश्वास स्कोर:',
    confidenceLevel: 'विश्वास स्तर',
    
    // Delay Dashboard
    delayDashboard: 'विलंब संभावना डैशबोर्ड',
    flightNumberRoute: 'उड़ान संख्या या मार्ग',
    analyze: 'विश्लेषण करें',
    likelihoodDelay: 'विलंब की संभावना',
    probabilityDelay: 'विलंब की संभावना',
    weatherImpact: 'मौसम प्रभाव',
    historicalTrends: 'ऐतिहासिक विलंब रुझान',
    delayRate: 'विलंब दर',
    averageDelay: 'पिछले 12 महीनों में औसत विलंब प्रतिशत',
    
    // Weather conditions
    clearSkies: 'साफ आसमान - न्यूनतम प्रभाव',
    lightRain: 'हल्की बारिश - मध्यम प्रभाव',
    heavyMonsoon: 'भारी मानसून - उच्च प्रभाव',
    fogConditions: 'कोहरे की स्थिति - मध्यम प्रभाव',
    strongWinds: 'तेज हवाएं - उच्च प्रभाव',
    
    // Severity
    low: 'कम',
    medium: 'मध्यम',
    high: 'उच्च',
    
    // Classes
    economy: 'इकोनॉमी',
    premiumEconomy: 'प्रीमियम इकोनॉमी',
    business: 'बिजनेस',
    firstClass: 'फर्स्ट क्लास',
    
    // Footer
    citiesCovered: 'भारतीय शहर कवर किए गए',
    airlinesTracked: 'प्रमुख एयरलाइनों को ट्रैक किया गया',
    predictionAccuracy: 'पूर्वानुमान सटीकता',
  },
};

const LanguageContext = createContext(undefined);

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('en');

  const t = (key) => {
    return translations[language][key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
