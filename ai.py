from __future__ import annotations

import os

from prompt import SYSTEM_PROMPT, build_prompt


try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass


def _as_records(top_regions) -> list[dict]:
    if hasattr(top_regions, "to_dict"):
        return top_regions.to_dict("records")
    return list(top_regions)


def mock_response(user_profile: dict, top_regions) -> str:
    regions = _as_records(top_regions)
    if not regions:
        return "추천 결과가 없어 설명을 생성할 수 없습니다. 입력 조건과 지역 데이터를 다시 확인해 주세요."

    lines = ["추천 TOP3 요약"]
    for index, region in enumerate(regions[:3], start=1):
        policies = region.get("related_policies", []) or []
        policy_names = ", ".join(policy.get("policy_name", "정책명 확인 필요") for policy in policies[:2])
        if not policy_names:
            policy_names = "연결 정책 정보 확인 필요"
        lines.append(
            f"{index}. {region.get('region')} - 적합 확률 {region.get('probability')}, "
            f"추천 이유는 {region.get('matched_reason')}"
        )
        lines.append(f"   주의사항: {region.get('risk_note')}")
        lines.append(f"   연결 정책: {policy_names}")

    lines.append(
        "정착 조언: 추천 결과는 귀농·귀촌 의사결정을 돕기 위한 참고 자료입니다. "
        "최종 결정 전에는 최소 1회 이상 현장 방문을 하고, 주거비와 이동 동선, 의료 접근성, 정책 신청 자격을 지자체 담당 부서에 확인하는 것이 좋습니다."
    )
    return "\n".join(lines)


def generate_ai_explanation(user_profile: dict, top_regions) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return mock_response(user_profile, top_regions)

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
            max_tokens=1200,
            temperature=0.2,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_prompt(user_profile, top_regions)}],
        )
        return response.content[0].text
    except Exception as exc:
        return (
            "Claude API 호출에 실패해 mock 응답을 표시합니다.\n\n"
            f"{mock_response(user_profile, top_regions)}\n\n"
            f"오류 내용: {exc}"
        )


# 이전 단계 app.py와의 임시 호환용 래퍼입니다.
def ask_claude(user_profile: dict, recommendations, question: str | None = None) -> str:
    return generate_ai_explanation(user_profile, recommendations)
