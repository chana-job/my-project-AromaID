import React from 'react';
import { PredictionResult } from '../types';
import { CheckCircle, XCircle } from 'lucide-react';

interface ResultCardProps {
  result: PredictionResult;
}

const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
  const { originalValues, filteredValues, prediction, confidence, smellName } = result;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">תוצאת הניתוח</h3>
          <div className="flex items-center">
            {prediction ? (
              <CheckCircle className="w-6 h-6 text-green-500 mr-2" />
            ) : (
              <XCircle className="w-6 h-6 text-red-500 mr-2" />
            )}
            <span className={`text-sm font-medium ${prediction ? 'text-green-500' : 'text-red-500'}`}>
              {prediction ? 'זוהה' : 'לא זוהה'}
            </span>
          </div>
        </div>

        <div className="mb-4">
          <p className="text-lg font-bold text-blue-600">
            {smellName}
          </p>
          <p className="text-sm text-gray-500">
            רמת ביטחון: {(confidence * 100).toFixed(2)}%
          </p>
        </div>

        <div className="mt-6">
          <h4 className="text-sm font-medium text-gray-700 mb-2">ערכי חיישנים</h4>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h5 className="text-xs font-medium text-gray-500 mb-1">מקורי</h5>
              <div className="bg-gray-50 p-2 rounded text-xs">
                {originalValues.map((value, index) => (
                  <div key={`original-${index}`} className="flex justify-between py-1">
                    <span>חיישן {index + 1}:</span>
                    <span className="font-mono">{value.toFixed(4)}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h5 className="text-xs font-medium text-gray-500 mb-1">מסונן (קלמן)</h5>
              <div className="bg-gray-50 p-2 rounded text-xs">
                {filteredValues.map((value, index) => (
                  <div key={`filtered-${index}`} className="flex justify-between py-1">
                    <span>חיישן {index + 1}:</span>
                    <span className="font-mono">{value.toFixed(4)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;