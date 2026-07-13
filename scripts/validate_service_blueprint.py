#!/usr/bin/env python3
"""Validate Product Blueprint service contracts against their rendered evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
DECISION_NEEDED = "decision-needed:"
NA_PREFIX = "n/a:"

STANDARD_ARTIFACTS = (
    "00-brief.md",
    "00-decision-log.md",
    "00-review-dashboard.html",
    "02-prd.md",
    "02.1-product-definition.json",
    "02.5-screen-contracts.md",
    "02.6-service-manifest.json",
    "02.8-undefined-surfaces.md",
    "03-storyboard.html",
    "03.7-ux-writing.md",
    "04.1-visual-quality-gate.md",
    "04.2-backend-systems-brief.md",
    "04.3-design-system.md",
    "04.32-design-system-workbench.md",
    "04.36-clickable-demo.md",
    "04.4-prototype-test.md",
    "04.45-design-critique.md",
    "04.5-feasibility-review.md",
    "05-design-acceptance.json",
    "05-engineering-handoff.md",
)

LITE_ARTIFACTS = (
    "00-brief.md",
    "00-decision-log.md",
    "00-review-dashboard.html",
    "02-prd.md",
    "02.1-product-definition.json",
    "02.5-screen-contracts.md",
    "02.6-service-manifest.json",
    "03-storyboard.html",
)

CONTRACT_ARTIFACTS = (
    "00-brief.md",
    "00-decision-log.md",
    "00-review-dashboard.html",
    "02-prd.md",
    "02.1-product-definition.json",
    "02.5-screen-contracts.md",
    "02.6-service-manifest.json",
)

PROTOTYPE_ARTIFACTS = CONTRACT_ARTIFACTS + (
    "03-storyboard.html",
    "04.2-backend-systems-brief.md",
    "04.36-clickable-demo.md",
)

DESIGN_ARTIFACTS = tuple(item for item in STANDARD_ARTIFACTS if item != "05-engineering-handoff.md")
DESIGN_SOURCE_FILES = (
    "02.1-product-definition.json",
    "02-prd.md",
    "02.5-screen-contracts.md",
    "02.6-service-manifest.json",
    "02.8-undefined-surfaces.md",
    "03-storyboard.html",
    "03.7-ux-writing.md",
    "04.1-visual-quality-gate.md",
    "04.2-backend-systems-brief.md",
    "04.3-design-system.md",
    "04.32-design-system-workbench.md",
    "04.36-clickable-demo.md",
    "04.37-runtime-verification.json",
    "04.4-prototype-test.md",
    "04.45-design-critique.md",
    "04.5-feasibility-review.md",
)

SURFACE_TYPES = {"screen", "overlay", "sheet", "dialog", "panel", "background"}
ACTION_TYPES = {"navigate", "open-overlay", "close-overlay", "read", "write", "destructive", "external"}
STATE_TYPES = {"default", "loading", "empty", "error", "success", "locked", "permission", "offline", "conflict", "paid"}
OPERATION_TYPES = {"read", "write", "destructive", "external"}
OPERATION_OWNERS = {"frontend-local", "backend", "external"}
PERSISTENCE_TYPES = {"none", "session", "account", "cross-device"}
RISK_DOMAINS = {"adult", "minors", "payments", "ugc", "pii", "ai-generated"}
STATUS_KEYS = ("defined", "prototyped", "wired", "contracted", "verified")
REQUIREMENT_KINDS = {"journey", "content", "interaction", "system", "quality"}
ENTRY_POINT_LIFECYCLES = {
    "first-use",
    "returning",
    "external-result",
    "edit",
    "redirect",
    "refresh",
    "back",
    "cross-device",
    "offline",
}
DESIGN_FINDING_CATEGORIES = {"mental-model", "flow", "surface", "responsive", "visual", "copy", "accessibility"}
VISUAL_EVIDENCE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".svg"}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    path: str
    owner: str


class DemoParser(HTMLParser):
    """Collect contract evidence without third-party HTML dependencies."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: dict[str, dict[str, str]] = {}
        self.duplicate_ids: set[str] = set()
        self.product_controls: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        element_id = values.get("id")
        if element_id:
            if element_id in self.elements:
                self.duplicate_ids.add(element_id)
            self.elements[element_id] = values

        interactive = tag in {"button", "a"} or values.get("role") in {
            "button",
            "link",
            "menuitem",
            "switch",
            "tab",
        }
        if interactive and "data-demo-control" not in values:
            self.product_controls.append((tag, values))


class Validator:
    def __init__(self, root: Path, profile: str | None = None, stage: str = "handoff") -> None:
        self.root = root.resolve()
        self.profile_override = profile
        self.stage = stage
        self.manifest_path = self.root / "02.6-service-manifest.json"
        self.product_definition_path = self.root / "02.1-product-definition.json"
        self.design_acceptance_path = self.root / "05-design-acceptance.json"
        self.manifest: dict[str, Any] = {}
        self.product_definition: dict[str, Any] = {}
        self.design_acceptance: dict[str, Any] = {}
        self.personas: dict[str, dict[str, Any]] = {}
        self.requirements: dict[str, dict[str, Any]] = {}
        self.entry_points: dict[str, dict[str, Any]] = {}
        self.findings: list[Finding] = []
        self.demo_cache: dict[Path, DemoParser] = {}

    def add(self, code: str, message: str, path: str, owner: str, severity: str = "error") -> None:
        self.findings.append(Finding(code, severity, message, path, owner))

    def run(self) -> dict[str, Any]:
        self._load_manifest()
        self._load_product_definition()
        profile = self._profile()
        if self.stage in {"design", "handoff", "technical"} and profile != "lite":
            self._load_design_acceptance()
        self._validate_artifacts(profile, self.stage)
        if self.product_definition:
            self._validate_product_definition()
        if self.manifest:
            self._validate_shape(profile)
            self._validate_contract(profile, self.stage)
            if self.stage in {"design", "handoff", "technical"} and profile != "lite":
                self._validate_design_acceptance()
            if self.stage == "handoff":
                self._validate_readiness_claims()
        return self._report(profile)

    def _load_manifest(self) -> None:
        if not self.manifest_path.exists():
            self.add(
                "SERVICE_MANIFEST_MISSING",
                "Create 02.6-service-manifest.json with product-blueprint:service-contract before handoff.",
                "02.6-service-manifest.json",
                "service-contract",
            )
            return
        try:
            loaded = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.add("MANIFEST_INVALID_JSON", str(exc), "02.6-service-manifest.json", "service-contract")
            return
        if not isinstance(loaded, dict):
            self.add("MANIFEST_INVALID_SHAPE", "Manifest root must be an object.", "02.6-service-manifest.json", "service-contract")
            return
        self.manifest = loaded

    def _load_product_definition(self) -> None:
        if not self.product_definition_path.exists():
            self.add(
                "PRODUCT_DEFINITION_MISSING",
                "Create and explicitly confirm 02.1-product-definition.json before screen contracts.",
                "02.1-product-definition.json",
                "product-definition",
            )
            return
        try:
            loaded = json.loads(self.product_definition_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.add("PRODUCT_DEFINITION_INVALID", str(exc), "02.1-product-definition.json", "product-definition")
            return
        if not isinstance(loaded, dict):
            self.add("PRODUCT_DEFINITION_INVALID", "Product definition root must be an object.", "02.1-product-definition.json", "product-definition")
            return
        self.product_definition = loaded

    def _load_design_acceptance(self) -> None:
        if not self.design_acceptance_path.exists():
            self.add(
                "DESIGN_ACCEPTANCE_MISSING",
                "Create 05-design-acceptance.json after complete visual review and explicit user approval.",
                "05-design-acceptance.json",
                "design-acceptance",
            )
            return
        try:
            loaded = json.loads(self.design_acceptance_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.add("DESIGN_ACCEPTANCE_INVALID", str(exc), "05-design-acceptance.json", "design-acceptance")
            return
        if not isinstance(loaded, dict):
            self.add("DESIGN_ACCEPTANCE_INVALID", "Design acceptance root must be an object.", "05-design-acceptance.json", "design-acceptance")
            return
        self.design_acceptance = loaded

    def _profile(self) -> str:
        if self.profile_override:
            return self.profile_override
        project = self.manifest.get("project", {}) if self.manifest else {}
        mode = project.get("mode", "standard") if isinstance(project, dict) else "standard"
        return mode if mode in {"lite", "standard", "deep"} else "standard"

    def _validate_artifacts(self, profile: str, stage: str) -> None:
        if stage == "contract":
            required = CONTRACT_ARTIFACTS
        elif stage == "prototype":
            required = PROTOTYPE_ARTIFACTS
        elif stage == "design":
            required = DESIGN_ARTIFACTS
        else:
            required = LITE_ARTIFACTS if profile == "lite" else STANDARD_ARTIFACTS
        for relative in required:
            if not (self.root / relative).is_file():
                self.add(
                    "REQUIRED_ARTIFACT_MISSING",
                    f"Required {profile} artifact is missing: {relative}",
                    relative,
                    "orchestrate",
                )

    def _validate_shape(self, profile: str) -> None:
        if self.manifest.get("schema_version") != "1.0":
            self.add("UNSUPPORTED_SCHEMA_VERSION", "schema_version must be 1.0.", "02.6-service-manifest.json", "service-contract")

        project = self._mapping("project")
        if not self._meaningful(project.get("name")):
            self.add("PROJECT_NAME_MISSING", "project.name is required.", "project.name", "service-contract")
        mode = project.get("mode")
        if mode not in {"lite", "standard", "deep"}:
            self.add("INVALID_PROFILE", "project.mode must be lite, standard, or deep.", "project.mode", "service-contract")
        elif self.profile_override and mode != profile:
            self.add("PROFILE_MISMATCH", f"Manifest mode {mode!r} does not match --profile {profile!r}.", "project.mode", "service-contract")

        release = self._mapping("release_profile")
        if not self._meaningful(release.get("id")):
            self.add("RELEASE_PROFILE_MISSING", "release_profile.id is required.", "release_profile.id", "prd")
        if not isinstance(release.get("roles"), list) or not release.get("roles"):
            self.add("RELEASE_ROLES_MISSING", "release_profile.roles needs at least one role.", "release_profile.roles", "prd")
        self._validate_exclusions(release.get("excluded", []))
        self._validate_accepted_limitations(release.get("accepted_limitations", []))
        risk_domains = release.get("risk_domains", [])
        if not isinstance(risk_domains, list) or any(item not in RISK_DOMAINS for item in risk_domains):
            self.add("INVALID_RISK_DOMAINS", f"risk_domains must contain only: {', '.join(sorted(RISK_DOMAINS))}.", "release_profile.risk_domains", "risk-register")
        elif self.stage in {"design", "handoff", "technical"} and risk_domains and not (self.root / "04.55-risk-register.md").is_file():
            self.add("RISK_REGISTER_MISSING", "A risk register is mandatory for the declared risk domains.", "04.55-risk-register.md", "risk-register")

        for key in ("surfaces", "actions", "states", "operations", "ai_assists", "journeys"):
            if not isinstance(self.manifest.get(key), list):
                self.add("MANIFEST_INVALID_SHAPE", f"{key} must be an array.", key, "service-contract")

        for key in ("surfaces", "actions", "journeys"):
            if not self.manifest.get(key):
                self.add("CONTRACT_COLLECTION_EMPTY", f"{key} cannot be empty for {profile}.", key, "service-contract")

        validation = self._mapping("user_validation")
        status = validation.get("status")
        if status not in {"not-run", "heuristic", "real-user"}:
            self.add("INVALID_USER_VALIDATION_STATUS", "Use not-run, heuristic, or real-user.", "user_validation.status", "prototype-test")
        if status == "real-user" and not validation.get("evidence"):
            self.add("REAL_USER_EVIDENCE_MISSING", "real-user status requires evidence.", "user_validation.evidence", "prototype-test")

    def _validate_product_definition(self) -> None:
        definition = self.product_definition
        if definition.get("schema_version") != "1.0":
            self.add("UNSUPPORTED_PRODUCT_DEFINITION_VERSION", "schema_version must be 1.0.", "02.1-product-definition.json", "product-definition")
        if definition.get("status") != "user-confirmed":
            self.add("PRODUCT_DEFINITION_UNCONFIRMED", "The product definition needs explicit user confirmation before contract pass.", "status", "product-definition")
        confirmation = definition.get("confirmation")
        if not isinstance(confirmation, dict):
            self.add("PRODUCT_DEFINITION_UNCONFIRMED", "confirmation must be an object.", "confirmation", "product-definition")
        else:
            if confirmation.get("kind") != "explicit-user":
                self.add("PRODUCT_DEFINITION_UNCONFIRMED", "confirmation.kind must be explicit-user.", "confirmation.kind", "product-definition")
            for key in ("decision_ref", "confirmed_at", "evidence"):
                if not self._meaningful(confirmation.get(key)):
                    self.add("PRODUCT_DEFINITION_UNCONFIRMED", f"confirmation.{key} is required.", f"confirmation.{key}", "product-definition")

        self.personas = self._definition_index("personas")
        self.requirements = self._definition_index("requirements")
        self.entry_points = self._definition_index("entry_points")
        if not self.personas:
            self.add("PRODUCT_DEFINITION_EMPTY", "At least one persona is required.", "personas", "product-definition")
        if not self.requirements:
            self.add("PRODUCT_DEFINITION_EMPTY", "At least one requirement is required.", "requirements", "product-definition")
        if not self.entry_points:
            self.add("PRODUCT_DEFINITION_EMPTY", "At least one entry point is required.", "entry_points", "product-definition")

        for persona_id, persona in self.personas.items():
            path = f"personas.{persona_id}"
            for key in ("label", "mental_model"):
                if not self._meaningful(persona.get(key)):
                    self.add("PERSONA_INCOMPLETE", f"{key} is required in user language.", f"{path}.{key}", "product-definition")
            for key in ("jobs", "source_refs"):
                if not isinstance(persona.get(key), list) or not persona.get(key):
                    self.add("PERSONA_INCOMPLETE", f"{key} needs at least one item.", f"{path}.{key}", "product-definition")

        for requirement_id, requirement in self.requirements.items():
            path = f"requirements.{requirement_id}"
            if requirement.get("kind") not in REQUIREMENT_KINDS:
                self.add("INVALID_REQUIREMENT_KIND", f"kind must be one of: {', '.join(sorted(REQUIREMENT_KINDS))}.", f"{path}.kind", "product-definition")
            if requirement.get("priority") not in {"P0", "P1", "P2"}:
                self.add("INVALID_REQUIREMENT_PRIORITY", "priority must be P0, P1, or P2.", f"{path}.priority", "product-definition")
            if requirement.get("status") not in {"included", "excluded"}:
                self.add("INVALID_REQUIREMENT_STATUS", "status must be included or excluded.", f"{path}.status", "product-definition")
            for key in ("statement", "decision_ref"):
                if not self._meaningful(requirement.get(key)):
                    self.add("REQUIREMENT_INCOMPLETE", f"{key} is required.", f"{path}.{key}", "product-definition")
            for key in ("persona_ids", "source_refs", "acceptance_outcomes"):
                values = requirement.get(key)
                if not isinstance(values, list) or not values:
                    self.add("REQUIREMENT_INCOMPLETE", f"{key} needs at least one item.", f"{path}.{key}", "product-definition")
            for persona_id in requirement.get("persona_ids", []):
                if persona_id not in self.personas:
                    self.add("UNKNOWN_PERSONA_REFERENCE", f"Unknown persona {persona_id!r}.", f"{path}.persona_ids", "product-definition")
            if requirement.get("status") == "excluded" and not self._meaningful(requirement.get("current_entry_behavior")):
                self.add("EXCLUDED_REQUIREMENT_UNDEFINED", "Excluded requirements need current_entry_behavior.", f"{path}.current_entry_behavior", "product-definition")

        for entry_id, entry in self.entry_points.items():
            path = f"entry_points.{entry_id}"
            if entry.get("persona_id") not in self.personas:
                self.add("UNKNOWN_PERSONA_REFERENCE", f"Unknown persona {entry.get('persona_id')!r}.", f"{path}.persona_id", "product-definition")
            for key in ("label", "trigger", "context", "expected_outcome"):
                if not self._meaningful(entry.get(key)):
                    self.add("ENTRY_POINT_INCOMPLETE", f"{key} is required.", f"{path}.{key}", "product-definition")
            lifecycle = entry.get("lifecycle")
            if not isinstance(lifecycle, list) or not lifecycle or any(item not in ENTRY_POINT_LIFECYCLES for item in lifecycle):
                self.add("ENTRY_POINT_INCOMPLETE", "lifecycle needs valid entry/lifecycle values.", f"{path}.lifecycle", "product-definition")
            if not isinstance(entry.get("source_refs"), list) or not entry.get("source_refs"):
                self.add("ENTRY_POINT_INCOMPLETE", "source_refs needs at least one item.", f"{path}.source_refs", "product-definition")

        roles = self._mapping("release_profile").get("roles", []) if self.manifest else []
        for role in roles if isinstance(roles, list) else []:
            if role not in self.personas:
                self.add("UNKNOWN_PERSONA_REFERENCE", f"Release role {role!r} is not a confirmed persona ID.", "release_profile.roles", "product-definition")

    def _definition_index(self, key: str) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        values = self.product_definition.get(key, [])
        if not isinstance(values, list):
            self.add("PRODUCT_DEFINITION_INVALID", f"{key} must be an array.", key, "product-definition")
            return result
        for position, item in enumerate(values):
            path = f"{key}[{position}]"
            if not isinstance(item, dict):
                self.add("PRODUCT_DEFINITION_INVALID", f"{path} must be an object.", path, "product-definition")
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not ID_RE.fullmatch(item_id):
                self.add("INVALID_CONTRACT_ID", f"{path}.id must match {ID_RE.pattern}.", f"{path}.id", "product-definition")
                continue
            if item_id in result:
                self.add("DUPLICATE_CONTRACT_ID", f"Duplicate id: {item_id}", f"{path}.id", "product-definition")
                continue
            result[item_id] = item
        return result

    def _validate_contract(self, profile: str, stage: str) -> None:
        surfaces = self._index("surfaces", "screen-contract")
        actions = self._index("actions", "screen-contract")
        states = self._index("states", "screen-contract")
        operations = self._index("operations", "service-contract")
        ai_assists = self._index("ai_assists", "service-contract")
        journeys = self._index("journeys", "service-contract")

        self._validate_surfaces(surfaces, actions, states, profile, stage)
        self._validate_actions(actions, surfaces, operations, profile, stage)
        self._validate_states(states, surfaces, actions, profile, stage)
        self._validate_operations(operations, profile)
        self._validate_ai_assists(ai_assists, actions)
        self._validate_journeys(journeys, surfaces, actions, states, profile)
        self._validate_product_traceability(surfaces, actions, operations, journeys)
        self._validate_reachability(surfaces, actions, journeys)
        if profile != "lite" and stage in {"prototype", "design", "handoff", "technical"}:
            self._validate_uncontracted_controls(actions)
            self._validate_runtime_evidence(actions, states)

    def _validate_product_traceability(
        self,
        surfaces: dict[str, dict[str, Any]],
        actions: dict[str, dict[str, Any]],
        operations: dict[str, dict[str, Any]],
        journeys: dict[str, dict[str, Any]],
    ) -> None:
        if not self.product_definition:
            return
        declared_file = self.manifest.get("product_definition_file")
        if declared_file != "02.1-product-definition.json":
            self.add("PRODUCT_DEFINITION_LINK_MISSING", "product_definition_file must be 02.1-product-definition.json.", "product_definition_file", "service-contract")

        coverage: dict[str, set[str]] = {requirement_id: set() for requirement_id in self.requirements}
        entry_coverage: dict[str, set[str]] = {entry_id: set() for entry_id in self.entry_points}

        for collection_name, items in (("surfaces", surfaces), ("actions", actions), ("operations", operations), ("journeys", journeys)):
            for item_id, item in items.items():
                path = f"{collection_name}.{item_id}.requirement_ids"
                refs = item.get("requirement_ids")
                if not isinstance(refs, list) or not refs:
                    self.add("REQUIREMENT_TRACE_MISSING", f"{collection_name[:-1]} {item_id!r} needs requirement_ids.", path, "service-contract")
                    continue
                for requirement_id in refs:
                    if requirement_id not in self.requirements:
                        self.add("UNKNOWN_REQUIREMENT_REFERENCE", f"Unknown requirement {requirement_id!r}.", path, "service-contract")
                    else:
                        coverage[requirement_id].add(collection_name[:-1])

        for surface_id, surface in surfaces.items():
            path = f"surfaces.{surface_id}.persona_ids"
            refs = surface.get("persona_ids")
            if surface.get("priority") == "P0" and (not isinstance(refs, list) or not refs):
                self.add("PERSONA_TRACE_MISSING", "P0 surface needs persona_ids.", path, "screen-contract")
            for persona_id in refs if isinstance(refs, list) else []:
                if persona_id not in self.personas:
                    self.add("UNKNOWN_PERSONA_REFERENCE", f"Unknown persona {persona_id!r}.", path, "screen-contract")

        for journey_id, journey in journeys.items():
            path = f"journeys.{journey_id}"
            persona_id = journey.get("persona_id")
            if persona_id not in self.personas:
                self.add("UNKNOWN_PERSONA_REFERENCE", f"Unknown journey persona {persona_id!r}.", f"{path}.persona_id", "service-contract")
            entry_ids = journey.get("entry_point_ids")
            if not isinstance(entry_ids, list) or not entry_ids:
                self.add("ENTRY_POINT_TRACE_MISSING", "Journey needs entry_point_ids.", f"{path}.entry_point_ids", "service-contract")
            else:
                for entry_id in entry_ids:
                    if entry_id not in self.entry_points:
                        self.add("UNKNOWN_ENTRY_POINT_REFERENCE", f"Unknown entry point {entry_id!r}.", f"{path}.entry_point_ids", "service-contract")
                    else:
                        entry_coverage[entry_id].add(journey_id)
                        if persona_id != self.entry_points[entry_id].get("persona_id"):
                            self.add("ENTRY_POINT_PERSONA_MISMATCH", f"Entry point {entry_id!r} belongs to another persona.", f"{path}.entry_point_ids", "service-contract")

        for requirement_id, requirement in self.requirements.items():
            if requirement.get("status") != "included" or requirement.get("priority") != "P0":
                continue
            required_kinds = {"surface", "journey"}
            if requirement.get("kind") == "interaction":
                required_kinds.add("action")
            if requirement.get("kind") == "system":
                required_kinds.add("operation")
            missing = sorted(required_kinds - coverage.get(requirement_id, set()))
            if missing:
                self.add("P0_REQUIREMENT_UNCOVERED", f"P0 requirement {requirement_id!r} is missing: {', '.join(missing)}.", f"requirements.{requirement_id}", "service-contract")

        for entry_id, journey_ids in entry_coverage.items():
            if not journey_ids:
                self.add("ENTRY_POINT_UNCOVERED", f"Entry point {entry_id!r} has no journey.", f"entry_points.{entry_id}", "service-contract")

    def _mapping(self, key: str) -> dict[str, Any]:
        value = self.manifest.get(key, {})
        if isinstance(value, dict):
            return value
        self.add("MANIFEST_INVALID_SHAPE", f"{key} must be an object.", key, "service-contract")
        return {}

    def _index(self, key: str, owner: str) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        values = self.manifest.get(key, [])
        if not isinstance(values, list):
            return result
        for position, item in enumerate(values):
            path = f"{key}[{position}]"
            if not isinstance(item, dict):
                self.add("MANIFEST_INVALID_SHAPE", f"{path} must be an object.", path, owner)
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not ID_RE.fullmatch(item_id):
                self.add("INVALID_CONTRACT_ID", f"{path}.id must match {ID_RE.pattern}.", f"{path}.id", owner)
                continue
            if item_id in result:
                self.add("DUPLICATE_CONTRACT_ID", f"Duplicate id: {item_id}", f"{path}.id", owner)
                continue
            result[item_id] = item
        return result

    def _validate_exclusions(self, exclusions: Any) -> None:
        if not isinstance(exclusions, list):
            self.add("MANIFEST_INVALID_SHAPE", "release_profile.excluded must be an array.", "release_profile.excluded", "prd")
            return
        for index, item in enumerate(exclusions):
            path = f"release_profile.excluded[{index}]"
            if not isinstance(item, dict):
                self.add("MANIFEST_INVALID_SHAPE", f"{path} must be an object.", path, "prd")
                continue
            for key in ("id", "decision_ref", "current_entry_behavior"):
                if not self._meaningful(item.get(key)):
                    self.add("DEFERRED_ENTRY_UNDEFINED", f"{path}.{key} is required.", f"{path}.{key}", "prd")

    def _validate_accepted_limitations(self, limitations: Any) -> None:
        if not isinstance(limitations, list):
            self.add("MANIFEST_INVALID_SHAPE", "release_profile.accepted_limitations must be an array.", "release_profile.accepted_limitations", "implementation-readiness")
            return
        for index, item in enumerate(limitations):
            path = f"release_profile.accepted_limitations[{index}]"
            if not isinstance(item, dict):
                self.add("MANIFEST_INVALID_SHAPE", f"{path} must be an object.", path, "implementation-readiness")
                continue
            for key in ("id", "decision_ref", "owner", "consequence"):
                if not self._meaningful(item.get(key)):
                    self.add("ACCEPTED_LIMITATION_INCOMPLETE", f"{path}.{key} is required.", f"{path}.{key}", "implementation-readiness")

    def _validate_surfaces(
        self,
        surfaces: dict[str, dict[str, Any]],
        actions: dict[str, dict[str, Any]],
        states: dict[str, dict[str, Any]],
        profile: str,
        stage: str,
    ) -> None:
        responsive_web = "responsive-web" in self._mapping("project").get("platforms", [])
        for surface_id, surface in surfaces.items():
            path = f"surfaces.{surface_id}"
            if surface.get("type") not in SURFACE_TYPES:
                self.add("INVALID_SURFACE_TYPE", f"Unknown surface type: {surface.get('type')!r}", f"{path}.type", "screen-contract")
            if surface.get("priority") not in {"P0", "P1", "P2"}:
                self.add("INVALID_SURFACE_PRIORITY", "priority must be P0, P1, or P2.", f"{path}.priority", "prd")
            if not self._meaningful(surface.get("purpose")):
                self.add("SURFACE_PURPOSE_MISSING", "Surface purpose is required.", f"{path}.purpose", "screen-contract")

            for key in ("entry_action_ids", "exit_action_ids"):
                refs = surface.get(key, [])
                if not isinstance(refs, list):
                    self.add("MANIFEST_INVALID_SHAPE", f"{path}.{key} must be an array.", f"{path}.{key}", "screen-contract")
                    continue
                for ref in refs:
                    if ref not in actions:
                        self.add("UNKNOWN_ACTION_REFERENCE", f"Unknown action {ref!r}.", f"{path}.{key}", "screen-contract")
            for ref in surface.get("required_state_ids", []):
                if ref not in states:
                    self.add("UNKNOWN_STATE_REFERENCE", f"Unknown state {ref!r}.", f"{path}.required_state_ids", "screen-contract")

            if surface.get("priority") == "P0" and surface.get("type") != "background" and profile != "lite":
                required_status = ("defined",)
                if stage == "prototype":
                    required_status = STATUS_KEYS[:-1]
                elif stage in {"design", "handoff", "technical"}:
                    required_status = STATUS_KEYS
                self._validate_status(surface.get("status"), path, required_status)
                if stage in {"prototype", "design", "handoff", "technical"}:
                    self._validate_dom_reference(surface.get("prototype"), surface_id, "data-surface", "SURFACE_NOT_PROTOTYPED", path, "clickable-demo")

            if responsive_web and surface.get("priority") == "P0" and surface.get("type") == "screen" and profile != "lite":
                responsive = surface.get("responsive", {})
                if not isinstance(responsive, dict) or not self._meaningful(responsive.get("strategy")):
                    self.add("RESPONSIVE_EVIDENCE_MISSING", "P0 screen needs a responsive strategy.", f"{path}.responsive", "screen-contract")
                else:
                    has_desktop = self._meaningful(responsive.get("desktop_element_id"))
                    has_rule = self._meaningful(responsive.get("derivation_rule"))
                    if not (has_desktop or has_rule):
                        self.add("RESPONSIVE_EVIDENCE_MISSING", "Provide desktop evidence or an explicit derivation rule.", f"{path}.responsive", "clickable-demo")
                    if has_desktop and stage in {"prototype", "design", "handoff", "technical"}:
                        prototype = surface.get("prototype", {})
                        reference = {"file": prototype.get("file"), "element_id": responsive.get("desktop_element_id")}
                        self._validate_dom_reference(reference, None, None, "RESPONSIVE_EVIDENCE_MISSING", f"{path}.responsive", "clickable-demo")

    def _validate_status(self, status: Any, path: str, required_status: tuple[str, ...]) -> None:
        if not isinstance(status, dict):
            self.add("SURFACE_STATUS_MISSING", "P0 surface needs five evidence-backed status fields.", f"{path}.status", "service-contract")
            return
        seen_false = False
        for key in STATUS_KEYS:
            value = status.get(key)
            if not isinstance(value, bool):
                self.add("SURFACE_STATUS_MISSING", f"{path}.status.{key} must be boolean.", f"{path}.status.{key}", "service-contract")
                continue
            if seen_false and value:
                self.add("INVALID_STATUS_PROGRESSION", f"{key} cannot be true after an earlier stage is false.", f"{path}.status.{key}", "service-contract")
            seen_false = seen_false or not value
        if any(status.get(key) is not True for key in required_status):
            code = "SURFACE_NOT_VERIFIED" if "verified" in required_status else "SURFACE_STAGE_INCOMPLETE"
            self.add(code, f"Required maturity stages are not complete for {self.stage}: {', '.join(required_status)}.", f"{path}.status", "implementation-readiness")

    def _validate_actions(
        self,
        actions: dict[str, dict[str, Any]],
        surfaces: dict[str, dict[str, Any]],
        operations: dict[str, dict[str, Any]],
        profile: str,
        stage: str,
    ) -> None:
        for action_id, action in actions.items():
            path = f"actions.{action_id}"
            action_type = action.get("kind")
            if action_type not in ACTION_TYPES:
                self.add("INVALID_ACTION_TYPE", f"Unknown action type: {action_type!r}", f"{path}.kind", "screen-contract")
            source = action.get("source_surface_id")
            if source not in surfaces:
                self.add("UNKNOWN_SURFACE_REFERENCE", f"Unknown source surface {source!r}.", f"{path}.source_surface_id", "screen-contract")
            elif action_id not in surfaces[source].get("exit_action_ids", []):
                self.add("WIRING_MATRIX_MISMATCH", f"Source surface {source!r} does not list {action_id!r} as an exit.", f"{path}.source_surface_id", "screen-contract")

            target = action.get("target", {})
            if not isinstance(target, dict) or not (self._meaningful(target.get("surface_id")) or self._meaningful(target.get("effect"))):
                self.add("ACTION_TARGET_MISSING", "Action needs target.surface_id or target.effect.", f"{path}.target", "screen-contract")
            elif target.get("surface_id") and target.get("surface_id") not in surfaces:
                self.add("UNKNOWN_SURFACE_REFERENCE", f"Unknown target surface {target.get('surface_id')!r}.", f"{path}.target.surface_id", "screen-contract")
            elif target.get("surface_id") and action_id not in surfaces[target["surface_id"]].get("entry_action_ids", []):
                self.add("WIRING_MATRIX_MISMATCH", f"Target surface {target['surface_id']!r} does not list {action_id!r} as an entry.", f"{path}.target.surface_id", "screen-contract")

            operation_id = action.get("operation_id")
            if action_type in {"read", "write", "destructive", "external"}:
                if operation_id not in operations:
                    self.add("INCOMPLETE_OPERATION_CONTRACT", "Data/external action needs a valid operation_id.", f"{path}.operation_id", "service-contract")
                elif operations[operation_id].get("kind") != action_type:
                    self.add("OPERATION_KIND_MISMATCH", f"Action kind {action_type!r} and operation kind {operations[operation_id].get('kind')!r} differ.", f"{path}.operation_id", "service-contract")
            if action_type == "destructive" and not self._meaningful(action.get("confirmation")):
                self.add("DESTRUCTIVE_CONFIRMATION_MISSING", "Destructive actions require an explicit confirmation contract.", f"{path}.confirmation", "screen-contract")

            for group, keys in (("feedback", ("t0", "during", "done")), ("accessibility", ("keyboard", "focus", "announcement"))):
                values = action.get(group, {})
                if not isinstance(values, dict):
                    self.add("INCOMPLETE_ACTION_CONTRACT", f"{group} must be an object.", f"{path}.{group}", "screen-contract")
                    continue
                for key in keys:
                    if not self._meaningful(values.get(key)):
                        self.add("INCOMPLETE_ACTION_CONTRACT", f"{group}.{key} is required; use n/a:<reason> only when inapplicable.", f"{path}.{group}.{key}", "screen-contract")

            if profile != "lite" and stage in {"prototype", "design", "handoff", "technical"}:
                self._validate_action_dom(action_id, action)

    def _validate_states(
        self,
        states: dict[str, dict[str, Any]],
        surfaces: dict[str, dict[str, Any]],
        actions: dict[str, dict[str, Any]],
        profile: str,
        stage: str,
    ) -> None:
        for state_id, state in states.items():
            path = f"states.{state_id}"
            if state.get("surface_id") not in surfaces:
                self.add("UNKNOWN_SURFACE_REFERENCE", f"Unknown state surface {state.get('surface_id')!r}.", f"{path}.surface_id", "screen-contract")
            elif state.get("required") is True and state_id not in surfaces[state["surface_id"]].get("required_state_ids", []):
                self.add("STATE_MATRIX_MISMATCH", f"Surface {state['surface_id']!r} does not list required state {state_id!r}.", f"{path}.surface_id", "screen-contract")
            if state.get("kind") not in STATE_TYPES:
                self.add("INVALID_STATE_TYPE", f"Unknown state type: {state.get('kind')!r}", f"{path}.kind", "screen-contract")
            recovery = state.get("recovery_action_id")
            if recovery and recovery not in actions:
                self.add("UNKNOWN_ACTION_REFERENCE", f"Unknown recovery action {recovery!r}.", f"{path}.recovery_action_id", "screen-contract")
            if state.get("required") is True and profile != "lite" and stage in {"prototype", "design", "handoff", "technical"}:
                if not self._meaningful(state.get("reproduction")):
                    self.add("STATE_REPRODUCTION_MISSING", "Required state needs a stable browser reproduction path.", f"{path}.reproduction", "clickable-demo")
                self._validate_dom_reference(state.get("prototype"), None, None, "STATE_NOT_REPRODUCIBLE", path, "clickable-demo")

    def _validate_operations(self, operations: dict[str, dict[str, Any]], profile: str) -> None:
        required = (
            "source_of_truth",
            "input_promise",
            "output_promise",
            "authorization",
            "idempotency",
            "consistency",
            "conflict_strategy",
            "failure",
            "recovery",
            "audit_retention",
            "latency_class",
            "cost_class",
            "observability",
            "abuse_boundary",
        )
        for operation_id, operation in operations.items():
            path = f"operations.{operation_id}"
            if operation.get("kind") not in OPERATION_TYPES:
                self.add("INVALID_OPERATION_TYPE", f"Unknown operation type: {operation.get('kind')!r}", f"{path}.kind", "service-contract")
            if operation.get("owner") not in OPERATION_OWNERS:
                self.add("INCOMPLETE_OPERATION_CONTRACT", "owner must be frontend-local, backend, or external.", f"{path}.owner", "service-contract")
            if operation.get("persistence") not in PERSISTENCE_TYPES:
                self.add("INCOMPLETE_OPERATION_CONTRACT", "Invalid persistence boundary.", f"{path}.persistence", "service-contract")
            for key in required:
                value = operation.get(key)
                if isinstance(value, str) and value.strip().startswith(DECISION_NEEDED):
                    self.add("OPERATION_DECISION_BLOCKER", f"Resolve {key} before readiness.", f"{path}.{key}", "backend-systems-brief")
                elif not self._meaningful(value):
                    self.add("INCOMPLETE_OPERATION_CONTRACT", f"{key} is required; use n/a:<reason> when inapplicable.", f"{path}.{key}", "service-contract")

    def _validate_ai_assists(
        self,
        ai_assists: dict[str, dict[str, Any]],
        actions: dict[str, dict[str, Any]],
    ) -> None:
        fields = ("input", "result_widget", "editable_unit", "save_destination", "failure_ui")
        for assist_id, assist in ai_assists.items():
            path = f"ai_assists.{assist_id}"
            if assist.get("trigger_action_id") not in actions:
                self.add("UNKNOWN_ACTION_REFERENCE", f"Unknown AI assist trigger {assist.get('trigger_action_id')!r}.", f"{path}.trigger_action_id", "service-contract")
            for key in fields:
                if not self._meaningful(assist.get(key)):
                    self.add("AI_ASSIST_HANDWAVE", f"AI assist requires {key}.", f"{path}.{key}", "service-contract")

    def _validate_journeys(
        self,
        journeys: dict[str, dict[str, Any]],
        surfaces: dict[str, dict[str, Any]],
        actions: dict[str, dict[str, Any]],
        states: dict[str, dict[str, Any]],
        profile: str,
    ) -> None:
        for journey_id, journey in journeys.items():
            path = f"journeys.{journey_id}"
            current = journey.get("start_surface_id")
            if current not in surfaces:
                self.add("UNKNOWN_SURFACE_REFERENCE", f"Unknown journey start {current!r}.", f"{path}.start_surface_id", "service-contract")
            steps = journey.get("steps", [])
            if not isinstance(steps, list) or not steps:
                self.add("JOURNEY_STEPS_MISSING", "Journey needs at least one action step.", f"{path}.steps", "service-contract")
                steps = []
            for position, action_id in enumerate(steps):
                action = actions.get(action_id)
                if not action:
                    self.add("UNKNOWN_ACTION_REFERENCE", f"Unknown journey action {action_id!r}.", f"{path}.steps[{position}]", "service-contract")
                    continue
                if current in surfaces and action.get("source_surface_id") != current:
                    self.add("JOURNEY_DISCONNECTED", f"Step {action_id} starts at {action.get('source_surface_id')!r}, expected {current!r}.", f"{path}.steps[{position}]", "service-contract")
                target_surface = action.get("target", {}).get("surface_id") if isinstance(action.get("target"), dict) else None
                if target_surface:
                    current = target_surface
            expected_end = journey.get("expected_end_surface_id")
            if expected_end not in surfaces:
                self.add("UNKNOWN_SURFACE_REFERENCE", f"Unknown journey end {expected_end!r}.", f"{path}.expected_end_surface_id", "service-contract")
            elif current != expected_end:
                self.add("JOURNEY_END_UNREACHABLE", f"Journey ends at {current!r}, not {expected_end!r}.", f"{path}.expected_end_surface_id", "service-contract")

            for key in ("refresh_resume", "back_behavior", "cross_device_behavior"):
                if not self._meaningful(journey.get(key)):
                    self.add("JOURNEY_LIFECYCLE_MISSING", f"{key} is required; use n/a:<reason> when inapplicable.", f"{path}.{key}", "service-contract")
            exceptions = journey.get("exception_paths", [])
            if profile != "lite" and not isinstance(exceptions, list):
                self.add("MANIFEST_INVALID_SHAPE", "exception_paths must be an array.", f"{path}.exception_paths", "service-contract")
            elif isinstance(exceptions, list):
                for index, branch in enumerate(exceptions):
                    if not isinstance(branch, dict):
                        self.add("MANIFEST_INVALID_SHAPE", "Exception path must be an object.", f"{path}.exception_paths[{index}]", "service-contract")
                        continue
                    state_id = branch.get("state_id")
                    recovery_id = branch.get("recovery_action_id")
                    if state_id not in states:
                        self.add("UNKNOWN_STATE_REFERENCE", f"Unknown exception state {state_id!r}.", f"{path}.exception_paths[{index}].state_id", "service-contract")
                    if recovery_id not in actions:
                        self.add("UNKNOWN_ACTION_REFERENCE", f"Unknown exception recovery {recovery_id!r}.", f"{path}.exception_paths[{index}].recovery_action_id", "service-contract")

    def _validate_reachability(
        self,
        surfaces: dict[str, dict[str, Any]],
        actions: dict[str, dict[str, Any]],
        journeys: dict[str, dict[str, Any]],
    ) -> None:
        graph: dict[str, set[str]] = {surface_id: set() for surface_id in surfaces}
        for action in actions.values():
            source = action.get("source_surface_id")
            target = action.get("target", {}).get("surface_id") if isinstance(action.get("target"), dict) else None
            if source in graph and target in surfaces:
                graph[source].add(target)
        stack = [journey.get("start_surface_id") for journey in journeys.values() if journey.get("start_surface_id") in surfaces]
        reachable: set[str] = set(stack)
        while stack:
            current = stack.pop()
            for target in graph.get(current, set()):
                if target not in reachable:
                    reachable.add(target)
                    stack.append(target)
        for surface_id, surface in surfaces.items():
            if surface.get("priority") == "P0" and surface.get("type") != "background" and surface_id not in reachable:
                self.add("UNREACHABLE_SURFACE", f"P0 surface {surface_id!r} is unreachable from every journey start.", f"surfaces.{surface_id}", "screen-contract")

    def _validate_uncontracted_controls(self, actions: dict[str, dict[str, Any]]) -> None:
        known = set(actions)
        files = {self._safe_path(surface.get("prototype", {}).get("file")) for surface in self.manifest.get("surfaces", []) if isinstance(surface, dict)}
        for path in {item for item in files if item is not None and item.exists()}:
            parser = self._demo(path)
            for tag, attrs in parser.product_controls:
                action_id = attrs.get("data-action")
                element = attrs.get("id", f"<{tag}>")
                if not action_id:
                    self.add("UNCONTRACTED_CONTROL", f"Product control {element!r} has no data-action.", str(path.relative_to(self.root)), "clickable-demo")
                elif action_id not in known:
                    self.add("UNCONTRACTED_CONTROL", f"Product control {element!r} references unknown action {action_id!r}.", str(path.relative_to(self.root)), "clickable-demo")
                if tag == "a" and attrs.get("href") == "#" and not action_id:
                    self.add("DEAD_CONTROL", f"Anchor {element!r} has href=# and no contracted action.", str(path.relative_to(self.root)), "clickable-demo")

    def _validate_runtime_evidence(
        self,
        actions: dict[str, dict[str, Any]],
        states: dict[str, dict[str, Any]],
    ) -> None:
        evidence = self._mapping("evidence")
        report_path = self._safe_path(evidence.get("runtime_report_file"))
        demo_path = self._safe_path(evidence.get("demo_file"))
        if report_path is None or not report_path.is_file():
            self.add("RUNTIME_REPORT_MISSING", "Run the demo in a real browser and create the hash-bound runtime report.", "evidence.runtime_report_file", "clickable-demo")
            return
        if demo_path is None or not demo_path.is_file():
            self.add("PROTOTYPE_UNREADABLE", "evidence.demo_file is missing.", "evidence.demo_file", "clickable-demo")
            return
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.add("RUNTIME_REPORT_INVALID", str(exc), str(report_path.relative_to(self.root)), "clickable-demo")
            return
        if not isinstance(report, dict):
            self.add("RUNTIME_REPORT_INVALID", "Runtime report root must be an object.", str(report_path.relative_to(self.root)), "clickable-demo")
            return
        expected_manifest_hash = self._manifest_hash()
        expected_demo_hash = hashlib.sha256(demo_path.read_bytes()).hexdigest()
        if report.get("manifest_sha256") != expected_manifest_hash or report.get("demo_sha256") != expected_demo_hash:
            self.add("RUNTIME_REPORT_STALE", "Runtime report hashes do not match the current manifest and demo.", str(report_path.relative_to(self.root)), "clickable-demo")
        if report.get("runner") != "browser" or not self._meaningful(report.get("checked_at")):
            self.add("RUNTIME_REPORT_INVALID", "Runtime report requires runner=browser and checked_at.", str(report_path.relative_to(self.root)), "clickable-demo")

        transitions = self._runtime_rows(report.get("transitions"), "transitions", report_path)
        effects = self._runtime_rows(report.get("effects"), "effects", report_path)
        state_rows = self._runtime_rows(report.get("states"), "states", report_path, key="state_id")

        for action_id, action in actions.items():
            target = action.get("target", {}) if isinstance(action.get("target"), dict) else {}
            target_surface = target.get("surface_id")
            target_effect = target.get("effect")
            if target_surface:
                row = transitions.get(action_id)
                if (
                    not row
                    or row.get("status") != "pass"
                    or row.get("from_surface_id") != action.get("source_surface_id")
                    or row.get("expected_surface_id") != target_surface
                    or row.get("landed_surface_id") != target_surface
                ):
                    self.add("RUNTIME_TRANSITION_UNVERIFIED", f"Browser evidence for transition {action_id!r} is missing or failed.", f"actions.{action_id}", "clickable-demo")
            elif target_effect:
                row = effects.get(action_id)
                if (
                    not row
                    or row.get("status") != "pass"
                    or row.get("source_surface_id") != action.get("source_surface_id")
                    or row.get("expected_effect") != target_effect
                    or row.get("observed_effect") != target_effect
                ):
                    self.add("RUNTIME_EFFECT_UNVERIFIED", f"Browser evidence for effect {action_id!r} is missing or failed.", f"actions.{action_id}", "clickable-demo")

        for state_id, state in states.items():
            if state.get("required") is True:
                row = state_rows.get(state_id)
                if not row or row.get("status") != "pass" or row.get("reproduction") != state.get("reproduction"):
                    self.add("RUNTIME_STATE_UNVERIFIED", f"Browser evidence for required state {state_id!r} is missing or failed.", f"states.{state_id}", "clickable-demo")

        demo_relative = str(demo_path.relative_to(self.root))
        for index, surface in enumerate(self.manifest.get("surfaces", [])):
            if not isinstance(surface, dict) or surface.get("priority") != "P0" or surface.get("type") == "background":
                continue
            if surface.get("prototype", {}).get("file") != demo_relative:
                self.add("DEMO_FILE_MISMATCH", "Every P0 surface must use the single whole-service demo file.", f"surfaces[{index}].prototype.file", "clickable-demo")

    def _runtime_rows(
        self,
        value: Any,
        name: str,
        report_path: Path,
        key: str = "action_id",
    ) -> dict[str, dict[str, Any]]:
        if not isinstance(value, list):
            self.add("RUNTIME_REPORT_INVALID", f"{name} must be an array.", str(report_path.relative_to(self.root)), "clickable-demo")
            return {}
        result: dict[str, dict[str, Any]] = {}
        for item in value:
            if not isinstance(item, dict) or not self._meaningful(item.get(key)):
                self.add("RUNTIME_REPORT_INVALID", f"Every {name} row needs {key}.", str(report_path.relative_to(self.root)), "clickable-demo")
                continue
            result[item[key]] = item
        return result

    def _validate_dom_reference(
        self,
        reference: Any,
        expected_value: str | None,
        expected_attribute: str | None,
        code: str,
        contract_path: str,
        owner: str,
    ) -> None:
        if not isinstance(reference, dict):
            self.add(code, "Prototype evidence needs file and element_id.", contract_path, owner)
            return
        path = self._safe_path(reference.get("file"))
        element_id = reference.get("element_id")
        if path is None or not path.is_file() or not self._meaningful(element_id):
            self.add(code, "Prototype evidence file/element_id is missing.", contract_path, owner)
            return
        attrs = self._demo(path).elements.get(str(element_id))
        if attrs is None:
            self.add(code, f"Element #{element_id} does not exist in {path.relative_to(self.root)}.", contract_path, owner)
            return
        if expected_attribute and attrs.get(expected_attribute) != expected_value:
            self.add(code, f"#{element_id} must have {expected_attribute}={expected_value!r}.", contract_path, owner)

    def _validate_action_dom(self, action_id: str, action: dict[str, Any]) -> None:
        source_id = action.get("source_surface_id")
        surface = next((item for item in self.manifest.get("surfaces", []) if isinstance(item, dict) and item.get("id") == source_id), None)
        prototype = surface.get("prototype", {}) if isinstance(surface, dict) else {}
        reference = {"file": prototype.get("file"), "element_id": action.get("control_element_id")}
        path = self._safe_path(reference.get("file"))
        element_id = reference.get("element_id")
        contract_path = f"actions.{action_id}"
        if path is None or not path.is_file() or not self._meaningful(element_id):
            self.add("ACTION_NOT_PROTOTYPED", "Action needs a control_element_id in its source prototype.", contract_path, "clickable-demo")
            return
        attrs = self._demo(path).elements.get(str(element_id))
        if attrs is None or attrs.get("data-action") != action_id:
            self.add("ACTION_NOT_PROTOTYPED", f"#{element_id} must exist with data-action={action_id!r}.", contract_path, "clickable-demo")
            return
        target = action.get("target", {})
        target_surface = target.get("surface_id") if isinstance(target, dict) else None
        if target_surface and action.get("kind") in {"navigate", "open-overlay"} and attrs.get("data-go") != target_surface:
            self.add("TRANSITION_DOM_MISMATCH", f"#{element_id} data-go must be {target_surface!r}.", contract_path, "clickable-demo")
        target_effect = target.get("effect") if isinstance(target, dict) else None
        if target_effect and attrs.get("data-effect") != target_effect:
            self.add("EFFECT_DOM_MISMATCH", f"#{element_id} data-effect must be {target_effect!r}.", contract_path, "clickable-demo")

    def _safe_path(self, value: Any) -> Path | None:
        if not isinstance(value, str) or not value:
            return None
        candidate = (self.root / value).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError:
            self.add("EVIDENCE_PATH_OUTSIDE_PROJECT", f"Evidence path escapes planning directory: {value}", value, "service-contract")
            return None
        return candidate

    def _demo(self, path: Path) -> DemoParser:
        if path not in self.demo_cache:
            parser = DemoParser()
            try:
                parser.feed(path.read_text(encoding="utf-8"))
            except OSError as exc:
                self.add("PROTOTYPE_UNREADABLE", str(exc), str(path), "clickable-demo")
            self.demo_cache[path] = parser
            for element_id in parser.duplicate_ids:
                self.add("DUPLICATE_DOM_ID", f"Prototype contains duplicate id {element_id!r}.", str(path.relative_to(self.root)), "clickable-demo")
        return self.demo_cache[path]

    def _validate_design_acceptance(self) -> None:
        acceptance = self.design_acceptance
        if not acceptance:
            return
        if acceptance.get("schema_version") != "1.0":
            self.add("UNSUPPORTED_DESIGN_ACCEPTANCE_VERSION", "schema_version must be 1.0.", "05-design-acceptance.json", "design-acceptance")
        if acceptance.get("status") != "user-approved":
            self.add("DESIGN_NOT_APPROVED", "Design remains blocked until the user explicitly approves the current all-P0 evidence.", "status", "design-acceptance")
        approval = acceptance.get("approval")
        if not isinstance(approval, dict):
            self.add("DESIGN_NOT_APPROVED", "approval must be an object.", "approval", "design-acceptance")
        else:
            if approval.get("kind") != "explicit-user" or approval.get("scope") != "all-p0":
                self.add("DESIGN_NOT_APPROVED", "Approval must be explicit-user and cover all-p0.", "approval", "design-acceptance")
            for key in ("decision_ref", "approved_at", "evidence"):
                if not self._meaningful(approval.get(key)):
                    self.add("DESIGN_NOT_APPROVED", f"approval.{key} is required.", f"approval.{key}", "design-acceptance")

        source_hashes = acceptance.get("source_hashes")
        if not isinstance(source_hashes, dict):
            self.add("DESIGN_BASELINE_STALE", "source_hashes must be an object.", "source_hashes", "design-acceptance")
            source_hashes = {}
        required_sources = list(DESIGN_SOURCE_FILES)
        if self._mapping("release_profile").get("risk_domains"):
            required_sources.append("04.55-risk-register.md")
        for relative in required_sources:
            path = self.root / relative
            expected = source_hashes.get(relative)
            if not path.is_file() or not self._meaningful(expected):
                self.add("DESIGN_BASELINE_STALE", f"Missing bound source hash for {relative}.", f"source_hashes.{relative}", "design-acceptance")
                continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if expected != actual:
                self.add("DESIGN_BASELINE_STALE", f"Bound source changed after design approval: {relative}.", f"source_hashes.{relative}", "design-acceptance")

        component_contracts = self._acceptance_index("component_contracts")
        for component_id, component in component_contracts.items():
            path = f"component_contracts.{component_id}"
            for key in ("purpose", "accessibility"):
                if not self._meaningful(component.get(key)):
                    self.add("COMPONENT_CONTRACT_INCOMPLETE", f"{key} is required.", f"{path}.{key}", "design-acceptance")
            for key in ("variants", "states", "token_refs"):
                if not isinstance(component.get(key), list) or not component.get(key):
                    self.add("COMPONENT_CONTRACT_INCOMPLETE", f"{key} needs at least one item.", f"{path}.{key}", "design-acceptance")
            self._validate_hashed_visual(component.get("evidence"), f"{path}.evidence", "COMPONENT_EVIDENCE_STALE")

        visual_rows = self._acceptance_index("visual_evidence")
        review_rounds = self._acceptance_index("review_rounds")
        surfaces = self._index("surfaces", "screen-contract")
        states = self._index("states", "screen-contract")
        viewports = self._mapping("release_profile").get("viewports", [])
        if not isinstance(viewports, list) or not viewports:
            viewports = []
        coverage: set[tuple[str, str]] = set()

        for evidence_id, row in visual_rows.items():
            path = f"visual_evidence.{evidence_id}"
            surface_id = row.get("surface_id")
            viewport = row.get("viewport")
            if surface_id not in surfaces:
                self.add("UNKNOWN_SURFACE_REFERENCE", f"Unknown visual surface {surface_id!r}.", f"{path}.surface_id", "design-acceptance")
                continue
            if viewport not in viewports:
                self.add("UNKNOWN_VIEWPORT_REFERENCE", f"Viewport {viewport!r} is not in the release profile.", f"{path}.viewport", "design-acceptance")
            else:
                coverage.add((surface_id, viewport))
            if row.get("visual_gate") != "pass":
                self.add("VISUAL_GATE_NOT_PASSED", "Every P0 visual evidence row must pass the visual gate.", f"{path}.visual_gate", "visual-quality-gate")
            if row.get("review_round_id") not in review_rounds:
                self.add("DESIGN_REVIEW_EVIDENCE_MISSING", "Visual evidence must belong to a recorded review round.", f"{path}.review_round_id", "design-acceptance")
            component_ids = row.get("component_ids")
            if not isinstance(component_ids, list) or not component_ids:
                self.add("COMPONENT_TRACE_MISSING", "Visual evidence needs component_ids.", f"{path}.component_ids", "design-acceptance")
            else:
                for component_id in component_ids:
                    if component_id not in component_contracts:
                        self.add("UNKNOWN_COMPONENT_REFERENCE", f"Unknown component {component_id!r}.", f"{path}.component_ids", "design-acceptance")
            state_ids = row.get("state_ids")
            if not isinstance(state_ids, list):
                self.add("VISUAL_STATE_COVERAGE_MISSING", "state_ids must be an array.", f"{path}.state_ids", "design-acceptance")
                state_ids = []
            expected_states = {
                state_id
                for state_id in surfaces[surface_id].get("required_state_ids", [])
                if state_id in states and states[state_id].get("required") is True
            }
            missing_states = sorted(expected_states - set(state_ids))
            if missing_states:
                self.add("VISUAL_STATE_COVERAGE_MISSING", f"Evidence is missing required states: {', '.join(missing_states)}.", f"{path}.state_ids", "design-acceptance")
            for state_id in state_ids:
                if state_id not in states or states[state_id].get("surface_id") != surface_id:
                    self.add("UNKNOWN_STATE_REFERENCE", f"State {state_id!r} does not belong to {surface_id!r}.", f"{path}.state_ids", "design-acceptance")
            self._validate_hashed_visual({"file": row.get("file"), "sha256": row.get("sha256")}, path, "VISUAL_EVIDENCE_STALE")

        for surface_id, surface in surfaces.items():
            if surface.get("priority") != "P0" or surface.get("type") == "background":
                continue
            for viewport in viewports:
                if (surface_id, viewport) not in coverage:
                    self.add("VISUAL_VIEWPORT_COVERAGE_MISSING", f"P0 surface {surface_id!r} has no current {viewport!r} visual evidence.", f"surfaces.{surface_id}", "design-acceptance")

        completed_rounds = [row for row in review_rounds.values() if row.get("status") == "completed"]
        all_evidence_ids = set(visual_rows)
        if not completed_rounds or not any(set(row.get("reviewed_evidence_ids", [])) >= all_evidence_ids for row in completed_rounds):
            self.add("DESIGN_REVIEW_INCOMPLETE", "A completed review round must cover every current visual evidence row.", "review_rounds", "design-acceptance")
        for round_id, row in review_rounds.items():
            if row.get("status") not in {"revised", "completed", "rejected"} or not self._meaningful(row.get("summary")):
                self.add("DESIGN_REVIEW_INCOMPLETE", "Review round needs a valid status and summary.", f"review_rounds.{round_id}", "design-acceptance")

        findings = acceptance.get("findings")
        if not isinstance(findings, list):
            self.add("DESIGN_FINDINGS_INVALID", "findings must be an array.", "findings", "design-acceptance")
            findings = []
        for index, finding in enumerate(findings):
            path = f"findings[{index}]"
            if not isinstance(finding, dict):
                self.add("DESIGN_FINDINGS_INVALID", "Finding must be an object.", path, "design-acceptance")
                continue
            if finding.get("category") not in DESIGN_FINDING_CATEGORIES:
                self.add("DESIGN_FINDINGS_INVALID", "Finding category is invalid.", f"{path}.category", "design-acceptance")
            if finding.get("severity") not in {"P0", "P1", "P2"}:
                self.add("DESIGN_FINDINGS_INVALID", "Finding severity must be P0, P1, or P2.", f"{path}.severity", "design-acceptance")
            if finding.get("severity") == "P0" and finding.get("status") != "resolved":
                self.add("UNRESOLVED_P0_DESIGN_FINDING", "P0 design findings cannot be deferred or accepted away.", path, "design-acceptance")
            if finding.get("status") not in {"resolved", "deferred"}:
                self.add("DESIGN_FINDINGS_INVALID", "Finding status must be resolved or deferred.", f"{path}.status", "design-acceptance")
            for key in ("id", "evidence", "resolution", "decision_ref"):
                if not self._meaningful(finding.get(key)):
                    self.add("DESIGN_FINDINGS_INVALID", f"{key} is required.", f"{path}.{key}", "design-acceptance")

        checks = acceptance.get("mental_model_checks")
        if not isinstance(checks, list):
            self.add("MENTAL_MODEL_REVIEW_INCOMPLETE", "mental_model_checks must be an array.", "mental_model_checks", "design-acceptance")
            checks = []
        checked_personas: set[str] = set()
        checked_requirements: set[str] = set()
        journeys = self._index("journeys", "service-contract")
        for index, check in enumerate(checks):
            path = f"mental_model_checks[{index}]"
            if not isinstance(check, dict):
                self.add("MENTAL_MODEL_REVIEW_INCOMPLETE", "Mental-model check must be an object.", path, "design-acceptance")
                continue
            persona_id = check.get("persona_id")
            if persona_id not in self.personas:
                self.add("UNKNOWN_PERSONA_REFERENCE", f"Unknown persona {persona_id!r}.", f"{path}.persona_id", "design-acceptance")
            else:
                checked_personas.add(persona_id)
            if check.get("verdict") != "pass" or not self._meaningful(check.get("evidence")):
                self.add("MENTAL_MODEL_REVIEW_INCOMPLETE", "Mental-model checks need pass verdict and evidence.", path, "design-acceptance")
            for requirement_id in check.get("requirement_ids", []):
                if requirement_id not in self.requirements:
                    self.add("UNKNOWN_REQUIREMENT_REFERENCE", f"Unknown requirement {requirement_id!r}.", f"{path}.requirement_ids", "design-acceptance")
                else:
                    checked_requirements.add(requirement_id)
            journey_ids = check.get("journey_ids")
            if not isinstance(journey_ids, list) or not journey_ids:
                self.add("MENTAL_MODEL_REVIEW_INCOMPLETE", "journey_ids needs at least one journey.", f"{path}.journey_ids", "design-acceptance")
            else:
                for journey_id in journey_ids:
                    if journey_id not in journeys:
                        self.add("UNKNOWN_JOURNEY_REFERENCE", f"Unknown journey {journey_id!r}.", f"{path}.journey_ids", "design-acceptance")
        required_personas = set(self.personas)
        required_requirements = {
            requirement_id
            for requirement_id, requirement in self.requirements.items()
            if requirement.get("status") == "included" and requirement.get("priority") == "P0"
        }
        if required_personas - checked_personas or required_requirements - checked_requirements:
            self.add("MENTAL_MODEL_REVIEW_INCOMPLETE", "Every persona and included P0 requirement needs a mental-model journey review.", "mental_model_checks", "design-acceptance")

        target_validation = acceptance.get("target_user_validation")
        manifest_validation = self._mapping("user_validation")
        if not isinstance(target_validation, dict) or target_validation.get("status") not in {"not-run", "heuristic", "real-user"}:
            self.add("TARGET_USER_VALIDATION_INVALID", "Use not-run, heuristic, or real-user.", "target_user_validation", "prototype-test")
        elif target_validation.get("status") != manifest_validation.get("status"):
            self.add("TARGET_USER_VALIDATION_MISMATCH", "Design acceptance and service manifest must report the same target-user validation status.", "target_user_validation.status", "prototype-test")
        elif target_validation.get("status") == "real-user" and not target_validation.get("evidence"):
            self.add("REAL_USER_EVIDENCE_MISSING", "real-user status requires evidence.", "target_user_validation.evidence", "prototype-test")

    def _acceptance_index(self, key: str) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        values = self.design_acceptance.get(key, [])
        if not isinstance(values, list):
            self.add("DESIGN_ACCEPTANCE_INVALID", f"{key} must be an array.", key, "design-acceptance")
            return result
        for position, item in enumerate(values):
            path = f"{key}[{position}]"
            if not isinstance(item, dict):
                self.add("DESIGN_ACCEPTANCE_INVALID", f"{path} must be an object.", path, "design-acceptance")
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not ID_RE.fullmatch(item_id):
                self.add("INVALID_CONTRACT_ID", f"{path}.id must match {ID_RE.pattern}.", f"{path}.id", "design-acceptance")
                continue
            if item_id in result:
                self.add("DUPLICATE_CONTRACT_ID", f"Duplicate id: {item_id}", f"{path}.id", "design-acceptance")
                continue
            result[item_id] = item
        return result

    def _validate_hashed_visual(self, evidence: Any, path: str, code: str) -> None:
        if not isinstance(evidence, dict):
            self.add(code, "Visual evidence needs file and sha256.", path, "design-acceptance")
            return
        visual_path = self._safe_path(evidence.get("file"))
        expected = evidence.get("sha256")
        if visual_path is None or not visual_path.is_file() or visual_path.suffix.lower() not in VISUAL_EVIDENCE_SUFFIXES:
            self.add(code, "Visual evidence must be a local png, jpg, jpeg, webp, or svg file.", path, "design-acceptance")
            return
        actual = hashlib.sha256(visual_path.read_bytes()).hexdigest()
        if expected != actual:
            self.add(code, "Visual evidence hash is missing or stale.", path, "design-acceptance")

    def _validate_readiness_claims(self) -> None:
        dashboard = self.root / "00-review-dashboard.html"
        handoff = self.root / "05-engineering-handoff.md"
        claims_pass = False
        if dashboard.exists():
            text = dashboard.read_text(encoding="utf-8", errors="replace")
            claims_pass = bool(re.search(r'data-readiness-status=["\']pass["\']|개발 착수 준비 완료', text, re.IGNORECASE))
        if handoff.exists():
            text = handoff.read_text(encoding="utf-8", errors="replace")
            claims_pass = claims_pass or bool(re.search(r"planning-readiness:\s*pass", text, re.IGNORECASE))
            if claims_pass and re.search(r"planning readiness blockers[\s\S]{0,500}- \[ \]", text, re.IGNORECASE):
                self.add("READINESS_CLAIM_CONFLICT", "Planning readiness is claimed while a planning blocker is unchecked.", "05-engineering-handoff.md", "engineering-handoff")
        if claims_pass and any(f.severity == "error" for f in self.findings):
            self.add("READINESS_CLAIM_CONFLICT", "Dashboard/handoff claims readiness while deterministic checks fail.", "00-review-dashboard.html", "decision-dashboard")

    def _meaningful(self, value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip()) and not value.strip().startswith(DECISION_NEEDED)

    def _manifest_hash(self) -> str | None:
        if not self.manifest_path.exists():
            return None
        return hashlib.sha256(self.manifest_path.read_bytes()).hexdigest()

    def _file_hash(self, path: Path) -> str | None:
        if not path.is_file():
            return None
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _report(self, profile: str) -> dict[str, Any]:
        errors = [finding for finding in self.findings if finding.severity == "error"]
        validation = self.manifest.get("user_validation", {}) if self.manifest else {}
        user_validated = isinstance(validation, dict) and validation.get("status") == "real-user" and bool(validation.get("evidence"))
        stage_rank = {"contract": 0, "prototype": 1, "design": 2, "handoff": 3, "technical": 4}.get(self.stage, -1)
        error_owners = {finding.owner for finding in errors}
        contract_owners = {"product-definition", "prd", "screen-contract", "service-contract", "backend-systems-brief"}
        prototype_owners = contract_owners | {"clickable-demo", "prototype-test", "implementation-readiness"}
        design_owners = prototype_owners | {
            "design-acceptance",
            "visual-quality-gate",
            "design-system",
            "design-critique",
            "feasibility-review",
            "ux-writing",
            "risk-register",
        }
        handoff_owners = design_owners | {"engineering-handoff", "decision-dashboard", "orchestrate"}
        product_contract_ready = profile != "lite" and stage_rank >= 0 and not (error_owners & contract_owners)
        prototype_ready = product_contract_ready and stage_rank >= 1 and not (error_owners & prototype_owners)
        design_owner_approved = self.design_acceptance.get("status") == "user-approved" if self.design_acceptance else False
        design_accepted = prototype_ready and stage_rank >= 2 and design_owner_approved and not (error_owners & design_owners)
        product_handoff_ready = design_accepted and stage_rank >= 3 and not (error_owners & handoff_owners)
        technical_design_ready = False
        implementation_ready = False
        engineering_ready = implementation_ready
        if errors:
            status = "fail"
        elif profile == "lite":
            status = "lite-pass"
        else:
            status = f"{self.stage}-pass"
        return {
            "schema_version": "1.0",
            "status": status,
            "stage": self.stage,
            "profile": profile,
            "engineering_ready": engineering_ready,
            "product_contract_ready": product_contract_ready,
            "prototype_ready": prototype_ready,
            "design_owner_approved": design_owner_approved,
            "design_accepted": design_accepted,
            "product_handoff_ready": product_handoff_ready,
            "technical_design_ready": technical_design_ready,
            "implementation_ready": implementation_ready,
            "user_validated": user_validated,
            "manifest_sha256": self._manifest_hash(),
            "product_definition_sha256": self._file_hash(self.product_definition_path),
            "design_acceptance_sha256": self._file_hash(self.design_acceptance_path),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "findings": [asdict(finding) for finding in self.findings],
            "accepted_limitations": self._mapping("release_profile").get("accepted_limitations", []) if self.manifest else [],
        }


def write_report(root: Path, report: dict[str, Any]) -> None:
    json_path = root / "05-readiness-report.json"
    md_path = root / "05-readiness-report.md"
    _atomic_write(json_path, json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# Service Readiness Report",
        "",
        f"- Status: **{report['status']}**",
        f"- Engineering ready: **{str(report['engineering_ready']).lower()}**",
        f"- Product contract ready: **{str(report['product_contract_ready']).lower()}**",
        f"- Prototype ready: **{str(report['prototype_ready']).lower()}**",
        f"- Design owner approved: **{str(report['design_owner_approved']).lower()}**",
        f"- Design accepted: **{str(report['design_accepted']).lower()}**",
        f"- Product handoff ready: **{str(report['product_handoff_ready']).lower()}**",
        f"- Technical design ready: **{str(report['technical_design_ready']).lower()}**",
        f"- Implementation ready: **{str(report['implementation_ready']).lower()}**",
        f"- User validated: **{str(report['user_validated']).lower()}**",
        f"- Manifest SHA-256: `{report['manifest_sha256'] or 'missing'}`",
        f"- Checked at: `{report['checked_at']}`",
        "",
        "## Findings",
        "",
    ]
    if report["findings"]:
        lines.extend("- `{code}` [{severity}] {message} — owner: `{owner}`, path: `{path}`".format(**item) for item in report["findings"])
    else:
        lines.append("- None")
    lines.extend(["", "## Accepted Limitations", ""])
    if report["accepted_limitations"]:
        for item in report["accepted_limitations"]:
            lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
    else:
        lines.append("- None")
    _atomic_write(md_path, "\n".join(lines) + "\n")


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("planning_dir", type=Path)
    parser.add_argument("--profile", choices=("lite", "standard", "deep"))
    parser.add_argument("--stage", choices=("contract", "prototype", "design", "handoff", "technical"), default="handoff")
    parser.add_argument("--no-write", action="store_true", help="Print findings without writing readiness reports")
    parser.add_argument("--json", action="store_true", help="Print the full JSON report")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.planning_dir.expanduser().resolve()
    if not root.is_dir():
        print(f"Planning directory does not exist: {root}", file=sys.stderr)
        return 2
    report = Validator(root, args.profile, args.stage).run()
    if not args.no_write and args.stage == "handoff":
        write_report(root, report)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"{report['status']}: {len(report['findings'])} finding(s)")
        for finding in report["findings"]:
            print(f"- {finding['code']} [{finding['severity']}]: {finding['message']} ({finding['path']})")
    return 0 if report["status"] in {"contract-pass", "prototype-pass", "pass", "lite-pass"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
