import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from preprocessing import select_ml_features, TARGET_COLUMN, CATEGORICAL_FEATURES, NUMERIC_FEATURES


def build_preprocessor():
    return ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES
            ),
            ("num", "passthrough", NUMERIC_FEATURES)
        ],
        remainder="drop"
    )


def build_pipeline():
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=400,
                    max_depth=None,
                    min_samples_split=4,
                    min_samples_leaf=2,
                    class_weight="balanced_subsample",
                    n_jobs=-1,
                    random_state=42
                )
            )
        ]
    )


def train_model():
    """Trains a Random Forest pipeline on the full available dataset."""
    print("=== Starting Random Forest Training Phase ===")
    
    if not os.path.exists("training_dataset.csv"):
        print("Error: training_dataset.csv not found! Run create_training_dataset.py first.")
        return

    df = pd.read_csv("training_dataset.csv")
    df = select_ml_features(df)
    print(f"Loaded training dataset with shape: {df.shape}")
    
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN].astype(str)
    
    label_counts = y.value_counts()
    print(f"Unique target classes: {len(label_counts)}")
    if label_counts.min() < 2:
        print(
            "Warning: Some scheme labels appear only once. "
            "Stratified split is disabled to allow training to proceed."
        )
        stratify_value = None
    else:
        stratify_value = y

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=stratify_value
    )
    print(f"Training set shape: {X_train.shape}")
    print(f"Testing set shape: {X_test.shape}")
    
    model = build_pipeline()
    print("\nTraining Random Forest pipeline...")
    model.fit(X_train, y_train)
    print("Model training completed.")
    
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    
    print(f"\nTraining Accuracy: {train_acc * 100:.2f}%")
    print(f"Testing Accuracy: {test_acc * 100:.2f}%")
    
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "rf_model.pkl")
    joblib.dump(model, model_path)
    print(f"\nTrained pipeline serialized and saved to {model_path}")

if __name__ == "__main__":
    train_model()
