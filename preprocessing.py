import pandas as pd

TARGET_COLUMN = "Recommended_Scheme"
NUMERIC_FEATURES = ["Age", "Income"]
CATEGORICAL_FEATURES = ["Gender", "Occupation", "Category"]
ML_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def select_ml_features(df: pd.DataFrame) -> pd.DataFrame:
    """Returns only the approved ML features and target from a dataset."""
    required_columns = ML_FEATURES + [TARGET_COLUMN]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required ML columns: {missing}")
    return df[required_columns].copy()


def build_inference_dataframe(features: dict) -> pd.DataFrame:
    """Builds a DataFrame for model inference using approved features."""
    missing = [key for key in ML_FEATURES if key not in features]
    if missing:
        raise ValueError(f"Missing required inference inputs: {missing}")
    return pd.DataFrame([{key: features[key] for key in ML_FEATURES}])


def is_model_compatible(model, expected_features=None) -> bool:
    """Checks whether a loaded model was trained with the expected feature names."""
    if expected_features is None:
        expected_features = ML_FEATURES

    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_) == list(expected_features)

    if hasattr(model, "n_features_in_"):
        return model.n_features_in_ == len(expected_features)

    return True
