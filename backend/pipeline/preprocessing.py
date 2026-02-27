"""
pipeline/preprocessing.py – Data Cleaning & Normalization
SkillGenome X
"""
import pandas as pd
import numpy as np

# Canonical feature columns used across the pipeline
FEATURE_COLUMNS = [
    'creation_output', 'learning_behavior', 'experience_consistency',
    'economic_activity', 'innovation_problem_solving', 'collaboration_community',
    'offline_capability', 'digital_presence', 'learning_hours', 'projects'
]

# All required columns with synthetic default generators
REQUIRED_COLUMNS = {
    'creation_output': lambda n: np.random.randint(20, 90, size=n),
    'learning_behavior': lambda n: np.random.randint(20, 90, size=n),
    'experience_consistency': lambda n: np.random.randint(20, 90, size=n),
    'economic_activity': lambda n: np.random.randint(20, 90, size=n),
    'innovation_problem_solving': lambda n: np.random.randint(20, 90, size=n),
    'collaboration_community': lambda n: np.random.randint(20, 90, size=n),
    'offline_capability': lambda n: np.random.randint(20, 90, size=n),
    'digital_presence': lambda n: np.random.randint(20, 90, size=n),
    'learning_hours': lambda n: np.random.randint(20, 90, size=n),
    'projects': lambda n: np.random.randint(20, 90, size=n),
    'state': lambda n: np.random.choice(
        ["Maharashtra", "Karnataka", "Punjab", "Bihar", "Tamil Nadu", "Gujarat", "Kerala", "Uttar Pradesh"], size=n
    ),
    'digital_access': lambda n: np.random.choice(["High", "Regular", "Limited", "Occasional"], size=n),
    'opportunity_level': lambda n: np.random.choice(["High", "Moderate", "Low"], size=n),
    'domain': lambda n: np.random.choice(
        ["Retail & Sales", "Manufacturing & Operations", "Agriculture & Allied", "Construction & Skilled Trades"], size=n
    ),
    'area_type': lambda n: np.random.choice(["Urban", "Semi-Urban", "Rural"], size=n),
    'skill_score': lambda n: np.random.randint(30, 90, size=n),
    # Socio-economic columns
    'internet_penetration': lambda n: np.random.uniform(20, 95, size=n).round(1),
    'urban_population_percent': lambda n: np.random.uniform(15, 85, size=n).round(1),
    'per_capita_income': lambda n: np.random.uniform(30000, 350000, size=n).round(0),
    'workforce_participation': lambda n: np.random.uniform(30, 75, size=n).round(1),
    'literacy_rate': lambda n: np.random.uniform(55, 98, size=n).round(1),
    'unemployment_rate': lambda n: np.random.uniform(2, 25, size=n).round(1),
}


def load_csv(filepath: str) -> pd.DataFrame:
    """Load a CSV dataset from disk."""
    import os
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    df = pd.read_csv(filepath)
    if df.empty:
        raise ValueError(f"Data file is empty: {filepath}")
    print(f"[pipeline/preprocessing] Loaded {len(df)} rows from {filepath}")
    return df


def validate_columns(df: pd.DataFrame, auto_heal: bool = True) -> pd.DataFrame:
    """Validate required columns; auto-heal missing ones with synthetic data."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing and not auto_heal:
        raise ValueError(f"Missing required columns: {missing}")
    for col in missing:
        df[col] = REQUIRED_COLUMNS[col](len(df))
        print(f"[pipeline/preprocessing] Auto-healed: {col}")
    # Remove legacy Healthcare domain
    if 'domain' in df.columns:
        df = df[df['domain'] != 'Healthcare']
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill NaNs: median for numeric, mode for categorical."""
    filled = 0
    for col in FEATURE_COLUMNS + ['skill_score']:
        if col in df.columns:
            nans = df[col].isna().sum()
            if nans > 0:
                df[col] = df[col].fillna(df[col].median())
                filled += nans
    for col in ['state', 'domain', 'area_type', 'digital_access', 'opportunity_level']:
        if col in df.columns:
            nans = df[col].isna().sum()
            if nans > 0:
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
                filled += nans
    print(f"[pipeline/preprocessing] Filled {filled} missing values")
    return df


def normalize_features(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """Min-max normalize numeric columns to 0-100."""
    if columns is None:
        columns = FEATURE_COLUMNS
    for col in columns:
        if col in df.columns:
            cmin, cmax = df[col].min(), df[col].max()
            if cmax > cmin:
                df[col] = ((df[col] - cmin) / (cmax - cmin) * 100).round(1)
    return df


def get_feature_matrix(df: pd.DataFrame) -> tuple:
    """Extract X, y, feature_names from preprocessed DataFrame."""
    extra = [
        'behavioral_avg', 'output_to_learning_ratio', 'consistency_score',
        'digital_economic_index', 'digital_index', 'economic_activity_index', 'opportunity_gap'
    ]
    all_features = FEATURE_COLUMNS + [c for c in extra if c in df.columns]
    X = df[all_features].fillna(0)
    y = df['skill_score'].fillna(50)
    print(f"[pipeline/preprocessing] Feature matrix: {X.shape[0]} × {X.shape[1]}")
    return X, y, all_features
