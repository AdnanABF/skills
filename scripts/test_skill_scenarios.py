"""Regression tests for routing-contract validation, not model routing."""

import unittest

from validate_skill_scenarios import route_errors, validate_scenarios


class RoutingTests(unittest.TestCase):
	def setUp(self):
		self.active = {"forms", "lint", "deploy"}
		self.scenario = {
			"scenario": "Copy-only change",
			"skills": ["lint"],
			"forbidden_skills": ["forms"],
			"forbidden_actions": ["deploy"],
		}

	def test_route_boundaries(self):
		self.assertEqual(route_errors(self.scenario, ["lint"], []), [])
		for skills, actions in [([], []), (["lint", "forms"], []), (["lint"], ["deploy"])]:
			with self.subTest(skills=skills, actions=actions):
				self.assertTrue(route_errors(self.scenario, skills, actions))

	def test_legacy_schema(self):
		self.assertEqual(validate_scenarios([{"scenario": "Legacy", "skills": ["lint"]}], self.active), [])

	def test_cases(self):
		self.scenario["cases"] = [
			{"skills": ["lint"], "actions": [], "valid": True},
			{"skills": ["lint", "forms"], "actions": [], "valid": False},
			{"skills": ["lint"], "actions": ["deploy"], "valid": False},
		]
		self.assertEqual(validate_scenarios([self.scenario], self.active), [])
		self.scenario["cases"][0]["valid"] = False
		self.assertTrue(validate_scenarios([self.scenario], self.active))

	def test_malformed_values_do_not_crash(self):
		for field in ("skills", "forbidden_skills", "forbidden_actions"):
			for value in (None, "lint", [{}], [1], [""]):
				with self.subTest(field=field, value=value):
					self.assertTrue(validate_scenarios([{**self.scenario, field: value}], self.active))

	def test_invalid_catalogs(self):
		for catalog in (None, {}, [None], [{"scenario": "", "skills": []}],
			[self.scenario, self.scenario],
			[{**self.scenario, "skills": ["unknown"]}],
			[{**self.scenario, "skills": ["lint", "lint"]}],
			[{**self.scenario, "forbidden_skills": ["lint"]}],
			[{**self.scenario, "cases": [None]}],
			[{**self.scenario, "cases": [{"valid": True, "skills": [{}], "actions": []}]}]):
			with self.subTest(catalog=catalog):
				self.assertTrue(validate_scenarios(catalog, self.active))


if __name__ == "__main__":
	unittest.main()
