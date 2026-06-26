from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


SCORE_COLUMNS = [
    "transport_score",
    "housing_score",
    "youth_support_score",
    "farming_support_score",
    "smartfarm_score",
    "medical_score",
    "culture_score",
    "job_score",
]

LABEL_COLUMNS = [
    "youth_support_score",
    "farming_support_score",
    "smartfarm_score",
    "housing_score",
    "medical_score",
    "transport_score",
]


def _validate_regions(regions_df: pd.DataFrame) -> None:
    missing = [column for column in SCORE_COLUMNS if column not in regions_df.columns]
    if missing:
        raise ValueError(f"regions_df에 필요한 컬럼이 없습니다: {', '.join(missing)}")


def _make_demo_label(frame: pd.DataFrame) -> pd.Series:
    weighted_score = (
        frame["youth_support_score"] * 0.18
        + frame["farming_support_score"] * 0.22
        + frame["smartfarm_score"] * 0.18
        + frame["housing_score"] * 0.16
        + frame["medical_score"] * 0.13
        + frame["transport_score"] * 0.13
    )
    threshold = weighted_score.median()
    return (weighted_score >= threshold).astype(int)


def _augment_regions(regions_df: pd.DataFrame, copies: int = 30) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    numeric = regions_df[SCORE_COLUMNS].astype(float)
    augmented = []

    for _ in range(copies):
        noise = rng.normal(loc=0.0, scale=0.35, size=numeric.shape)
        sampled = numeric + noise
        sampled = sampled.clip(lower=1, upper=5).round(2)
        augmented.append(sampled)

    return pd.concat([numeric, *augmented], ignore_index=True)


def train_demo_model(regions_df: pd.DataFrame) -> Pipeline:
    """Train a LogisticRegression model with synthetic demo labels."""
    _validate_regions(regions_df)

    train_df = _augment_regions(regions_df)
    x = train_df[SCORE_COLUMNS]
    y = _make_demo_label(train_df)

    if y.nunique() < 2:
        y.iloc[0] = 1 - y.iloc[0]

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    model.fit(x, y)
    return model


def _profile_value(user_profile: dict, *keys: str, default=None):
    for key in keys:
        if key in user_profile:
            return user_profile[key]
    return default


def _is_youth(user_profile: dict) -> bool:
    age = _profile_value(user_profile, "age", default=None)
    age_group = str(_profile_value(user_profile, "age_group", "연령대", default=""))
    if isinstance(age, (int, float)):
        return age <= 39
    return "20" in age_group or "30" in age_group or "청년" in age_group


def _build_profile_weights(user_profile: dict) -> dict[str, float]:
    weights = {column: 1.0 for column in SCORE_COLUMNS}
    interest = str(
        _profile_value(user_profile, "interest", "field_interest", "move_goal", "관심분야", default="")
    )
    job = str(_profile_value(user_profile, "job", "직업", default=""))
    budget_level = str(_profile_value(user_profile, "budget_level", "예산수준", default=""))
    budget = _profile_value(user_profile, "budget", "예산", default=None)
    family = bool(_profile_value(user_profile, "family", "with_family", "family_move", default=False))
    remote_work = bool(_profile_value(user_profile, "remote_work", "remote", "원격근무", default=False))

    if "스마트팜" in interest:
        weights["smartfarm_score"] += 0.8
        weights["farming_support_score"] += 0.3

    if "농" in interest or "귀농" in interest:
        weights["farming_support_score"] += 0.6
        weights["housing_score"] += 0.2

    if _is_youth(user_profile):
        weights["youth_support_score"] += 0.7
        weights["job_score"] += 0.2

    if family:
        weights["medical_score"] += 0.6
        weights["housing_score"] += 0.5
        weights["culture_score"] += 0.2

    if budget_level == "낮음" or (isinstance(budget, (int, float)) and budget <= 6000):
        weights["housing_score"] += 0.7

    if remote_work or "개발" in job or "IT" in job.upper():
        weights["transport_score"] += 0.4
        weights["job_score"] += 0.6

    return weights


def _reason_features(row: pd.Series, weights: dict[str, float], limit: int = 3) -> str:
    contributions = []
    for column in SCORE_COLUMNS:
        contributions.append((column, float(row[column]) * weights[column]))
    top_columns = [column for column, _ in sorted(contributions, key=lambda item: item[1], reverse=True)[:limit]]
    labels = {
        "transport_score": "교통",
        "housing_score": "주거",
        "youth_support_score": "청년지원",
        "farming_support_score": "영농지원",
        "smartfarm_score": "스마트팜",
        "medical_score": "의료",
        "culture_score": "문화",
        "job_score": "일자리",
    }
    return ", ".join(labels[column] for column in top_columns)


def predict_suitability(model: Pipeline, user_profile: dict, regions_df: pd.DataFrame) -> pd.DataFrame:
    """Return region suitability probabilities adjusted by user profile."""
    _validate_regions(regions_df)

    base_probability = model.predict_proba(regions_df[SCORE_COLUMNS])[:, 1]
    weights = _build_profile_weights(user_profile)
    weighted_features = regions_df[SCORE_COLUMNS].astype(float).copy()

    for column, weight in weights.items():
        weighted_features[column] = weighted_features[column] * weight

    profile_score = weighted_features.sum(axis=1) / (5 * sum(weights.values()))
    final_probability = (base_probability * 0.65) + (profile_score * 0.35)

    result = pd.DataFrame(
        {
            "region": regions_df["region"],
            "probability": np.round(final_probability, 4),
            "ml_score": np.round(base_probability * 100, 2),
            "reason_features": [
                _reason_features(row, weights) for _, row in regions_df.iterrows()
            ],
        }
    )
    return result.sort_values("probability", ascending=False).reset_index(drop=True)
