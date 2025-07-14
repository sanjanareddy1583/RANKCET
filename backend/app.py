import pandas as pd
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS # This is crucial for connecting frontend and backend

app = Flask(__name__)
CORS(app) # Enable CORS for all routes - allows your React app to talk to Flask

# Define your data directory relative to app.py
DATA_DIR = 'DATA'

# Global variables to store combined EAMCET data
# college_details is no longer needed as the CSV is removed
eamcet_data = pd.DataFrame()

def load_all_data():
    """
    Loads and combines EAMCET cutoff data from CSVs.
    Adds 'Year' and 'Phase' columns to the combined DataFrame.
    This function runs once when the Flask server starts.
    """
    global eamcet_data # Declare as global to modify it

    all_eamcet_data_frames = []

    # --- Load 2024 CSV files (using the simplified names you just created) ---
    csv_files_2024 = {
        '2024_Phase1.csv': 'Phase 1',
        '2024_Phase2.csv': 'Phase 2',
        '2024_FinalPhase.csv': 'Final Phase'
    }
    print("\nAttempting to load 2024 data...")
    for filename, phase_name in csv_files_2024.items():
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath, encoding='latin1', skiprows=1)
                df['Year'] = 2024
                df['Phase'] = phase_name

                # --- !!! CRITICAL: RENAME COLUMNS HERE FOR YOUR 2024 DATA !!! ---
                # Open your 2024 CSV files (e.g., 2024_Phase1.csv) in a text editor or spreadsheet.
                # Look at the FIRST ROW (header).
                # Replace the 'OldColumnNameFromYourCSV' with the EXACT name from your CSV.
                # The 'NewStandardColumnName' is what your code expects (e.g., 'College Name', 'OC BOYS').
                df.rename(columns={
                    'Inst\n Code': 'College Code',
                    'Institute Name': 'College Name',
                    'Place': 'Place',
                    'Dist \nCode': 'District Code',
                    'Co Education': 'Co Education',
                    'College Type': 'College Type',
                    'Year of Estab': 'Year of Establishment',
                    'Branch Code': 'Branch Code',
                    'Branch Name': 'Branch Name',
                    'OC \nBOYS': 'OC BOYS',
                    'OC \nGIRLS': 'OC GIRLS',
                    'BC_A \nBOYS': 'BC_A BOYS',
                    'BC_A \nGIRLS': 'BC_A GIRLS',
                    'BC_B \nBOYS': 'BC_B BOYS',
                    'BC_B \nGIRLS': 'BC_B GIRLS',
                    'BC_C \nBOYS': 'BC_C BOYS',
                    'BC_C \nGIRLS': 'BC_C GIRLS',
                    'BC_D \nBOYS': 'BC_D BOYS',
                    'BC_D \nGIRLS': 'BC_D GIRLS',
                    'BC_E \nBOYS': 'BC_E BOYS',
                    'BC_E \nGIRLS': 'BC_E GIRLS',
                    'SC \nBOYS': 'SC BOYS',
                    'SC \nGIRLS': 'SC GIRLS',
                    'ST \nBOYS': 'ST BOYS',
                    'ST \nGIRLS': 'ST GIRLS',
                    'EWS \nGEN OU': 'EWS BOYS',
                    'EWS \nGIRLS OU': 'EWS GIRLS',
                    'Tuition Fee': 'Tuition Fee',
                    'Affiliated To': 'Affiliated To'
                }, inplace=True, errors='ignore')

                all_eamcet_data_frames.append(df)
                print(f"Loaded 2024 {filename}")
            except Exception as e:
                print(f"Error loading 2024 {filename}: {e}")
        else:
            print(f"Warning: 2024 {filename} not found. Skipping.")

    # Combine all loaded DataFrames
    if all_eamcet_data_frames:
        eamcet_data = pd.concat(all_eamcet_data_frames, ignore_index=True)
        eamcet_data.rename(columns={
            'Institute Name': 'College Name',
            'Branch Name': 'Branch Name',
        }, inplace=True, errors='ignore')
        print("\nAll EAMCET data combined successfully.")
        print("Final Combined DataFrame Columns:", eamcet_data.columns.tolist())
    else:
        print("No EAMCET data loaded from any source.")
        eamcet_data = pd.DataFrame()


# Load data once when the Flask application starts
with app.app_context():
    load_all_data()


# Route to handle requests from your React frontend
@app.route('/predict', methods=['POST'])
def predict_college():
    try:
        data_from_frontend = request.get_json()
        rank = int(data_from_frontend['rank'])
        category = data_from_frontend['category']
        gender = data_from_frontend['gender']
        year_preference = int(data_from_frontend['year_preference'])
        phase_preference = data_from_frontend['phase_preference']

        rank_column = f"{category} {gender}"

        if eamcet_data.empty:
            return jsonify({'predictions': [], 'error': 'EAMCET data not loaded on server. Please check server logs.'}), 500

        filtered_by_year_phase = eamcet_data[
            (eamcet_data['Year'] == year_preference) &
            (eamcet_data['Phase'] == phase_preference)
        ].copy()

        predicted_colleges_list = []

        if rank_column in filtered_by_year_phase.columns:
            filtered_by_year_phase[rank_column] = pd.to_numeric(filtered_by_year_phase[rank_column], errors='coerce')

            colleges_meeting_criteria = filtered_by_year_phase[
                (filtered_by_year_phase[rank_column].notna()) &
                (filtered_by_year_phase[rank_column] >= rank)
            ]

            colleges_meeting_criteria = colleges_meeting_criteria.sort_values(by=rank_column, ascending=True)

            # --- Removed the merge with college_details as it's no longer loaded ---
            
            cols_to_return = [
                'College Name',
                'Branch Name',
                'Year',
                'Phase',
                # You can add 'Tuition Fee' and 'Affiliated To' if you want to display them
                # 'Tuition Fee',
                # 'Affiliated To'
            ]

            if rank_column in colleges_meeting_criteria.columns:
                cols_to_return.append(rank_column)
            
            existing_cols = [col for col in cols_to_return if col in colleges_meeting_criteria.columns]
            
            final_predictions_df = colleges_meeting_criteria[existing_cols].copy()
            
            if rank_column in final_predictions_df.columns:
                final_predictions_df.rename(columns={rank_column: 'ClosingRank'}, inplace=True)
            
            predicted_colleges_list = []
            for index, row in final_predictions_df.iterrows():
                row_dict = row.to_dict()
                row_dict['category'] = category 
                row_dict['gender'] = gender     
                predicted_colleges_list.append(row_dict)

        else:
            print(f"Error: Rank column '{rank_column}' not found in data for year {year_preference}, phase {phase_preference}.")
            return jsonify({'predictions': [], 'error': f"Data for category/gender ('{category} {gender}') is not available for {year_preference} {phase_preference}. Please check your data's column names or try different inputs."}), 400

        if not predicted_colleges_list:
             return jsonify({'predictions': [], 'message': 'No colleges found for the given criteria. Try adjusting your rank or preferences.'}), 200

        return jsonify({'predictions': predicted_colleges_list})

    except KeyError as e:
        return jsonify({'predictions': [], 'error': f"Missing data in request: {e}. Please ensure all fields are submitted from the frontend."}), 400
    except ValueError as e:
        return jsonify({'predictions': [], 'error': f"Invalid input: {e}. Rank must be a number."}), 400
    except Exception as e:
        print(f"An unexpected error occurred in /predict route: {e}")
        return jsonify({'predictions': [], 'error': f"An internal server error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
