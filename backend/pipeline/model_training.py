"""
pipeline/model_training.py – Model Training, Comparison & Evaluation
SkillGenome X
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, IsolationForest
from sklearn.model_selection import train_test_split as sklearn_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def split_data(X, y, test_size=0.2, random_state=42):
    """Split into train/test sets."""
    X_train, X_test, y_train, y_test = sklearn_split(X, y, test_size=test_size, random_state=random_state)
    print(f"[pipeline/model_training] Split: {len(X_train)} train / {len(X_test)} test")
    return {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}


def compare_models(X_train, y_train, X_test, y_test,
                   n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42):
    """
    Train LinearRegression, RandomForest, GradientBoosting.
    Evaluate each (R², MAE, RMSE). Auto-select best by R².
    """
    candidates = {
        'linear': LinearRegression(),
        'random_forest': RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state),
        'gradient_boosting': GradientBoostingRegressor(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=random_state)
    }
    names = {'linear': 'LinearRegression', 'random_forest': 'RandomForest', 'gradient_boosting': 'GradientBoosting'}
    results, trained = {}, {}

    for key, model in candidates.items():
        print(f"[pipeline/model_training] Training {names[key]}...")
        model.fit(X_train, y_train)
        trained[key] = model
        y_pred = model.predict(X_test)
        results[key] = {
            'r2_score': round(r2_score(y_test, y_pred), 4),
            'mae': round(mean_absolute_error(y_test, y_pred), 2),
            'rmse': round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 2),
            'accuracy_pct': round(r2_score(y_test, y_pred) * 100, 1)
        }
        print(f"[pipeline/model_training]   {names[key]}: R²={results[key]['r2_score']}, MAE={results[key]['mae']}")

    best_key = max(results, key=lambda k: results[k]['r2_score'])
    best = trained[best_key]
    importances = {}
    if hasattr(best, 'feature_importances_'):
        importances = dict(zip(X_train.columns, [round(float(v), 4) for v in best.feature_importances_]))
    elif hasattr(best, 'coef_'):
        importances = dict(zip(X_train.columns, [round(float(v), 4) for v in best.coef_]))

    print(f"[pipeline/model_training] ★ Best: {names[best_key]} (R²={results[best_key]['r2_score']})")
    return {
        'best_model_name': names[best_key], 'best_model_key': best_key,
        'best_model': best, 'best_metrics': results[best_key],
        'all_models': {k: results[k]['r2_score'] for k in results},
        'all_metrics': results, 'feature_importances': importances, 'trained_models': trained
    }


def train_model(X_train, y_train, n_estimators=100, learning_rate=0.1,
                max_depth=3, random_state=42, train_anomaly=True, X_full=None):
    """Train GBR + optional IsolationForest (used for startup)."""
    gbr = GradientBoostingRegressor(n_estimators=n_estimators, learning_rate=learning_rate,
                                    max_depth=max_depth, random_state=random_state)
    gbr.fit(X_train, y_train)
    importances = dict(zip(X_train.columns, [round(float(v), 4) for v in gbr.feature_importances_]))

    anomaly_model = None
    if train_anomaly:
        iso = IsolationForest(contamination=0.03, random_state=random_state)
        iso.fit(X_full if X_full is not None else X_train)
        anomaly_model = iso

    return {'skill_model': gbr, 'anomaly_model': anomaly_model, 'feature_importances': importances}


def evaluate_model(model, X_test, y_test):
    """Evaluate model: R², MAE, RMSE."""
    y_pred = model.predict(X_test)
    return {
        'r2_score': round(r2_score(y_test, y_pred), 4),
        'mae': round(mean_absolute_error(y_test, y_pred), 2),
        'rmse': round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 2),
        'accuracy_pct': round(r2_score(y_test, y_pred) * 100, 1),
        'samples_tested': len(y_test)
    }
