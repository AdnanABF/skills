# Routing Contracts

`routing-scenarios.json` records explicit expectations, not an automatic prompt router.
Existing scenarios remain compatible with just `scenario` and `skills`.

## Fields

- `scenario`: unique, non-empty description of a task and its scope.
- `skills`: non-empty list of required active skill names; additional skills are permitted unless forbidden.
- `forbidden_skills`: optional active skill names that must not be selected for this particular scope.
- `forbidden_actions`: optional exact action labels, such as `deploy` or `create-skill`. These are test labels, not harness permissions or runtime enforcement.
- `cases`: optional explicit selections, each with `skills`, `actions`, and boolean `valid`. Include both accepted and rejected selections for new boundary scenarios.

The validator checks schema, references, duplicate names/skills, contradictory requirements, and case outcomes. Cases can reject missing required skills, forbidden skills, or forbidden actions. It does not interpret scenario prose or determine whether an agent actually follows instructions. To evaluate model routing, separately collect the skills/actions selected for a prompt and compare them using `route_errors` in the validator; manual review is still needed for relevance and prose intent.

## Verification

```sh
PYTHONDONTWRITEBYTECODE=1 python3 .agents/scripts/validate_skill_scenarios.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s .agents/scripts -p 'test_*.py'
```
