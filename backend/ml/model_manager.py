"""
model_manager.py – Model Persistence (Save / Load)
SkillGenome X ML Pipeline
"""
import os
import json
import joblib
from datetime import datetime


MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'saved')


def _ensure_dir():
    """Create model directory if it doesn't exist."""
    os.makedirs(MODEL_DIR, exist_ok=True)


def save_model(skill_model, anomaly_model=None, metadata: dict = None, tag: str = 'latest') -> dict:
    """
    Save trained models and metadata to disk using joblib.

    Args:
        skill_model: Trained GradientBoostingRegressor.
        anomaly_model: Trained IsolationForest (optional).
        metadata: Dict of training metrics, feature names, etc.
        tag: Version tag (default 'latest').

    Returns:
        dict with saved file paths and sizes.
    """
    _ensure_dir()

    skill_path = os.path.join(MODEL_DIR, f'skill_model_{tag}.joblib')
    joblib.dump(skill_model, skill_path)
    skill_size = os.path.getsize(skill_path)

    result = {
        'skill_model_path': skill_path,
        'skill_model_size_kb': round(skill_size / 1024, 1),
        'tag': tag,
        'saved_at': datetime.now().isoformat()
    }

    if anomaly_model is not None:
        anomaly_path = os.path.join(MODEL_DIR, f'anomaly_model_{tag}.joblib')
        joblib.dump(anomaly_model, anomaly_path)
        result['anomaly_model_path'] = anomaly_path
        result['anomaly_model_size_kb'] = round(os.path.getsize(anomaly_path) / 1024, 1)

    # Save metadata
    if metadata:
        meta_path = os.path.join(MODEL_DIR, f'metadata_{tag}.json')
        meta_to_save = {**metadata, 'saved_at': result['saved_at'], 'tag': tag}
        with open(meta_path, 'w') as f:
            json.dump(meta_to_save, f, indent=2, default=str)
        result['metadata_path'] = meta_path

    print(f"[model_manager] Saved models with tag '{tag}' → {MODEL_DIR}")
    return result


def load_model(tag: str = 'latest') -> dict:
    """
    Load saved models from disk.

    Args:
        tag: Version tag to load (default 'latest').

    Returns:
        dict with: skill_model, anomaly_model (or None), metadata (or {})

    Raises:
        FileNotFoundError: If no saved model found for the given tag.
    """
    skill_path = os.path.join(MODEL_DIR, f'skill_model_{tag}.joblib')

    if not os.path.exists(skill_path):
        raise FileNotFoundError(f"No saved model found for tag '{tag}' at {skill_path}")

    skill_model = joblib.load(skill_path)
    print(f"[model_manager] Loaded skill model from {skill_path}")

    anomaly_model = None
    anomaly_path = os.path.join(MODEL_DIR, f'anomaly_model_{tag}.joblib')
    if os.path.exists(anomaly_path):
        anomaly_model = joblib.load(anomaly_path)
        print(f"[model_manager] Loaded anomaly model from {anomaly_path}")

    metadata = {}
    meta_path = os.path.join(MODEL_DIR, f'metadata_{tag}.json')
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            metadata = json.load(f)

    return {
        'skill_model': skill_model,
        'anomaly_model': anomaly_model,
        'metadata': metadata
    }


def list_saved_models() -> list:
    """List all saved model tags."""
    _ensure_dir()
    files = os.listdir(MODEL_DIR)
    tags = set()
    for f in files:
        if f.startswith('skill_model_') and f.endswith('.joblib'):
            tag = f.replace('skill_model_', '').replace('.joblib', '')
            tags.add(tag)
    return sorted(tags)
