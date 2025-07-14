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
    print("Attempting to load 2024 data...")
    for f in all_files:
        try:
            # Read CSV, skipping the first row (header is in second row)
            df = pd.read_csv(f, skiprows=[0])
            
            # Rename columns for consistency and easier access
            # IMPORTANT: We are now keeping 'Inst Code' as 'Inst Code'
            df.rename(columns={
                #'College Code': 'College Code', # If your CSV has this, keep it.
                'Co-Education': 'Co Education', # Handle potential hyphen
                'Branch Code': 'Branch Code',
                'OC Boys': 'OC BOYS',
                'OC Girls': 'OC GIRLS',
                'BC-A Boys': 'BC_A BOYS', # Standardize BC categories
                'BC-A Girls': 'BC_A GIRLS',
                'BC-B Boys': 'BC_B BOYS',
                'BC-B Girls': 'BC_B GIRLS',
                'BC-C Boys': 'BC_C BOYS',
                'BC-C Girls': 'BC_C GIRLS',
                'BC-D Boys': 'BC_D BOYS',
                'BC-D Girls': 'BC_D GIRLS',
                'BC-E Boys': 'BC_E BOYS',
                'BC-E Girls': 'BC_E GIRLS',
                'SC Boys': 'SC BOYS',
                'SC Girls': 'SC GIRLS',
                'ST Boys': 'ST BOYS',
                'ST Girls': 'ST GIRLS',
                'EWS Boys': 'EWS BOYS',
                'EWS Girls': 'EWS GIRLS',
                'Tuition Fee': 'Tuition Fee',
                'Affiliated To': 'Affiliated To',
                # Ensure 'College Name', 'Place', 'District Code', 'College Type', 'Year of Establishment', 'Branch Name', 'Year', 'Phase' are correctly mapped if their CSV names differ.
                # For 'Inst Code', we assume it's already named 'Inst Code' in the CSV and we want to keep it.
            }, inplace=True)

            # Extract Year and Phase from filename if not present or incorrect
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
        # Ensure 'Inst Code' is treated as string if it exists
        if 'Inst Code' in final_combined_df.columns:
            final_combined_df['Inst Code'] = final_combined_df['Inst Code'].astype(str)
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

    filtered_df = final_combined_df[
        (final_combined_df['Year'] == int(year_preference)) &
        (final_combined_df['Phase'] == phase_preference) &
        (final_combined_df[rank_column] >= rank)
    ].copy()

    filtered_df.sort_values(by=rank_column, ascending=True, inplace=True)

    # Ensure 'ClosingRank' column exists for consistent frontend display
    if 'ClosingRank' not in filtered_df.columns:
        filtered_df['ClosingRank'] = filtered_df[rank_column]

    # Add 'category' and 'gender' columns if they don't exist, for frontend display
    if 'category' not in filtered_df.columns:
        filtered_df['category'] = category
    if 'gender' not in filtered_df.columns:
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

