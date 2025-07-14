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
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'DATA') 
    
    print(f"DEBUG: Current working directory: {os.getcwd()}")
    print(f"DEBUG: app.py directory: {base_dir}")
    print(f"Attempting to load data from: {data_dir}")
    
    try:
        print(f"DEBUG: Contents of {base_dir}: {os.listdir(base_dir)}")
        if os.path.exists(data_dir):
            print(f"DEBUG: Contents of {data_dir}: {os.listdir(data_dir)}")
        else:
            print(f"DEBUG: Data directory '{data_dir}' does not exist during os.listdir check.")
    except Exception as e:
        print(f"DEBUG: Could not list contents or access data_dir: {e}")

    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' does not exist. Please ensure it's in your GitHub repo and correctly capitalized ('DATA').")
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")
        
    all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]

    df_list = []
    print("Attempting to load data from CSVs...")
    for f_path in all_files:
        try:
            df = pd.read_csv(f_path, skiprows=[0])
            
            # --- CRITICAL FIX: Match CSV headers exactly, including newlines and spaces ---
            df.rename(columns={
                'Inst\n Code': 'Inst Code', # Fix for Inst Code
                'Institute Name': 'College Name',
                'Dist\nCode': 'District Code', # Fix for Dist Code
                'Co Education': 'Co Education', # This seems correct
                'College Type': 'College Type', # This seems correct
                'Year of Estab': 'Year of Establishment', # This seems correct
                'Branch Code': 'Branch Code', # This seems correct
                'Branch Name': 'Branch Name', # This seems correct
                'OC\nBOYS': 'OC BOYS', # Fix for OC BOYS
                'OC\nGIRLS': 'OC GIRLS', # Fix for OC GIRLS
                'BC_A\nBOYS': 'BC_A BOYS', # Fix for BC_A BOYS
                'BC_A\nGIRLS': 'BC_A GIRLS', # Fix for BC_A GIRLS
                'BC_B\nBOYS': 'BC_B BOYS', # Fix for BC_B BOYS
                'BC_B\nGIRLS': 'BC_B GIRLS', # Fix for BC_B GIRLS
                'BC_C\nBOYS': 'BC_C BOYS', # Fix for BC_C BOYS
                'BC_C\nGIRLS': 'BC_C GIRLS', # Fix for BC_C GIRLS
                'BC_D\nBOYS': 'BC_D BOYS', # Fix for BC_D BOYS
                'BC_D\nGIRLS': 'BC_D GIRLS', # Fix for BC_D GIRLS
                'BC_E\nBOYS': 'BC_E BOYS', # Fix for BC_E BOYS
                'BC_E\nGIRLS': 'BC_E GIRLS', # Fix for BC_E GIRLS
                'SC\nBOYS': 'SC BOYS', # Fix for SC BOYS
                'SC\nGIRLS': 'SC GIRLS', # Fix for SC GIRLS
                'ST\nBOYS': 'ST BOYS', # Fix for ST BOYS
                'ST\nGIRLS': 'ST GIRLS', # Fix for ST GIRLS
                'EWS\nGEN OU': 'EWS BOYS', # Mapping from CSV header 'EWS GEN OU'
                'EWS\nGIRLS OU': 'EWS GIRLS', # Mapping from CSV header 'EWS GIRLS OU'
                'Tuition Fee': 'Tuition Fee', # This seems correct
                'Affiliated To': 'Affiliated To', # This seems correct
            }, inplace=True)

            # Ensure 'Inst Code' column exists and is string type AFTER renaming
            if 'Inst Code' in df.columns:
                df['Inst Code'] = df['Inst Code'].astype(str)
            else:
                print(f"Warning: 'Inst Code' column still not found after renaming in {os.path.basename(f_path)}. Adding empty column.")
                df['Inst Code'] = '' 

            # Extract Year and Phase from filename
            filename = os.path.basename(f_path)
            if '2024' in filename:
                df['Year'] = 2024
            if 'Phase1' in filename:
                df['Phase'] = 'Phase 1'
            elif 'Phase2' in filename:
                df['Phase'] = 'Phase 2'
            elif 'FinalPhase' in filename:
                df['Phase'] = 'Final Phase'
            
            df_list.append(df)
            print(f"Loaded {os.path.basename(f_path)}")
        except Exception as e:
            print(f"Error loading {f_path}: {e}")

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

    # Construct the rank column name using the standardized format
    rank_column = f"{category} {gender}"

    # Filter the DataFrame based on user inputs
    if rank_column not in final_combined_df.columns:
        # This error should now be less likely if renaming is correct
        return jsonify({'error': f"Rank column '{rank_column}' not found in data after processing."}), 400

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
