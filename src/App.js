import React, { useState } from 'react';
import './App.css';
import data from './data';

function App() {
  const [rank, setRank] = useState('');
  const [category, setCategory] = useState('OC');
  const [phase, setPhase] = useState('Phase 1');
  const [results, setResults] = useState([]);

  const handleFindColleges = () => {
    const numericRank = parseInt(rank);
    if (isNaN(numericRank)) {
      setResults([]);
      return;
    }

    const filtered = data.filter(
      (college) =>
        numericRank <= college.closingRank &&
        college.category === category &&
        college.phase === phase
    );

    setResults(filtered);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleFindColleges();
    }
  };

  return (
    <div className="App">
      <h1>🎓 RANKCET - TS EAMCET 2024 College Predictor</h1>
      <p>Find the best colleges based on your rank, category, and counselling round.</p>

      <div className="input-card">
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
          <option value="BC-E">BC-E</option>
          <option value="SC">SC</option>
          <option value="ST">ST</option>
        </select>

        <select value={phase} onChange={(e) => setPhase(e.target.value)}>
          <option value="Phase 1">Phase 1</option>
          <option value="Phase 2">Phase 2</option>
          <option value="Final Phase">Final Phase</option>
        </select>

        <button onClick={handleFindColleges}>Find Colleges</button>
      </div>

      <div className="results">
        {results.length === 0 ? (
          <p className="no-results">No colleges to show.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>College</th>
                  <th>Branch</th>
                  <th>Category</th>
                  <th>Closing Rank</th>
                  <th>Phase</th>
                </tr>
              </thead>
              <tbody>
                {results.map((college, index) => (
                  <tr key={index}>
                    <td>{college.name}</td>
                    <td>{college.branch}</td>
                    <td>{college.category}</td>
                    <td>{college.closingRank}</td>
                    <td>{college.phase}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
