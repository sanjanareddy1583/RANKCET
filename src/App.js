import React, { useState } from 'react';
import './App.css';

function App() {
  const [rank, setRank] = useState('');
  const [category, setCategory] = useState('OC');
  const [gender, setGender] = useState('BOYS');
  const [yearPreference, setYearPreference] = useState('2024');
  const [phasePreference, setPhasePreference] = useState('Final Phase');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFindColleges = async () => {
    const numericRank = parseInt(rank);
    if (isNaN(numericRank) || numericRank <= 0) {
      setResults([]);
      setError("Please enter a valid positive rank.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const flaskApiUrl = 'http://127.0.0.1:5000/predict';

      const response = await fetch(flaskApiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rank: numericRank,
          category: category,
          gender: gender,
          year_preference: yearPreference,
          phase_preference: phasePreference
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Something went wrong on the server.');
      }

      const data = await response.json();
      
      console.log("Received data from Flask:", data); 

      if (data.predictions && Array.isArray(data.predictions) && data.predictions.length > 0) {
        setResults(data.predictions);
        console.log("Results set:", data.predictions);
      } else {
        setResults([]);
        setError(data.message || "No colleges found for the given criteria.");
        console.log("No predictions or empty predictions received.");
      }

    } catch (err) {
      console.error("Error fetching data:", err);
      setError(err.message || "Failed to fetch college predictions. Ensure backend is running.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleFindColleges();
    }
  };

  console.log("Current results length (before render):", results.length);

  return (
    <div className="app-container">
      <div className="glass-card">
        {/* Explicitly wrapping all direct children of glass-card in a React Fragment */}
        <>
          <h1>🎓 RANKCET - TS EAMCET 2024 College Predictor</h1>
          <p>Find the best colleges based on your rank, category, and counselling round.</p>

          {/* This is the input section */}
          <div className="input-section">
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
              <option value="BC_A">BC-A</option>
              <option value="BC_B">BC-B</option>
              <option value="BC_C">BC-C</option>
              <option value="BC_D">BC-D</option>
              <option value="BC_E">BC-E</option>
              <option value="EWS">EWS</option>
            </select>

            <select value={gender} onChange={(e) => setGender(e.target.value)}>
              <option value="BOYS">Boys</option>
              <option value="GIRLS">Girls</option>
            </select>

            <select value={yearPreference} onChange={(e) => setYearPreference(e.target.value)}>
              <option value="2024">2024 Cutoffs</option>
            </select>

            <select value={phasePreference} onChange={(e) => setPhasePreference(e.target.value)}>
                <option value="Final Phase">Final Phase</option>
                <option value="Phase 1">Phase 1</option>
                <option value="Phase 2">Phase 2</option>
            </select>

            <button onClick={handleFindColleges} disabled={loading}>
              {loading ? 'Finding...' : 'Find Colleges'}
            </button>
          </div> {/* End input-section */}

          {error && <p className="error-message">{error}</p>}

          {/* This is the results section */}
          <div className="results-section">
            {results.length === 0 && !loading && !error ? (
              <p>No colleges to show. Enter your details and click "Find Colleges".</p>
            ) : results.length === 0 && !loading && error ? (
              null
            ) : (
              <div className="table-container">
                <table className="results-table">
                  <thead>
                    <tr>
                      <th>College Name</th><th>Branch</th><th>Category/Gender</th><th>Closing Rank</th><th>Year</th><th>Phase</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.map((college, idx) => (
                      <tr key={idx}>
                        <td>{college['College Name']}</td>
                        <td>{college['Branch Name']}</td>
                        <td>{`${college.category} ${college.gender}`}</td>
                        <td>{college.ClosingRank}</td>
                        <td>{college.Year}</td>
                        <td>{college.Phase}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div> {/* End results-section */}
        </> {/* End React Fragment */}
      </div>
    </div>
  );
}

export default App;
