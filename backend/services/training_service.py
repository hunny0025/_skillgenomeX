"""
services/training_service.py – Training Orchestration
SkillGenome X

Orchestrates the full ML pipeline: load → validate → preprocess → engineer → split → compare → save.
"""
import os
import time
import joblib
from datetime import datetime

from pipeline.preprocessing import load_csv, validate_columns, handle_missing_values, get_feature_matrix, FEATURE_COLUMNS
from pipeline.feature_engineering import feature_engineering
from pipeline.model_training import split_data, compare_models, train_model, evaluate_model

# Default paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'saved')


class TrainingService:
    """Orchestrates model training pipeline."""

    @staticmethod
    def run_pipeline(data_file: str, test_size=0.2, n_estimators=100,
                     learning_rate=0.1, max_depth=3) -> dict:
        """
        Full pipeline: load → validate → preprocess → engineer → split → compare → save.

        Returns:
            dict with metrics, comparison, saved info, timing.
        """
        start = time.time()

        # Load & preprocess
        df = load_csv(data_file)
        df = validate_columns(df, auto_heal=True)
        df = handle_missing_values(df)
        df = feature_engineering(df)

        # Feature matrix
        X, y, feature_names = get_feature_matrix(df)

        # Split
        splits = split_data(X, y, test_size=test_size)

        # Compare models
        comparison = compare_models(
            splits['X_train'], splits['y_train'],
            splits['X_test'], splits['y_test'],
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth
        )

        # Train anomaly model on full data
        from sklearn.ensemble import IsolationForest
        iso = IsolationForest(contamination=0.03, random_state=42)
        iso.fit(X)

        # Save best model
        save_info = TrainingService.save_models(
            comparison['best_model'], iso,
            metadata={
                **comparison['best_metrics'],
                'features': feature_names,
                'samples': len(df),
                'best_model': comparison['best_model_name']
            }
        )

        elapsed = round(time.time() - start, 2)

        return {
            'status': 'success',
            'df': df,
            'best_model': comparison['best_model'],
            'best_model_name': comparison['best_model_name'],
            'anomaly_model': iso,
            'best_metrics': comparison['best_metrics'],
            'all_models': comparison['all_models'],
            'all_metrics': comparison['all_metrics'],
            'feature_importances': comparison.get('feature_importances', {}),
            'feature_names': feature_names,
            'splits': splits,
            'save_info': save_info,
            'elapsed_seconds': elapsed,
            'data_info': {
                'samples': len(df),
                'features': len(feature_names),
                'train_size': len(splits['X_train']),
                'test_size': len(splits['X_test'])
            }
        }

    @staticmethod
    def startup_load_or_train(data_file: str) -> dict:
        """
        Startup logic: load saved model from disk if exists, else train fresh.

        Returns:
            dict with skill_model, anomaly_model, training_score, feature_names, source
        """
        try:
            result = TrainingService.load_models()
            print("AI ENGINE: Model loaded from disk")
            return {**result, 'source': 'disk'}
        except FileNotFoundError:
            print("AI ENGINE: No saved model found. Model trained fresh.")
            pipeline_result = TrainingService.run_pipeline(data_file)
            return {
                'skill_model': pipeline_result['best_model'],
                'anomaly_model': pipeline_result['anomaly_model'],
                'training_score': pipeline_result['best_metrics']['accuracy_pct'],
                'feature_names': pipeline_result['feature_names'],
                'metadata': pipeline_result['best_metrics'],
                'source': 'trained_fresh'
            }

    @staticmethod
    def save_models(skill_model, anomaly_model=None, metadata=None, tag='latest'):
        """Save models to disk using joblib."""
        os.makedirs(MODEL_DIR, exist_ok=True)

        skill_path = os.path.join(MODEL_DIR, f'skill_model_{tag}.joblib')
        joblib.dump(skill_model, skill_path)
        result = {
            'skill_model_path': skill_path,
            'skill_model_size_kb': round(os.path.getsize(skill_path) / 1024, 1),
            'tag': tag,
            'saved_at': datetime.now().isoformat()
        }

        if anomaly_model:
            anomaly_path = os.path.join(MODEL_DIR, f'anomaly_model_{tag}.joblib')
            joblib.dump(anomaly_model, anomaly_path)
            result['anomaly_model_path'] = anomaly_path

        if metadata:
            import json
            meta_path = os.path.join(MODEL_DIR, f'metadata_{tag}.json')
            with open(meta_path, 'w') as f:
                json.dump({**metadata, 'saved_at': result['saved_at']}, f, indent=2, default=str)

        print(f"[TrainingService] Models saved (tag={tag})")
        return result

    @staticmethod
    def load_models(tag='latest'):
        """Load models from disk."""
        skill_path = os.path.join(MODEL_DIR, f'skill_model_{tag}.joblib')
        if not os.path.exists(skill_path):
            raise FileNotFoundError(f"No model for tag '{tag}'")

        result = {'skill_model': joblib.load(skill_path)}

        anomaly_path = os.path.join(MODEL_DIR, f'anomaly_model_{tag}.joblib')
        result['anomaly_model'] = joblib.load(anomaly_path) if os.path.exists(anomaly_path) else None

        import json
        meta_path = os.path.join(MODEL_DIR, f'metadata_{tag}.json')
        result['metadata'] = {}
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                result['metadata'] = json.load(f)

        result['training_score'] = result['metadata'].get('accuracy_pct', 0)
        result['feature_names'] = result['metadata'].get('features', FEATURE_COLUMNS)
        return result

    @staticmethod
    def list_tags():
        """List available saved model tags."""
        os.makedirs(MODEL_DIR, exist_ok=True)
        tags = set()
        for f in os.listdir(MODEL_DIR):
            if f.startswith('skill_model_') and f.endswith('.joblib'):
                tags.add(f.replace('skill_model_', '').replace('.joblib', ''))
        return sorted(tags)
