export interface User {
  id: string;
  username: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface SensorData {
  id: string;
  timestamp: string;
  values: number[];
  label?: boolean;
  prediction?: boolean;
  isFiltered?: boolean;
}

export interface DatasetFile {
  id: string;
  name: string;
  uploadDate: string;
  sampleCount: number;
  isProcessed: boolean;
  isModelTrained: boolean;
}

export interface ModelInfo {
  id: string;
  name: string;
  createdAt: string;
  accuracy: number;
  datasetId: string;
}

export interface PredictionInput {
  sensorValues: number[];
}

export interface PredictionResult {
  originalValues: number[];
  filteredValues: number[];
  prediction: boolean;
  confidence: number;
  smellName: string;
}