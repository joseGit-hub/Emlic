import pandas as pd
import sqlite3
import re
import os
import pytz
from datetime import datetime

# Define where files go
DB_PATH = 'data-cleaned/leads_manager.db'
EXPORT_PATH = 'data-cleaned/crm_upload_ready.csv'

def validate_email(email):
    """
    Checks if an email follows a standard format.
    Returns 'Valid' or 'Invalid'.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, str(email)):
        return "Valid"
    return "Invalid"

def clean_and_store(file_path, do_dedup, do_timezone, do_report):
    """
    This is the main engine that cleans the data and saves it to the database.
    """
    if not os.path.exists(file_path):
        return f"Wait, I can't find the file at: {file_path}"

    try:
        # Load the file and automatically figure out if it uses commas or semicolons
        df = pd.read_csv(file_path, sep=None, engine='python')
        
        # Clean up the headers so there aren't any accidental spaces causing errors
        df.columns = [str(c).strip() for c in df.columns]

        # Safety check: if there are two columns with the same name, we drop the extras
        # This prevents the 'duplicate column name' error when saving to SQL
        df = df.loc[:, ~df.columns.duplicated()]

        # Handle the Name Column
        # Instead of just taking the first column, we look for 'First Name' or 'Full Name'
        name_options = ['Full Name', 'First Name', 'Name', 'Customer Name']
        found_name_col = next((c for c in df.columns if c in name_options), None)

        if found_name_col:
            # If we find a specific name column, we use it
            df['Full Name'] = df[found_name_col].astype(str).str.strip().str.title()
        else:
            # Fallback: find the first column that actually contains text (not just numbers)
            # This prevents the Index/ID column from being used as the name
            for col in df.columns:
                if not pd.to_numeric(df[col], errors='coerce').notnull().all():
                    df['Full Name'] = df[col].astype(str).str.strip().str.title()
                    break

        # Handle the Email Column
        # If 'Email' isn't a header, we check the second column
        if 'Email' not in df.columns:
            if len(df.columns) > 1:
                df.rename(columns={df.columns[1]: 'Email'}, inplace=True)
            else:
                return "I couldn't find an Email column to work with."

        # Clean up emails and check if they are valid
        df['Email'] = df['Email'].astype(str).str.strip().str.lower()
        df['Email_Status'] = df['Email'].apply(validate_email)

        # Remove duplicates if the user asked for it
        if do_dedup:
            df = df.drop_duplicates(subset=['Email'], keep='first')

        # Add local time info if the user wants to know when to contact leads
        if do_timezone:
            location_headers = ['City', 'Location', 'Town']
            loc_col = next((c for c in df.columns if c in location_headers or 'city' in c.lower()), None)
            
            if loc_col:
                # Common timezones for quick lookups
                tz_map = {
                    'Manila': 'Asia/Manila', 
                    'New York': 'America/New_York', 
                    'London': 'Europe/London', 
                    'Dubai': 'Asia/Dubai'
                }
                
                def get_local_time(city):
                    city_name = str(city).strip().title()
                    if city_name in tz_map:
                        zone = pytz.timezone(tz_map[city_name])
                        return datetime.now(zone).strftime('%I:%M %p')
                    return "Unknown"
                
                df['Lead_Local_Time'] = df[loc_col].apply(get_local_time)

        # Save everything to our SQLite database
        # 'replace' ensures we overwrite the old data so the preview updates correctly
        conn = sqlite3.connect(DB_PATH)
        df.to_sql('automated_leads', conn, if_exists='replace', index=False)
        
        # Also save a CSV version for the user to download
        df.to_csv(EXPORT_PATH, index=False)
        conn.close()

        return "Success"

    except Exception as e:
        return f"Something went wrong during automation: {str(e)}"