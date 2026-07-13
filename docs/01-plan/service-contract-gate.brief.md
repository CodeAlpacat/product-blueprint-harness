# Service Contract Gate — Brief

## 멘탈모델

Product Blueprint의 `standard/deep` 산출물은 참고 문서 묶음이 아니라, 구현 전에 실제 서비스처럼 처음부터 끝까지 걸어볼 수 있는 **검증 가능한 서비스 계약**이다. 화면이 예쁘게 존재하는 것만으로는 완료가 아니며, 각 진입점·행동·상태·데이터 책임·복구 경로가 서로 이어져야 한다.

## 사용자가 원하는 차이

현재 하네스와의 차이는 세 가지다.

1. 모든 최소 구현 화면과 횡단 표면이 명시되고, 누락·이연은 사용자 결정 근거 없이 숨길 수 없다.
2. 모든 주요 사용자 흐름이 클릭 가능한 프로토타입에서 끊김 없이 작동하며, happy path뿐 아니라 로딩·빈 상태·오류·권한·결제·충돌·복구를 재현할 수 있다.
3. 각 상호작용이 프론트 상태와 백엔드 책임에 연결되어, 이후 기술 설계와 구현이 같은 서비스 방향을 보존한다.

## 선행근거

### 내부 실측

- `skills/orchestrate/SKILL.md`는 P0 화면, Wiring Matrix, clickable demo, coverage self-audit를 이미 요구한다.
- `skills/screen-contract/SKILL.md`는 허용 액션 전수와 목적지 표를 요구한다.
- `skills/clickable-demo/SKILL.md`는 전이 검증을 요구하지만 검증 결과를 강제하는 기계 판정기는 없다.
- dogfood 기준선은 `00-review-dashboard.html`에서 “개발 착수 준비 완료”를 선언했지만 필수 `04.36-clickable-demo.md`가 없고, `05-engineering-handoff.md`에는 아직 미체크인 출고 항목이 남아 있어 “기획 readiness”와 “구현/출고 readiness”의 경계가 모호하다. 현재 규칙은 이 차이를 기계적으로 판정하지 못한다.

### 외부 선행근거 — Matt Pocock skills

- 작고 조합 가능한 skill을 두고, 인터뷰/도메인 모델링 → spec → vertical ticket → implement/review로 책임을 분리한다.
- UI prototype은 실제 앱 맥락과 데이터 밀도에서 URL로 재현 가능한 변형을 만들고, logic prototype은 상태 전이를 순수 로직 뒤에 둔다.
- spec은 사용자 스토리와 테스트 seam을 먼저 합의하고, ticket은 UI·로직·데이터·테스트를 관통하는 독립 검증 가능한 vertical slice로 나눈다.
- review는 “코드 표준 준수”와 “spec 충족”을 별도 축으로 판정한다.

참조:

- https://github.com/mattpocock/skills
- https://github.com/mattpocock/skills/blob/main/skills/engineering/prototype/SKILL.md
- https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md
- https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md
- https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md

## 최소 모델

새로운 거대 오케스트레이터를 만들지 않는다. 기존 skill을 유지하고 아래 두 개의 작은 책임만 추가한다.

1. `service-contract`: 기존 PRD·screen contract를 기계 판독 가능한 단일 `service-manifest.json`으로 정규화하고, downstream skill이 증거를 갱신하게 한다.
2. `implementation-readiness`: 파일·manifest·prototype DOM·handoff 주장 사이를 결정론적으로 검증해 handoff의 ready/not-ready를 판정한다.

프로토타입 탐색법이나 TDD 전체를 복제하지 않는다. 필요한 원칙만 현재 Product Blueprint 흐름에 연결한다.

## Scope

### 포함

- Standard/Deep의 서비스 계약 manifest와 스키마/예시
- 화면·overlay·entry point·action·transition·상태·데이터 책임·권한·반응형·prototype evidence 모델
- 누락 화면, dead control, 끊긴 전이, 미소유 mutation, 미증거 완료 선언을 잡는 validator
- orchestrate/screen-contract/clickable-demo/prototype-test/engineering-handoff의 gate 연동
- 초기화 스크립트와 README/manifest 설명 갱신
- dogfood false-pass를 재현하는 회귀 fixture와 자동 테스트
- Codex/Claude plugin validation 및 로컬 업데이트 절차

### 제외

- 특정 제품의 실제 DB schema, API endpoint, 프레임워크 아키텍처 생성
- Figma 연동이나 production UI 코드 자동 승격
- 실제 사용자 조사 결과를 heuristic test로 대체
- 기존 dogfood 제품 문서 자체 수정

## 비결정 항목 처리

| 항목 | 처리 |
| --- | --- |
| manifest 형식 | 내 기본값: JSON. validator와 프로토타입 DOM 대조가 결정론적이기 때문 |
| 프로토타입 형식 | 내 기본값: 기존 단일 HTML 유지. 빌드 0·file URL 재현성을 보존 |
| 실제 API/DB 설계 | scope-out. product-level data/operation contract까지만 필수 |
| 실사용자 만족 | 실사용자 검증. 하네스는 프로토콜과 `unverified` 상태만 강제 |
| Lite mode | 내 기본값: 축약 manifest는 만들되 full runtime readiness는 요구하지 않음 |
