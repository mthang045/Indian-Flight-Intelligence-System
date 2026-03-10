import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

export function DelayAnalysisSimple() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-sky-50 to-white">
      <header className="bg-sky-600 text-white shadow-lg p-6">
        <div className="max-w-7xl mx-auto flex items-center gap-4">
          <Link 
            to="/" 
            className="bg-sky-700 hover:bg-sky-800 p-2 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold">Phân Tích Delay</h1>
            <p className="text-sky-200 text-sm">Test page - Route hoạt động!</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">✅ Routing hoạt động!</h2>
          <p className="text-gray-600 mb-4">
            Nếu bạn thấy trang này, React Router đã OK.
          </p>
          <Link 
            to="/" 
            className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
          >
            ← Về trang chủ
          </Link>
        </div>
      </main>
    </div>
  );
}
