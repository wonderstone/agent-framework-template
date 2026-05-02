# Managed Terminal Prompt Dispatch Receipt

- Generated At: {{generated_at}}
- Execution ID: {{execution_id}}
- Executor Lane: {{executor_lane}}
- Starter Command: {{starter_command}}
- Terminal Label: {{terminal_label}}
- Prompt Purpose: {{prompt_purpose}}

## Dispatch Contract

The managed terminal prompt-dispatch contract is complete only when all three steps are captured in order:

1. `prompt_staged`
2. `enter_sent`
3. `post_dispatch_output_read`

## Step 1 — Prompt Staged

- Timestamp: {{prompt_staged_at}}
- Prompt Source: {{prompt_source}}
- Control State After Step: `prompt_staged`
- Notes: {{prompt_staged_notes}}

## Step 2 — Enter Sent

- Timestamp: {{enter_sent_at}}
- Dispatch Action: {{dispatch_action}}
- Control State After Step: `enter_sent`
- Notes: {{enter_sent_notes}}

## Step 3 — Post-Dispatch Output Read

- Timestamp: {{output_read_at}}
- First Observed Output: {{first_observed_output}}
- Running Confirmed: {{running_confirmed}}
- Control State After Step: {{final_control_state}}
- Notes: {{output_read_notes}}

## Result

- Packet Status: {{packet_status}}
- Next Expected Action: {{next_action}}
- Owner Notes: {{owner_notes}}