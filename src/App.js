import React, { useState } from 'react';
import './App.css';
import data from './data';

function App() {
  const [rank, setRank] = useState('');
  const [category, setCategory] = useState('OC');
  const [gender, setGender] = useState('Male');
  const [results, setResults] = useState([]);

  const handleFindColleges = () => {
    const numericRank = parseInt(rank);
    if (isNaN(numericRank)) {
      setResults([]);
      return;
    }

    const filtered = data.filter(college =>
      college.category === category &&
      college.gender === gender &&
      numericRank >= college.closingRankLow &&
      numericRank <= college.closingRankHigh
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
          placeholder="Enter your rank"
        />

        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="OC">OC</option>
          <option value="SC">SC</option>
          <option value="ST">ST</option>
          <option value="BC-A">BC-A</option>
          <option value="BC-B">BC-B</option>
          <option value="BC-C">BC-C</option>
          <option value="BC-D">BC-D</option>
          <option value="BC-E">BC-E</option>
        </select>

        <select value={gender} onChange={(e) => setGender(e.target.value)}>
          <option value="Male">Boys</option>
          <option value="Female">Girls</option>
        </select>

        <button onClick={handleFindColleges}>Find Colleges</button>

        <div className="results">
          {results.length === 0 ? (
            <p>No colleges to show.</p>
          ) : (
            <table className="results-table">
              <thead>
                <tr>
                  <th>College Name</th>
                  <th>Branch</th>
                  <th>Gender</th>
                  <th>Category</th>
                  <th>Closing Rank</th>
                </tr>
              </thead>
              <tbody>
                {results.map((college, idx) => (
                  <tr key={idx}>
                    <td>{college.name}</td>
                    <td>{college.branch}</td>
                    <td>{college.gender}</td>
                    <td>{college.category}</td>
                    <td>{college.closingRankHigh}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
