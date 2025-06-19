import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FileText, Upload } from 'lucide-react';
import Button from './ui/Button';

interface FileUploadProps {
  onFileSelected: (file: File) => void;
  accept?: Record<string, string[]>;
  maxSize?: number;
  loading?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelected,
  accept = {
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    'application/vnd.ms-excel': ['.xls'],
  },
  maxSize = 5242880, // 5MB
  loading = false,
}) => {
  const [fileName, setFileName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length) {
        const file = acceptedFiles[0];
        setFileName(file.name);
        setError(null);
        onFileSelected(file);
      }
    },
    [onFileSelected]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    maxSize,
    multiple: false,
    onDropRejected: (fileRejections) => {
      const rejection = fileRejections[0];
      if (rejection.errors[0].code === 'file-too-large') {
        setError(`הקובץ גדול מדי. גודל מקסימלי הוא ${maxSize / 1024 / 1024}MB`);
      } else if (rejection.errors[0].code === 'file-invalid-type') {
        setError('סוג קובץ לא חוקי. נא להעלות קובץ אקסל (.xlsx או .xls)');
      } else {
        setError('שגיאה בהעלאת הקובץ. נא לנסות שוב.');
      }
    },
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-colors duration-200 ease-in-out
          ${
            isDragActive
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          }
          ${error ? 'border-red-500' : ''}
        `}
      >
        <input {...getInputProps()} disabled={loading} />
        <div className="flex flex-col items-center justify-center gap-2">
          {fileName ? (
            <>
              <FileText size={36} className="text-blue-500" />
              <p className="text-sm font-medium text-gray-700">{fileName}</p>
              <p className="text-xs text-gray-500">לחץ או גרור להחלפה</p>
            </>
          ) : (
            <>
              <Upload size={36} className="text-gray-400" />
              <p className="text-sm font-medium text-gray-700">
                {isDragActive
                  ? 'שחרר את קובץ האקסל כאן'
                  : 'לחץ להעלאה או גרור לכאן'}
              </p>
              <p className="text-xs text-gray-500">קבצי אקסל בלבד (.xlsx, .xls)</p>
            </>
          )}
        </div>
      </div>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      
      {fileName && (
        <div className="mt-4 flex justify-center">
          {/* <Button
            disabled={loading}
            isLoading={loading}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
            }}
          >
            {loading ? 'מעבד...' : 'עבד קובץ'}
          </Button> */}
        </div>
      )}
    </div>
  );
};

export default FileUpload;