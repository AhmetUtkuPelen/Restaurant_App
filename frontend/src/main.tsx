import { createRoot } from 'react-dom/client'
import '@mantine/core/styles.css';
import './index.css'
import App from './App.tsx'


createRoot(document.getElementById('root')!).render(
  <>
    <App />
  </>
)
