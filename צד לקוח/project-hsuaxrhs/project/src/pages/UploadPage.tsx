import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CheckCircle, FileSpreadsheet } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import { DataService } from '../services/api';

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isTraining, setIsTraining] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [trainingComplete, setTrainingComplete] = useState(false);
  const navigate = useNavigate();

  const handleFileSelected = (selectedFile: File) => {
    setFile(selectedFile);
    setFileName(selectedFile.name);
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    try {
      setIsUploading(true);
      await DataService.uploadDataset(file, fileName);
      setUploadComplete(true);
      setIsUploading(false);
    } catch (error) {
      setIsUploading(false);
      console.error('Error uploading file:', error);
    }
  };

  const handleInitialize = async () => {
    try {
      setIsTraining(true);
      await DataService.trainModel('demo-dataset-id');
      setTrainingComplete(true);
      setIsTraining(false);
      
      setTimeout(() => {
        navigate('/predict');
      }, 2000);
    } catch (error) {
      setIsTraining(false);
      console.error('Error training model:', error);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">העלאת נתוני אימון</h1>
          <p className="text-gray-600 mb-6">
            העלה קובץ אקסל המכיל נתוני דגימות מחיישני גז עם תוויות לאימון המודל שלך.
            כל דגימה צריכה לכלול קריאות ממספר חיישנים ותווית המציינת האם הריח זוהה.
          </p>

          <form onSubmit={handleUpload} className="space-y-6">
            <FileUpload
              onFileSelected={handleFileSelected}
              loading={isUploading}
            />

            {file && !isUploading && !uploadComplete && (
              <div className="mt-6">
                <Input
                  id="fileName"
                  label="שם מערך הנתונים"
                  value={fileName}
                  onChange={(e) => setFileName(e.target.value)}
                  required
                  placeholder="הזן שם עבור מערך נתונים זה"
                />

                <div className="mt-4 flex justify-center">
                  <Button type="submit" disabled={!fileName} isLoading={isUploading}>
                    העלאת נתונים
                  </Button>
                </div>
              </div>
            )}
          </form>

          {uploadComplete && !isTraining && !trainingComplete && (
            <div className="mt-8 text-center">
              <div className="flex justify-center mb-4">
                <CheckCircle className="h-12 w-12 text-green-500" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                הנתונים הועלו בהצלחה
              </h3>
              <p className="text-gray-600 mb-6">
                מערך הנתונים שלך הועלה ומוכן לעיבוד.
                לחץ על הכפתור למטה כדי לאתחל את המערכת ולאמן את המודל שלך.
              </p>
              <Button onClick={handleInitialize} size="lg">
                אתחול המערכת
              </Button>
            </div>
          )}

          {isTraining && (
            <div className="mt-8 text-center">
              <div className="flex justify-center mb-4">
                <div className="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                אימון בתהליך
              </h3>
              <p className="text-gray-600">
                המערכת מעבדת את הנתונים שלך באמצעות סינון קלמן ומאמנת
                מודל למידת מכונה. התהליך עשוי להימשך מספר דקות.
              </p>
            </div>
          )}

          {trainingComplete && (
            <div className="mt-8 text-center">
              <div className="flex justify-center mb-4">
                <CheckCircle className="h-12 w-12 text-green-500" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                המערכת אותחלה בהצלחה
              </h3>
              <p className="text-gray-600 mb-4">
                המודל שלך אומן ומוכן לשימוש. תועבר לדף החיזוי בקרוב.
              </p>
              <Button onClick={() => navigate('/predict')} variant="outline">
                עבור לדף החיזוי
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadPage;