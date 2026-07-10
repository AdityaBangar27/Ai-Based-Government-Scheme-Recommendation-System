import os
import random
import pandas as pd
import numpy as np

# Education level hierarchy for checking eligibility
education_hierarchy = {
    "illiterate": 0,
    "primary": 1,
    "10th": 2,
    "12th": 3,
    "graduate": 4,
    "post graduate": 5
}

def is_eligible(user, scheme):
    """Evaluates if a user is eligible for a specific scheme based on rules."""
    
    # 1. Age check
    if not (scheme["Min_Age"] <= user["Age"] <= scheme["Max_Age"]):
        return False
        
    # 2. Income limit check (Annual Family Income <= Scheme Income Limit)
    if user["Annual_Family_Income"] > scheme["Income_Limit"]:
        return False
        
    # 3. Gender check
    if scheme["Gender"] != "all" and scheme["Gender"] != user["Gender"]:
        return False
        
    # 4. State check
    if scheme["State"] != "all" and scheme["State"] != user["State"]:
        return False
        
    # 5. Education check
    # If scheme requires a specific education level, user must meet or exceed it
    sch_edu = scheme["Education"]
    usr_edu = user["Education"]
    if sch_edu != "all":
        # Get hierarchy values, default to 0 if not found
        sch_val = education_hierarchy.get(sch_edu, 0)
        usr_val = education_hierarchy.get(usr_edu, 0)
        if usr_val < sch_val:
            return False
            
    # 6. Occupation check
    if scheme["Occupation"] != "all" and scheme["Occupation"] != user["Occupation"]:
        return False
        
    # 7. Category check
    # Check if scheme lists a specific category (sc, st, obc, ews, general)
    # Special rule: If scheme is Stand-Up India, it supports SC/ST or Female.
    if scheme["Scheme_Name"] == "stand-up india scheme":
        if not (user["Category"] in ["sc", "st"] or user["Gender"] == "female"):
            return False
    elif scheme["Category"] != "all" and scheme["Category"] != user["Category"]:
        return False
        
    # 8. Disability Status check
    if scheme["Disability_Status"] == "yes" and user["Disability_Status"] != "yes":
        return False
        
    # 9. Rural / Urban check
    if scheme["Rural_Urban"] != "all" and scheme["Rural_Urban"] != user["Rural_Urban"]:
        return False
        
    # 10. Employment Status check
    if scheme["Employment_Status"] != "all" and scheme["Employment_Status"] != user["Employment_Status"]:
        return False
        
    # 11. Farmer Status check
    if scheme["Farmer_Status"] == "yes" and user["Farmer_Status"] != "yes":
        return False
        
    # 12. Student Status check
    if scheme["Student_Status"] == "yes" and user["Student_Status"] != "yes":
        return False
        
    # 13. BPL Status check
    if scheme["BPL_Status"] == "yes" and user["BPL_Status"] != "yes":
        return False
        
    # 14. Minority Status check
    if scheme["Minority_Status"] == "yes" and user["Minority_Status"] != "yes":
        return False
        
    # 15. Marital Status check
    if scheme["Marital_Status"] != "all" and scheme["Marital_Status"] != user["Marital_Status"]:
        return False
        
    return True

EXTERNAL_TRAINING_DATA_PATH = r"E:\New folder\AI_Scheme_Recommendation\training_dataset.csv"


def generate_training_dataset():
    """Generates the training dataset by matching users and schemes."""
    print("=== Starting Eligibility Matching Engine ===")
    
    if os.path.exists(EXTERNAL_TRAINING_DATA_PATH):
        print(f"Using attached training dataset at {EXTERNAL_TRAINING_DATA_PATH}")
        try:
            training_df = pd.read_csv(EXTERNAL_TRAINING_DATA_PATH)
            training_df.to_csv("training_dataset.csv", index=False)
            print("Copied attached training dataset into workspace training_dataset.csv")
            print(f"Loaded attached dataset with shape: {training_df.shape}")
        except Exception as e:
            print(f"Error loading external training dataset: {e}")
        return
    
    # Load cleaned datasets
    try:
        users = pd.read_csv("cleaned_users.csv")
        schemes = pd.read_csv("cleaned_schemes.csv")
        print("Cleaned datasets loaded successfully.")
    except Exception as e:
        print(f"Error loading cleaned CSV files: {e}")
        return
        
    training_records = []
    
    # Match every user with every scheme
    for _, user in users.iterrows():
        for _, scheme in schemes.iterrows():
            if is_eligible(user, scheme):
                # Only the five approved ML input features are included in the training dataset.
                training_records.append({
                    "Age": user["Age"],
                    "Income": user["Income"],
                    "Occupation": user["Occupation"],
                    "Gender": user["Gender"],
                    "Category": user["Category"],
                    "Recommended_Scheme": scheme["Scheme_Name"]  # Store scheme name as target
                })
                
    # Create DataFrame
    training_df = pd.DataFrame(training_records)
    
    print(f"Total eligible pairings matched: {len(training_df)}")
    
    # Remove duplicates
    initial_len = len(training_df)
    training_df = training_df.drop_duplicates()
    final_len = len(training_df)
    print(f"Removed {initial_len - final_len} duplicate records.")

    # Ensure at least 100,000 rows for a single target scheme
    target_scheme = "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)"
    if target_scheme not in training_df["Recommended_Scheme"].unique():
        target_scheme = training_df["Recommended_Scheme"].value_counts().idxmax()
        print(f"Target scheme not found. Using most frequent scheme: {target_scheme}")

    target_rows = training_df[training_df["Recommended_Scheme"] == target_scheme].copy()
    target_count = len(target_rows)
    additional_needed = max(0, 100000 - target_count)
    if additional_needed > 0 and not target_rows.empty:
        augmented_rows = []
        seen = set(
            tuple(row) for row in target_rows[["Age", "Income", "Occupation", "Gender", "Category", "Recommended_Scheme"]].itertuples(index=False, name=None)
        )
        scheme_info = None
        if os.path.exists("cleaned_schemes.csv"):
            schemes = pd.read_csv("cleaned_schemes.csv")
            row = schemes[schemes["Scheme_Name"] == target_scheme]
            if not row.empty:
                scheme_info = row.iloc[0]

        min_age = int(scheme_info["Min_Age"]) if scheme_info is not None else int(target_rows["Age"].min())
        max_age = int(scheme_info["Max_Age"]) if scheme_info is not None else int(target_rows["Age"].max())
        income_limit = int(scheme_info["Income_Limit"]) if scheme_info is not None else int(target_rows["Income"].max())

        current = target_rows.reset_index(drop=True)
        i = 0
        while len(augmented_rows) < additional_needed:
            base = current.iloc[i % len(current)].copy()
            age = int(base["Age"] + random.choice([-2, -1, 0, 1, 2]))
            age = max(min_age, min(max_age, age))
            income = int(base["Income"] + random.choice([-500, -250, 0, 250, 500]))
            income = max(0, min(income_limit, income))
            record = {
                "Age": age,
                "Income": income,
                "Occupation": base["Occupation"],
                "Gender": base["Gender"],
                "Category": base["Category"],
                "Recommended_Scheme": base["Recommended_Scheme"]
            }
            tup = tuple(record.values())
            if tup not in seen:
                seen.add(tup)
                augmented_rows.append(record)
            i += 1
            if i > additional_needed * 20:
                break

        if augmented_rows:
            augmented_df = pd.DataFrame(augmented_rows)
            training_df = pd.concat([training_df, augmented_df], ignore_index=True)
            print(f"Augmented {len(augmented_df)} additional rows for scheme '{target_scheme}'.")
        else:
            print(f"Warning: Unable to augment rows for {target_scheme}; using existing count {target_count}.")

    final_len = len(training_df)
    training_df.to_csv("training_dataset.csv", index=False)
    print(f"Saved {final_len} training records to training_dataset.csv")
    
    # Display sample records
    print("\nSample records from training dataset:")
    print(training_df.head(5))

if __name__ == "__main__":
    generate_training_dataset()
