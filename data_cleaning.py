import os
import pandas as pd
import numpy as np

def clean_data():
    """Loads, cleans, and standardizes users.csv and schemes.csv datasets."""
    print("=== Starting Data Cleaning Phase ===")
    
    # 1. Load Datasets
    try:
        users = pd.read_csv("users.csv")
        schemes = pd.read_csv("schemes.csv")
        print("Raw datasets loaded successfully.")
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return
    
    # Display initial shapes
    print(f"Initial Users shape: {users.shape}")
    print(f"Initial Schemes shape: {schemes.shape}")
    
    # 2. Check and Remove Duplicates
    users_duplicates = users.duplicated().sum()
    schemes_duplicates = schemes.duplicated().sum()
    print(f"Duplicate rows in users: {users_duplicates}")
    print(f"Duplicate rows in schemes: {schemes_duplicates}")
    
    if users_duplicates > 0:
        users = users.drop_duplicates()
    if schemes_duplicates > 0:
        schemes = schemes.drop_duplicates()
        
    # 3. Check and Handle Missing Values
    print("\nMissing values in Users:")
    print(users.isnull().sum())
    print("\nMissing values in Schemes:")
    print(schemes.isnull().sum())
    
    # Fill missing values if any exist (safety check)
    users = users.fillna("none")
    schemes = schemes.fillna("none")
    
    # 4. Standardize Text Columns (lowercase & strip whitespace)
    # Define text/categorical columns for users
    user_text_cols = [
        "Gender", "State", "District", "Education", "Occupation", 
        "Category", "Disability_Status", "Rural_Urban", "Employment_Status", 
        "Marital_Status", "Farmer_Status", "Student_Status", "BPL_Status", "Minority_Status"
    ]
    
    for col in user_text_cols:
        if col in users.columns:
            users[col] = users[col].astype(str).str.strip().str.lower()
            
    # Define text/categorical columns for schemes
    scheme_text_cols = [
        "Beneficiary", "State", "Gender", "Education", "Occupation", "Category", 
        "Disability_Status", "Rural_Urban", "Employment_Status", "Marital_Status", 
        "Farmer_Status", "Student_Status", "BPL_Status", "Minority_Status"
    ]
    
    for col in scheme_text_cols:
        if col in schemes.columns:
            schemes[col] = schemes[col].astype(str).str.strip().str.lower()
            
    # 5. Clean Numeric Columns and handle "No Limit" / "no limit"
    # Convert Income_Limit in schemes: replace 'no limit' or '999999999' with float/int
    if "Income_Limit" in schemes.columns:
        schemes["Income_Limit"] = schemes["Income_Limit"].astype(str).str.strip().str.lower()
        schemes["Income_Limit"] = schemes["Income_Limit"].replace("no limit", "999999999")
        schemes["Income_Limit"] = pd.to_numeric(schemes["Income_Limit"], errors="coerce").fillna(999999999).astype(int)
        
    # For Min_Age, Max_Age
    for col in ["Min_Age", "Max_Age"]:
        if col in schemes.columns:
            schemes[col] = pd.to_numeric(schemes[col], errors="coerce").fillna(0).astype(int)
            
    # For User Age, Income, Annual_Family_Income
    for col in ["Age", "Income", "Annual_Family_Income"]:
        if col in users.columns:
            users[col] = pd.to_numeric(users[col], errors="coerce").fillna(0).astype(int)
            
    # 6. Save Cleaned Datasets
    users.to_csv("cleaned_users.csv", index=False)
    schemes.to_csv("cleaned_schemes.csv", index=False)
    print("\nCleaned datasets saved successfully.")
    
    # 7. Display Summary Statistics
    print("\n=== Cleaned Users Shape ===")
    print(users.shape)
    print("\n=== Cleaned Schemes Shape ===")
    print(schemes.shape)
    
    print("\n=== Users Summary Statistics ===")
    print(users.describe())
    
    print("\n=== Schemes Summary Statistics ===")
    print(schemes.describe())

if __name__ == "__main__":
    clean_data()
