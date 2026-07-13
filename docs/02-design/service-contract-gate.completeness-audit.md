# Service Contract Gate — Completeness Audit

## 0. 정초 상태

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| 사용자 멘탈모델 | 충족 | brief §멘탈모델 |
| 내부 선행근거 | 충족 | 기존 skill·dogfood false-pass 실측 |
| 외부 선행근거 | 충족 | Matt Pocock skills 공식 저장소 |
| 최소 모델 | 충족 | 신규 skill 2 + validator 1, 기존 pipeline 유지 |

## 1. 산출물/접점 매트릭스

| 접점 | 정의 | 생성 | 소비 | 검증 | 잔여 |
| --- | --- | --- | --- | --- | --- |
| user story | PRD | `prd` | screen contract | story ID reference | 없음 |
| surface/action/state | screen contract | `screen-contract` | manifest/demo | ref + DOM | 없음 |
| operation | service contract | `service-contract` | backend/handoff/tech plan | required fields | 없음 |
| journey | service contract | `service-contract` | demo/test/handoff | graph/ordered path | 없음 |
| prototype evidence | DOM protocol | `clickable-demo` | readiness | HTML parser | 없음 |
| user evidence | task protocol | `prototype-test` | readiness/handoff | explicit real-user status | 없음 |
| readiness | derived report | validator | dashboard/handoff | manifest hash | 없음 |

Downstream census 결과 `storyboard`, `ux-writing`, `design-system-workbench`, `visual-quality-gate`, `design-critique`, `feasibility-review`, `risk-register`, `feature-adoption`도 manifest ID 소비자로 포함했다. screen-contract와 manifest를 각각 독립 SoT로 두지 않는다.

## 2. 진입점 × 생명주기

| 진입점 | 정체성/권한 | hydrate | 진행 상태 | teardown/복귀 |
| --- | --- | --- | --- | --- |
| route/deep link | journey precondition + operation auth | source of truth | loading/error state | refresh_resume |
| in-product navigation | source action | target surface/state | T0/During/Done | back_behavior |
| guest→auth gate | guest persona + auth precondition | pending intent | permission/auth state | original journey resume |
| notification/external link | explicit external entry | entity lookup | missing/permission state | safe destination |
| returning/cross-device | account identity | persisted operation output | conflict/offline state | cross_device_behavior |

각 제품은 해당 없는 진입점을 `n/a:<reason>`으로 명시한다. 빈칸은 허용하지 않는다.

## 3. 화면/인터랙션 완전성

| 차원 | 계약 위치 | validator |
| --- | --- | --- |
| 정보 목적/사용자 질문 | surface purpose | required string |
| 반응형 | surface responsive | viewport evidence/rule |
| 정적 상태 | state array | DOM evidence |
| 전이 피드백 | action feedback | T0/During/Done non-empty |
| 접근성 | action accessibility | keyboard/focus/announcement |
| 카피/멘탈모델 | labels + purpose | human review, machine presence |
| 배선 | action target + journey | graph + DOM data-go |
| 데이터 책임 | operation | owner/SoT/persistence/failure |

## 4. 10-lens inline gap sweep

| 렌즈 | 발견 | 설계 반영 |
| --- | --- | --- |
| 제품/수익 | P1 defer가 P0 entry를 오염 가능 | release profile + defer entry behavior |
| UX/접근성 | 클릭 배선만 있고 focus/announcement 누락 가능 | accessibility contract |
| 백엔드/데이터 | backend 질문이 action과 분리 | operation ID + SoT/consistency/lifecycle |
| 보안/악용 | 권한/유료/파괴 action gate 누락 가능 | authorization/abuse/confirmation |
| 운영/비용/관측 | AI/외부 operation 운영 경계 누락 | latency/cost/observability |
| 법무/정책 | age/PII/payment/UGC가 화면 목록에서만 존재 가능 | risk decision ref + audit/retention |
| 엣지/동시성/생명주기 | refresh/back/multi-tab/cross-device 누락 | journey lifecycle fields |
| 경쟁사/카테고리 parity | agent가 아는 화면만 계약 | PRD baseline inventory + explicit disposition |
| AI-assist hand-wave | “AI가 생성”만 있고 수정/저장/실패 UI 없음 | AI 5-cell |
| transient feedback | static states는 있으나 클릭→결과 연속성 누락 | T0/During/Done |

P0 미해소 0. 실사용자 만족은 결정론으로 닫지 않고 `user_validated=false`로 보존한다.

## 5. 비결정 처리

| 항목 | 분류 | 처리 |
| --- | --- | --- |
| JSON vs YAML | 내 기본값 | JSON + stdlib validator |
| 실제 API/DB shape | 사용자 요청 시 후속 | opt-in tech-plan |
| heuristic UX pass | 실사용자 검증 아님 | 별도 status |
| legacy artifact 자동변환 | 내 기본값 | 위험한 자동 ready 금지, migration 안내 |
| marketplace publishing | 사용자 결정 | 로컬 reinstall까지만 |

## 6. 판정

- 설계 completeness: pass
- 구현 진입 blocker: 0
- 정직한 잔여: 실제 dogfood 재실행에서 추가 finding code가 필요할 수 있으며, validator false positive/negative는 fixture로 반복 조정한다.

## 7. Design Review

| 영역 | 판정 | 근거 |
| --- | --- | --- |
| D1 소비자 전수 | 보완 후 pass | `rg`로 screen contract/P0/readiness 참조 파일 열거, downstream 8종 추가 |
| D2 data-flow | pass | manifest → prototype/test/report/handoff/tech-plan 단방향 흐름 |
| D3 mutation | n/a | production data mutation 없음; planning artifact 생성만 수행 |
| D4 진입점×생명주기 | pass | route/deep link/nav/auth/external/returning 5종, lifecycle 빈칸 0 |
| Spec 정합 | pass | 실제 API/DB 자동설계는 scope-out, product-level operation까지만 |
| 구조적 방지 | pass | ready를 자연어 자기판정이 아니라 validator-derived report로만 표현 |

Critical 1건(옛 screen-contract만 소비하는 downstream dual-SoT 위험)을 위 접점 확장으로 해소했다. Warning 0.
