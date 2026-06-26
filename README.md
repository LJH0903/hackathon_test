# 전남 귀농·귀촌 의사결정 지원 서비스

사용자 조건을 입력받아 전남 시군 중 귀농·귀촌 적합 지역 TOP3를 추천하는 Streamlit MVP입니다.

## 주요 기능

- 예산, 차량 보유, 이주 목적, 농업 관심도, 원격근무 필요 여부 입력
- CSV 기반 전남 22개 시군 지표 로드
- scikit-learn Logistic Regression 기반 기본 적합도 계산
- 사용자 조건 기반 가중 점수로 TOP3 추천
- 추천 지역별 강점, 주의점, 연계 정책 표시
- Claude API 키가 있으면 AI 상담 답변 생성
- API 키가 없으면 기본 규칙 기반 답변으로 동작

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

Claude API를 사용하려면 환경변수를 설정합니다.

```bash
set ANTHROPIC_API_KEY=your_api_key
```

PowerShell에서는 다음처럼 설정할 수 있습니다.

```powershell
$env:ANTHROPIC_API_KEY="your_api_key"
```

## 프로젝트 구조

```text
app.py
data/
  regions.csv
  policies.csv
recommend.py
ml_model.py
ai.py
prompt.py
requirements.txt
README.md
```

## 데이터 설명

- `data/regions.csv`: 전남 시군별 주거비, 농업, 스마트팜, 자연환경, 인프라, 의료, 교통, 정책 지표
- `data/policies.csv`: 공통 및 일부 시군별 귀농·귀촌 정책 연결 정보

## 참고

추천 결과는 의사결정 보조용입니다. 실제 이주 전에는 현장 방문, 정책 자격 확인, 매물 상태 확인이 필요합니다.
