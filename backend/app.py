import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Global variable to store combined DataFrame
final_combined_df = pd.DataFrame()

def load_and_combine_data():
    global final_combined_df
    
    # --- CRITICAL CHANGE: Use an absolute path for data_dir ---
    # This ensures the 'data' directory is found relative to app.py's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    print(f"DEBUG: Current working directory: {os.getcwd()}") # Added debug print
    print(f"DEBUG: app.py directory: {base_dir}") # Added debug print
    print(f"Attempting to load data from: {data_dir}") # Debugging print
    
    # --- NEW: Print contents of the backend directory ---
    try:
        print(f"DEBUG: Contents of {base_dir}: {os.listdir(base_dir)}")
    except Exception as e:
        print(f"DEBUG: Could not list contents of {base_dir}: {e}")

    # Check if the data directory actually exists
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' does not exist. Please ensure it's in your GitHub repo and correctly capitalized.")
        # Raise an error to stop deployment if data is missing
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")
        
    all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]

    df_list = []
    print("Attempting to load data from CSVs...")
    for f in all_files:
        try:
            # Read CSV, skipping the first row (header is in second row)
            df = pd.read_csv(f, skiprows=[0])
            
            # Rename columns for consistency and easier access
            df.rename(columns={
                'Institute Name': 'College Name',
                'Dist Code': 'District Code',
                'Co Education': 'Co Education',
                'College Type': 'College Type',
                'Year of Estab': 'Year of Establishment',
                'Branch Code': 'Branch Code',
                'Branch Name': 'Branch Name',
                'OC Boys': 'OC BOYS',
                'OC Girls': 'OC GIRLS',
                'BC-A Boys': 'BC_A BOYS',
                'BC-A Girls': 'BC_A GIRLS',
                'BC-B Boys': 'BC_B BOYS',
                'BC-B Girls': 'BC_B GIRLS',
                'BC-C Boys': 'BC_C BOYS',
                'BC_C Girls': 'BC_C GIRLS',
                'BC-D Boys': 'BC_D BOYS',
                'BC_D Girls': 'BC_D GIRLS',
                'BC-E Boys': 'BC_E BOYS',
                'BC-E Girls': 'BC_E GIRLS',
                'SC Boys': 'SC BOYS',
                'SC Girls': 'SC GIRLS',
                'ST Boys': 'ST BOYS',
                'ST Girls': 'ST GIRLS',
                'EWS GEN OU': 'EWS BOYS', # Mapping from CSV header 'EWS GEN OU'
                'EWS GIRLS OU': 'EWS GIRLS', # Mapping from CSV header 'EWS GIRLS OU'
                'Tuition Fee': 'Tuition Fee',
                'Affiliated To': 'Affiliated To',
                # 'Inst Code' is assumed to be correctly named and present in CSV, no renaming for it here.
            }, inplace=True)

            # Ensure 'Inst Code' column exists and is string type
            if 'Inst Code' in df.columns:
                df['Inst Code'] = df['Inst Code'].astype(str)
            else:
                print(f"Warning: 'Inst Code' column not found in {os.path.basename(f)}. Adding empty column.")
                df['Inst Code'] = '' # Add an empty column if not found to prevent errors

            # Extract Year and Phase from filename
            filename = os.path.basename(f)
            if '2024' in filename:
                df['Year'] = 2024
            if 'Phase1' in filename:
                df['Phase'] = 'Phase 1'
            elif 'Phase2' in filename:
                df['Phase'] = 'Phase 2'
            elif 'FinalPhase' in filename:
                df['Phase'] = 'Final Phase'
            
            df_list.append(df)
            print(f"Loaded {os.path.basename(f)}")
        except Exception as e:
            print(f"Error loading {f}: {e}")

    if df_list:
        final_combined_df = pd.concat(df_list, ignore_index=True)
        print("All EAMCET data combined successfully.")
        print("Final Combined DataFrame Columns:", final_combined_df.columns.tolist())
    else:
        print("No CSV files loaded. Combined DataFrame is empty.")

# Call the function to load data when the app starts
load_and_combine_data()

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    data = request.get_json()
    rank = data.get('rank')
    category = data.get('category')
    gender = data.get('gender')
    year_preference = data.get('year_preference')
    phase_preference = data.get('phase_preference')

    if not all([rank, category, gender, year_preference, phase_preference]):
        return jsonify({'error': 'Missing data. Please provide rank, category, gender, year, and phase.'}), 400

    rank_column = f"{category} {gender}"

    # Filter the DataFrame based on user inputs
    if rank_column not in final_combined_df.columns:
        return jsonify({'error': f"Rank column '{rank_column}' not found in data."}), 400

    filtered_df = final_combined_df[
        (final_combined_df['Year'] == int(year_preference)) &
        (final_combined_df['Phase'] == phase_preference) &
        (pd.to_numeric(final_combined_df[rank_column], errors='coerce') >= rank) # Convert to numeric for comparison
    ].copy()

    # Drop rows where rank_column conversion failed (NaNs)
    filtered_df.dropna(subset=[rank_column], inplace=True)
    filtered_df[rank_column] = pd.to_numeric(filtered_df[rank_column]) # Ensure it's numeric for sorting

    filtered_df.sort_values(by=rank_column, ascending=True, inplace=True)

    # Ensure 'ClosingRank' column exists for consistent frontend display
    filtered_df['ClosingRank'] = filtered_df[rank_column]

    # Add 'category' and 'gender' columns if they don't exist, for frontend display
    filtered_df['category'] = category
    filtered_df['gender'] = gender

    # Select only the columns needed for the frontend display, including 'Inst Code'
    display_columns = [
        'Inst Code', # Explicitly include 'Inst Code'
        'College Name',
        'Branch Name',
        'ClosingRank',
        'Year',
        'Phase',
        'category',
        'gender'
    ]
    
    # Filter out display_columns that might not exist in the DataFrame (e.g., if a CSV is missing a column)
    actual_display_columns = [col for col in display_columns if col in filtered_df.columns]
    
    predictions = filtered_df[actual_display_columns].to_dict(orient='records')

    return jsonify({'predictions': predictions})

if __name__ == '__main__':
    app.run(debug=True)

