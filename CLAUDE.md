   # hg-agentic-workflow-demo

   A demo of an agentic coding workflow driven by Claude Code, built to show the
   Meshly team how spec-first, verification-gated AI development works in practice.

   ## What we're proving
   That the hard part of agentic work is the spec and the invariants, not the code
   generation. The workflow is: write the spec as executable tests first, let the
   agent implement against them, and never call anything "done" until the tests are
   green and the reasoning is on the record.

   ## Stack
   <!-- TODO: fill in once the first task is chosen, or let `claude /init` detect it -->
   - Language:
   - Framework:
   - Test runner:
   - Package manager:

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

