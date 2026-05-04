# Load with:
#   source <agent-framework-template>/shell/provider-switch.zsh

# Dynamically resolve the framework root (works regardless of where the repo is cloned)
0="${${(%):-%N}:A}"
export AGENT_FRAMEWORK_HOME="${0:A:h:h}"
export AGENT_PROVIDER_SWITCH_SCRIPT="$AGENT_FRAMEWORK_HOME/scripts/provider-switch.sh"

ccuse() {
  local profile="${1:-}"
  if [[ -z "$profile" ]]; then
    echo "Usage: ccuse <anth|ds-pro|ds-flash|reset>"
    return 1
  fi

  eval "$(bash "$AGENT_PROVIDER_SWITCH_SCRIPT" env "$profile")" || return 1
  echo "Claude Code profile: $profile"
}

ccrun() {
  local profile="${1:-}"
  shift || true
  if [[ -z "$profile" || $# -eq 0 ]]; then
    echo "Usage: ccrun <profile> <command> [args...]"
    return 1
  fi

  bash "$AGENT_PROVIDER_SWITCH_SCRIPT" exec "$profile" "$@"
}

ccstatus() {
  bash "$AGENT_PROVIDER_SWITCH_SCRIPT" status
}

ccprofiles() {
  bash "$AGENT_PROVIDER_SWITCH_SCRIPT" list
}
