from __future__ import annotations

import pandas as pd
import streamlit as st

from ai import generate_ai_explanation
from recommend import load_policies, load_regions, recommend_regions


st.set_page_config(page_title="AI 귀농·귀촌 의사결정 지원 서비스", page_icon="🌿", layout="wide")


@st.cache_data
def get_regions() -> pd.DataFrame:
    return load_regions()


@st.cache_data
def get_policies() -> pd.DataFrame:
    return load_policies()


def apply_style() -> None:
    st.markdown(
        """
        <style>
        .block-container { max-width: 1160px; padding-top: 2rem; padding-bottom: 3rem; }
        [data-testid="stSidebar"] { background: #f4f7f1; }
        h1, h2, h3, p, label { letter-spacing: 0; }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: 12px 0 24px;
        }
        .summary-item {
            background: #ffffff;
            border: 1px solid #dfe6dc;
            border-radius: 8px;
            padding: 14px;
        }
        .summary-label { color: #667064; font-size: .84rem; margin-bottom: 4px; }
        .summary-value { color: #1f2a22; font-size: 1.05rem; font-weight: 750; }
        .region-card {
            background: #ffffff;
            border: 1px solid #dfe6dc;
            border-radius: 8px;
            padding: 16px;
            min-height: 520px;
        }
        .rank { color: #2f6f46; font-size: .85rem; font-weight: 800; }
        .region-name { color: #1f2a22; font-size: 1.45rem; font-weight: 850; margin: 4px 0 6px; }
        .score { color: #1f2a22; font-size: 1.9rem; font-weight: 850; }
        .score small { color: #6f7a6d; font-size: .9rem; font-weight: 500; }
        .probability { color: #4f5a50; font-size: .9rem; margin-bottom: 10px; }
        .policy-box {
            background: #f7faf6;
            border: 1px solid #e1e8de;
            border-radius: 8px;
            padding: 10px;
            margin-top: 8px;
        }
        .policy-title { font-weight: 750; color: #243528; }
        .muted { color: #5c665e; font-size: .9rem; line-height: 1.5; }
        .presentation-note {
            margin-top: 28px;
            background: #f7faf6;
            border: 1px solid #dfe6dc;
            border-radius: 8px;
            padding: 14px 16px;
            color: #4f5a50;
            font-size: .92rem;
            line-height: 1.55;
        }
        @media (max-width: 900px) { .summary-grid { grid-template-columns: 1fr; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_input_form() -> dict | None:
    with st.form("profile_form"):
        st.subheader("입력 폼")
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("나이", min_value=19, max_value=90, value=35, step=1)
            job = st.selectbox("현재 직업", ["개발자", "회사원", "자영업", "농업 경험자", "프리랜서", "은퇴 예정", "기타"])
        with col2:
            family = st.selectbox("가족 구성", ["1인", "부부", "부부+자녀", "부모 동반", "기타"])
            monthly_budget = st.number_input("월 예산", min_value=50, max_value=1000, value=250, step=10, help="단위: 만원")
        with col3:
            interest = st.selectbox("관심 분야", ["스마트팜", "일반 농업", "전원생활", "창업", "원격근무", "문화·관광"])
            move_type = st.selectbox("귀농/귀촌 유형", ["귀농", "귀촌", "반농반X", "스마트팜 창업", "은퇴 후 정착"])

        submitted = st.form_submit_button("분석하기", type="primary", use_container_width=True)

    if not submitted:
        return None

    return {
        "age": age,
        "age_group": _age_group(age),
        "job": job,
        "family": family,
        "family_move": family not in ["1인"],
        "budget": monthly_budget,
        "monthly_budget": monthly_budget,
        "interest": interest,
        "move_goal": move_type,
        "remote_work": job == "개발자" or interest == "원격근무",
    }


def _age_group(age: int) -> str:
    if age < 30:
        return "20대"
    if age < 40:
        return "30대"
    if age < 50:
        return "40대"
    if age < 60:
        return "50대"
    return "60대 이상"


def render_user_summary(profile: dict) -> None:
    st.subheader("1. 사용자 입력 요약")
    st.markdown(
        f"""
        <div class="summary-grid">
            <div class="summary-item"><div class="summary-label">나이 / 직업</div><div class="summary-value">{profile['age']}세 / {profile['job']}</div></div>
            <div class="summary-item"><div class="summary-label">가족 구성</div><div class="summary-value">{profile['family']}</div></div>
            <div class="summary-item"><div class="summary-label">월 예산</div><div class="summary-value">{profile['monthly_budget']:,}만원</div></div>
            <div class="summary-item"><div class="summary-label">관심 분야</div><div class="summary-value">{profile['interest']}</div></div>
            <div class="summary-item"><div class="summary-label">귀농/귀촌 유형</div><div class="summary-value">{profile['move_goal']}</div></div>
            <div class="summary-item"><div class="summary-label">원격근무 고려</div><div class="summary-value">{'예' if profile['remote_work'] else '아니오'}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_policy(policy: dict) -> None:
    st.markdown(
        f"""
        <div class="policy-box">
            <div class="policy-title">{policy.get('policy_name')}</div>
            <div class="muted">{policy.get('category')} · {policy.get('target')}</div>
            <div class="muted">{policy.get('benefit')}</div>
            <div class="muted">{policy.get('apply_url')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation_cards(recommendations: pd.DataFrame) -> None:
    st.subheader("2. 추천 지역 TOP3")
    cols = st.columns(3)
    for rank, (_, row) in enumerate(recommendations.iterrows(), start=1):
        with cols[rank - 1]:
            st.markdown('<div class="region-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="rank">TOP {rank}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="region-name">{row["region"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="score">{row["score"]:.1f}<small> / 100</small></div>', unsafe_allow_html=True)
            st.progress(float(row["score"]) / 100, text="3. 적합도 점수")
            st.markdown(f'<div class="probability">4. 머신러닝 예측 확률: <b>{row["probability"]:.2%}</b></div>', unsafe_allow_html=True)
            st.markdown("**5. 추천 이유**")
            st.write(row["matched_reason"])
            st.markdown("**6. 주의사항**")
            st.write(row["risk_note"])
            st.markdown("**지역 설명**")
            st.write(row["description"])
            st.markdown("**7. 연결 가능한 지원정책**")
            for policy in row["related_policies"]:
                render_policy(policy)
            st.markdown("</div>", unsafe_allow_html=True)


def render_ai_analysis(profile: dict, recommendations: pd.DataFrame) -> None:
    st.subheader("8. Claude AI 종합 분석")
    with st.spinner("종합 분석을 생성하는 중입니다..."):
        analysis = generate_ai_explanation(profile, recommendations)
    st.markdown(analysis)


def render_presentation_note() -> None:
    st.markdown(
        """
        <div class="presentation-note">
        본 서비스는 실제 정착 성공 데이터를 보유하지 않은 1박 2일 해커톤 환경을 고려하여,
        전남 시군별 공개 정보와 데모용 로지스틱 회귀 모델을 활용한 MVP입니다.
        향후 실제 귀농·귀촌 정착 데이터가 확보되면 모델 정확도를 개선할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    apply_style()
    st.title("AI 귀농·귀촌 의사결정 지원 서비스")
    st.write("전남 시군별 데이터를 기반으로 나에게 맞는 귀농·귀촌 후보 지역을 추천합니다.")

    profile = render_input_form()
    if profile is None:
        st.info("조건을 입력한 뒤 분석하기 버튼을 눌러 추천 결과를 확인하세요.")
        return

    regions_df = get_regions()
    policies_df = get_policies()
    recommendations = recommend_regions(profile, regions_df, policies_df)

    render_user_summary(profile)
    render_recommendation_cards(recommendations)
    render_ai_analysis(profile, recommendations)
    render_presentation_note()


if __name__ == "__main__":
    main()
