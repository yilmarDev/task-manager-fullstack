import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Consume the root endpoint from the backend
    fetch('http://localhost:8000/')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setMessage(data.message);
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
      </main>
    </div>
  );
}

export default App;
