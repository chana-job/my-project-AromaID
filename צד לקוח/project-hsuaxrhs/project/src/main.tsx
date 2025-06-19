import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@fontsource/assistant';
import App from './App';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);