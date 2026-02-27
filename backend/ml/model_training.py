"""
model_training.py – Model Training, Comparison & Evaluation
SkillGenome X ML Pipeline
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, IsolationForest
from sklearn.model_selection import train_test_split as sklearn_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42) -> dict:
    """
    Split features and target into train/test sets.

    Args:
        X: Feature matrix.
        y: Target vector.
        test_size: Fraction of data for testing (default 0.2).
        random_state: Random seed for reproducibility.

    Returns:
        dict with keys: X_train, X_test, y_train, y_test
    """
    X_train, X_test, y_train, y_test = sklearn_split(X, y, test_size=test_size, random_state=random_state)

    print(f"[model_training] Split: {len(X_train)} train / {len(X_test)} test ({test_size*100:.0f}%)")
    return {
        'X_train': X_train, 'X_test': X_test,
        'y_train': y_train, 'y_test': y_test
    }


def compare_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    n_estimators: int = 100,
    learning_rate: float = 0.1,
    max_depth: int = 3,
    random_state: int = 42
) -> dict:
    """
    Train and evaluate multiple models, then select the best one.

    Models compared:
    - LinearRegression
    - RandomForestRegressor
    - GradientBoostingRegressor

    Selection criterion: highest R² score on test data.

    Returns:
        dict with: best_model_name, best_model, best_metrics, all_models (name→r2)
    """
    candidates = {
        'linear': LinearRegression(),
        'random_forest': RandomForestRegressor(
            n_estimators=n_estimators, max_depth=max_depth, random_state=random_state
        ),
        'gradient_boosting': GradientBoostingRegressor(
            n_estimators=n_estimators, learning_rate=learning_rate,
            max_depth=max_depth, random_state=random_state
        )
    }

    display_names = {
        'linear': 'LinearRegression',
        'random_forest': 'RandomForest',
        'gradient_boosting': 'GradientBoosting'
    }

    results = {}
    trained_models = {}

    for key, model in candidates.items():
        print(f"[model_training] Training {display_names[key]}...")
        model.fit(X_train, y_train)
        trained_models[key] = model

        y_pred = model.predict(X_test)
        r2 = round(r2_score(y_test, y_pred), 4)
        mae = round(mean_absolute_error(y_test, y_pred), 2)
        rmse = round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 2)

        results[key] = {
            'r2_score': r2,
            'mae': mae,
            'rmse': rmse,
            'accuracy_pct': round(r2 * 100, 1)
        }
        print(f"[model_training]   {display_names[key]}: R²={r2}, MAE={mae}")

    # Select best model by R² score
    best_key = max(results, key=lambda k: results[k]['r2_score'])
    best_model = trained_models[best_key]

    # Get feature importances if available
    feature_importances = {}
    if hasattr(best_model, 'feature_importances_'):
        feature_importances = dict(zip(X_train.columns, [round(float(v), 4) for v in best_model.feature_importances_]))
    elif hasattr(best_model, 'coef_'):
        feature_importances = dict(zip(X_train.columns, [round(float(v), 4) for v in best_model.coef_]))

    print(f"[model_training] ★ Best model: {display_names[best_key]} (R²={results[best_key]['r2_score']})")

    return {
        'best_model_name': display_names[best_key],
        'best_model_key': best_key,
        'best_model': best_model,
        'best_metrics': results[best_key],
        'all_models': {k: results[k]['r2_score'] for k in results},
        'all_metrics': results,
        'feature_importances': feature_importances,
        'trained_models': trained_models
    }


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_estimators: int = 100,
    learning_rate: float = 0.1,
    max_depth: int = 3,
    random_state: int = 42,
    train_anomaly: bool = True,
    X_full: pd.DataFrame = None
) -> dict:
    """
    Train GradientBoostingRegressor and optionally IsolationForest.
    Used for startup training (no comparison needed).

    Returns:
        dict with keys: skill_model, anomaly_model (or None), feature_importances
    """
    print(f"[model_training] Training GradientBoostingRegressor (n={n_estimators}, lr={learning_rate}, d={max_depth})...")

    gbr = GradientBoostingRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        random_state=random_state
    )
    gbr.fit(X_train, y_train)

    importances = dict(zip(X_train.columns, [round(float(v), 4) for v in gbr.feature_importances_]))
    sorted_imp = sorted(importances.items(), key=lambda x: x[1], reverse=True)
    print(f"[model_training] Top features: {sorted_imp[:5]}")

    anomaly_model = None
    if train_anomaly:
        print("[model_training] Training IsolationForest for anomaly detection...")
        iso = IsolationForest(contamination=0.03, random_state=random_state)
        iso.fit(X_full if X_full is not None else X_train)
        anomaly_model = iso
        print("[model_training] Anomaly model trained")

    return {
        'skill_model': gbr,
        'anomaly_model': anomaly_model,
        'feature_importances': importances
    }


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    Evaluate a trained model on test data.

    Returns:
        dict with: r2_score, mae, rmse, accuracy_pct, samples_tested
    """
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    metrics = {
        'r2_score': round(r2, 4),
        'mae': round(mae, 2),
        'rmse': round(float(rmse), 2),
        'accuracy_pct': round(r2 * 100, 1),
        'samples_tested': len(y_test)
    }

    print(f"[model_training] Evaluation: R²={metrics['r2_score']}, MAE={metrics['mae']}, RMSE={metrics['rmse']}")
    return metrics
