   # hg-agentic-workflow-demo

   A demo of an agentic coding workflow driven by Claude Code, built to show how
   spec-first, verification-gated AI development works in practice.

   ## What we're proving
   That the hard part of agentic work is the spec and the invariants, not the code
   generation. The workflow is: write the spec as executable tests first, let the
   agent implement against them, and never call anything "done" until the tests are
   green and the reasoning is on the record.

   ## Stack
   - Language: Python
   - Framework: none
   - Test runner: pytest
   - Package manager: pip

   ## Specs

   ### Reconciliation (`reconciliation.py`)
   `reconcile(computed, invoiced, tolerance=0.01)` compares a computed amount
   against an invoiced amount and returns `(verdict, gap)`.
   - `gap = computed - invoiced` (signed: negative when invoiced exceeds computed).
   - `verdict` is `"RECONCILED"` if `abs(gap) <= tolerance`, else `"DISCREPANCY"`.
   - Edge cases covered by tests (`tests/test_reconciliation.py`): exact match,
     difference just under tolerance, difference exactly at tolerance (inclusive
     boundary), difference just over tolerance, and a negative gap where invoiced
     exceeds computed.

   `reconcile_csv(path, tolerance=0.01)` applies `reconcile()` to every row of a
   CSV of line items (columns: `id, computed, invoiced`). Returns
   `{"reconciled": count, "flagged": count, "details": [...]}` — only flagged
   rows appear in `details`, since the point is to surface what needs review,
   not to re-list what already ties out.
   - Each flagged detail is `{"id", "computed", "invoiced", "gap", "error"}`.
     Rows with a genuine discrepancy have `error: None` and a numeric `gap`.
   - Rows with a missing column or a non-numeric amount are also counted as
     flagged (they need a human to look at them too), with `gap: None` and an
     `error` message describing why — malformed data doesn't crash the run.
   - An empty file (header only, no data rows) returns `reconciled: 0,
     flagged: 0, details: []`.
   - Known limitation: tolerance is absolute only. A fixed `0.01` is too tight
     for large invoices and too loose for tiny ones; relative tolerance
     (e.g. percentage-of-amount) is not implemented yet.
   - Demo: `python reconciliation.py sample_data/line_items.csv` runs it against
     a small synthetic dataset with a couple of planted discrepancies.

   ## How to work in this repo
   - Restate the task and your plan before writing code. If the task is ambiguous,
     ask before implementing.
   - Test-driven by default: write or update the tests that encode the spec first,
     confirm they fail, then implement until they pass.
   - Keep changes small and reviewable: one logical change per commit, clear messages.
   - Prefer clarity over cleverness. If a simpler approach exists, take it.
   - Don't add dependencies or restructure the project without flagging it first.

   ## Definition of done (hard gates)
   A task is complete only when ALL of these hold:
   - The tests that encode the spec pass, and you've shown the output.
   - No existing tests were broken.
   - The change is explained: what, why, and any tradeoffs, in the summary or PR.
   Do not describe work as finished on any other basis.

   ## Out of scope for this demo
   - No customer or production data. Synthetic/sample data only.
   - No secrets or credentials committed to the repo.

