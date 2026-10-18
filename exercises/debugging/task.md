# Debugging exercise: page count

A proposed pagination helper computes page count with this expression:

```python
pages = total // page_size + 1
```

The contract is: zero items produces zero pages; a full final page must not add another page; a partial final page does. Page size must be a positive integer and total must be a nonnegative integer.

Reproduce the failure with totals 0, 20 and 21 at page size 20. Write a small pure function and regression tests before integrating it anywhere. Explain the failure using integer division, then show passing boundary tests. Avoid introducing floating-point rounding for an integer count.

This exercise is intentionally independent of the sample API's response contract. Follow [the debugging workflow](../../workflows/debugging.md); do not change the API merely to complete the exercise.
