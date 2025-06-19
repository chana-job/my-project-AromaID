import React, { useState } from 'react';
import { PredictionInput } from '../types';
import Button from './ui/Button';
import Input from './ui/Input';

interface SensorInputFormProps {
  onSubmit: (data: PredictionInput) => void;
  numSensors?: number;
  isLoading?: boolean;
}

const SensorInputForm: React.FC<SensorInputFormProps> = ({
  onSubmit,
  numSensors = 6,
  isLoading = false,
}) => {
  const [sensorValues, setSensorValues] = useState<number[]>(Array(numSensors).fill(0));

  const handleChange = (index: number, value: string) => {
    const newValues = [...sensorValues];
    newValues[index] = parseFloat(value) || 0;
    setSensorValues(newValues);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ sensorValues });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.from({ length: numSensors }).map((_, index) => (
          <Input
            key={`sensor-${index}`}
            id={`sensor-${index}`}
            label={`חיישן ${index + 1}`}
            type="number"
            step="0.01"
            value={sensorValues[index] || ''}
            onChange={(e) => handleChange(index, e.target.value)}
            disabled={isLoading}
            //required
          />
        ))}
      </div>
      <div className="mt-6 flex justify-center">
        <Button
          type="submit"
          disabled={isLoading}
          isLoading={isLoading}
          size="lg"
        >
          {isLoading ? 'מעבד...' : 'נתח דגימה'}
        </Button>
      </div>
    </form>
  );
};

export default SensorInputForm;