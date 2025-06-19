import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FileSpreadsheet, 
  FilterX, 
  BrainCircuit, 
  Search,
  ArrowRight
} from 'lucide-react';
import { useAuth } from '../context/auth';
import Button from '../components/ui/Button';

const DashboardPage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          ברוך הבא, {user?.username}
        </h1>
        <p className="text-gray-600 mt-1">
          AromaID מסייעת לך לנתח נתוני חיישני גז ולזהות ריחות ספציפיים.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="p-6">
            <div className="flex items-center justify-center w-12 h-12 rounded-md bg-blue-100 text-blue-600 mb-4">
              <FileSpreadsheet className="w-6 h-6" />
            </div>
            <h2 className="text-lg font-medium text-gray-900 mb-2">
              העלאת נתוני אימון
            </h2>
            <p className="text-gray-600 mb-4">
              העלה קובצי אקסל עם נתוני חיישני גז מתויגים לאימון מודל הזיהוי שלך.
            </p>
            <Link to="/upload">
              <Button variant="outline" fullWidth>
                העלאת נתונים <ArrowRight className="w-4 h-4 mr-2" />
              </Button>
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="p-6">
            <div className="flex items-center justify-center w-12 h-12 rounded-md bg-teal-100 text-teal-600 mb-4">
              <FilterX className="w-6 h-6" />
            </div>
            <h2 className="text-lg font-medium text-gray-900 mb-2">
              סינון קלמן
            </h2>
            <p className="text-gray-600 mb-4">
              הנתונים שלך מנוקים אוטומטית באמצעות סינון קלמן להסרת רעשים.
            </p>
            <Button variant="outline" fullWidth disabled>
              תהליך אוטומטי
            </Button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="p-6">
            <div className="flex items-center justify-center w-12 h-12 rounded-md bg-purple-100 text-purple-600 mb-4">
              <BrainCircuit className="w-6 h-6" />
            </div>
            <h2 className="text-lg font-medium text-gray-900 mb-2">
              אימון מודל למידת מכונה
            </h2>
            <p className="text-gray-600 mb-4">
              מודלים של למידת מכונה מאומנים על הנתונים המסוננים שלך לחיזוי מדויק.
            </p>
            <Button variant="outline" fullWidth disabled>
              תהליך אוטומטי
            </Button>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-blue-600 to-teal-600 rounded-lg shadow-lg overflow-hidden">
        <div className="p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">מוכן לבצע חיזויים?</h2>
          <p className="mb-6 opacity-90">
            לאחר העלאת נתוני האימון ואתחול המערכת, תוכל לנתח קריאות חיישנים חדשות ולקבל חיזויים.
          </p>
          <div className="flex justify-start">
            <Link to="/predict">
              <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100">
                <Search className="w-5 h-5 ml-2" />
                התחל בחיזוי
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;