🎓 RANKCET - TS EAMCET College Predictor
This project is a web application designed to help students predict colleges based on their TS EAMCET rank, category, gender, and preferred counselling phase for the year 2024.

✨ Features
College Prediction: Get a list of colleges and branches you might be eligible for based on your EAMCET rank.

Filter Options: Filter results by:

Rank

Category (OC, SC, ST, BC-A, BC-B, BC-C, BC-D, BC-E, EWS)

Gender (Boys, Girls)

Counselling Phase (Phase 1, Phase 2, Final Phase)

Responsive Design: User-friendly interface accessible on both desktop and mobile devices.

🚀 Technologies Used
This application was developed using a modern web development stack to ensure a responsive user experience and efficient data processing.

Frontend:

React.js: Used for building the dynamic and interactive Single Page Application (SPA), leveraging its component-based architecture for modular and maintainable UI.

CSS: Custom CSS was applied for styling, providing a clean, modern, and responsive design, including a "glassmorphism" aesthetic.

Backend:

Flask: A lightweight Python web framework, employed to create a RESTful API that serves college prediction data to the frontend. Its simplicity facilitated rapid development and deployment.

Pandas: A powerful Python library for data manipulation and analysis, crucial for efficiently loading, filtering, and processing the large CSV datasets of college cutoffs.

Deployment:

Vercel: Utilized for deploying the React frontend, providing seamless continuous deployment from GitHub, automatic SSL, and a global CDN.

Render: Used for deploying the Flask backend API, offering a straightforward platform for web service deployment, environment setup, and Python dependency management.

📊 Data Source
The core of this college predictor relies on comprehensive cutoff data. The college cutoff information was sourced directly from official TS EAMCET 2024 last rank statements. This data is provided in structured CSV (Comma Separated Values) format and is stored within the backend/DATA directory of this repository. Each CSV file corresponds to a specific counselling phase for the 2024 academic year.

🌐 Live Application
The application is deployed on cloud platforms, ensuring it is always available online without requiring a local machine to be running.

Frontend (Vercel): https://rankcet.vercel.app/

Backend API (Render): https://rankcet.onrender.com

⚙️ Local Development Setup
The project was set up and run locally for development and testing using the following steps:

Prerequisites
Node.js (LTS version recommended): Required for running the React frontend.

Python 3.8+: Necessary for the Flask backend and its dependencies.

Git: For initializing the repository and managing version control.









1. Repository Setup
First, this project repository was initialized and set up on the local machine using Git:

git init
git add .
git commit -m "Initial commit of RANKCET project"
# Then, connect to your remote GitHub repository
git remote add origin [https://github.com/sanjanareddy1583/RANKCET.git](https://github.com/sanjanareddy1583/RANKCET.git)
git push -u origin main # or master

(Note: If you already have the repository on your local machine, you might skip git init and git remote add origin if it's already connected to your GitHub.)

2. Backend Setup (Flask)
The backend directory was navigated into. Here, a Python virtual environment was set up, necessary Python packages (listed in requirements.txt) were installed, and the Flask development server was started.

cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

The Flask backend API typically runs on http://127.0.0.1:5000 by default.

3. Frontend Setup (React)
In a new terminal window (keeping the backend terminal running), the frontend directory was navigated into. JavaScript dependencies (defined in package.json) were installed, and then the React development server was started.

cd ../frontend
npm install
npm start

The React application usually opens automatically in the default web browser at http://localhost:3000.

Important Note on API URL:
When running locally, the flaskApiUrl constant in frontend/src/App.js should be set to the local Flask backend URL (http://127.0.0.1:5000/predict). When preparing for deployment to Vercel, this flaskApiUrl needs to be updated to the deployed Render API URL (https://rankcet.onrender.com/predict).

🙏 Acknowledgements
This project was developed with the aid of various programming tools and learning resources.
