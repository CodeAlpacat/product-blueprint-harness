# Improvement Backlog — 2026-07-10 Doyo 도그푸드 2차 발견

> 출처: Doyo 심화 세션 (haven-chat 채택 분석 → 화면·데스크톱·폼 상태·아트 프로덕션 전 과정). 공통 패턴 = **유저가 물어봐야 갭이 드러남** — 하네스가 선제적으로 커버리지를 감사하지 않았다.

## 근본 문제 1개 (P0) — "물어봐야 나온다"

이번 세션에서 유저 질문 3개가 각각 실제 P0 갭을 적중:
- "화면·사이드패널·배선 미리 안 그리나?" → 데스크톱 문법 0장, 배선 전수표 부재
- "데스크톱은 모바일 확장 + 최대 폭이지" → 데모가 다른 문법(3열 그리드)으로 그림
- "Storybook식 상태 전수는?" → 폼 컨트롤 상태·검증 정책·전역 fallback 부재

**개선: `coverage-self-audit` 단계 신설 (orchestrate 의무 게이트)** — engineering-handoff 직전에 "개발자 관점 갭 스캔"을 하네스가 스스로 실행하고 결과를 대시보드 "남은 갭" 섹션에 박제:
1. 반응형 문법 도해 존재? (모바일 확장 + max-width 캡 원칙)
2. 컴포넌트/폼 상태 전수 렌더 존재? (Storybook식)
3. 배선 전수표(화면×액션→목적지) 존재? (클릭 전이 ✅ / 견본 구분)
4. 전역 fallback 3종(404·연결 끊김·점검) + lazy auth + 신고 시트 도해?
5. 폼 검증 정책(검증 시점·미입력 제출·저장 분류·파괴 확인) 문서화?

## 스킬별 개선 (P1)

| # | 스킬 | 발견 | 개선 |
|---|---|---|---|
| 1 | `design-system` / `design-system-workbench` | 컴포넌트 6종 + 상태 "범례"로 통과 — 실제 상태별 렌더 없음 | **Form Controls 상태 전수 섹션 의무**: TextField·TextArea(카운터)·Choice Card(locked=비활성 아님)·Toggle·Checkbox·Toast·Confirm Dialog × default/focus/error/disabled. + **Form Policy 5규칙** 산출 의무. Doyo `doyo-design-system.html` §Form Controls = 견본 |
| 2 | `clickable-demo` | 모바일 프레임만 계약 — 데스크톱/반응형 무언급 | **반응형 문법 단계 의무**: 원칙 = "데스크톱은 모바일의 확장, 앱 max-width 캡(제타/WHIF), 다른 문법 금지". 도해 최소 3장(발견·상세·채팅+패널) + 나머지는 규칙 파생 선언. 캡 밖 여백 시각화 |
| 3 | `screen-contract` | Entry/Exit 산문 맵만 — 전수성 검증 불가 | **Wiring Matrix 의무**(화면×액션→목적지 표, 클릭 전이/상태 견본 구분) + 데모 전이 무결성 스크립트와 대조 |
| 4 | `references/quality-bar.md` | 전역 fallback·lazy auth·신고 시트가 체크리스트에 없음 | 완료 체크에 추가: 404/연결 끊김(진행 보존 고지)/점검 + 게스트 lazy 로그인 + 신고 경로 도해 |
| 5 | **신규 `art-production`** | 아트 루프(팩→파일럿→판정→배치→리롤→배선)가 전부 애드혹 | 스킬 신설: 고정 외형 태그 블록 + 파일럿 N샷 → 듀오톤 콘택트 시트 보드 대조 → 시드/프리픽스 확정 → 배치 → FAIL 리롤(태그 교정) → 데모 배선 교체 → 보드 렌더 게이트. **파일럿 학습 코드화**: ① 연령은 형용사 금지, 명시 숫자("29 years old") ② 무보정 기본 = 드리프트(마초/수염/아머/네온) — 컨셉 부정 네거티브 필수 ③ 리롤 상한 3 + ACCEPT-FLAG |
| 6 | **신규 `feature-adoption`** (선택) | 기존 자산(haven-chat) 전수 분석→채택 맵이 애드혹으로 큰 가치 | 기존 코드베이스 보유 유저용: 3축 병렬 조사(코어 도메인/제작/플랫폼) → 채택/각색/제외 표 + "이식 기준 2개"(돈·법 검증 자산 vs 얽힘·단순화) |
| 7 | `tech-plan` | "재사용=이식" 과대평가를 유저가 정정 | 독트린 추가: 이식 판정 기준 = ① 정확성이 돈/법 직결 + 실전 검증 → 이식 ② 얽힘 크고 요구 단순 → 참조-재작성. fork drift 비용 명시 |
| 8 | `orchestrate` | 다음 단계 "추천"은 하지만 갭 스캔은 안 함 | P0 항목의 coverage-self-audit 편입 + decision-dashboard에 "남은 갭(하네스 자가 감사)" 섹션 의무 |

## 기존 발견 (누적, 미반영)

- `init_prd_project.py` slugify 한글 제거 → unicode \w 보존
- `parallel-concepts` 추상성 → 화면/메커닉 수준 구체 차 + 대표 시각물 (일부 반영됨 — 재검증 필요)

## 반영 시 검증 방법

Doyo 패키지가 견본 = 각 개선이 요구하는 산출물이 이미 존재 (`doyo-demo.html` D1~D3·ST, `doyo-design-system.html` §Form Controls, `02.5` Wiring Matrix, `06.1` 아트 팩 §0). 스킬 문구는 "이 견본과 동형 산출"으로 캘리브레이션하면 됨.
