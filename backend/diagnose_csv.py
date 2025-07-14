import os
import chardet
import pandas as pd

DATA_DIR = 'DATA'
filename_to_diagnose = '2024_Phase1.csv' # We'll start with this one
filepath = os.path.join(DATA_DIR, filename_to_diagnose)

print(f"--- Diagnosing: {filepath} ---")

if not os.path.exists(filepath):
    print(f"Error: File not found at {filepath}. Please ensure the file exists and the path is correct.")
else:
    # 1. Detect Encoding
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read(100000) # Read up to 100KB to detect encoding
        detection = chardet.detect(raw_data)
        detected_encoding = detection['encoding']
        confidence = detection['confidence']
        print(f"\nEncoding detected: {detected_encoding} with confidence {confidence:.2f}")
    except Exception as e:
        print(f"Error detecting encoding: {e}")
        detected_encoding = None

    # 2. Try reading with detected encoding and common alternatives
    encodings_to_try = [detected_encoding, 'utf-8', 'latin1', 'cp1252']
    delimiters_to_try = [',', ';', '\t'] # Comma, Semicolon, Tab

    print("\n--- Attempting to read with various parameters ---")
    read_success = False
    for enc in encodings_to_try:
        if not enc: continue # Skip if encoding detection failed
        for delim in delimiters_to_try:
            print(f"Trying encoding='{enc}', delimiter='{delim}'...")
            try:
                # Try reading, skipping first few rows
                for skip_rows_count in [0, 1, 2, 3]: # Try skipping 0, 1, 2, or 3 rows
                    try:
                        df_test = pd.read_csv(filepath, encoding=enc, delimiter=delim, skiprows=skip_rows_count, nrows=5) # Read only 5 rows for test
                        print(f"  SUCCESS! Read with encoding='{enc}', delimiter='{delim}', skiprows={skip_rows_count}.")
                        print("  First 5 rows (head):\n", df_test.head())
                        print("  Columns detected:\n", df_test.columns.tolist())
                        read_success = True
                        break # Stop trying parameters if successful
                    except pd.errors.ParserError as pe:
                        # print(f"    ParserError with skiprows={skip_rows_count}: {pe}")
                        continue # Try next skiprows
                    except UnicodeDecodeError as ude:
                        # print(f"    UnicodeDecodeError with skiprows={skip_rows_count}: {ude}")
                        continue # Try next skiprows
                    except Exception as e:
                        # print(f"    Other error with skiprows={skip_rows_count}: {e}")
                        continue # Try next skiprows
                if read_success: break
            except Exception:
                continue
        if read_success: break

    if not read_success:
        print("\n--- Failed to read with common CSV parameters. Trying raw line read. ---")
        try:
            # 3. Read raw lines if Pandas fails completely
            with open(filepath, 'rb') as f:
                print("\nFirst 10 raw bytes:", f.read(10))
                f.seek(0) # Go back to beginning
                print("\nFirst 10 lines (raw bytes):")
                for i, line in enumerate(f):
                    if i >= 10: break
                    print(f"Line {i+1}: {line}")
        except Exception as e:
            print(f"Error reading raw bytes: {e}")

print("\n--- Diagnosis Complete ---")