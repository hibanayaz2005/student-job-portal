import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TestMentorAPI = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const testAPI = async () => {
      try {
        console.log('Testing mentorship API...');
        const response = await axios.get('http://127.0.0.1:8000/api/mentorship/mentors/');
        console.log('API Response:', response.data);
        setData(response.data);
      } catch (err) {
        console.error('API Error:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    testAPI();
  }, []);

  return (
    <div style={{
      position: 'fixed',
      top: '10px',
      right: '10px',
      background: 'white',
      border: '2px solid #333',
      borderRadius: '8px',
      padding: '15px',
      maxWidth: '300px',
      zIndex: 9999,
      fontSize: '12px'
    }}>
      <h4 style={{ margin: '0 0 10px 0' }}>Mentor API Test</h4>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {data && (
        <div>
          <p style={{ color: 'green', margin: '5px 0' }}>✓ API Working!</p>
          <p style={{ margin: '5px 0' }}>Mentors found: {data.mentors?.length || 0}</p>
          {data.mentors?.length > 0 && (
            <div style={{ marginTop: '10px' }}>
              <strong>First mentor:</strong><br/>
              {data.mentors[0].name}<br/>
              {data.mentors[0].mentor_type}<br/>
              Status: {data.mentors[0].today_available ? 'Available Today' : 'Not Available'}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TestMentorAPI;
