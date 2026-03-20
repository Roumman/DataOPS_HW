"""Скрипт обучения модели при сборке Docker."""
from pathlib import Path

from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import mlflow.sklearn

diabetes = load_diabetes(scaled=False)
X, y = diabetes.data, diabetes.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestRegressor(n_estimators=100, random_state=42)),
])
pipeline.fit(X_train, y_train)

model_dir = Path(__file__).parent.parent / "mlapp" / "model"
model_dir.mkdir(parents=True, exist_ok=True)
mlflow.sklearn.save_model(pipeline, str(model_dir))
print(f"Model saved to {model_dir}")
