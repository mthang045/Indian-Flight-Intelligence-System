import { Languages } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const languages = [
  { code: 'vi', name: 'Tiếng Việt', flag: '🇻🇳' },
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
];

export function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage();

  return (
    <div className="flex items-center gap-2">
      <Languages className="w-5 h-5 text-blue-200" />
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="bg-blue-800 text-white border border-blue-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-sky-400 focus:border-transparent cursor-pointer hover:bg-blue-700 transition-colors"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.flag} {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
}
