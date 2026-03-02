import React from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';

function App() {
  return (
    <div className="app-container">
      <Navbar />
      <Home />
      <footer>
        <div className="footer-logo">CareerBridge</div>
        <p>India's first verified student job portal • © 2026</p>
      </footer>
    </div>
  );
}

export default App;