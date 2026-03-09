from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

MODEL_DIR = Path("ml/artifacts")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def export_training_data(csv_path: str = "ml/artifacts/training_events.csv") -> str:
    df = pd.DataFrame(
        [
            {"width": 150, "height": 90, "confidence": 0.95, "target": 1},
            {"width": 130, "height": 85, "confidence": 0.90, "target": 1},
            {"width": 80, "height": 60, "confidence": 0.51, "target": 0},
            {"width": 70, "height": 50, "confidence": 0.43, "target": 0},
        ]
    )
    df.to_csv(csv_path, index=False)
    return csv_path


def retrain_baseline(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)
    X = df[["width", "height", "confidence"]]
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
    model = DummyClassifier(strategy="most_frequent")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    metrics = {"accuracy": float(accuracy_score(y_test, preds)), "rows": int(len(df))}
    (MODEL_DIR / "metrics.json").write_text(str(metrics))
    return metrics


if __name__ == "__main__":
    csv = export_training_data()
    print(retrain_baseline(csv))
