"""
preprocessing.py
Data pipeline for SkillGenome X – Real Data Upgrade.
Handles loading, cleaning, normalization, and encoding for the India socio-economic dataset.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Canonical feature columns (everything except State & target)
FEATURE_COLUMNS = [
    'Literacy_Rate',
    'Internet_Penetration',
    'Workforce_Participation',
    'Urban_Population_Percent',
    'Per_Capita_Income',
    'Skill_Training_Count'
]

TARGET_COLUMN = 'Unemployment_Rate'


def get_feature_columns():
    """Return the canonical list of feature column names."""
    return FEATURE_COLUMNS.copy()


def load_and_clean(path: str) -> pd.DataFrame:
    """
    Load a CSV from `path`, enforce numeric types, and drop rows with nulls.
    Returns a clean DataFrame.
    """
    df = pd.read_csv(path)

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include='object').columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    # Coerce numeric columns
    numeric_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with any nulls in key columns
    key_cols = [c for c in numeric_cols if c in df.columns]
    before = len(df)
    df = df.dropna(subset=key_cols)
    after = len(df)
    if before != after:
        print(f"[Preprocessing] Dropped {before - after} rows with missing values.")

    df = df.reset_index(drop=True)
    print(f"[Preprocessing] Loaded {len(df)} clean records.")
    return df


def normalize_features(df: pd.DataFrame, scaler: MinMaxScaler = None):
    """
    Normalize feature columns using MinMaxScaler.
    If scaler is None, fits a new one on df.
    Returns (normalized_df, fitted_scaler).
    """
    df = df.copy()
    cols = [c for c in FEATURE_COLUMNS if c in df.columns]

    if scaler is None:
        scaler = MinMaxScaler()
        df[cols] = scaler.fit_transform(df[cols])
    else:
        df[cols] = scaler.transform(df[cols])

    return df, scaler


def encode_categoricals(df: pd.DataFrame):
    """
    Label-encode the 'State' column so it can optionally be used as a feature.
    Returns (df_with_encoded_state, label_encoder).
    """
    df = df.copy()
    le = LabelEncoder()
    if 'State' in df.columns:
        df['State_Encoded'] = le.fit_transform(df['State'].astype(str))
    return df, le


def prepare_dataset(path: str):
    """
    Full pipeline: load → clean → encode → normalize → split X/y.
    Returns (X, y, scaler, label_encoder, clean_df).
    """
    df = load_and_clean(path)
    df, le = encode_categoricals(df)
    df_norm, scaler = normalize_features(df)

    feature_cols = [c for c in FEATURE_COLUMNS if c in df_norm.columns]
    X = df_norm[feature_cols].values
    y = df[TARGET_COLUMN].values if TARGET_COLUMN in df.columns else None

    return X, y, scaler, le, df
