import axios from 'axios';
import { LoginCredentials, PredictionInput, PredictionResult, User } from '../types';

// Base URL would be set based on your backend location
const API_BASE_URL = 'http://127.0.0.1:5000';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  withCredentials: true,  // חשוב לשליחת קוקיז סשן
  // headers: {
  //   'Content-Type': 'application/json',
  // },
});

// Add auth token to requests if available
// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem('token');
//   if (token && config.headers) {
//     config.headers.Authorization = `Bearer ${token}`;
//   }
//   return config;
// });

export const AuthService = {
  async login(credentials: LoginCredentials): Promise<{ user: User; token: string }> {
    const response = await api.post('/auth/login', credentials, {
     // withCredentials: true, // ← קריטי כאן, לא רק בהגדרת axios כללית
    
    });
    // localStorage.setItem('token', response.data.token);
    return response.data;

    // For demo purposes, mock the login - replace with actual API call
    // return new Promise((resolve) => {
    //   setTimeout(() => {
    //     // Mock successful login
    //     const response = {
    //       user: { id: '1', username: credentials.username },
    //       token: 'mock-jwt-token',
    //     };
    //     localStorage.setItem('token', response.token);
    //     resolve(response);
    //   }, 800);
    // });
    
    // Real implementation:
    // const response = await api.post('/auth/login', credentials);
    // localStorage.setItem('token', response.data.token);
    // return response.data;
  },

  logout() {
    localStorage.removeItem('token');
  },


    // 📡 נתיב: GET /auth/me
  async getCurrentUser(): Promise<User | null> {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      localStorage.removeItem('token');
      return null;
    }
  },
};
  // async getCurrentUser(): Promise<User | null> {
  //   // For demo purposes, mock the current user - replace with actual API call
  //   return new Promise((resolve) => {
  //     const token = localStorage.getItem('token');
  //     if (!token) {
  //       resolve(null);
  //       return;
  //     }
      
  //     setTimeout(() => {
  //       resolve({ id: '1', username: 'demo_user' });
  //     }, 300);
  //   });
    
    // Real implementation:
    // try {
    //   const response = await api.get('/auth/me');
    //   return response.data;
    // } catch (error) {
    //   localStorage.removeItem('token');
    //   return null;
    // }
//   },
// };
export const DataService = {
  // 📡 נתיב: POST /datasets/upload
  async uploadDataset(file: File, name: string): Promise<{ success: boolean; message: string }> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);

    const response = await api.post('/datasets/upload', formData, {
      withCredentials: true,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },


// export const DataService = {
//   async uploadDataset(file: File, name: string): Promise<{ success: boolean; message: string }> {
//     // For demo purposes - replace with actual API call
//     return new Promise((resolve) => {
//       setTimeout(() => {
//         resolve({ success: true, message: 'File uploaded successfully' });
//       }, 1500);
//     });
    
    // Real implementation:
    // const formData = new FormData();
    // formData.append('file', file);
    // formData.append('name', name);
    // const response = await api.post('/datasets/upload', formData, {
    //   headers: {
    //     'Content-Type': 'multipart/form-data',
    //   },
    // });
    // return response.data;
  // },

  // async trainModel(datasetId: string): Promise<{ success: boolean; message: string }> {
  //   // For demo purposes - replace with actual API call
  //   return new Promise((resolve) => {
  //     setTimeout(() => {
  //       resolve({ success: true, message: 'Model trained successfully' });
  //     }, 3000);
  //   });
  // 📡 נתיב: POST /models/train/:datasetId
  async trainModel(datasetId: string): Promise<{ success: boolean; message: string }> {
    const response = await api.post(`/models/train/${datasetId}`,null,{withCredentials: true});
    return response.data;
  },
    
    // Real implementation:
    // const response = await api.post(`/models/train/${datasetId}`);
    // return response.data;
  // },

  // async predict(input: PredictionInput): Promise<PredictionResult> {
  //   // For demo purposes - replace with actual API call
  //   return new Promise((resolve) => {
  //     setTimeout(() => {
  //       const originalValues = input.sensorValues;
  //       const filteredValues = originalValues.map(v => v + (Math.random() * 0.1 - 0.05)); // Simulate Kalman filtering
        
  //       resolve({
  //         originalValues,
  //         filteredValues,
  //         prediction: Math.random() > 0.5, // Random prediction for demo
  //         confidence: Math.random() * 0.3 + 0.7, // Random confidence between 70-100%
  //         smellName: 'Lavender', // Example smell name
  //       });
  //     }, 2000);
  //   });
    
  //   // Real implementation:
  //   // const response = await api.post('/predict', input);
  //   // return response.data;
  // },
  // 📡 נתיב: POST /predict
  async predict(input: PredictionInput): Promise<PredictionResult> {
    const response = await api.post('/predict', input, {withCredentials: true},);
    return response.data;
  },
};


export default api;