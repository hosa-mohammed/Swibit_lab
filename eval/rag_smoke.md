# RAG Smoke Test Results

## Positive Tests

| Question | Source | Status |
|---|---|---|
| Who is eligible for remote work? | remote-work-policy.md | PASS |
| How many vacation days? | vacation-policy.md | PASS |
| What is the meal limit? | expense-policy.md | PASS |

## Negative Tests

| Question | Result | Status |
|---|---|---|
| What is the stock price? | I don't know | PASS |
| What is my salary? | I don't know | PASS |
| Health insurance? | I don't know | PASS |

## Summary
- Positive: 3/3 passed
- Negative: 3/3 passed (all "I don't know")
- Citations included: YES