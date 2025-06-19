import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    host: '127.0.0.1',   // ← כאן אתה מגדיר את הכתובת
    port: 5173,          // ← לא חובה אם אתה מריץ כבר על 5173
  },
});
