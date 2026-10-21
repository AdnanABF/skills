#!/usr/bin/env python3
"""Validate that documented skill-routing scenarios reference active skills.

Run with: python3 .agents/scripts/validate_skill_scenarios.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def route_errors(scenario: dict, skills: list[str], actions: list[str]) -> list[str]:
	"""Check an explicit selection; this does not infer a route from prose."""
	errors = []
	for skill in scenario["skills"]:
		if skill not in skills:
			errors.append(f"Missing required skill {skill!r}")
	for skill in scenario.get("forbidden_skills", []):
		if skill in skills:
			errors.append(f"Forbidden skill {skill!r}")
	for action in scenario.get("forbidden_actions", []):
		if action in actions:
			errors.append(f"Forbidden action {action!r}")
	return errors


def validate_scenarios(scenarios: object, active_skills: set[str]) -> list[str]:
	errors: list[str] = []
	if not isinstance(scenarios, list):
		return ["Scenario catalog must be a JSON array"]
	names: set[str] = set()
	for index, scenario in enumerate(scenarios, 1):
		prefix = f"Scenario {index}"
		if not isinstance(scenario, dict):
			errors.append(f"{prefix} must be an object")
			continue
		name = scenario.get("scenario")
		if not isinstance(name, str) or not name.strip():
			errors.append(f"{prefix} needs a non-empty scenario name")
		elif name.strip() in names:
			errors.append(f"{prefix} has a duplicate scenario name")
		else:
			names.add(name.strip())
		valid = True
		for field in ("skills", "forbidden_skills", "forbidden_actions"):
			values = scenario.get(field, [] if field != "skills" else None)
			if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
				errors.append(f"{prefix} {field} must be a list of non-empty strings")
				valid = False
				continue
			if field == "skills" and not values:
				errors.append(f"{prefix} needs at least one skill")
			if len(values) != len(set(values)):
				errors.append(f"{prefix} {field} contains duplicates")
			if field != "forbidden_actions":
				for skill in values:
					if skill not in active_skills:
						errors.append(f"{prefix} references inactive skill {skill!r}")
		if not valid:
			continue
		if set(scenario["skills"]) & set(scenario.get("forbidden_skills", [])):
			errors.append(f"{prefix} requires and forbids the same skill")
		cases = scenario.get("cases", [])
		if not isinstance(cases, list):
			errors.append(f"{prefix} cases must be an array")
			continue
		for case_index, case in enumerate(cases, 1):
			label = f"{prefix} case {case_index}"
			if not isinstance(case, dict) or type(case.get("valid")) is not bool:
				errors.append(f"{label} needs a boolean valid expectation")
				continue
			case_valid = True
			for field in ("skills", "actions"):
				values = case.get(field)
				if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
					errors.append(f"{label} {field} must be a list of non-empty strings")
					case_valid = False
				elif field == "skills" and any(v not in active_skills for v in values):
					errors.append(f"{label} references inactive skills")
					case_valid = False
			if case_valid and (not route_errors(scenario, case["skills"], case["actions"])) != case["valid"]:
				errors.append(f"{label} selection does not match valid={case['valid']}")
	return errors


def main() -> int:
	root = Path(__file__).resolve().parents[1]
	skills_dir = root / "skills"
	scenarios_path = skills_dir / "routing-scenarios.json"
	active_skills = {path.parent.name for path in skills_dir.glob("*/SKILL.md")}

	try:
		scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as error:
		print(f"Unable to read {scenarios_path}: {error}", file=sys.stderr)
		return 1

	errors = validate_scenarios(scenarios, active_skills)

	if errors:
		print("Skill scenario validation failed:", file=sys.stderr)
		for error in errors:
			print(f"- {error}", file=sys.stderr)
		return 1

	print(f"Skill scenarios valid: {len(scenarios)} scenarios checked.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
