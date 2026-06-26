from __future__ import annotations

from pathlib import Path

import pandas as pd

from ml_model import predict_suitability, train_demo_model


DATA_DIR = Path("data")
REGIONS_PATH = DATA_DIR / "regions.csv"
POLICIES_PATH = DATA_DIR / "policies.csv"


def load_regions(path: str | Path = REGIONS_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def load_policies(path: str | Path = POLICIES_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


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


def _make_matched_reason(row: pd.Series, user_profile: dict) -> str:
    reasons: list[str] = []
    interest = str(
        _profile_value(user_profile, "interest", "field_interest", "move_goal", "관심분야", default="")
    )
    job = str(_profile_value(user_profile, "job", "직업", default=""))
    budget = _profile_value(user_profile, "budget", "예산", default=None)
    family = bool(_profile_value(user_profile, "family", "with_family", "family_move", default=False))
    remote_work = bool(_profile_value(user_profile, "remote_work", "remote", "원격근무", default=False))

    if "스마트팜" in interest and row["smartfarm_score"] >= 4:
        reasons.append("스마트팜 관심도가 높아 스마트팜 점수가 높은 지역을 우선 추천했습니다.")
    if ("농" in interest or "귀농" in interest) and row["farming_support_score"] >= 4:
        reasons.append("농업 정착 의지가 있어 영농지원 점수가 높은 지역과 잘 맞습니다.")
    if _is_youth(user_profile) and row["youth_support_score"] >= 4:
        reasons.append("청년층에게 필요한 청년지원 지표가 높습니다.")
    if family and row["medical_score"] >= 4 and row["housing_score"] >= 4:
        reasons.append("가족 동반 이주에 중요한 의료와 주거 지표가 안정적입니다.")
    if isinstance(budget, (int, float)) and budget <= 6000 and row["housing_score"] >= 4:
        reasons.append("예산이 낮은 편이라 주거 부담이 낮은 지역을 높게 반영했습니다.")
    if (remote_work or "개발" in job or "IT" in job.upper()) and (
        row["transport_score"] >= 4 or row["job_score"] >= 4
    ):
        reasons.append("원격근무나 개발자 직무를 고려해 교통·일자리 지표를 반영했습니다.")

    if reasons:
        return " ".join(reasons[:2])
    return f"{row['region']}은 입력 조건과 지역 점수의 균형이 좋아 추천 후보에 포함했습니다."


def _related_policies(region: str, policies_df: pd.DataFrame) -> list[dict]:
    rows = policies_df[policies_df["region"] == region]
    return rows[["policy_name", "category", "target", "benefit", "apply_url"]].to_dict("records")


def recommend_regions(
    user_profile: dict,
    regions_df: pd.DataFrame | None = None,
    policies_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    regions = load_regions() if regions_df is None else regions_df.copy()
    policies = load_policies() if policies_df is None else policies_df.copy()

    model = train_demo_model(regions)
    predictions = predict_suitability(model, user_profile, regions)
    merged = predictions.merge(
        regions[["region", "description", "risk_note"]],
        on="region",
        how="left",
    )

    top3 = merged.head(3).copy()
    region_lookup = regions.set_index("region")
    top3["score"] = (top3["probability"] * 100).round(1)
    top3["matched_reason"] = top3.apply(
        lambda row: _make_matched_reason(region_lookup.loc[row["region"]], user_profile),
        axis=1,
    )
    top3["related_policies"] = top3["region"].apply(lambda region: _related_policies(region, policies))

    return top3[
        [
            "region",
            "score",
            "probability",
            "description",
            "risk_note",
            "matched_reason",
            "related_policies",
        ]
    ].reset_index(drop=True)
