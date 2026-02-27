"""
preprocessing.py – Data Preprocessing & Feature Engineering
SkillGenome X ML Pipeline
"""
import pandas as pd
import numpy as np
from ml.data_loader import FEATURE_COLUMNS


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing / NaN values in the dataset.

    Strategy:
    - Numeric columns: fill with column median (robust to outliers)
    - Categorical columns: fill with mode (most frequent)

    Args:
        df: Input DataFrame.

    Returns:
        DataFrame with no NaN values in feature or target columns.
    """
    filled_count = 0

    for col in FEATURE_COLUMNS + ['skill_score']:
        if col in df.columns:
            nans = df[col].isna().sum()
            if nans > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                filled_count += nans

    # Categorical columns
    for col in ['state', 'domain', 'area_type', 'digital_access', 'opportunity_level']:
        if col in df.columns:
            nans = df[col].isna().sum()
            if nans > 0:
                mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                df[col] = df[col].fillna(mode_val)
                filled_count += nans

    if filled_count > 0:
        print(f"[preprocessing] Filled {filled_count} missing values")
    else:
        print(f"[preprocessing] No missing values found")

    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived features to improve model performance.

    Behavioral features:
    - behavioral_avg: mean of all 8 behavioral dimensions
    - output_to_learning_ratio: creation_output / (learning_behavior + 1)
    - consistency_score: experience_consistency * offline_capability / 100
    - digital_economic_index: (digital_presence + economic_activity) / 2

    Socio-economic features:
    - digital_index: internet_penetration × urban_population_percent / 100
    - economic_activity_index: per_capita_income × workforce_participation / 100000
    - opportunity_gap: literacy_rate − unemployment_rate

    Args:
        df: Input DataFrame with base features.

    Returns:
        DataFrame with additional engineered columns.
    """
    behavioral_dims = [
        'creation_output', 'learning_behavior', 'experience_consistency',
        'economic_activity', 'innovation_problem_solving', 'collaboration_community',
        'offline_capability', 'digital_presence'
    ]

    # Only use columns that exist
    existing_dims = [c for c in behavioral_dims if c in df.columns]

    if existing_dims:
        df['behavioral_avg'] = df[existing_dims].mean(axis=1).round(1)

    if 'creation_output' in df.columns and 'learning_behavior' in df.columns:
        df['output_to_learning_ratio'] = (df['creation_output'] / (df['learning_behavior'] + 1)).round(2)

    if 'experience_consistency' in df.columns and 'offline_capability' in df.columns:
        df['consistency_score'] = (df['experience_consistency'] * df['offline_capability'] / 100).round(1)

    if 'digital_presence' in df.columns and 'economic_activity' in df.columns:
        df['digital_economic_index'] = ((df['digital_presence'] + df['economic_activity']) / 2).round(1)

    # ── Socio-Economic Engineered Features ──
    if 'internet_penetration' in df.columns and 'urban_population_percent' in df.columns:
        df['digital_index'] = (df['internet_penetration'] * df['urban_population_percent'] / 100).round(1)

    if 'per_capita_income' in df.columns and 'workforce_participation' in df.columns:
        df['economic_activity_index'] = (df['per_capita_income'] * df['workforce_participation'] / 100000).round(2)

    if 'literacy_rate' in df.columns and 'unemployment_rate' in df.columns:
        df['opportunity_gap'] = (df['literacy_rate'] - df['unemployment_rate']).round(1)

    all_engineered = [
        'behavioral_avg', 'output_to_learning_ratio', 'consistency_score', 'digital_economic_index',
        'digital_index', 'economic_activity_index', 'opportunity_gap'
    ]
    new_cols = [c for c in all_engineered if c in df.columns]
    print(f"[preprocessing] Engineered {len(new_cols)} features: {new_cols}")

    return df


def normalize_features(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Normalize numeric feature columns to 0–100 range using min-max scaling.

    Args:
        df: Input DataFrame.
        columns: List of column names to normalize. Defaults to FEATURE_COLUMNS.

    Returns:
        DataFrame with normalized columns.
    """
    if columns is None:
        columns = FEATURE_COLUMNS

    for col in columns:
        if col in df.columns:
            col_min = df[col].min()
            col_max = df[col].max()
            if col_max > col_min:
                df[col] = ((df[col] - col_min) / (col_max - col_min) * 100).round(1)

    print(f"[preprocessing] Normalized {len(columns)} feature columns to 0-100 scale")
    return df


def get_feature_matrix(df: pd.DataFrame) -> tuple:
    """
    Extract feature matrix X and target vector y from preprocessed DataFrame.

    Returns:
        (X: pd.DataFrame, y: pd.Series, feature_names: list)
    """
    # Use base features + any engineered features that exist
    extra_features = [
        'behavioral_avg', 'output_to_learning_ratio', 'consistency_score', 'digital_economic_index',
        'digital_index', 'economic_activity_index', 'opportunity_gap'
    ]
    all_features = FEATURE_COLUMNS + [c for c in extra_features if c in df.columns]

    X = df[all_features].fillna(0)
    y = df['skill_score'].fillna(50)

    print(f"[preprocessing] Feature matrix: {X.shape[0]} samples × {X.shape[1]} features")
    return X, y, all_features
