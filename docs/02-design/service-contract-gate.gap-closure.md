# Service Contract Gate — Gap Closure Ledger

| ID | Gap | Severity | Deterministic | Closure |
| --- | --- | --- | --- | --- |
| G1 | 산문 규칙과 실제 파일/DOM 불일치 | P0 | yes | manifest + validator |
| G2 | designed/complete가 여러 성숙도를 뭉갬 | P0 | yes | 5-stage status, boolean complete 금지 |
| G3 | dashboard/handoff가 독립적으로 ready 주장 | P0 | yes | generated readiness report SoT |
| G4 | action과 backend responsibility 연결 없음 | P0 | yes | operation ID contract |
| G5 | state가 legend에만 존재 | P0 | yes | DOM element evidence |
| G6 | click path만 있고 refresh/back/auth/cross-device 끊김 | P0 | yes | journey lifecycle |
| G7 | 접근성·전이 피드백 누락 | P1 | yes | action accessibility + T0/During/Done |
| G8 | AI assist interaction이 hand-wave | P1 | yes | AI 5-cell |
| G9 | P1 defer가 현재 release에서 어떻게 보이는지 불명 | P0 | yes | release entry behavior + decision ref |
| G10 | real-user validation 과장 | P0 | yes | independent `user_validated` flag |
| G11 | 구현 ticket이 FE/BE로 찢어져 user outcome이 늦게 드러남 | P1 | yes | journey tracer-bullet slices |
| G12 | legacy folder migration 비용 | P1 | yes | fail + actionable migration report |
| G13 | 실제 사용자 만족 | P1 | no | test protocol; 결과 없으면 unverified |
| G14 | downstream visual/risk skill이 옛 screen contract만 소비해 manifest와 drift | P0 | yes | 모든 P0/state/flow 소비자가 manifest ID를 함께 참조 |

재스윕 결과 새 P0 gap 0. 구현 후 동일 ledger를 code review와 scenario verification에서 다시 대조한다.
