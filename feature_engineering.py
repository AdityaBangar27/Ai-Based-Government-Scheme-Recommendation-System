import os
import pandas as pd

EXTERNAL_TRAINING_DATA_PATH = r"E:\New folder\AI_Scheme_Recommendation\training_dataset.csv"


def run_feature_engineering():
    """Prepares the training dataset for model training and validation."""
    print("=== Starting Feature Engineering Phase ===")
    
    training_dataset_path = "training_dataset.csv"
    if os.path.exists(EXTERNAL_TRAINING_DATA_PATH):
        training_dataset_path = EXTERNAL_TRAINING_DATA_PATH
        print(f"Using attached external training dataset at {EXTERNAL_TRAINING_DATA_PATH}")
    elif not os.path.exists(training_dataset_path):
        print("Error: training_dataset.csv not found! Run create_training_dataset.py first.")
        return
        
    df = pd.read_csv(training_dataset_path)
    print(f"Loaded training dataset with shape: {df.shape}")

    required_columns = [
        "Age", "Gender", "Income", "State", "Education", "Occupation",
        "Category", "Disability_Status", "Employment_Status", "Rural_Urban",
        "Marital_Status", "Farmer_Status", "Student_Status", "BPL_Status",
        "Minority_Status", "Recommended_Scheme"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing required columns from training dataset: {missing_columns}")
        return

    df = df[required_columns].copy()
    df["Recommended_Scheme"] = df["Recommended_Scheme"].astype(str)

    os.makedirs("models", exist_ok=True)
    df.to_csv("encoded_training_dataset.csv", index=False)
    print("Saved encoded training dataset to encoded_training_dataset.csv")
    print("Note: preserved all raw ML feature columns for model pipeline training.")

    print("\nSample training records:")
    print(df.head(3))

if __name__ == "__main__":
    run_feature_engineering()
