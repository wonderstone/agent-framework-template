# Managed Terminal Prompt Dispatch Receipt

- Generated At: {{generated_at}}
- Execution ID: {{execution_id}}
- Executor Lane: {{executor_lane}}
- Starter Command: {{starter_command}}
- Terminal Label: {{terminal_label}}
- Prompt Purpose: {{prompt_purpose}}

## Dispatch Contract

Record the prompt-dispatch handshake in order, then classify the outcome:

1. pre-read
2. send prompt
3. read output immediately
4. one allowed Enter only if the prompt buffered in the visible input area
5. read output again
6. classify the outcome as `started`, `started_after_submit`, or `degraded`

## Step 1 — Pre-Read

- Timestamp: {{pre_read_at}}
- Readable Output Before Send: {{pre_read_output}}
- Notes: {{pre_read_notes}}

## Step 2 — Send Prompt

- Timestamp: {{prompt_sent_at}}
- Prompt Source: {{prompt_source}}
- Notes: {{prompt_sent_notes}}

## Step 3 — Immediate Output Read

- Timestamp: {{first_output_read_at}}
- Immediate Output: {{first_observed_output}}
- Prompt Buffered In Visible Input Area: {{prompt_buffered}}
- Notes: {{first_output_read_notes}}

## Step 4 — Allowed Enter Step

- Timestamp: {{submit_enter_at}}
- Allowed Enter Used: {{submit_enter_used}}
- Notes: {{submit_enter_notes}}

## Step 5 — Second Output Read

- Timestamp: {{second_output_read_at}}
- Output After Allowed Enter: {{second_observed_output}}
- Notes: {{second_output_read_notes}}

## Outcome Classification

- Dispatch Outcome: {{dispatch_outcome}}
- Outcome Meaning:
	- `started`: prompt continued without the Enter step
	- `started_after_submit`: prompt buffered, one allowed Enter was sent, and the agent then continued running
	- `degraded`: control was lost, output was unreadable, or prompt-plus-one-allowed-Enter still did not continue execution
- Lane Reuse Decision: {{lane_reuse_decision}}

## Result

- Packet Status: {{packet_status}}
- Next Expected Action: {{next_action}}
- Owner Notes: {{owner_notes}}