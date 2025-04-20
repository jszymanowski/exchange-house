import { render } from 'preact'
import './index.css'
import { App } from './app.tsx'

const container = document.getElementById('app');
if (!container) {
  throw new Error('Root element "#app" not found');
}
render(<App />, container);
