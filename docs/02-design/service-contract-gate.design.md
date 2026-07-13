# Service Contract Gate — Design

## 0. 정초

- 멘탈모델: Standard/Deep blueprint는 구현 참고문서 묶음이 아니라, 화면·행동·상태·데이터 책임이 연결되고 프로토타입으로 재현되는 서비스 계약이다.
- 내부 근거: 기존 `screen-contract`, `clickable-demo`, `coverage-self-audit`, `engineering-handoff`는 필요한 항목을 산문으로 요구하지만 공통 식별자와 결정론 validator가 없다.
- 외부 근거: Matt Pocock의 composable skill, test-seam-first spec, prototype, tracer-bullet ticket, standards/spec 이중 review를 현재 pipeline에 맞게 채택한다.
- 최소 모델: 기존 skill을 합치지 않고 manifest 소유 skill 하나와 readiness 판정 skill 하나, stdlib validator 하나만 추가한다.

## 1. 변경 접점 전수

| 접점 | 현재 책임 | 변경 |
| --- | --- | --- |
| `scripts/init_prd_project.py` | 산출물 scaffold | manifest template, readiness report 자리, enhanced stubs 생성 |
| `scripts/validate_service_blueprint.py` | 없음 | manifest/HTML/artifact/claim 검증과 report 생성 |
| `assets/templates/service-manifest.json` | 없음 | canonical schema example |
| `skills/service-contract/SKILL.md` | 없음 | manifest 생성·갱신 책임 |
| `skills/implementation-readiness/SKILL.md` | 없음 | validator 실행, failure upstream routing |
| `skills/orchestrate/SKILL.md` | phase routing | screen contract 뒤 manifest, prototype 뒤/hand-off 전 readiness gate |
| `skills/prd/SKILL.md` | 요구·story | stable story ID, entry inventory, category baseline surface disposition |
| `skills/screen-contract/SKILL.md` | 화면·배선 | stable surface/action/state ID, feedback/operation ref |
| `skills/clickable-demo/SKILL.md` | HTML demo | DOM evidence protocol (`data-surface`, `data-action`, `data-go`, demo exclusion) |
| `skills/storyboard/SKILL.md` | flow visualization | journey/surface/action ID를 frame과 transition annotation에 유지 |
| `skills/ux-writing/SKILL.md` | P0 copy/state copy | surface/action/state ID별 copy coverage |
| `skills/design-system-workbench/SKILL.md` | component/state/P0 renders | manifest P0/state coverage matrix 소비 |
| `skills/visual-quality-gate/SKILL.md` | rendered P0 breadth | manifest P0 set × DOM/workbench evidence 대조 |
| `skills/design-critique/SKILL.md` | product/UX review | contract fidelity와 visual quality를 별도 축으로 판정 |
| `skills/prototype-test/SKILL.md` | task walk-through | manifest journey를 test source로 사용 |
| `skills/backend-systems-brief/SKILL.md` | backend 질문·invariant | operation owner/consistency/failure/ops boundary를 product language로 고정 |
| `skills/feasibility-review/SKILL.md` | mechanism feasibility | P0 operation/mechanism dependency를 manifest ID로 판정 |
| `skills/risk-register/SKILL.md` | policy/safety risks | trigger surface/action/operation ID 역참조 |
| `skills/feature-adoption/SKILL.md` | existing-code delta | 채택 delta가 manifest surface/action/operation에 반영되도록 cascade |
| `skills/decision-dashboard/SKILL.md` | visual status | readiness report status만 소비 |
| `skills/engineering-handoff/SKILL.md` | product→engineering | report와 journey vertical slice 필수, 수동 ready 선언 금지 |
| `skills/tech-plan/SKILL.md` | optional architecture | action/operation/journey ID를 API/DB/FE/BE 계획에 역참조 |
| `references/coverage-self-audit.md` | prose coverage | manifest/validator와 역할 정렬, 중복 self-grade 제거 |
| `references/quality-bar.md` + visual references | evidence checklist | P0 set의 SoT를 manifest로 전환, machine gate와 human/visual gate 구분 |
| `README.md` | 사용법/skill map | service contract flow와 명령 설명 |
| Claude/Codex manifests | capability discovery | 신규 skill/capability 설명, Codex cachebuster는 helper 사용 |

## 2. Manifest contract

### 2.1 Top-level

```json
{
  "schema_version": "1.0",
  "project": {},
  "release_profile": {},
  "surfaces": [],
  "actions": [],
  "states": [],
  "operations": [],
  "journeys": [],
  "user_validation": {},
  "evidence": {}
}
```

ID pattern은 `[a-z][a-z0-9-]*`로 제한한다. 사람이 읽는 label은 별도 필드다. 화면 번호 `S1`처럼 순서에 묶인 값을 identity로 쓰지 않는다.

### 2.2 Surface

- `id`, `label`, `type`: `screen|overlay|sheet|dialog|panel|background`
- `priority`: `P0|P1|P2`
- `purpose`, `route_or_trigger`
- `entry_action_ids`, `exit_action_ids`
- `required_state_ids`
- `prototype`: `{ file, element_id }`
- `responsive`: `{ strategy, mobile_element_id, desktop_element_id, derivation_rule }`
- `status`: `{ defined, prototyped, wired, contracted, verified }`

P0 screen/overlay/sheet/dialog/panel은 prototype evidence가 필수다. `background`는 UI가 없음을 명시하고 inspect/recovery surface를 연결한다.

### 2.3 Action

- `id`, `label`, `source_surface_id`, `control_element_id`
- `kind`: `navigate|open-overlay|close-overlay|read|write|destructive|external`
- `intent`, `preconditions`
- `target`: `surface_id` 또는 `effect`
- `operation_id`(read/write/destructive는 필수)
- `feedback`: `{ t0, during, done }`
- `accessibility`: `{ keyboard, focus, announcement }`

Demo DOM에서 제품 control은 `data-action="<id>"`, surface root는 `data-surface="<id>"`를 가진다. navigation/open action은 `data-go="<surface-id>"`가 manifest target과 같아야 한다. jump bar와 board toggle은 `data-demo-control`로 제외한다.

### 2.4 State

- `id`, `surface_id`, `kind`: `default|loading|empty|error|success|locked|permission|offline|conflict|paid`
- `required`, `trigger`, `recovery_action_id`
- `prototype`: `{ file, element_id }`

Required state는 legend/text listing이 아니라 DOM element evidence가 있어야 한다.

### 2.5 Operation

- `id`, `kind`: `read|write|destructive|external`
- `owner`: `frontend-local|backend|external`
- `source_of_truth`, `input_promise`, `output_promise`
- `authorization`, `persistence`: `none|session|account|cross-device`
- `idempotency`, `consistency`, `conflict_strategy`
- `failure`, `recovery`, `audit_retention`
- `latency_class`, `cost_class`, `observability`, `abuse_boundary`

값을 모르면 빈 문자열 대신 `decision-needed:<id>`를 사용하고 readiness blocker로 처리한다. 해당 없음은 `n/a:<reason>`이다.

### 2.6 Journey

- `id`, `persona`, `start_surface_id`, `preconditions`
- `steps`: action ID sequence
- `expected_end_surface_id`
- `exception_paths`: failure state/action sequence
- `refresh_resume`, `back_behavior`, `cross_device_behavior`

validator는 action graph와 ordered steps를 모두 확인한다.

## 3. Validator architecture

### 3.1 Modules in one script

외부 dependency를 만들지 않기 위해 한 파일 안에서 작은 순수 함수로 나눈다.

- `load_manifest`
- `validate_shape`
- `index_contract`
- `parse_demo` (`html.parser.HTMLParser`)
- `validate_references`
- `validate_dom_evidence`
- `validate_operations`
- `validate_journeys`
- `validate_artifacts_and_claims`
- `derive_readiness`
- `write_report`

각 finding은 `{code, severity, message, path, owner}` 구조다. `owner`는 upstream artifact/skill이다.

### 3.2 Readiness derivation

- `pass`: error finding 0, standard/deep 필수 evidence 충족
- `fail`: error 1개 이상
- `lite-pass`: Lite contract 자체는 유효하지만 `engineering_ready=false`
- `user_validated`: real-user evidence가 있을 때만 true

`ACCEPT-FLAG`는 validator error를 삭제하지 않는다. manifest의 `accepted_limitations`에 decision ref, owner, consequence가 있으면 report에서 `accepted`로 분리하되 READY 표시 옆에 항상 노출한다.

### 3.3 Report files

- `05-readiness-report.json`: status, engineering_ready, user_validated, manifest SHA-256, checked_at, findings, accepted limitations
- `05-readiness-report.md`: 사람이 읽는 요약과 upstream별 수정 ledger

Dashboard/handoff는 report가 없거나 manifest hash가 다르면 stale/fail로 표시한다.

## 4. Profile rules

| Rule | Lite | Standard | Deep |
| --- | --- | --- | --- |
| Manifest | 축약 필수 | 필수 | 필수 |
| P0 prototype DOM evidence | 선택, 미검증 명시 | 필수 | 필수 |
| Required non-happy states | 계약만 가능 | DOM evidence | DOM evidence + richer boundary |
| Operation contract | core action만 | 모든 P0 read/write | 모든 P0 + P1 decision-impact |
| Journey | core happy 1개 | happy/exception/boundary | persona/role별 전수 |
| Engineering ready | 항상 false | validator pass 시 true | validator pass 시 true |

## 5. Flow and lifecycle

```text
PRD user story IDs
  → screen-contract surface/action/state IDs
  → service-manifest operation/journey ownership
  → clickable-demo DOM evidence
  → prototype-test journey evidence
  → readiness report
  → engineering-handoff vertical slices
  → optional tech-plan API/DB/FE/BE mapping
```

Screen set가 바뀌면 manifest hash와 report가 stale해진다. handoff/dashboard가 이전 report를 계속 소비할 수 없다.

## 6. Failure routing

| Finding family | 수정 owner |
| --- | --- |
| missing baseline surface/story | `prd` |
| missing contract/action/entry/exit | `screen-contract` |
| missing operation/data responsibility | `service-contract` 또는 `backend-systems-brief` |
| DOM missing/mismatch/dead control | `clickable-demo` |
| journey task/real-user evidence | `prototype-test` |
| stale/false ready claim | `decision-dashboard` / `engineering-handoff` |

## 7. Vertical implementation slices

Engineering handoff는 journey마다 다음 표를 만든다.

| Slice | Journey IDs | Surfaces | Actions | Operations | Persistence/invariants | Verification seam |
| --- | --- | --- | --- | --- | --- | --- |

각 slice는 UI만 또는 backend만 따로 떼지 않고 한 사용자 결과까지 관통한다. 구체 endpoint/table/component는 opt-in `tech-plan`에서 채운다.

## 8. Migration and compatibility

- 새 scaffold는 manifest template을 생성한다.
- 기존 planning folder는 manifest가 없으면 `SERVICE_MANIFEST_MISSING`으로 fail하고, `service-contract` 실행 안내를 낸다.
- 기존 markdown을 위험하게 자동 추론해 ready로 승격하지 않는다.
- Claude/Codex 모두 같은 `skills/`와 `scripts/`를 사용한다.
- marketplace 파일은 직접 수정하지 않고 기존 local marketplace/update helper 흐름을 따른다.

## 9. Test design

- unittest temporary directories로 fixture를 복사해 report write가 tracked fixture를 오염시키지 않게 한다.
- valid-standard 1개, valid-lite 1개, invalid cases는 한 fixture에 여러 원인을 섞지 않는다.
- HTML parser tests: screen/action/data-go/state evidence/demo-control exclusion.
- graph tests: missing target, unreachable surface, journey end mismatch, exception path.
- report tests: stable codes, engineering_ready, user_validated, manifest hash stale behavior.
- dogfood는 portable unit fixture가 아니라 수동 read-only regression command로 사용한다.

## 10. Rollout

1. core validator와 fixture를 먼저 커밋한다.
2. planning skill이 manifest를 생산하도록 연결한다.
3. prototype skill이 DOM evidence를 생산하도록 연결한다.
4. readiness consumers를 report 기반으로 전환한다.
5. init/README/manifests/cachebuster/reinstall을 마감한다.

기존 plugin 사용자는 새 thread에서 재로드한다. push/release는 별도 승인 전 수행하지 않는다.
