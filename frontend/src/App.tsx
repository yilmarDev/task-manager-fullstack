import { useState, useEffect } from 'react';
import './App.css';

export interface APIHealthStatus {
  status: string;
  service: string;
  database: string;
}

function App() {
  const [message, setMessage] = useState('');
  const [health, setHealth] = useState<APIHealthStatus>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Consume the root endpoint from the backend
    Promise.all([
      fetch('http://localhost:8000/').then((r) => r.json()),
      fetch('http://localhost:8000/health').then((r) => r.json()),
    ])
      .then(([rootData, healthData]) => {
        setMessage(rootData.message);
        setHealth(healthData);
        setLoading(false);
      })
      .catch((err) => {
        setError(`Error: ${err.message}`);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header>
        <h1>Task Manager</h1>
      </header>
      <main>
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {message && (
          <p>
            <strong>Backend says:</strong> {message}
          </p>
        )}
        {health && (
          <p>
            <strong>Health Status:</strong> {health.status} - {health.service}
          </p>
        )}
      </main>
    </div>
  );
}

export default App;
