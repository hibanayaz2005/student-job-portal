import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import App from './App';
import Login from './components/Login';
import Register from './components/Register';

const AppRouter = () => {
  // const [isAuthenticated, setIsAuthenticated] = useState(true); // Set to true for testing

  return (
    <Router>
      <Routes>
        <Route 
          path="/" 
          element={<App />} 
        />
        <Route 
          path="/login" 
          element={<Login />} 
        />
        <Route 
          path="/register" 
          element={<Register />} 
        />
        <Route 
          path="*" 
          element={<Navigate to="/" />} 
        />
      </Routes>
    </Router>
  );
};

export default AppRouter;
