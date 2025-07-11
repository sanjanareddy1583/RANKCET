import React, { useState } from 'react';
import './App.css';
import { collegeData } from './data';

function App() {
  const [rank, setRank] = useState('');
  const [category, setCategory] = useState('OC');
  const [gender, setGender] = useState('Female');
  const [phase, setPhase] = useState('Phase 1');
  const [results, setResults] = useState([]);

  const handleFindColleges = () => {
    const numericRank = parseInt(rank);
    if (isNaN(numericRank)) {
      setResults([]);
      return;
    }

    const filtered = collegeData.filter((college) =>
  college.phase === phase &&
  college.eligibility.some((entry) =>
    entry.category === category &&
    entry.gender === gender &&
    numericRank >= entry.minRank &&
    numericRank <= entry.maxRank
  )
);


    setResults(filtered);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleFindColleges();
    }
  };

  return (
    <div className="app-container">
      <div className="glass-card">
        <h1>🎓 RANKCET - TS EAMCET 2024 College Predictor</h1>
        <p>Find the best colleges based on your rank, category, and counselling round.</p>

        <input
          type="number"
          value={rank}
          onChange={(e) => setRank(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Enter your EAMCET rank"
        />

        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="OC">OC</option>
          <option value="BC-A">BC-A</option>
          <option value="BC-B">BC-B</option>
          <option value="BC-C">BC-C</option>
          <option value="BC-D">BC-D</option>
          <option value="SC">SC</option>
          <option value="ST">ST</option>
        </select>

        <select value={gender} onChange={(e) => setGender(e.target.value)}>
          <option value="Female">Female</option>
          <option value="Male">Male</option>
        </select>

        <select value={phase} onChange={(e) => setPhase(e.target.value)}>
          <option value="Phase 1">Phase 1</option>
          <option value="Phase 2">Phase 2</option>
          <option value="Final Phase">Final Phase</option>
        </select>

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
    </div>
  );
}

export default App;
