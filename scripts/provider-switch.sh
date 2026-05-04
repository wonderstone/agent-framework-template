#!/usr/bin/env bash

set -euo pipefail

SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_TOOLS_HOME="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$AGENT_TOOLS_HOME/.env"

load_env_file() {
  if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
  fi

  # Normalize legacy or alternate key names used in other workspaces.
  if [[ -z "${DEEPSEEK_API_KEY:-}" && -n "${DeepSeek_KEY:-}" ]]; then
    export DEEPSEEK_API_KEY="$DeepSeek_KEY"
  fi
}

usage() {
  cat <<'EOF'
Usage:
  source provider-switch.sh apply <profile>
  provider-switch.sh env <profile>
  provider-switch.sh exec <profile> <command> [args...]
  provider-switch.sh status
  provider-switch.sh list

Profiles:
  anth       Reset to direct Anthropic-style defaults
  ds-pro     DeepSeek V4 Pro via Anthropic-compatible endpoint
  ds-flash   DeepSeek V4 Flash via Anthropic-compatible endpoint
  reset      Alias for anth

Examples:
  source provider-switch.sh apply ds-pro
  eval "$(provider-switch.sh env ds-flash)"
  provider-switch.sh exec ds-pro claude
EOF
}

profile_exists() {
  case "${1:-}" in
    anth|reset|ds-pro|ds-flash) return 0 ;;
    *) return 1 ;;
  esac
}

print_exports() {
  local profile="${1:-}"
  if ! profile_exists "$profile"; then
    echo "Unknown profile: $profile" >&2
    exit 1
  fi

  case "$profile" in
    anth|reset)
      cat <<'EOF'
unset ANTHROPIC_BASE_URL
unset ANTHROPIC_AUTH_TOKEN
unset ANTHROPIC_MODEL
unset ANTHROPIC_DEFAULT_OPUS_MODEL
unset ANTHROPIC_DEFAULT_SONNET_MODEL
unset ANTHROPIC_DEFAULT_HAIKU_MODEL
unset CLAUDE_CODE_SUBAGENT_MODEL
unset CLAUDE_CODE_EFFORT_LEVEL
unset CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC
unset API_TIMEOUT_MS
EOF
      ;;
    ds-pro)
      cat <<EOF
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="${DEEPSEEK_API_KEY:-}"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_EFFORT_LEVEL="max"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"
export API_TIMEOUT_MS="600000"
EOF
      ;;
    ds-flash)
      cat <<EOF
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="${DEEPSEEK_API_KEY:-}"
export ANTHROPIC_MODEL="deepseek-v4-flash"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-flash"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_EFFORT_LEVEL="high"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"
export API_TIMEOUT_MS="600000"
EOF
      ;;
  esac
}

apply_profile() {
  local profile="${1:-}"
  if ! profile_exists "$profile"; then
    echo "Unknown profile: $profile" >&2
    return 1
  fi

  eval "$(print_exports "$profile")"

  if [[ "$profile" == "ds-pro" || "$profile" == "ds-flash" ]]; then
    if [[ -z "${DEEPSEEK_API_KEY:-}" ]]; then
      echo "Warning: DEEPSEEK_API_KEY is empty. Set it before launching Claude Code." >&2
    fi
  fi

  echo "Applied profile: $profile"
}

exec_with_profile() {
  local profile="${1:-}"
  shift || true
  if [[ $# -eq 0 ]]; then
    echo "Missing command for exec mode." >&2
    exit 1
  fi

  local command=("$@")
  local export_lines
  export_lines="$(print_exports "$profile")"

  (
    eval "$export_lines"
    exec "${command[@]}"
  )
}

status() {
  cat <<EOF
ANTHROPIC_BASE_URL=${ANTHROPIC_BASE_URL:-}
ANTHROPIC_AUTH_TOKEN=$( [[ -n "${ANTHROPIC_AUTH_TOKEN:-}" ]] && echo "<set>" || echo "" )
ANTHROPIC_MODEL=${ANTHROPIC_MODEL:-}
ANTHROPIC_DEFAULT_OPUS_MODEL=${ANTHROPIC_DEFAULT_OPUS_MODEL:-}
ANTHROPIC_DEFAULT_SONNET_MODEL=${ANTHROPIC_DEFAULT_SONNET_MODEL:-}
ANTHROPIC_DEFAULT_HAIKU_MODEL=${ANTHROPIC_DEFAULT_HAIKU_MODEL:-}
CLAUDE_CODE_SUBAGENT_MODEL=${CLAUDE_CODE_SUBAGENT_MODEL:-}
CLAUDE_CODE_EFFORT_LEVEL=${CLAUDE_CODE_EFFORT_LEVEL:-}
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=${CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC:-}
API_TIMEOUT_MS=${API_TIMEOUT_MS:-}
DEEPSEEK_API_KEY=$( [[ -n "${DEEPSEEK_API_KEY:-}" ]] && echo "<set>" || echo "" )
EOF
}

list_profiles() {
  cat <<'EOF'
anth
ds-pro
ds-flash
reset
EOF
}

main() {
  load_env_file

  local command="${1:-}"
  case "$command" in
    apply)
      if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        echo "apply must be sourced. Use:" >&2
        echo "  source $SCRIPT_NAME apply <profile>" >&2
        echo "or:" >&2
        echo "  eval \"\$($SCRIPT_NAME env <profile>)\"" >&2
        exit 1
      fi
      apply_profile "${2:-}"
      ;;
    env)
      print_exports "${2:-}"
      ;;
    exec)
      shift || true
      exec_with_profile "${1:-}" "${@:2}"
      ;;
    status)
      status
      ;;
    list)
      list_profiles
      ;;
    ""|-h|--help|help)
      usage
      ;;
    *)
      echo "Unknown command: $command" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
