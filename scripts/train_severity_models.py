import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
import xgboost as xgb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "indian_roads_dataset.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def train_and_evaluate():
    print(f"Loading real Indian accident dataset from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} records.")

    # Target variable normalization: 'minor', 'major', 'fatal'
    df['accident_severity'] = df['accident_severity'].str.lower().str.strip()
    valid_classes = ['minor', 'major', 'fatal']
    df = df[df['accident_severity'].isin(valid_classes)].copy()
    print("Class distribution:")
    print(df['accident_severity'].value_counts())

    # Features selection
    categorical_features = ['road_type', 'weather', 'visibility', 'traffic_density', 'traffic_signal', 'is_weekend', 'is_peak_hour']
    numerical_features = ['hour', 'lanes', 'temperature', 'vehicles_involved']

    # Impute missing or clean
    for col in categorical_features:
        df[col] = df[col].astype(str).str.lower().fillna('unknown')
    for col in numerical_features:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())

    X = df[categorical_features + numerical_features]
    y = df['accident_severity']

    # Mapping target classes: minor: 0, major: 1, fatal: 2
    label_map = {'minor': 0, 'major': 1, 'fatal': 2}
    inv_label_map = {0: 'minor', 1: 'major', 2: 'fatal'}
    y_encoded = y.map(label_map)

    # Train-test split (80/20) with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
            ('num', StandardScaler(), numerical_features)
        ]
    )

    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    feature_names = preprocessor.get_feature_names_out()

    print(f"\nPreprocessed feature vector size: {X_train_proc.shape[1]}")

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=150, max_depth=12, class_weight='balanced', random_state=42, n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42
        ),
        "XGBoost": xgb.XGBClassifier(
            n_estimators=150, max_depth=5, learning_rate=0.08, eval_metric='mlogloss', random_state=42
        )
    }

    results = {}
    best_model_name = None
    best_f1 = -1

    for name, model in models.items():
        print(f"\n================ Training {name} ================")
        model.fit(X_train_proc, y_train)
        y_pred = model.predict(X_test_proc)
        y_prob = model.predict_proba(X_test_proc)

        acc = float(accuracy_score(y_test, y_pred))
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division=0)
        p_wt, r_wt, f1_wt, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()
        report = classification_report(y_test, y_pred, target_names=['minor', 'major', 'fatal'], output_dict=True)

        results[name] = {
            "accuracy": acc,
            "macro_f1": float(f1_macro),
            "macro_precision": float(p_macro),
            "macro_recall": float(r_macro),
            "weighted_f1": float(f1_wt),
            "confusion_matrix": cm,
            "classification_report": report
        }

        print(f"{name} Metrics:")
        print(f"  Accuracy:         {acc:.4f}")
        print(f"  Macro Precision:  {p_macro:.4f}")
        print(f"  Macro Recall:     {r_macro:.4f}")
        print(f"  Macro F1:         {f1_macro:.4f}")
        print(f"  Weighted F1:      {f1_wt:.4f}")
        print(f"  Confusion Matrix (Minor, Major, Fatal):\n{np.array(cm)}")

        if f1_macro > best_f1:
            best_f1 = f1_macro
            best_model_name = name

    print(f"\nSelected Best Model by Macro F1: {best_model_name} (F1: {best_f1:.4f})")
    best_model = models[best_model_name]

    # Save artifacts
    joblib.dump(best_model, os.path.join(MODELS_DIR, "severity_model.joblib"))
    joblib.dump(preprocessor, os.path.join(MODELS_DIR, "preprocessor.joblib"))
    with open(os.path.join(MODELS_DIR, "model_metadata.json"), "w") as f:
        json.dump({
            "best_model": best_model_name,
            "label_map": label_map,
            "inv_label_map": inv_label_map,
            "feature_names": list(feature_names),
            "categorical_features": categorical_features,
            "numerical_features": numerical_features,
            "metrics": results
        }, f, indent=2)

    print("\nSaved artifacts to models/ directory successfully.")

if __name__ == "__main__":
    train_and_evaluate()
