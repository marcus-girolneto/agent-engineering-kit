# Debugging

Start with the observed behavior, expected behavior and smallest reproducible input. Record the environment and relevant versions. If reproduction is missing, inspect the data path and add targeted instrumentation without logging secrets.

Write a falsifiable hypothesis: “the empty string is accepted because validation runs before trimming.” Run one experiment that distinguishes it from another explanation. Keep an evidence trail of input, command and observed output.

Fix the cause at the responsible boundary. Add a regression test that fails on the original implementation and passes after the fix. Run adjacent behavior tests and then the full gate. Do not repair a symptom by broad exception handling or a more permissive assertion.

For intermittent failures, capture timing, ordering and state. Retries are appropriate only when the operation is safe to repeat and the failure is transient; bound attempts and delay. Avoid making a flaky test pass by removing its assertions.

Hand off the cause, reproduction, correction and remaining uncertainty. Exercise: [empty-page calculation](../exercises/debugging/task.md).
