import React, { useState } from 'react';
import './App.css';
import data from './data'; // ✅ Default import

function App() {
  const [rank, setRank] = useState('');
  const [results, setResults] = useState([]);

  const handleFindColleges = () => {
    const numericRank = parseInt(rank);
    if (isNaN(numericRank)) {
      setResults([]);
      return;
    }

    const filtered = data.filter(
      (college) => numericRank <= college.closingRank
    );
    setResults(filtered);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleFindColleges();
    }
  };

  return (
    <div className="App" style={{ textAlign: 'center', padding: '2rem', fontFamily: 'Arial' }}>
      <h1>🎓 RANKCET - College Predictor</h1>
      <p>Enter your TS EAMCET 2024 Rank:</p>

      <input
        type="number"
        value={rank}
        onChange={(e) => setRank(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Enter your EAMCET rank"
        style={{
          padding: '10px',
          width: '250px',
          fontSize: '16px',
          marginBottom: '1rem'
        }}
      />

      <br />

      <button
        onClick={handleFindColleges}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginBottom: '1rem'
        }}
      >
        Find Colleges
      </button>

      <div className="results" style={{ maxWidth: '500px', margin: '0 auto', textAlign: 'left' }}>
        {results.length === 0 ? (
          <p>No colleges to show.</p>
        ) : (
          <ul>
            {results.map((college, index) => (
              <li key={index} style={{ marginBottom: '10px' }}>
                <strong>{college.name}</strong> - {college.branch} (Closing Rank: {college.closingRank})
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
