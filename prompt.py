SYSTEM_PROMPT = """
당신은 전남 귀농·귀촌 의사결정을 돕는 분석 도우미입니다.
추천 결과를 바탕으로 사용자가 다음 현장 확인과 정책 상담을 준비할 수 있게 설명하세요.

반드시 지킬 원칙:
- 추천 지역 TOP3 요약, 지역별 추천 이유, 주의사항, 연결 가능한 지원정책, 현실적인 정착 조언을 포함합니다.
- 과장된 효과나 보장 표현을 쓰지 않습니다.
- "지역소멸을 해결한다" 같은 표현은 피하고 "귀농·귀촌 의사결정 지원" 관점으로 설명합니다.
- 실제 정책 신청 가능 여부는 지자체 공고와 담당 부서 확인이 필요하다고 안내합니다.
- 한국어로 작성하고, 읽기 쉽게 구분합니다.
"""


def _format_profile(user_profile: dict) -> str:
    if not user_profile:
        return "- 입력 조건 없음"
    return "\n".join(f"- {key}: {value}" for key, value in user_profile.items())


def _format_policy(policy: dict) -> str:
    return (
        f"{policy.get('policy_name', '정책명 없음')} "
        f"({policy.get('category', '분류 없음')}) - "
        f"대상: {policy.get('target', '확인 필요')}, "
        f"혜택: {policy.get('benefit', '확인 필요')}, "
        f"URL: {policy.get('apply_url', '확인 필요')}"
    )


def _format_region(region: dict, rank: int) -> str:
    policies = region.get("related_policies", []) or []
    policy_text = "\n".join(f"    - {_format_policy(policy)}" for policy in policies)
    if not policy_text:
        policy_text = "    - 연결 정책 정보 없음"

    return f"""
+{rank}. {region.get('region', '지역명 없음')}
+  - 추천 점수: {region.get('score', 'N/A')}
+  - 적합 확률: {region.get('probability', 'N/A')}
+  - 지역 설명: {region.get('description', '설명 없음')}
+  - 추천 근거: {region.get('matched_reason', region.get('reason_features', '근거 없음'))}
+  - 주의사항: {region.get('risk_note', '현장 확인 필요')}
+  - 연결 가능한 지원정책:
+{policy_text}
+""".strip()


def build_prompt(user_profile: dict, top_regions) -> str:
    if hasattr(top_regions, "to_dict"):
        region_rows = top_regions.to_dict("records")
    else:
        region_rows = list(top_regions)

    region_text = "\n\n".join(
        _format_region(region, rank) for rank, region in enumerate(region_rows, start=1)
    )

    return f"""
사용자 입력 조건:
{_format_profile(user_profile)}

추천 지역 TOP3 데이터:
{region_text}

작성할 내용:
1. 추천 지역 TOP3를 한눈에 요약합니다.
2. 각 지역이 사용자 조건과 맞는 이유를 설명합니다.
3. 각 지역별로 실제 확인해야 할 주의사항을 설명합니다.
4. 연결 가능한 지원정책을 지역별로 정리합니다.
5. 최종 결정 전 현장 방문, 예산 점검, 정책 자격 확인 등 현실적인 정착 조언을 제시합니다.

표현 가이드:
- "지역소멸 해결"처럼 성과를 과장하지 마세요.
- 이 서비스는 귀농·귀촌 의사결정 지원 서비스라는 관점으로 설명하세요.
- 추천은 참고용이며 최종 결정에는 현장 확인이 필요하다고 안내하세요.
""".strip()
