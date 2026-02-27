"""
pipeline/feature_engineering.py – Derived Feature Creation
SkillGenome X
"""
import pandas as pd


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived features from base columns.

    Behavioral:
    - behavioral_avg
    - output_to_learning_ratio
    - consistency_score
    - digital_economic_index

    Socio-economic:
    - digital_index = internet_penetration × urban_population_percent / 100
    - economic_activity_index = per_capita_income × workforce_participation / 100000
    - opportunity_gap = literacy_rate − unemployment_rate
    """
    # ── Behavioral ──
    behavioral_dims = [
        'creation_output', 'learning_behavior', 'experience_consistency',
        'economic_activity', 'innovation_problem_solving', 'collaboration_community',
        'offline_capability', 'digital_presence'
    ]
    existing = [c for c in behavioral_dims if c in df.columns]

    if existing:
        df['behavioral_avg'] = df[existing].mean(axis=1).round(1)

    if 'creation_output' in df.columns and 'learning_behavior' in df.columns:
        df['output_to_learning_ratio'] = (df['creation_output'] / (df['learning_behavior'] + 1)).round(2)

    if 'experience_consistency' in df.columns and 'offline_capability' in df.columns:
        df['consistency_score'] = (df['experience_consistency'] * df['offline_capability'] / 100).round(1)

    if 'digital_presence' in df.columns and 'economic_activity' in df.columns:
        df['digital_economic_index'] = ((df['digital_presence'] + df['economic_activity']) / 2).round(1)

    # ── Socio-Economic ──
    if 'internet_penetration' in df.columns and 'urban_population_percent' in df.columns:
        df['digital_index'] = (df['internet_penetration'] * df['urban_population_percent'] / 100).round(1)

    if 'per_capita_income' in df.columns and 'workforce_participation' in df.columns:
        df['economic_activity_index'] = (df['per_capita_income'] * df['workforce_participation'] / 100000).round(2)

    if 'literacy_rate' in df.columns and 'unemployment_rate' in df.columns:
        df['opportunity_gap'] = (df['literacy_rate'] - df['unemployment_rate']).round(1)

    all_engineered = [
        'behavioral_avg', 'output_to_learning_ratio', 'consistency_score',
        'digital_economic_index', 'digital_index', 'economic_activity_index', 'opportunity_gap'
    ]
    created = [c for c in all_engineered if c in df.columns]
    print(f"[pipeline/feature_engineering] Created {len(created)} features: {created}")
    return df
