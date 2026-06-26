from pathlib import Path

import pandas as pd
import streamlit as st


APP_TITLE = "전남 귀촌 Compass"
DATA_DIR = Path("data")
REGION_FILE = DATA_DIR / "region_features.csv"
HOUSE_FILE = DATA_DIR / "house_list.csv"
POLICY_FILE = DATA_DIR / "policies.csv"


def ensure_sample_data() -> None:
    """시연용 CSV가 없을 때 바로 실행 가능한 샘플 데이터를 생성합니다."""
    DATA_DIR.mkdir(exist_ok=True)

    if not REGION_FILE.exists():
        pd.DataFrame(
            [
                ["나주시", "광주 접근성과 생활 인프라가 좋은 균형형 후보지", 8500, 92, 72, 68, 84, 88, 45, 80, 70],
                ["고흥군", "바다와 자연환경, 스마트팜 자원이 강한 후보지", 6200, 60, 95, 90, 96, 62, 82, 72, 76],
                ["담양군", "광주 접근성과 자연환경이 좋아 관광 창업에 어울리는 지역", 7800, 74, 93, 75, 70, 78, 65, 74, 82],
                ["해남군", "낮은 주거비와 넓은 농지 기반이 강점인 지역", 5300, 55, 89, 95, 72, 58, 88, 68, 80],
                ["순천시", "정원, 생태, 생활 인프라를 함께 갖춘 안정형 후보지", 9200, 88, 88, 62, 66, 86, 52, 78, 84],
                ["영암군", "산업 일자리와 농업 기반을 함께 볼 수 있는 저예산 후보지", 5700, 58, 78, 88, 74, 60, 80, 70, 74],
            ],
            columns=[
                "region",
                "description",
                "avg_house_price",
                "infra_score",
                "nature_score",
                "farm_score",
                "smartfarm_score",
                "remote_score",
                "car_need",
                "youth_score",
                "senior_score",
            ],
        ).to_csv(REGION_FILE, index=False, encoding="utf-8-sig")

    if not HOUSE_FILE.exists():
        pd.DataFrame(
            [
                ["나주시", "혁신도시 20분권 단독주택", 7800, "대지 180평", "수리 필요", "생활권"],
                ["나주시", "읍내 인근 소형 주택", 9500, "대지 120평", "즉시 입주", "병원 근접"],
                ["고흥군", "스마트팜 단지 인근 빈집", 5200, "대지 240평", "부분 수리", "농지 연계"],
                ["고흥군", "바다 조망 단독주택", 6900, "대지 210평", "수리 필요", "자연환경"],
                ["담양군", "관광지 인근 소형 주택", 8300, "대지 150평", "양호", "창업"],
                ["담양군", "마을 안쪽 단독주택", 6100, "대지 95평", "부분 수리", "광주 접근"],
                ["해남군", "넓은 텃밭 포함 농가", 4800, "대지 300평", "수리 필요", "농업"],
                ["해남군", "읍내 차량 10분 주택", 5900, "대지 170평", "양호", "저예산"],
                ["순천시", "정원마을 인근 단독주택", 9800, "대지 130평", "즉시 입주", "인프라"],
                ["순천시", "생태공원권 빈집", 7600, "대지 110평", "부분 수리", "생태"],
                ["영암군", "귀촌 예정 농가주택", 5500, "대지 220평", "수리 필요", "농림"],
                ["영암군", "산단 접근 가능 주택", 6400, "대지 160평", "양호", "직업 전환"],
            ],
            columns=["region", "title", "price", "area", "condition", "tag"],
        ).to_csv(HOUSE_FILE, index=False, encoding="utf-8-sig")

    if not POLICY_FILE.exists():
        pd.DataFrame(
            [
                ["공통", "귀농·귀촌 종합상담", "주거, 교육, 자금, 농지 탐색을 한 번에 상담"],
                ["공통", "농업 교육 및 현장 실습", "기초 영농 교육과 멘토링 프로그램 연계"],
                ["고흥군", "스마트팜 청년창업 보육", "스마트팜 실습과 창업 준비를 지원"],
                ["나주시", "혁신도시 연계 일자리 상담", "전직, 원격근무, 생활권 정착 정보 제공"],
                ["담양군", "관광 창업 컨설팅", "카페, 체험농장, 로컬 브랜드 창업 상담"],
                ["해남군", "농지 임대 및 작목 상담", "지역 작목 기반 농업 정착 상담"],
                ["순천시", "생태·정원 분야 창업 지원", "정원, 생태관광, 로컬 서비스 창업 연계"],
                ["영암군", "농업·산업 일자리 연계", "농업 정착과 제조업 일자리 병행 탐색"],
            ],
            columns=["region", "policy", "summary"],
        ).to_csv(POLICY_FILE, index=False, encoding="utf-8-sig")


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ensure_sample_data()
    return pd.read_csv(REGION_FILE), pd.read_csv(HOUSE_FILE), pd.read_csv(POLICY_FILE)


def calculate_region_score(row: pd.Series, profile: dict) -> tuple[float, list[str], list[str]]:
    score = 35.0
    pros: list[str] = []
    cons: list[str] = []

    budget_gap = profile["budget"] - row["avg_house_price"]
    if budget_gap >= 1500:
        score += 12
        pros.append("예산 대비 평균 주거비 여유가 있습니다.")
    elif budget_gap >= 0:
        score += 6
        pros.append("예산 안에서 주거 후보를 찾을 가능성이 있습니다.")
    else:
        score -= min(18, abs(budget_gap) / 500)
        cons.append("평균 주거비가 예산보다 높아 초기 비용 부담이 있습니다.")

    if profile["has_car"] and row["car_need"] >= 75:
        score += 6
        pros.append("차량이 있으면 마을 간 이동 부담이 낮습니다.")
    elif not profile["has_car"] and row["car_need"] >= 75:
        score -= 15
        cons.append("차량 의존도가 높아 실제 이동 동선을 확인해야 합니다.")
    elif not profile["has_car"]:
        score += 5
        pros.append("차량 없이도 생활권 접근성이 비교적 괜찮습니다.")

    if profile["remote_work"]:
        score += row["remote_score"] * 0.08 + row["infra_score"] * 0.03
        if row["remote_score"] >= 75:
            pros.append("원격근무와 병행하기 좋은 생활·통신 환경입니다.")
        else:
            cons.append("원격근무 생활권으로는 다소 제약이 있을 수 있습니다.")

    score += row["farm_score"] * (profile["farm_interest"] / 10) * 0.11
    score += row["smartfarm_score"] * (profile["smartfarm_interest"] / 10) * 0.10
    score += row["nature_score"] * (profile["nature_preference"] / 10) * 0.10
    score += row["infra_score"] * (profile["infra_importance"] / 10) * 0.11

    if profile["farm_interest"] >= 7 and row["farm_score"] >= 80:
        pros.append("농업 기반과 작목 선택지가 넓습니다.")
    if profile["smartfarm_interest"] >= 7 and row["smartfarm_score"] >= 80:
        pros.append("스마트팜 관련 자원을 활용하기 좋습니다.")
    if profile["nature_preference"] >= 7 and row["nature_score"] >= 85:
        pros.append("자연환경 선호가 높은 사용자에게 매력적입니다.")
    if profile["infra_importance"] >= 7 and row["infra_score"] < 65:
        cons.append("생활 인프라를 중요하게 본다면 불편할 수 있습니다.")
    elif profile["infra_importance"] >= 7 and row["infra_score"] >= 80:
        pros.append("병원, 상권, 문화시설 접근성이 좋은 편입니다.")

    if profile["age"] < 40:
        score += row["youth_score"] * 0.05
    elif profile["age"] >= 55:
        score += row["senior_score"] * 0.05

    if profile["job"] == "농업/축산 경험자":
        score += row["farm_score"] * 0.05
        pros.append("기존 농업 경험을 활용하기 좋습니다.")
    elif profile["job"] == "IT/사무직":
        score += row["remote_score"] * 0.04
    elif profile["job"] == "자영업/창업 희망":
        score += (row["infra_score"] + row["nature_score"]) * 0.03
        pros.append("로컬 창업 아이템을 검토하기 좋습니다.")

    if not pros:
        pros.append("입력 조건과 전반적으로 무난하게 맞는 지역입니다.")
    if not cons:
        cons.append("큰 위험 요인은 적지만 실제 방문 확인은 필요합니다.")
    return round(max(0, min(100, score)), 1), pros[:4], cons[:3]


def build_recommendations(regions: pd.DataFrame, profile: dict) -> pd.DataFrame:
    rows = []
    for _, row in regions.iterrows():
        score, pros, cons = calculate_region_score(row, profile)
        item = row.to_dict()
        item.update({"score": score, "pros": pros, "cons": cons})
        rows.append(item)
    return pd.DataFrame(rows).sort_values("score", ascending=False).head(3)


def make_ai_reply(user_text: str, region: str, profile: dict, recommendations: pd.DataFrame) -> str:
    top = recommendations.iloc[0]
    if "예산" in user_text or "비용" in user_text:
        return (
            f"{region} 기준으로 주택 매입가, 수리비, 6개월 생활비를 분리해서 보세요. "
            f"현재 예산은 {profile['budget']:,}만원이고, 1순위 {top['region']}의 평균 주거비는 "
            f"{int(top['avg_house_price']):,}만원입니다."
        )
    if "빈집" in user_text or "집" in user_text:
        return "빈집은 사진보다 등기, 도로 접근, 상하수도, 전기 용량, 수리 견적을 먼저 확인하는 것이 좋습니다."
    if "농업" in user_text or "스마트팜" in user_text or "작목" in user_text:
        return f"{region}에서는 관심도 기준으로 농업 {profile['farm_interest']}/10, 스마트팜 {profile['smartfarm_interest']}/10에 맞춰 작목과 교육 과정을 함께 비교해보세요."
    if "정책" in user_text or "지원" in user_text:
        return f"{region} 담당 부서나 전남 귀농산어촌 종합지원센터 상담을 먼저 잡는 흐름을 추천합니다. 교육 이수, 거주 요건, 자금 한도를 미리 정리해두면 좋습니다."
    return f"현재 조건에서는 {top['region']}이 {top['score']}점으로 가장 높습니다. 예산, 빈집, 농업 아이템, 정책 지원 중 하나를 더 구체적으로 물어보세요."


def apply_design() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg:#f7f8f3;
            --panel:#ffffff;
            --ink:#202124;
            --muted:#6b7280;
            --line:#d9ded3;
            --green:#3f7d58;
            --green-soft:#edf6ee;
            --red-soft:#fff2ef;
        }
        html, body, [data-testid="stAppViewContainer"] { background:var(--bg); color:var(--ink); }
        [data-testid="stHeader"] { background:transparent; }
        [data-testid="stSidebar"] { background:#eef3ea; border-right:1px solid var(--line); }
        .block-container { max-width:1180px; padding-top:1.4rem; padding-bottom:3rem; }
        h1, h2, h3, h4, p { letter-spacing:0; }
        .intro { padding:22px 0 14px; border-bottom:1px solid var(--line); margin-bottom:18px; }
        .intro h1 { font-size:clamp(2rem,4vw,3.4rem); line-height:1.08; margin:0 0 10px; font-weight:800; }
        .intro p { max-width:760px; color:var(--muted); line-height:1.65; margin:0; font-size:1.02rem; }
        .badge { display:inline-block; background:var(--green-soft); color:var(--green); border:1px solid #c9dfcd; border-radius:999px; padding:5px 10px; font-weight:700; font-size:.82rem; margin-bottom:12px; }
        .summary-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin:18px 0 8px; }
        .summary-item, .rank-card, .factor-box, .house-card, .policy-card, .chat-shell { background:var(--panel); border:1px solid var(--line); border-radius:8px; box-shadow:0 1px 2px rgba(20,30,20,.04); }
        .summary-item { padding:14px; }
        .summary-item span { display:block; color:var(--muted); font-size:.8rem; margin-bottom:4px; }
        .summary-item b { font-size:1.05rem; }
        .section-label { margin:26px 0 10px; color:var(--green); font-weight:800; font-size:.95rem; }
        .rank-card { display:grid; grid-template-columns:36px 1fr 52px; gap:10px; align-items:center; padding:13px; margin-bottom:10px; }
        .rank-card.primary { border-color:#9fc7a8; background:var(--green-soft); }
        .rank-no { color:var(--green); font-weight:800; }
        .rank-name { font-weight:800; }
        .rank-desc { color:var(--muted); font-size:.82rem; margin-top:2px; }
        .rank-score { text-align:right; font-weight:800; }
        .result-note { background:#243528; color:white; border-radius:8px; padding:16px; margin-bottom:12px; line-height:1.55; }
        .result-note b, .result-note .score { color:#bfe8c5; }
        .factor-grid, .card-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }
        .card-grid { grid-template-columns:repeat(3,minmax(0,1fr)); }
        .factor-box, .house-card, .policy-card { padding:15px; }
        .factor-box.good { background:var(--green-soft); }
        .factor-box.bad { background:var(--red-soft); }
        .factor-box h4, .house-card h4, .policy-card h4 { margin:0 0 8px; font-size:.98rem; }
        .factor-box ul { margin:0; padding-left:18px; }
        .factor-box li { margin:5px 0; }
        .tag { display:inline-block; border-radius:999px; background:#f3f4f0; color:#4b5563; padding:3px 8px; margin-bottom:8px; font-size:.78rem; font-weight:700; }
        .price { font-size:1.18rem; font-weight:850; margin-bottom:6px; }
        .chat-shell { padding:16px; margin-top:12px; }
        .chat-shell h3 { margin:0 0 6px; font-size:1.05rem; }
        .chat-shell p { color:var(--muted); margin:0; }
        .stButton > button { border:1px solid var(--line); border-radius:8px; background:white; color:var(--ink); font-weight:700; }
        .stButton > button:hover { border-color:#9fc7a8; color:var(--green); background:var(--green-soft); }
        @media (max-width:900px) { .summary-grid, .factor-grid, .card-grid { grid-template-columns:1fr; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_intro(recommendations: pd.DataFrame) -> None:
    top = recommendations.iloc[0]
    st.markdown(
        f"""
        <section class="intro">
            <div class="badge">1박 2일 해커톤 MVP</div>
            <h1>전남 귀촌 후보지를<br>조건에 맞춰 빠르게 좁혀보세요</h1>
            <p>
                예산, 차량 여부, 원격근무 가능성, 농업·스마트팜 관심도를 바탕으로
                추천 지역 TOP3와 확인해야 할 리스크를 보여줍니다.
                현재 조건의 1순위는 <b>{top['region']}</b>, 적합도는 <b>{top['score']}점</b>입니다.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_profile(profile: dict, top_region: str) -> None:
    car_text = "차량 있음" if profile["has_car"] else "차량 없음"
    remote_text = "원격 가능" if profile["remote_work"] else "원격 어려움"
    st.markdown(
        f"""
        <div class="summary-grid">
            <div class="summary-item"><span>나이 / 직업</span><b>{profile['age']}세</b><br>{profile['job']}</div>
            <div class="summary-item"><span>정착 예산</span><b>{profile['budget']:,}만원</b><br>주택·수리 기준</div>
            <div class="summary-item"><span>이동 / 근무</span><b>{car_text}</b><br>{remote_text}</div>
            <div class="summary-item"><span>현재 1순위</span><b>{top_region}</b><br>추천 TOP3 기준</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendations(recommendations: pd.DataFrame) -> str:
    selected_region = st.session_state.get("selected_region", recommendations.iloc[0]["region"])
    if selected_region not in recommendations["region"].tolist():
        selected_region = recommendations.iloc[0]["region"]
    selected = recommendations[recommendations["region"] == selected_region].iloc[0]

    st.markdown('<div class="section-label">추천 결과</div>', unsafe_allow_html=True)
    rank_col, detail_col = st.columns([0.9, 1.6], gap="large")
    with rank_col:
        st.markdown("### TOP 3 지역")
        for rank, (_, region) in enumerate(recommendations.iterrows(), start=1):
            if st.button(
                f"{rank}위 · {region['region']} · {region['score']}점",
                key=f"select-{region['region']}",
                use_container_width=True,
            ):
                st.session_state["selected_region"] = region["region"]
                st.rerun()
            card_class = "rank-card primary" if selected_region == region["region"] else "rank-card"
            desc = "선택된 지역" if selected_region == region["region"] else region["description"]
            st.markdown(
                f"""
                <div class="{card_class}">
                    <div class="rank-no">{rank}</div>
                    <div><div class="rank-name">{region['region']}</div><div class="rank-desc">{desc}</div></div>
                    <div class="rank-score">{region['score']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with detail_col:
        good_items = "".join(f"<li>{item}</li>" for item in selected["pros"])
        bad_items = "".join(f"<li>{item}</li>" for item in selected["cons"])
        st.markdown(
            f"""
            <div class="result-note">
                <b>{selected['region']}</b>은 현재 조건에서
                <span class="score">{selected['score']}점</span>입니다. {selected['description']}
            </div>
            <div class="factor-grid">
                <div class="factor-box good"><h4>잘 맞는 이유</h4><ul>{good_items}</ul></div>
                <div class="factor-box bad"><h4>확인할 점</h4><ul>{bad_items}</ul></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    return selected_region


def render_house_cards(houses: pd.DataFrame, region: str, budget: int) -> None:
    region_houses = houses[houses["region"] == region].copy()
    region_houses["budget_gap"] = budget - region_houses["price"]
    region_houses = region_houses.sort_values(["budget_gap", "price"], ascending=[False, True]).head(3)
    st.markdown('<div class="section-label">주택 후보</div>', unsafe_allow_html=True)
    cards = []
    for _, house in region_houses.iterrows():
        budget_note = "예산 안" if house["price"] <= budget else "예산 초과"
        cards.append(
            f"""
            <div class="house-card">
                <div class="tag">{house['tag']}</div>
                <h4>{house['title']}</h4>
                <div class="price">{house['price']:,}만원</div>
                <p>{house['area']} · {house['condition']} · {budget_note}</p>
            </div>
            """
        )
    st.markdown(f'<div class="card-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def render_policy_cards(policies: pd.DataFrame, region: str) -> None:
    matched = policies[(policies["region"] == "공통") | (policies["region"] == region)].head(3)
    cards = [
        f"""
        <div class="policy-card">
            <div class="tag">{row['region']}</div>
            <h4>{row['policy']}</h4>
            <p>{row['summary']}</p>
        </div>
        """
        for _, row in matched.iterrows()
    ]
    st.markdown('<div class="section-label">정책 연결</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def render_chatbot(selected_region: str, profile: dict, recommendations: pd.DataFrame) -> None:
    st.markdown('<div class="section-label">상담 시뮬레이션</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="chat-shell">
            <h3>귀촌 준비 질문</h3>
            <p>해커톤 버전에서는 규칙 기반 답변으로 구현하고, 이후 Claude API 연결 영역으로 확장할 수 있습니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": f"{selected_region} 기준으로 예산, 빈집, 농업 아이템, 정책 지원을 질문해보세요."}
        ]

    quick_prompts = ["정착 로드맵 알려줘", "예산은 어떻게 나눌까?", "빈집 볼 때 확인할 점", "농업 아이템 추천", "정책 지원 알려줘"]
    for col, prompt in zip(st.columns(5), quick_prompts):
        with col:
            if st.button(prompt, key=f"quick-{prompt}", use_container_width=True):
                st.session_state["chat_messages"].append({"role": "user", "content": prompt})
                st.session_state["chat_messages"].append(
                    {"role": "assistant", "content": make_ai_reply(prompt, selected_region, profile, recommendations)}
                )
                st.rerun()

    for message in st.session_state["chat_messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("예: 고흥군에서 스마트팜으로 시작하려면?")
    if user_message:
        st.session_state["chat_messages"].append({"role": "user", "content": user_message})
        st.session_state["chat_messages"].append(
            {"role": "assistant", "content": make_ai_reply(user_message, selected_region, profile, recommendations)}
        )
        st.rerun()


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="compass", layout="wide")
    regions, houses, policies = load_data()
    apply_design()

    with st.sidebar:
        st.header("조건 입력")
        age = st.number_input("나이", min_value=19, max_value=90, value=42, step=1)
        job = st.selectbox("직업", ["IT/사무직", "농업/축산 경험자", "자영업/창업 희망", "은퇴 예정/은퇴자", "기타"])
        budget = st.slider("예산", min_value=3000, max_value=15000, value=8000, step=500, help="단위: 만원")
        has_car = st.toggle("차량 보유", value=True)
        remote_work = st.toggle("원격근무 가능", value=True)
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

    render_intro(recommendations)
    render_profile(profile, top_region)
    selected_region = render_recommendations(recommendations)
    render_house_cards(houses, selected_region, budget)
    render_policy_cards(policies, selected_region)
    render_chatbot(selected_region, profile, recommendations)


if __name__ == "__main__":
    main()
