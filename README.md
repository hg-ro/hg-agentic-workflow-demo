# hg-agentic-workflow-demo

A small demo of a spec-first, verification-gated agentic coding workflow built
with Claude Code.

The idea: the agent writes the tests that encode the spec *first*, confirms
they fail, then implements until they're green — and never declares a task
done without passing tests and stated reasoning. See `CLAUDE.md` for the
full ground rules this repo works under.

## Worked example: `reconcile()`

`reconciliation.py` compares a computed amount against an invoiced amount and
returns a verdict plus the gap. It was built the way this repo is meant to
work:

1. `tests/test_reconciliation.py` was written first, encoding the spec
   (exact match, just-under-tolerance, just-over-tolerance, boundary-at-tolerance,
   and a negative gap when invoiced exceeds computed).
2. The tests were run and confirmed to fail (`ModuleNotFoundError` —
   `reconciliation.py` didn't exist yet).
3. `reconcile()` was implemented until all tests passed.

Run it yourself:

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## GitHub Actions

This repo has a Claude Code GitHub Action wired up (`.github/workflows/`).
Tag `@claude` in an issue or PR comment to have it respond or make changes;
it also runs an automated review on new PRs.

This is a demo, not a production template — scope and tooling are kept
intentionally minimal.
