import React, { useState } from 'react';
import { FileSpreadsheet } from 'lucide-react';
import SensorInputForm from '../components/SensorInputForm';
import ResultCard from '../components/ResultCard';
import { DataService } from '../services/api';
import { PredictionInput, PredictionResult } from '../types';

const PredictPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);

  const handleSubmit = async (data: PredictionInput) => {
    try {
      setIsLoading(true);
      const result = await DataService.predict(data);
      setResult(result);
      setIsLoading(false);
    } catch (error) {
      setIsLoading(false);
      console.error('Error predicting:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">חיזוי ריח</h1>
          <p className="text-gray-600 mb-6">
            הזן את קריאות החיישנים מחיישני הגז שלך. המערכת תפעיל סינון קלמן
            לניקוי הנתונים ותספק חיזוי המבוסס על המודל המאומן שלך.
          </p>

          <div className="mb-8">
            <h2 className="text-lg font-medium text-gray-900 mb-4">קריאות חיישנים</h2>
            <SensorInputForm
              onSubmit={handleSubmit}
              numSensors={6}
              isLoading={isLoading}
            />
          </div>

          {isLoading && (
            <div className="flex justify-center my-8">
              <div className="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full" />
            </div>
          )}

          {result && !isLoading && (
            <div className="mt-10">
              <h2 className="text-lg font-medium text-gray-900 mb-4">תוצאת החיזוי</h2>
              <ResultCard result={result} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PredictPage;