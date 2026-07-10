import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
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
                    random_state=42,
                    n_jobs=-1
                )
            )
        ]
    )


def tune_hyperparameters():
    """Tunes Random Forest hyperparameters using GridSearchCV."""
    print("=== Starting Hyperparameter Tuning Phase ===")

    if not os.path.exists("training_dataset.csv"):
        print("Error: training_dataset.csv not found! Run create_training_dataset.py first.")
        return

    df = pd.read_csv("training_dataset.csv")
    df = select_ml_features(df)
    print(f"Loaded training dataset with shape: {df.shape}")

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN].astype(str)

    label_counts = y.value_counts()
    if label_counts.min() < 2:
        print(
            "Warning: Some scheme labels appear only once. "
            "Stratified split is disabled for hyperparameter tuning."
        )
        stratify_value = None
    else:
        stratify_value = y

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=stratify_value
    )

    param_grid = {
        "classifier__n_estimators": [100, 200, 300],
        "classifier__max_depth": [10, 20, None],
        "classifier__min_samples_split": [2, 4],
        "classifier__min_samples_leaf": [1, 2],
        "classifier__class_weight": [None, "balanced_subsample"]
    }

    print("\nSetting up GridSearchCV with parameter grid:")
    print(param_grid)

    pipeline = build_pipeline()
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=3,
        scoring="accuracy",
        n_jobs=-1,
        verbose=1
    )

    print("\nFitting GridSearchCV (this may take a few moments)...")
    grid_search.fit(X_train, y_train)

    print("\n=== Tuning Results ===")
    print(f"Best Parameters: {grid_search.best_params_}")
    print(f"Best Cross-Validation Accuracy: {grid_search.best_score_ * 100:.2f}%")

    os.makedirs("models", exist_ok=True)
    best_model_path = os.path.join("models", "best_rf_model.pkl")
    joblib.dump(grid_search.best_estimator_, best_model_path)
    print(f"\nBest model successfully saved to {best_model_path}")


if __name__ == "__main__":
    tune_hyperparameters()
