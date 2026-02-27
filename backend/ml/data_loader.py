"""
data_loader.py – Data Loading & Validation
SkillGenome X ML Pipeline
"""
import os
import pandas as pd
import numpy as np


# Column spec: name → default generator
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
    # Socio-economic columns (for feature engineering)
    'internet_penetration': lambda n: np.random.uniform(20, 95, size=n).round(1),
    'urban_population_percent': lambda n: np.random.uniform(15, 85, size=n).round(1),
    'per_capita_income': lambda n: np.random.uniform(30000, 350000, size=n).round(0),
    'workforce_participation': lambda n: np.random.uniform(30, 75, size=n).round(1),
    'literacy_rate': lambda n: np.random.uniform(55, 98, size=n).round(1),
    'unemployment_rate': lambda n: np.random.uniform(2, 25, size=n).round(1),
}

FEATURE_COLUMNS = [
    'creation_output', 'learning_behavior', 'experience_consistency',
    'economic_activity', 'innovation_problem_solving', 'collaboration_community',
    'offline_capability', 'digital_presence', 'learning_hours', 'projects'
]


def load_csv(filepath: str) -> pd.DataFrame:
    """
    Load a CSV dataset from disk.

    Args:
        filepath: Absolute or relative path to CSV file.

    Returns:
        pd.DataFrame with raw data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or unreadable.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_csv(filepath)
    if df.empty:
        raise ValueError(f"Data file is empty: {filepath}")

    print(f"[data_loader] Loaded {len(df)} rows × {len(df.columns)} cols from {filepath}")
    return df


def validate_columns(df: pd.DataFrame, auto_heal: bool = True) -> pd.DataFrame:
    """
    Validate that all required columns exist.
    If auto_heal=True, missing columns are filled with synthetic defaults.

    Args:
        df: Input DataFrame.
        auto_heal: Whether to auto-generate missing columns.

    Returns:
        DataFrame with all required columns present.
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing and not auto_heal:
        raise ValueError(f"Missing required columns: {missing}")

    for col in missing:
        generator = REQUIRED_COLUMNS[col]
        df[col] = generator(len(df))
        print(f"[data_loader] Auto-healed missing column: {col}")

    # Filter out Healthcare domain if present (legacy data)
    if 'domain' in df.columns:
        before = len(df)
        df = df[df['domain'] != 'Healthcare']
        removed = before - len(df)
        if removed > 0:
            print(f"[data_loader] Removed {removed} Healthcare-domain rows")

    print(f"[data_loader] Validated: {len(df)} rows, {len(df.columns)} cols, {len(missing)} auto-healed")
    return df
