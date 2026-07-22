# 검증 방식과 명령

검증기는 문서가 존재하는지만 세지 않습니다. 핵심 문서의 실질 내용, 조사·아이데이션 근거, 사용자가 확정한 결정 기록, 파일 지문, 화면·행동·상태·서비스 책임의 연결을 확인합니다.

검증은 제품 판단이나 사용자 조사를 대신하지 않습니다. 구조적 누락, 오래된 검토 결과, 서로 충돌하는 상태를 빠르게 찾는 안전장치입니다.

## 기획 경계

제품 정의 전의 계약을 확인합니다.

```bash
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage contract
```

디자인 전달이 가능한 기획 패키지를 확인합니다.

```bash
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage planning
```

`planning` 단계는 다음을 요구합니다.

- 컨셉, 브랜드 방향, 메커니즘과 PRD
- 여섯 관점의 교차점검과 중요한 문제의 해결
- 사용자가 확정한 첫 버전 범위와 제품 정의
- 화면·서비스 계약, 실현성 점검과 미정의 화면 점검
- 낮은 해상도의 흐름 보드
- `03-design-brief.md`

시각 디자인 파일, 완성 화면, 프로토타입이나 디자인 승인은 요구하지 않습니다. 통과 상태는 `planning-structure-pass`이며 기획의 시장성이나 판단 품질이 증명됐다는 뜻은 아닙니다. Lite는 `lite-planning-pass`로 별도 표시됩니다.

## 선택형 디자인 제작 경계

디자인 제작을 시작한 프로젝트에서만 사용합니다.

시각 방향과 대표 화면을 각각 먼저 확인합니다.

```bash
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage visual-direction
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage key-screen
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage prototype
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage design
python3 scripts/validate_service_blueprint.py docs/product-planning/<slug> --stage handoff
```

모든 명령은 `00-validation-report.{json,md}`와 대시보드를 다시 씁니다. 마지막 명령은 `05-readiness-report.json`과 `05-readiness-report.md`도 씁니다. `design-pass`만으로는 전달 준비가 되지 않으며, `handoff-pass`만 사용자가 승인한 제품·디자인 전달 상태를 의미합니다. 기술 설계나 구현 준비 완료를 의미하지는 않습니다.

## 내부 데이터

- `02.05-planning-quality-review.json`은 교차점검 역할, 발견사항, 사용자 결정과 검토한 원본의 지문을 보관합니다.
- `02.1-product-definition.json`은 사용자, 요구사항과 진입점의 기준입니다.
- `02.6-service-manifest.json`은 화면, 행동, 상태, 서비스 작업과 여정의 연결을 보관합니다.
- `00-workflow-state.json`은 실제 사용자 메시지에 연결된 결정과 무효화 이력을 보관합니다.
- `03.4-visual-directions.json`과 `03.8-key-screen-review.json`은 선택형 디자인 과정의 중간 승인을 보관합니다.
- `05-design-acceptance.json`은 선택형 디자인 제작에서만 사용합니다.

원본 문서가 바뀌면 저장된 지문이 달라져 이전 검토나 디자인 승인이 오래된 것으로 판정됩니다. 내부 코드와 심각도 표시는 운영과 자동 검증을 위한 것이며 README의 사용자 안내에는 노출하지 않습니다.
