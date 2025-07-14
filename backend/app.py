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
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]

    df_list = []
    print("Attempting to load data from CSVs...")
    for f in all_files:
        try:
            # Read CSV, skipping the first row (header is in second row)
            df = pd.read_csv(f, skiprows=[0])
            
            # Rename columns for consistency and easier access
            # IMPORTANT: Explicitly map original CSV headers to desired DataFrame column names.
            # We are keeping 'Inst Code' as 'Inst Code'.
            df.rename(columns={
                'Institute Name': 'College Name',
                'Dist Code': 'District Code',
                'Co Education': 'Co Education',
                'College Type': 'College Type',
                'Year of Estab': 'Year of Establishment',
                'Branch Code': 'Branch Code',
                'Branch Name': 'Branch Name',
                'OC BOYS': 'OC BOYS',
                'OC GIRLS': 'OC GIRLS',
                'BC_A BOYS': 'BC_A BOYS',
                'BC_A GIRLS': 'BC_A GIRLS',
                'BC_B BOYS': 'BC_B BOYS',
                'BC_B GIRLS': 'BC_B GIRLS',
                'BC_C BOYS': 'BC_C BOYS',
                'BC_C GIRLS': 'BC_C GIRLS',
                'BC_D BOYS': 'BC_D BOYS',
                'BC_D GIRLS': 'BC_D GIRLS',
                'BC_E BOYS': 'BC_E BOYS',
                'BC_E GIRLS': 'BC_E GIRLS',
                'SC BOYS': 'SC BOYS',
                'SC GIRLS': 'SC GIRLS',
                'ST BOYS': 'ST BOYS',
                'ST GIRLS': 'ST GIRLS',
                'EWS GEN OU': 'EWS BOYS', # Mapping from CSV header 'EWS GEN OU'
                'EWS GIRLS OU': 'EWS GIRLS', # Mapping from CSV header 'EWS GIRLS OU'
                'Tuition Fee': 'Tuition Fee',
                'Affiliated To': 'Affiliated To',
                # 'Inst Code' is assumed to be correctly named and present in CSV, no renaming for it here.
                # If 'College Code' also exists and you need it, add it here.
            }, inplace=True)

            # Ensure 'Inst Code' column exists and is string type
            if 'Inst Code' in df.columns:
                df['Inst Code'] = df['Inst Code'].astype(str)
            else:
                print(f"Warning: 'Inst Code' column not found in {os.path.basename(f)}")
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
    # Ensure rank_column exists before filtering
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

