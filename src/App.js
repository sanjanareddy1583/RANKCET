import React, { useState } from "react";
import { colleges } from "./data"; // ✅ Import from data.js

function App() {
  const [rank, setRank] = useState("");
  const [results, setResults] = useState([]);

  const handleInputChange = (e) => {
    setRank(e.target.value);
  };

  const handleSubmit = () => {
    const numericRank = parseInt(rank);
    if (isNaN(numericRank)) {
      alert("⚠️ Please enter a valid numeric rank");
      return;
    }

    const eligible = colleges.filter(
      (college) =>
        numericRank >= college.rankRange[0] &&
        numericRank <= college.rankRange[1]
    );

    setResults(eligible);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "Arial" }}>
      <h1 style={{ color: "#007bff" }}>🎓 RANKCET College Predictor</h1>
      <p>Enter your EAMCET rank to see eligible colleges</p>

      <input
        type="number"
        placeholder="Enter your rank"
        value={rank}
        onChange={handleInputChange}
        style={{
          padding: "10px",
          width: "250px",
          fontSize: "16px",
          borderRadius: "5px",
          border: "1px solid #ccc",
        }}
      />

      <br />
      <br />

      <button
        onClick={handleSubmit}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "5px",
        }}
      >
        🔍 Find Colleges
      </button>

      <br />
      <br />

      <div id="results" style={{ maxWidth: "600px", margin: "auto" }}>
        <h3>📋 Eligible Colleges:</h3>
        {results.length === 0 ? (
          <p>No colleges found for this rank.</p>
        ) : (
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {results.map((college, index) => (
              <li
                key={index}
                style={{
                  padding: "10px",
                  marginBottom: "10px",
                  border: "1px solid #ddd",
                  borderRadius: "5px",
                  backgroundColor: "#f9f9f9",
                }}
              >
                <strong>{college.name}</strong> — {college.branch}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
