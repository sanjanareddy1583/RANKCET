// src/data.js

export const collegeData = [
  {
    name: 'JNTU Hyderabad',
    branch: 'CSE',
    phase: 'Phase 1',
    eligibility: [
      { category: 'OC', gender: 'Male', minRank: 1, maxRank: 1200 },
      { category: 'OC', gender: 'Female', minRank: 1, maxRank: 1500 },
      { category: 'BC-A', gender: 'Male', minRank: 1, maxRank: 2500 },
      { category: 'BC-A', gender: 'Female', minRank: 1, maxRank: 2800 }
    ]
  },
  {
    name: 'OU College of Engineering',
    branch: 'ECE',
    phase: 'Phase 1',
    eligibility: [
      { category: 'BC-B', gender: 'Male', minRank: 1000, maxRank: 4000 },
      { category: 'BC-B', gender: 'Female', minRank: 1000, maxRank: 4500 }
    ]
  },
  {
    name: 'CBIT',
    branch: 'IT',
    phase: 'Phase 2',
    eligibility: [
      { category: 'SC', gender: 'Female', minRank: 3000, maxRank: 9000 },
      { category: 'SC', gender: 'Male', minRank: 3200, maxRank: 9500 }
    ]
  },
  {
    name: 'Vasavi College',
    branch: 'CSE',
    phase: 'Final Phase',
    eligibility: [
      { category: 'OC', gender: 'Male', minRank: 1, maxRank: 2000 },
      { category: 'OC', gender: 'Female', minRank: 1, maxRank: 2200 }
    ]
  }
];
