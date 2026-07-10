import os
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
)
from sklearn.preprocessing import label_binarize
from preprocessing import select_ml_features, TARGET_COLUMN, is_model_compatible

def load_compatible_model(model_dir):
    candidate_paths = []
    best_model_path = os.path.join(model_dir, "best_rf_model.pkl")
    base_model_path = os.path.join(model_dir, "rf_model.pkl")

    if os.path.exists(best_model_path):
        candidate_paths.append(best_model_path)
    if os.path.exists(base_model_path):
        candidate_paths.append(base_model_path)

    if not candidate_paths:
        raise FileNotFoundError("No trained model found in models/.")

    for model_path in candidate_paths:
        model = joblib.load(model_path)
        if is_model_compatible(model):
            print(f"Loading compatible model ({os.path.basename(model_path)})...")
            return model
        print(f"Skipping incompatible model file: {os.path.basename(model_path)}")

    raise ValueError("No compatible trained model found. Rebuild the model using train_random_forest.py or hyperparameter_tuning.py.")


def evaluate():
    """Performs model evaluation and saves visualization plots using pure matplotlib."""
    print("=== Starting Model Evaluation Phase ===")

    if not os.path.exists("training_dataset.csv"):
        print("Error: training_dataset.csv not found.")
        return

    df = pd.read_csv("training_dataset.csv")
    df = select_ml_features(df)

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN].astype(str)

    label_counts = y.value_counts()
    if label_counts.min() < 2:
        print(
            "Warning: Some scheme labels appear only once. "
            "Stratified split is disabled for evaluation."
        )
        stratify_value = None
    else:
        stratify_value = y

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=stratify_value
    )

    model_dir = "models"
    try:
        model = load_compatible_model(model_dir)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    print("\n=== Model Metrics ===")
    print(f"Accuracy:  {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall:    {recall * 100:.2f}%")
    print(f"F1 Score:  {f1 * 100:.2f}%")

    report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True, zero_division=0)).transpose()
    print("\n=== Classification Report (Top 10 Classes by Support) ===")
    if "support" in report_df.columns:
        print(report_df.sort_values(by="support", ascending=False).head(10))
    else:
        print(report_df.head(10))

    os.makedirs("graphs", exist_ok=True)
    with open("graphs/classification_report.txt", "w") as f:
        f.write(classification_report(y_test, y_pred, output_dict=False, zero_division=0))
    print("Saved complete classification report to graphs/classification_report.txt")

    print("\nPlotting Confusion Matrix...")
    cm = confusion_matrix(y_test, y_pred)
    top_class_indices = np.argsort(np.sum(cm, axis=1))[::-1][:15]
    cm_subset = cm[np.ix_(top_class_indices, top_class_indices)]
    top_scheme_names = [model.classes_[i] for i in top_class_indices]

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(cm_subset, cmap="Blues", interpolation="nearest")

    for r in range(cm_subset.shape[0]):
        for c in range(cm_subset.shape[1]):
            val = cm_subset[r, c]
            ax.text(c, r, f"{val}", va="center", ha="center",
                    color="white" if val > (cm_subset.max() / 2) else "black")

    ax.set_xticks(np.arange(len(top_scheme_names)))
    ax.set_yticks(np.arange(len(top_scheme_names)))
    ax.set_xticklabels(top_scheme_names, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(top_scheme_names, fontsize=9)

    plt.title("Confusion Matrix (Top 15 Schemes by Support)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Predicted Label", fontsize=11, labelpad=10)
    plt.ylabel("True Label", fontsize=11, labelpad=10)
    fig.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()
    plt.savefig("graphs/confusion_matrix.png", dpi=300)
    plt.close()
    print("Saved Confusion Matrix plot to graphs/confusion_matrix.png")

    print("Plotting Feature Importances...")
    try:
        importances = model.named_steps["classifier"].feature_importances_
        feature_names = model.named_steps["preprocessor"].get_feature_names_out()
        feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=True)

        plt.figure(figsize=(10, 6))
        cmap = plt.get_cmap("viridis")
        colors = [cmap(val) for val in np.linspace(0.2, 0.8, len(feat_imp))]
        feat_imp.plot(kind="barh", color=colors)
        plt.title("Feature Importance in Scheme Recommendation Model", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel("Relative Importance", fontsize=11)
        plt.ylabel("Features", fontsize=11)
        plt.tight_layout()
        plt.savefig("graphs/feature_importance.png", dpi=300)
        plt.close()
        print("Saved Feature Importance plot to graphs/feature_importance.png")
    except Exception as imp_err:
        print(f"Unable to compute feature importance: {imp_err}")

    print("Plotting ROC Curve...")
    model_classes = model.classes_
    y_test_bin = label_binarize(y_test, classes=model_classes)

    plt.figure(figsize=(10, 8))
    fpr, tpr, _ = roc_curve(y_test_bin.ravel(), y_prob.ravel())
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"Micro-average ROC (AUC = {roc_auc:.2f})", color="deeppink", linestyle=":", linewidth=4)

    top_3_idx = top_class_indices[:3]
    colors_cycle = ["blue", "green", "red"]
    for i, idx in enumerate(top_3_idx):
        class_prob_idx = idx
        fpr_c, tpr_c, _ = roc_curve(y_test_bin[:, class_prob_idx], y_prob[:, class_prob_idx])
        auc_c = auc(fpr_c, tpr_c)
        short_name = str(model_classes[idx])[:30] + "..." if len(str(model_classes[idx])) > 30 else str(model_classes[idx])
        plt.plot(fpr_c, tpr_c, label=f"ROC of {short_name} (AUC = {auc_c:.2f})", color=colors_cycle[i], linewidth=2)

    plt.plot([0, 1], [0, 1], "k--", linewidth=1.5)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate", fontsize=11)
    plt.ylabel("True Positive Rate", fontsize=11)
    plt.title("Receiver Operating Characteristic (ROC) - Multi-Class", fontsize=14, fontweight="bold", pad=15)
    plt.legend(loc="lower right", fontsize=10)
    plt.tight_layout()
    plt.savefig("graphs/roc_curve.png", dpi=300)
    plt.close()
    print("Saved ROC Curve plot to graphs/roc_curve.png")
    print("=== Evaluation Phase Completed ===")


if __name__ == "__main__":
    evaluate()
