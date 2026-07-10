import os
import joblib
import pandas as pd
import numpy as np
from preprocessing import build_inference_dataframe

def load_inference_artifacts():
    """Loads the model for inference."""
    model_dir = "models"
    best_model_path = os.path.join(model_dir, "best_rf_model.pkl")
    base_model_path = os.path.join(model_dir, "rf_model.pkl")
    
    if os.path.exists(best_model_path):
        model_path = best_model_path
    elif os.path.exists(base_model_path):
        model_path = base_model_path
    else:
        raise FileNotFoundError("No trained Random Forest model files found. Please train a model first.")
        
    return joblib.load(model_path)


def get_input(prompt, allowed_options=None, default=None):
    """Safely gets input from command line with options and defaults."""
    display_prompt = prompt
    if allowed_options:
        display_prompt += f" ({'/'.join(allowed_options)})"
    if default is not None:
        display_prompt += f" [Default: {default}]"
    display_prompt += ": "
    
    while True:
        user_in = input(display_prompt).strip().lower()
        if not user_in and default is not None:
            return str(default).lower()
        if allowed_options:
            if user_in in [opt.lower() for opt in allowed_options]:
                return user_in
            print(f"Invalid option. Please choose from: {', '.join(allowed_options)}")
        else:
            return user_in


def cli_predict():
    """Runs the CLI prediction interface."""
    print("=== AI-Based Government Scheme Recommendation CLI ===")
    
    try:
        model = load_inference_artifacts()
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Initialization Error: {e}")
        return

    genders = ["male", "female", "other"]
    occupations = ["farmer", "student", "salaried", "self-employed", "business", "unemployed"]
    categories = ["general", "obc", "sc", "st", "ews"]
    
    print("\nPlease enter user demographics (press Enter to accept defaults):")
    
    age_str = get_input("1. Age (18-80)", default="35")
    try:
        age = int(age_str)
    except ValueError:
        print("Invalid age. Using default: 35")
        age = 35
        
    gender = get_input("2. Gender", allowed_options=genders, default="female")
    
    income_str = get_input("3. Monthly Income (Rs.)", default="8000")
    try:
        income = int(income_str)
    except ValueError:
        print("Invalid income. Using default: 8000")
        income = 8000
        
    occupation = get_input("4. Occupation", allowed_options=occupations, default="farmer")
    category = get_input("5. Category", allowed_options=categories, default="obc")
    
    input_data = {
        "Age": age,
        "Income": income,
        "Gender": gender,
        "State": "maharashtra",
        "Education": "12th",
        "Occupation": occupation,
        "Category": category,
        "Disability_Status": "no",
        "Employment_Status": "self-employed",
        "Rural_Urban": "rural",
        "Marital_Status": "married",
        "Farmer_Status": "no",
        "Student_Status": "no",
        "BPL_Status": "no",
        "Minority_Status": "no"
    }
    
    input_df = build_inference_dataframe(input_data)
    
    print("\nPredicting recommended schemes...")
    probabilities = model.predict_proba(input_df)[0]
    model_classes = model.classes_
    
    sorted_indices = np.argsort(probabilities)[::-1]
    top_k = 5
    top_indices = sorted_indices[:top_k]
    
    print("\n================ TOP 5 RECOMMENDED SCHEMES ================")
    for rank, idx in enumerate(top_indices, start=1):
        scheme_name = model_classes[idx]
        prob = probabilities[idx]
        print(f"{rank}. {scheme_name} (Relevance Score: {prob * 100:.2f}%)")
    print("===========================================================")

if __name__ == "__main__":
    cli_predict()
