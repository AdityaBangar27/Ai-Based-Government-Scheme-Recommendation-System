import os
import joblib
import pandas as pd
from flask import Flask, render_template, request
from preprocessing import build_inference_dataframe

app = Flask(__name__)

model = None
schemes_df = None
choices = {}


def initialize_app():
    """Loads ML artifacts and sets up choice lists."""
    global model, schemes_df, choices

    model_dir = "models"
    best_model_path = os.path.join(model_dir, "best_rf_model.pkl")
    base_model_path = os.path.join(model_dir, "rf_model.pkl")

    if os.path.exists(best_model_path):
        print("Flask App: Loading tuned model (best_rf_model.pkl)...")
        model = joblib.load(best_model_path)
    elif os.path.exists(base_model_path):
        print("Flask App: Loading base model (rf_model.pkl)...")
        model = joblib.load(base_model_path)
    else:
        raise FileNotFoundError("Model file not found. Train the model before running the app.")

    if os.path.exists("schemes.csv"):
        schemes_df = pd.read_csv("schemes.csv")
        print(f"Flask App: Loaded {len(schemes_df)} scheme records for metadata queries.")
    else:
        raise FileNotFoundError("schemes.csv not found in root directory.")

    if os.path.exists("cleaned_users.csv"):
        users_df = pd.read_csv("cleaned_users.csv")
    else:
        users_df = pd.DataFrame()

    ui_fields = [
        "Gender", "State", "Education", "Occupation", "Category",
        "Disability_Status", "Employment_Status", "Rural_Urban",
        "Marital_Status", "Farmer_Status", "Student_Status", "BPL_Status", "Minority_Status"
    ]
    for col in ui_fields:
        if col in users_df.columns:
            values = users_df[col].astype(str).str.lower().dropna().unique().tolist()
            choices[col] = sorted(values)
        else:
            choices[col] = []


@app.route("/", methods=["GET", "POST"])
def index():
    global model, schemes_df, choices

    recommendations = []
    form_values = {}

    if request.method == "POST":
        age = int(request.form.get("Age", 35))
        gender = request.form.get("Gender", "female")
        income = int(request.form.get("Income", 0))
        state = request.form.get("State", "maharashtra")
        education = request.form.get("Education", "12th")
        occupation = request.form.get("Occupation", "farmer")
        category = request.form.get("Category", "obc")
        employment = request.form.get("Employment_Status", "self-employed")
        r_u = request.form.get("Rural_Urban", "rural")
        marital = request.form.get("Marital_Status", "married")
        farmer = request.form.get("Farmer_Status", "no")
        student = request.form.get("Student_Status", "no")
        disability = request.form.get("Disability_Status", "no")
        bpl = request.form.get("BPL_Status", "no")
        minority = request.form.get("Minority_Status", "no")

        form_values = {
            "Age": age,
            "Gender": gender,
            "Income": income,
            "State": state,
            "Education": education,
            "Occupation": occupation,
            "Category": category,
            "Employment_Status": employment,
            "Rural_Urban": r_u,
            "Marital_Status": marital,
            "Farmer_Status": farmer,
            "Student_Status": student,
            "Disability_Status": disability,
            "BPL_Status": bpl,
            "Minority_Status": minority,
        }

        try:
            input_data = {
                "Age": age,
                "Income": income,
                "Gender": gender,
                "Occupation": occupation,
                "Category": category,
            }
            input_df = build_inference_dataframe(input_data)
            predicted_proba = model.predict_proba(input_df)[0]
            class_labels = model.classes_
            top_indices = predicted_proba.argsort()[::-1][:5]

            for idx in top_indices:
                scheme_name = class_labels[idx]
                prob = float(predicted_proba[idx])
                match_row = schemes_df[schemes_df["Scheme_Name"].str.lower() == str(scheme_name).lower()]

                if not match_row.empty:
                    scheme_details = match_row.iloc[0]
                    description = scheme_details.get("Description", "No description available.")
                    beneficiary = scheme_details.get("Beneficiary", "All Beneficiaries")
                    benefits = scheme_details.get("Benefits", "Financial/General assistance.")
                    documents = scheme_details.get("Required_Documents", "Aadhaar, income certificate, and general ID.")
                    website = scheme_details.get("Official_Website", "#")
                else:
                    description = "No description available."
                    beneficiary = "All Beneficiaries"
                    benefits = "Financial/General assistance."
                    documents = "Aadhaar, income certificate, and general ID."
                    website = "#"

                recommendations.append({
                    "name": scheme_name,
                    "score": prob,
                    "description": description,
                    "beneficiary": beneficiary,
                    "benefits": benefits,
                    "documents": documents,
                    "website": website,
                })
        except Exception as e:
            recommendations = [{"name": f"Error: {e}", "score": 0, "description": "", "beneficiary": "", "benefits": "", "documents": "", "website": "#"}]

    return render_template("index.html", choices=choices, recommendations=recommendations, form_values=form_values)


if __name__ == "__main__":
    initialize_app()
    app.run(debug=True, port=5000)
