# Service Contract Gate — Plan

## 1. 목표 결과

`standard/deep` Product Blueprint가 “화면 문서가 많다”가 아니라 다음을 증명해야 engineering handoff를 통과하게 한다.

- 최소 구현 표면이 모두 계약됨
- 모든 P0 진입점과 action이 목적지 또는 상태 변화로 이어짐
- 클릭 프로토타입에서 흐름과 실패/복구 상태를 재현할 수 있음
- 상호작용별 frontend feedback와 backend/data responsibility가 정해짐
- dashboard, handoff, 실제 파일과 검증 결과가 모순되지 않음

## 2. 대상 사용자와 성공 경험

- 1인 founder/PM: 대시보드와 하나의 프로토타입으로 서비스를 처음부터 끝까지 검토한다.
- product designer: 화면·overlay·상태·반응형 파생 규칙의 누락을 manifest에서 확인한다.
- frontend/backend engineer: 각 action의 사용자 약속, 상태 전이, 데이터 소유자, 실패/복구 경계를 바꾸지 않고 기술 설계를 시작한다.
- coding agent: handoff 문구가 아니라 validator 결과를 readiness의 기준으로 사용한다.

## 3. 실패하면 안 되는 엣지케이스

- deep link, 새로고침, 뒤로가기, 재진입, 다른 탭/기기에서 흐름이 사라지는 경우
- guest/authenticated/role-denied/age-gated/paid 상태에 따라 다른 entry와 transition
- overlay를 독립 화면처럼 세거나, 독립 화면을 toast로 대체하는 경우
- dead button, `href="#"`, 목적지 없는 navigation, 화면에는 있으나 contract에 없는 action
- mutation의 중복 submit, pending, failure, rollback/retry, persistence가 비어 있는 경우
- empty/loading/error/success가 legend에만 있고 실제 prototype에서 재현되지 않는 경우
- P1 이연 화면의 P0 진입점 처리 없이 “나중에”로 숨기는 경우
- dashboard는 완료인데 필수 파일이 없거나 handoff checklist가 미통과인 경우
- 실제 사용자 미검증을 “validated”로 승격하는 경우

## 4. 단일 SoT: `service-manifest.json`

초기 경로는 `02.6-service-manifest.json`으로 한다. 기존 markdown은 사람이 읽는 설명이고, readiness 판정은 manifest와 증거 파일을 기준으로 한다.

필수 영역:

- `release_profile`: P0/P1, supported roles/platforms/viewports, explicit exclusions와 decision reference
- `surfaces`: screen/overlay/sheet/dialog/background, purpose, route/state id, entry/exit, responsive disposition
- `actions`: source, control id/selector, user intent, target/effect, confirmation, T0/During/Done feedback
- `states`: loading/empty/error/success/locked/permission/offline/conflict/paid와 재현 방법
- `operations`: read/write, source of truth, data owner, input/output promise, auth, idempotency, persistence, failure/recovery
- `operations` 확장: consistency, concurrency/conflict, audit/retention, latency/cost class, observability, abuse/rate-limit concern
- `journeys`: persona, start condition, ordered action IDs, expected end, exception branches
- `evidence`: contract anchor, prototype selector, screenshot/test artifact, verification status
- `accessibility`: keyboard path, focus entry/return, accessible name, status/error announcement
- `ai_assists`(해당 시): input, result widget, editable unit, save destination, failure/truncation UI
- `status`: `defined`, `prototyped`, `wired`, `contracted`, `verified`; 상위 상태는 하위 증거 없이 설정 불가

`designed`나 `complete` 같은 단일 boolean은 금지한다.

## 5. 결정론 validator

새 스크립트 `scripts/validate_service_blueprint.py <planning-dir> [--profile standard|deep|lite]`를 만든다. 외부 패키지 없이 Python 표준 라이브러리로 동작하며, exit code 0/1과 사람이 읽는 ledger, 기계 판독 가능한 readiness report를 출력한다.

검사:

1. profile별 필수 파일 존재
2. manifest schema와 ID/참조 무결성
3. 모든 required surface의 entry/exit와 prototype evidence
4. 모든 action의 target/effect, 존재하는 target, dead selector/href 탐지
5. 모든 journey의 시작부터 끝까지 graph reachability
6. mutation/async action의 T0/During/Done, failure, retry/rollback, operation owner
7. required state의 prototype 재현 selector/URL
8. 권한·결제·파괴 action의 gate/confirmation/invariant
9. responsive-web profile의 mobile/desktop evidence 또는 승인된 파생 규칙
10. exclusion/defer의 decision reference와 현재 release entry behavior
11. dashboard/handoff의 ready claim이 validator 결과와 일치하는지
12. real-user test가 없으면 `user_validated=false` 유지
13. keyboard/focus/announcement 계약과 AI-assist 5-cell 완전성
14. operation의 consistency, conflict, audit, latency/cost, observability 경계

manifest를 채우지 않은 기존 프로젝트는 조용히 통과시키지 않고 migration guidance와 함께 fail한다. Lite는 축약 규칙으로 별도 판정한다.

validator가 `05-readiness-report.json`과 `05-readiness-report.md`를 생성한다. dashboard와 handoff는 자연어 완료 문구를 독자적으로 쓰지 않고 이 report의 status·실패 코드·검증 시각·manifest hash를 표시한다. 데모 전용 jump bar 같은 비제품 control은 `data-demo-control`로 명시 제외한다.

## 6. Skill 책임 재배치

### 새 skill

- `service-contract`: screen contract 이후 manifest 생성·갱신. product-level FE/BE boundary를 소유한다.
- `implementation-readiness`: prototype 이후와 handoff 직전에 validator를 실행하고 failure ledger를 upstream artifact로 돌려보낸다.

### 기존 skill 변경

- `orchestrate`: phase order에 두 gate를 삽입하고 validator pass 없이는 dashboard/handoff ready 금지
- `prd`: exhaustive numbered user stories와 entry-point inventory를 manifest seed로 제공
- `screen-contract`: 모든 action에 stable ID, surface type, T0/During/Done, operation reference 요구
- `clickable-demo`: `data-surface`, `data-action`, URL/state 재현 규약; manifest로부터 배선하고 transition test report 생성
- `storyboard`, `ux-writing`, `design-system-workbench`, `visual-quality-gate`: manifest의 surface/action/state ID와 P0 set을 공통 coverage source로 사용
- `design-critique`: visual quality와 service-contract fidelity를 별도 축으로 판정
- `prototype-test`: manifest journey를 task test로 사용하고 heuristic/real-user 상태 분리
- `backend-systems-brief`: 추상 질문만 남기지 않고 operation별 product invariant/data owner/failure consequence를 제공하되 endpoint/schema는 금지
- `feasibility-review`, `risk-register`: mechanism/risk row를 surface/action/operation ID에 역참조
- `feature-adoption`: 기존 제품 채택 delta를 manifest에도 cascade
- `engineering-handoff`: 수동 readiness 선언 제거. validator report, unresolved ledger, vertical implementation slices를 필수 입력으로 사용
- `decision-dashboard`: 완료 badge를 validator report에서만 파생
- `tech-plan`: 사용자가 기술 설계를 요청한 경우 service operation을 API/DB/FE architecture로 매핑하고, 각 매핑을 원래 action/journey ID에 역참조

## 7. Matt Pocock 방식에서 채택할 부분

- 작고 조합 가능한 skill: 기존 orchestrator는 순서만 소유하고 계약/검증 책임은 별도 skill에 둔다.
- grilling/domain modeling: 이미 답이 코드와 산출물에 있으면 사용자에게 되묻지 않고, 용어 충돌과 제품 결정을 구분한다.
- prototype 분리: 질문 탐색용 prototype과 전체 서비스 계약 prototype을 명시적으로 구분한다.
- test seam first: screen/action/operation/journey ID를 구현 전 검증 seam으로 고정한다.
- tracer bullet: handoff에서 journey별로 UI·operation·persistence·test를 관통하는 독립 demo 가능한 slice를 만든다.
- two-axis review: 향후 구현 review는 standards와 service-contract fidelity를 따로 판정한다.

채택하지 않는 부분:

- 질문 하나만 답하는 throwaway prototype을 최종 서비스 prototype으로 간주하지 않음
- 이 플러그인의 20여 디자인 skill을 하나의 거대 skill로 합치지 않음
- 특정 issue tracker나 프레임워크를 hard-code하지 않음

## 8. Acceptance samples

| ID | 샘플 | 기대 결과 |
| --- | --- | --- |
| AC-01 | dashboard는 ready, 필수 clickable-demo note 누락 | fail: `REQUIRED_ARTIFACT_MISSING` |
| AC-02 | handoff checklist 미체크인데 ready claim | fail: `READINESS_CLAIM_CONFLICT` |
| AC-03 | 화면 버튼이 manifest action/target 없이 존재 | fail: `UNCONTRACTED_CONTROL` |
| AC-04 | action target surface는 있으나 graph상 도달 불가 | fail: `UNREACHABLE_SURFACE` |
| AC-05 | write action에 pending/error/recovery 또는 data owner 없음 | fail: `INCOMPLETE_OPERATION_CONTRACT` |
| AC-06 | loading/error 상태가 문서에만 있고 demo selector 없음 | fail: `STATE_NOT_REPRODUCIBLE` |
| AC-07 | P1 이연 화면이 P0에서 노출되지만 entry behavior 없음 | fail: `DEFERRED_ENTRY_UNDEFINED` |
| AC-08 | guest→login→원래 작업 복귀가 journey에서 끊김 | fail: `JOURNEY_END_UNREACHABLE` |
| AC-09 | mobile만 있고 responsive-web desktop rule/evidence 없음 | fail: `RESPONSIVE_EVIDENCE_MISSING` |
| AC-10 | 모든 참조·flow·operation·evidence 충족 | pass + readiness report |
| AC-11 | heuristic pass, 실제 사용자 테스트 없음 | pass 가능하되 `user_validated=false` |
| AC-12 | Lite profile은 축약 manifest와 명시적 제한 보유 | lite pass, engineering-ready는 false |

### Happy

- AC-10: 완전한 standard fixture는 readiness report `pass`와 구현 vertical slice 목록을 만든다.
- AC-12: Lite fixture는 자체 profile 검증은 통과하지만 engineering-ready로 과장되지 않는다.

### Exception

- AC-01~AC-08: 산출물 누락, 거짓 완료 선언, dead control, 끊긴 graph, operation/state/defer/auth 복구 누락을 각각 고유 실패 코드로 반환한다.

### Boundary

- AC-09: responsive profile 경계를 검사한다.
- AC-11: heuristic 검증과 실제 사용자 검증의 증거 경계를 보존한다.
- demo-only control, overlay, background-only mechanism은 surface/action type 규칙에 따라 false positive 없이 분류한다.

## 9. Verifier-first 구현 순서

1. 최소 invalid/valid fixture와 위 AC를 테스트로 만든다.
2. validator skeleton을 작성해 invalid 기준선이 실패하고 valid fixture만 통과하게 한다.
3. manifest schema/template과 `service-contract` skill을 추가한다.
4. clickable demo DOM 대조와 journey graph 검사를 붙인다.
5. 기존 skill/orchestrator/dashboard/handoff를 validator에 연결한다.
6. `05-readiness-report.*` 생성과 dashboard/handoff 소비를 연결한다.
7. 실제 dogfood 폴더를 read-only 대상으로 실행해 기존 false-pass를 확인한다.
8. plugin/skill validator, init script tests, README links, cachebuster/reinstall을 검증한다.

## 10. 작업 단위

1. **Contract core**: schema/template + validator + fixtures/tests
2. **Planning integration**: PRD/screen/service-contract/backend skill
3. **Prototype integration**: clickable-demo/prototype-test + DOM/graph evidence
4. **Readiness integration**: orchestrate/dashboard/handoff + tracer-bullet handoff
5. **Packaging**: init scaffold, README, manifests, plugin/skill validation, local reinstall

각 단위는 독립 검증 후 별도 커밋으로 남긴다.

## 11. 검증 명령 계획

- `python3 -m unittest discover -s tests`
- `python3 scripts/init_prd_project.py "Service Contract Fixture" --root <tmp>` 후 생성물 검사
- `python3 scripts/validate_service_blueprint.py tests/fixtures/valid-standard`
- invalid fixture별 non-zero exit와 error code assertion
- dogfood 폴더 read-only baseline run
- `skill-creator/scripts/quick_validate.py`로 변경·신규 skill 전수
- `plugin-creator/scripts/validate_plugin.py`로 plugin 검증
- `git diff --check`
- cachebuster helper 후 `codex plugin add ...` 로 재설치, 새 thread smoke test 안내

## 11.1 Success metrics

- Before: dogfood 기준선에서 필수 artifact 누락과 미체크 handoff gate가 dashboard의 ready 선언과 공존한다.
- After: AC-01~AC-12 자동 테스트가 모두 통과하고, 같은 dogfood 기준선은 최소 `REQUIRED_ARTIFACT_MISSING`·`READINESS_CLAIM_CONFLICT`로 실패한다.
- After: 신규 standard scaffold는 manifest 없이는 handoff-ready가 될 수 없고, valid fixture만 readiness `pass`를 생성한다.
- 정성 지표: founder가 markdown 전수검사 없이 prototype과 readiness ledger만으로 누락 위치와 upstream owner를 찾을 수 있다. 실제 체감은 후속 dogfood에서 확인한다.

## 11.2 예상 작업량과 블로커

| 영역 | 추정 | 비고 |
| --- | --- | --- |
| validator/schema/tests | 1~1.5 person-day 상당 | stdlib JSON/HTML 검사, fixture 12개 |
| planning/prototype skill 연동 | 1~1.5 person-day 상당 | 기존 문구 중복 제거 포함 |
| readiness/handoff/dashboard 연동 | 0.5~1 person-day 상당 | generated report를 단일 status source로 사용 |
| packaging/dual-target 검증 | 0.5 person-day 상당 | Claude/Codex manifest, local reinstall |

블로커는 현재 없다. 실제 사용자 검증은 플러그인 구현 블로커가 아니며 `user_validated=false`로 남긴다.

## 12. 리스크와 완화

- **manifest 작성 비용 증가**: screen contract 표에서 seed하고 stable ID 재사용; 중복 설명 금지
- **기존 프로젝트 호환성**: 자동 통과 대신 migration report 제공; profile별 요구 수준 분리
- **HTML parser 취약성**: 표준 라이브러리만 사용하고 `data-*` 규약을 단순하게 유지
- **LLM이 evidence를 허위 기입**: 파일/selector/graph를 validator가 직접 대조
- **체크리스트 비대화**: 완성도 boolean 대신 실패 코드와 upstream owner를 반환
- **실제 구현과 drift**: handoff vertical slice와 후속 code review에서 service-contract fidelity 축 사용
- **보안·정책·운영 사각지대**: release profile과 operation contract가 permission, abuse, audit, retention, cost/latency/observability를 명시하고 해당 없음도 `n/a` 근거를 요구
- **dual-target drift**: Claude/Codex manifest와 공통 skill directory를 함께 검증하되 marketplace 파일은 update helper 흐름 밖에서 손대지 않음

## 12.1 비용·권한·데이터 영향

- 제품 production DB/API/권한에는 영향을 주지 않는다.
- 외부 서비스 호출이나 지속적인 런타임 비용은 추가하지 않는다.
- 변경 범위는 로컬 plugin source, 생성되는 planning artifact, 로컬 Codex plugin reinstall이다.
- push, PR, release는 별도 승인 없이는 수행하지 않는다.

## 13. 구현 진입 조건

- 사용자에게 이 plan의 scope와 `service-manifest.json` 도입 승인을 받는다.
- 승인 전에는 skill/script/manifest 동작 파일을 수정하지 않는다.
