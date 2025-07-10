import React, { useState } from 'react';
import './App.css';
import data from './data';

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

  // 💥 ENTER KEY FUNCTIONALITY HERE
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleFindColleges();
    }
  };

  return (
    <div className="App">
      <h1>🎓 RANKCET - College Predictor</h1>
      <p>Enter your TS EAMCET 2024 Rank:</p>

      <input
        type="number"
        value={rank}
        onChange={(e) => setRank(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Enter your EAMCET rank"
      />

      <button onClick={handleFindColleges}>Find Colleges</button>

      <div className="results">
        {results.length === 0 ? (
          <p>No colleges to show.</p>
        ) : (
          <ul>
            {results.map((college, index) => (
              <li key={index}>
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
