from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------------------------
APP_TITLE = "전남 귀농 Compass"
DATA_DIR = Path("data")
REGION_FILE = DATA_DIR / "region_features.csv"
HOUSE_FILE = DATA_DIR / "house_list.csv"
POLICY_FILE = DATA_DIR / "policies.csv"


def ensure_sample_data() -> None:
    """필수 CSV 파일이 없을 때 MVP용 샘플 데이터를 자동 생성합니다."""
    DATA_DIR.mkdir(exist_ok=True)

    if not REGION_FILE.exists():
        region_features = pd.DataFrame(
            [
                {
                    "region": "나주시",
                    "description": "광주와 가까운 생활권, 혁신도시 기반의 일자리와 생활 인프라가 강점",
                    "avg_house_price": 8500,
                    "infra_score": 92,
                    "nature_score": 72,
                    "farm_score": 68,
                    "smartfarm_score": 84,
                    "remote_score": 88,
                    "car_need": 45,
                    "youth_score": 80,
                    "senior_score": 70,
                },
                {
                    "region": "고흥군",
                    "description": "넓은 농지와 해안 자연환경, 스마트팜 혁신밸리와 우주산업 이미지 보유",
                    "avg_house_price": 6200,
                    "infra_score": 60,
                    "nature_score": 95,
                    "farm_score": 90,
                    "smartfarm_score": 96,
                    "remote_score": 62,
                    "car_need": 82,
                    "youth_score": 72,
                    "senior_score": 76,
                },
                {
                    "region": "담양군",
                    "description": "광주 접근성과 자연환경의 균형, 관광·로컬 비즈니스에 적합",
                    "avg_house_price": 7800,
                    "infra_score": 74,
                    "nature_score": 93,
                    "farm_score": 75,
                    "smartfarm_score": 70,
                    "remote_score": 78,
                    "car_need": 65,
                    "youth_score": 74,
                    "senior_score": 82,
                },
                {
                    "region": "해남군",
                    "description": "농업 기반이 탄탄하고 주거비가 낮은 편이나 차량 의존도가 높음",
                    "avg_house_price": 5300,
                    "infra_score": 55,
                    "nature_score": 89,
                    "farm_score": 95,
                    "smartfarm_score": 72,
                    "remote_score": 58,
                    "car_need": 88,
                    "youth_score": 68,
                    "senior_score": 80,
                },
                {
                    "region": "순천시",
                    "description": "정원·생태 도시 이미지와 비교적 우수한 생활 인프라를 함께 제공",
                    "avg_house_price": 9200,
                    "infra_score": 88,
                    "nature_score": 88,
                    "farm_score": 62,
                    "smartfarm_score": 66,
                    "remote_score": 86,
                    "car_need": 52,
                    "youth_score": 78,
                    "senior_score": 84,
                },
                {
                    "region": "영암군",
                    "description": "농업·제조업 기반이 있고 예산 부담이 낮지만 생활 인프라는 중간 수준",
                    "avg_house_price": 5700,
                    "infra_score": 58,
                    "nature_score": 78,
                    "farm_score": 88,
                    "smartfarm_score": 74,
                    "remote_score": 60,
                    "car_need": 80,
                    "youth_score": 70,
                    "senior_score": 74,
                },
            ]
        )
        region_features.to_csv(REGION_FILE, index=False, encoding="utf-8-sig")

    if not HOUSE_FILE.exists():
        house_list = pd.DataFrame(
            [
                {"region": "나주시", "title": "혁신도시 20분 농가주택", "price": 7800, "area": "대지 180평", "condition": "수리 필요", "tag": "생활권 우수"},
                {"region": "나주시", "title": "읍내 인근 단독주택", "price": 9500, "area": "대지 120평", "condition": "즉시 입주", "tag": "병원 가까움"},
                {"region": "고흥군", "title": "스마트팜 단지 인근 빈집", "price": 5200, "area": "대지 240평", "condition": "부분 수리", "tag": "농지 연계"},
                {"region": "고흥군", "title": "바다 조망 농가주택", "price": 6900, "area": "대지 210평", "condition": "수리 필요", "tag": "자연환경"},
                {"region": "담양군", "title": "메타세쿼이아길 인근 주택", "price": 8300, "area": "대지 150평", "condition": "양호", "tag": "관광 창업"},
                {"region": "담양군", "title": "마을 안쪽 소형 주택", "price": 6100, "area": "대지 95평", "condition": "부분 수리", "tag": "광주 접근"},
                {"region": "해남군", "title": "넓은 텃밭 포함 농가", "price": 4800, "area": "대지 300평", "condition": "수리 필요", "tag": "농업 최적"},
                {"region": "해남군", "title": "읍내 차량 10분 주택", "price": 5900, "area": "대지 170평", "condition": "양호", "tag": "저예산"},
                {"region": "순천시", "title": "정원마을 인근 단독주택", "price": 9800, "area": "대지 130평", "condition": "즉시 입주", "tag": "인프라"},
                {"region": "순천시", "title": "생태공원권 빈집", "price": 7600, "area": "대지 110평", "condition": "부분 수리", "tag": "자연+도시"},
                {"region": "영암군", "title": "월출산권 농가주택", "price": 5500, "area": "대지 220평", "condition": "수리 필요", "tag": "산림 경관"},
                {"region": "영암군", "title": "산단 접근 가능 주택", "price": 6400, "area": "대지 160평", "condition": "양호", "tag": "직업 전환"},
            ]
        )
        house_list.to_csv(HOUSE_FILE, index=False, encoding="utf-8-sig")

    if not POLICY_FILE.exists():
        policies = pd.DataFrame(
            [
                {"region": "공통", "policy": "귀농 창업 및 주택구입 지원", "summary": "요건 충족 시 창업 자금과 주택 구입 자금 융자 상담 가능"},
                {"region": "공통", "policy": "전남 귀농산어촌 정착 교육", "summary": "귀농 전 교육, 현장 실습, 멘토링 프로그램 연계"},
                {"region": "고흥군", "policy": "스마트팜 청년창업 보육", "summary": "스마트팜 관심자 대상 실습 중심 교육과 창업 연계"},
                {"region": "나주시", "policy": "혁신도시 연계 일자리 상담", "summary": "재택·전직 가능자를 위한 지역 일자리 정보 상담"},
                {"region": "담양군", "policy": "농촌 관광 창업 컨설팅", "summary": "카페, 체험농장, 로컬 브랜드 창업 상담"},
                {"region": "해남군", "policy": "농지 임대 및 작목 상담", "summary": "벼, 고구마, 배추 등 지역 작목 기반 정착 상담"},
                {"region": "순천시", "policy": "생태·정원 분야 창업 지원", "summary": "정원, 생태관광, 로컬 서비스 창업 상담"},
                {"region": "영암군", "policy": "농업·산업 일자리 연계", "summary": "농업 정착과 제조업 기반 일자리 병행 탐색"},
            ]
        )
        policies.to_csv(POLICY_FILE, index=False, encoding="utf-8-sig")


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """CSV 데이터를 읽어 화면과 추천 로직에서 사용할 DataFrame으로 반환합니다."""
    ensure_sample_data()
    regions = pd.read_csv(REGION_FILE)
    houses = pd.read_csv(HOUSE_FILE)
    policies = pd.read_csv(POLICY_FILE)
    return regions, houses, policies


def clamp(value: float, min_value: float = 0, max_value: float = 100) -> float:
    """점수가 0~100 범위를 벗어나지 않도록 보정합니다."""
    return max(min_value, min(max_value, value))


def calculate_region_score(row: pd.Series, profile: dict) -> tuple[float, list[str], list[str]]:
    """사용자 조건과 지역 특성을 비교해 적합도, 적합 요인, 비적합 요인을 계산합니다."""
    score = 50.0
    pros: list[str] = []
    cons: list[str] = []

    # 예산은 지역 평균 빈집 가격 대비 여유가 있을수록 가점합니다.
    budget_gap = profile["budget"] - row["avg_house_price"]
    if budget_gap >= 1500:
        score += 12
        pros.append("예산 대비 평균 주거비 여유가 있습니다.")
    elif budget_gap >= 0:
        score += 6
        pros.append("예산 안에서 주거 후보를 탐색할 수 있습니다.")
    else:
        penalty = min(18, abs(budget_gap) / 500)
        score -= penalty
        cons.append("평균 주거비가 예산보다 높아 초기 비용 부담이 있습니다.")

    # 차량이 없으면 차량 의존도가 높은 지역에 감점합니다.
    if profile["has_car"]:
        if row["car_need"] >= 75:
            score += 6
            pros.append("차량 보유로 외곽 마을 이동 부담이 낮습니다.")
    else:
        if row["car_need"] >= 75:
            score -= 15
            cons.append("차량 의존도가 높아 이동 편의성이 낮을 수 있습니다.")
        else:
            score += 5
            pros.append("차량이 없어도 생활권 접근성이 비교적 괜찮습니다.")

    # 재택근무 가능자는 원격근무 친화도와 생활 인프라를 함께 반영합니다.
    if profile["remote_work"]:
        remote_match = row["remote_score"] * 0.12 + row["infra_score"] * 0.05
        score += remote_match
        if row["remote_score"] >= 75:
            pros.append("재택근무와 병행하기 좋은 생활·통신 환경입니다.")
        else:
            cons.append("재택근무 생활권으로는 다소 한적할 수 있습니다.")

    # 관심도 입력은 0~10 슬라이더이므로 지역 점수와 곱해 영향도를 조절합니다.
    farm_weight = profile["farm_interest"] / 10
    smartfarm_weight = profile["smartfarm_interest"] / 10
    nature_weight = profile["nature_preference"] / 10
    infra_weight = profile["infra_importance"] / 10

    score += row["farm_score"] * farm_weight * 0.16
    score += row["smartfarm_score"] * smartfarm_weight * 0.14
    score += row["nature_score"] * nature_weight * 0.14
    score += row["infra_score"] * infra_weight * 0.16

    if farm_weight >= 0.7 and row["farm_score"] >= 80:
        pros.append("농업 기반과 작목 선택지가 풍부합니다.")
    if smartfarm_weight >= 0.7 and row["smartfarm_score"] >= 80:
        pros.append("스마트팜 관심도와 지역 자원이 잘 맞습니다.")
    if nature_weight >= 0.7 and row["nature_score"] >= 85:
        pros.append("자연환경 선호가 높은 사용자에게 매력적입니다.")
    if infra_weight >= 0.7 and row["infra_score"] < 65:
        cons.append("생활 인프라를 중요하게 본다면 불편함이 있을 수 있습니다.")
    elif infra_weight >= 0.7 and row["infra_score"] >= 80:
        pros.append("병원, 상권, 문화시설 접근성이 비교적 우수합니다.")

    # 연령대에 따라 청년 정착성 또는 은퇴 후 생활 안정성을 보정합니다.
    if profile["age"] < 40:
        score += row["youth_score"] * 0.08
        if row["youth_score"] >= 75:
            pros.append("청년 정착·창업 관점의 기회가 있습니다.")
    elif profile["age"] >= 55:
        score += row["senior_score"] * 0.08
        if row["senior_score"] >= 78:
            pros.append("은퇴 후 안정적인 생활 기반을 만들기 좋습니다.")

    # 직업 유형별 현실적인 정착 관점을 소폭 반영합니다.
    job = profile["job"]
    if job == "농업/축산 경험자":
        score += row["farm_score"] * 0.08
        pros.append("기존 농업 경험을 활용하기 쉽습니다.")
    elif job == "IT/사무직":
        score += row["remote_score"] * 0.07
        if row["remote_score"] < 65:
            cons.append("IT/사무직 병행에는 원격근무 여건 확인이 필요합니다.")
    elif job == "자영업/창업 희망":
        score += (row["infra_score"] + row["nature_score"]) * 0.04
        pros.append("로컬 창업 아이템을 검토할 수 있습니다.")

    # 카드가 비어 보이지 않도록 기본 요인을 보충합니다.
    if not pros:
        pros.append("입력 조건과 전반적으로 무난하게 맞는 지역입니다.")
    if not cons:
        cons.append("큰 비적합 요인은 적지만 실제 방문 확인이 필요합니다.")

    return round(clamp(score), 1), pros[:4], cons[:3]


def build_recommendations(regions: pd.DataFrame, profile: dict) -> pd.DataFrame:
    """모든 지역의 점수를 계산하고 TOP3 추천 목록을 만듭니다."""
    scored_rows = []
    for _, row in regions.iterrows():
        score, pros, cons = calculate_region_score(row, profile)
        item = row.to_dict()
        item.update({"score": score, "pros": pros, "cons": cons})
        scored_rows.append(item)

    return pd.DataFrame(scored_rows).sort_values("score", ascending=False).head(3)


def dummy_ai_response(question_type: str, region: str, profile: dict) -> str:
    """Claude API 연결 전까지 사용할 더미 AI 상담 응답입니다."""
    responses = {
        "정착 로드맵": f"{region} 정착은 1단계 현장 방문, 2단계 빈집·농지 확인, 3단계 정책 상담 순서로 진행하는 것이 좋습니다.",
        "예산 점검": f"현재 예산 {profile['budget']:,}만원 기준으로 매입가, 수리비, 6개월 생활비를 분리해 검토해보세요.",
        "농업 아이템": f"{region}에서는 지역 작목, 스마트팜 가능성, 판로 접근성을 함께 비교해 초기 작목을 고르는 것이 좋습니다.",
        "빈집 체크": "등기, 도로 접근, 상하수도, 누수, 전기 용량, 수리 견적을 현장 방문 때 우선 확인하세요.",
        "정책 상담": f"{region} 담당 부서와 전남 귀농산어촌 종합지원센터 상담을 연결하는 흐름으로 안내할 수 있습니다.",
    }
    return responses[question_type]


def render_metric_card(title: str, value: str, caption: str) -> None:
    """간단한 카드형 지표를 HTML로 렌더링합니다."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_house_cards(houses: pd.DataFrame, region: str, budget: int) -> None:
    """선택 지역의 빈집 후보를 예산 적합 순서로 보여줍니다."""
    region_houses = houses[houses["region"] == region].copy()
    region_houses["budget_gap"] = budget - region_houses["price"]
    region_houses = region_houses.sort_values(["budget_gap", "price"], ascending=[False, True]).head(2)

    if region_houses.empty:
        st.info("현재 샘플 데이터에는 해당 지역의 빈집 후보가 없습니다.")
        return

    cols = st.columns(len(region_houses))
    for col, (_, house) in zip(cols, region_houses.iterrows()):
        with col:
            price_note = "예산 내" if house["price"] <= budget else "예산 초과"
            st.markdown(
                f"""
                <div class="house-card">
                    <div class="chip">{house['tag']}</div>
                    <h4>{house['title']}</h4>
                    <p><b>{house['price']:,}만원</b> · {price_note}</p>
                    <p>{house['area']} · {house['condition']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_policy_notes(policies: pd.DataFrame, region: str) -> None:
    """지역별 및 공통 정책 정보를 간단히 표시합니다."""
    matched = policies[(policies["region"] == "공통") | (policies["region"] == region)].head(4)
    for _, policy in matched.iterrows():
        st.markdown(f"- **{policy['policy']}**: {policy['summary']}")


def main() -> None:
    """Streamlit 앱 진입점입니다."""
    st.set_page_config(page_title=APP_TITLE, page_icon="🧭", layout="wide")
    regions, houses, policies = load_data()

    st.markdown(
        """
        <style>
        .main-title {font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem;}
        .subtle {color: #5f6b7a; margin-bottom: 1.2rem;}
        .metric-card, .region-card, .house-card {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            background: #ffffff;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
        }
        .metric-title {font-size: 0.86rem; color: #64748b;}
        .metric-value {font-size: 1.35rem; font-weight: 800; color: #0f172a; margin-top: 0.2rem;}
        .metric-caption {font-size: 0.82rem; color: #64748b; margin-top: 0.25rem;}
        .region-card {margin-bottom: 1rem;}
        .rank {font-size: 0.82rem; color: #2563eb; font-weight: 700;}
        .score {font-size: 1.9rem; font-weight: 900; color: #166534;}
        .chip {
            display: inline-block;
            border-radius: 999px;
            padding: 0.18rem 0.55rem;
            background: #eef2ff;
            color: #3730a3;
            font-size: 0.76rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }
        .house-card h4 {margin: 0.15rem 0 0.4rem 0;}
        .house-card p {margin: 0.25rem 0; color: #475569;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 사이드바 입력폼
    # -----------------------------------------------------------------------
    with st.sidebar:
        st.header("나의 정착 조건")
        age = st.number_input("나이", min_value=19, max_value=90, value=42, step=1)
        job = st.selectbox(
            "직업",
            ["IT/사무직", "농업/축산 경험자", "자영업/창업 희망", "은퇴 예정/은퇴자", "기타"],
        )
        budget = st.slider("예산", min_value=3000, max_value=15000, value=8000, step=500, help="단위: 만원")
        has_car = st.toggle("차량 보유 여부", value=True)
        remote_work = st.toggle("재택근무 가능 여부", value=True)
        farm_interest = st.slider("농업 관심도", 0, 10, 6)
        smartfarm_interest = st.slider("스마트팜 관심도", 0, 10, 5)
        nature_preference = st.slider("자연환경 선호도", 0, 10, 8)
        infra_importance = st.slider("생활 인프라 중요도", 0, 10, 7)

    profile = {
        "age": age,
        "job": job,
        "budget": budget,
        "has_car": has_car,
        "remote_work": remote_work,
        "farm_interest": farm_interest,
        "smartfarm_interest": smartfarm_interest,
        "nature_preference": nature_preference,
        "infra_importance": infra_importance,
    }

    recommendations = build_recommendations(regions, profile)
    top_region = recommendations.iloc[0]["region"]

    # -----------------------------------------------------------------------
    # 본문: 사용자 요약과 추천 결과
    # -----------------------------------------------------------------------
    st.markdown(f'<div class="main-title">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtle">내 조건에 맞는 전남 귀농·귀촌 정착 후보지를 빠르게 비교하는 MVP입니다.</div>',
        unsafe_allow_html=True,
    )

    st.subheader("사용자 요약")
    summary_cols = st.columns(4)
    with summary_cols[0]:
        render_metric_card("나이 / 직업", f"{age}세", job)
    with summary_cols[1]:
        render_metric_card("주거 예산", f"{budget:,}만원", "빈집 매입·수리비 검토 기준")
    with summary_cols[2]:
        car_text = "차량 있음" if has_car else "차량 없음"
        remote_text = "재택 가능" if remote_work else "재택 어려움"
        render_metric_card("이동 / 근무", car_text, remote_text)
    with summary_cols[3]:
        render_metric_card("관심 키워드", f"농업 {farm_interest}/10", f"스마트팜 {smartfarm_interest}/10")

    st.divider()

    st.subheader("추천 지역 TOP3")
    for rank, (_, region) in enumerate(recommendations.iterrows(), start=1):
        col_info, col_factors = st.columns([1.05, 1.4])
        with col_info:
            st.markdown(
                f"""
                <div class="region-card">
                    <div class="rank">TOP {rank}</div>
                    <h3>{region['region']}</h3>
                    <div class="score">{region['score']}점</div>
                    <p>{region['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_factors:
            st.markdown("**적합 요인**")
            for pro in region["pros"]:
                st.success(pro)
            st.markdown("**비적합 요인**")
            for con in region["cons"]:
                st.warning(con)

        with st.expander(f"{region['region']} 빈집 후보와 정책 보기", expanded=(rank == 1)):
            st.markdown("**빈집 후보**")
            render_house_cards(houses, region["region"], budget)
            st.markdown("**연계 가능 정책**")
            render_policy_notes(policies, region["region"])

    st.divider()

    # -----------------------------------------------------------------------
    # 더미 AI 상담 영역: 실제 Claude API 연결 전 UI/흐름 검증용입니다.
    # -----------------------------------------------------------------------
    st.subheader("AI 상담")
    selected_region = st.selectbox("상담할 지역", recommendations["region"].tolist(), index=0)
    st.caption("현재는 Claude API 미연결 상태이므로 더미 응답을 표시합니다.")

    button_cols = st.columns(5)
    question_types = ["정착 로드맵", "예산 점검", "농업 아이템", "빈집 체크", "정책 상담"]
    for col, question_type in zip(button_cols, question_types):
        with col:
            if st.button(question_type, use_container_width=True):
                st.session_state["ai_answer"] = dummy_ai_response(question_type, selected_region, profile)

    if "ai_answer" not in st.session_state:
        st.session_state["ai_answer"] = dummy_ai_response("정착 로드맵", top_region, profile)

    st.info(st.session_state["ai_answer"])


if __name__ == "__main__":
    main()
