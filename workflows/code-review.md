# Code review

Start by identifying the base and head of the change. Read the diff, affected callers and existing tests. Unless implementation is requested, review without editing the patch.

Prioritize correctness, authorization, data integrity, injection, concurrency, backwards compatibility and missing behavior coverage. Separate demonstrated defects from questions. Do not pad a review with style preferences already enforced by tooling.

Each finding needs a concrete trigger, the resulting impact, a file and line, and evidence. Suggest the smallest useful correction. Use these severities:

| Severity | Meaning |
| --- | --- |
| critical | Demonstrated path to broad compromise or catastrophic data loss under the stated deployment assumptions |
| high | Realistic unauthorized access, substantial data corruption or a broken primary operation |
| medium | Incorrect behavior with bounded impact or a missing important failure path |
| low | Limited-impact defect worth addressing; not a cosmetic preference |

Run a focused reproduction when feasible and authorized. If a claim depends on production configuration, say which assumption is unverified. A passing test suite does not invalidate a demonstrated defect.

Deliver findings first, then checks performed and limitations. “No actionable findings” is acceptable and should still name the inspected scope and missing checks. Do not claim that a patch is secure because there were no findings.

For a structured review, follow [review.schema.json](../schemas/review.schema.json) and run `uv run --locked kit validate review path/to/review.json`. Schema validation checks shape, not the truth of a finding.

Practice with [the deliberately vulnerable fixture](../exercises/review/task.md).
