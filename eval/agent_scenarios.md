# Agent Scenarios

## Scenario 1: Policy Question
- Input: "How many vacation days do I get?"
- Tool Selected: search_policies
- Result: Answer from vacation-policy.md with citation
- Status: PASS

## Scenario 2: Task Summary
- Input: "Show my tasks summary"
- Tool Selected: get_task_summary
- Result: Task count for user
- Status: PASS

## Scenario 3: Bug Report
- Input: "The app crashes when I login"
- Tool Selected: classify_message
- Result: category=support, priority=high
- Status: PASS