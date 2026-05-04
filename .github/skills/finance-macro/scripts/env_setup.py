#!/usr/bin/env python3
"""Environment setup and API key validation for macro-finance skills.

Validates required API keys from environment variables or .env files.
Supports: FRED_API_KEY, WORLD_BANK_API_KEY (optional), IMF_API_KEY (optional).

Usage:
    python3 env_setup.py              # validate all keys
    python3 env_setup.py --check fred  # validate FRED only
"""

import os
import sys
from pathlib import Path

REQUIRED_VARS = {
    "FRED_API_KEY": {
        "description": "FRED API key from https://fred.stlouisfed.org/docs/api/api_key.html",
        "required": True,
    },
}

OPTIONAL_VARS = {
    "STATS_NZ_API_KEY": {
        "description": "Stats NZ API key — free registration at https://data.stats.govt.nz/",
        "required": False,
    },
    "ABS_API_KEY": {
        "description": "ABS (Australia) API key — free registration at https://api.data.abs.gov.au/",
        "required": False,
    },
    "IMF_API_KEY": {
        "description": "IMF Data API key — registration required at https://data.imf.org/ (note: old dataservices.imf.org was decommissioned 2025)",
        "required": False,
    },
    "OPENAI_API_KEY": {
        "description": "OpenAI API key for LLM-powered analysis (optional)",
        "required": False,
    },
}


def _load_dotenv():
    """Load .env from framework root or home directory if present."""
    env_paths = []
    # search upward from this script until we find .env or hit the filesystem root
    p = Path(__file__).resolve().parent
    for _ in range(10):
        candidate = p / ".env"
        if candidate.exists():
            env_paths.append(candidate)
            break
        if p.parent == p:
            break
        p = p.parent
    env_paths.append(Path.home() / ".claude" / ".env")
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, val = line.partition("=")
                        val = val.strip().strip('"').strip("'")
                        if key not in os.environ:
                            os.environ[key] = val


def validate(check_filter=None):
    _load_dotenv()
    errors = []
    warnings = []
    status = {}

    all_vars = {**REQUIRED_VARS, **OPTIONAL_VARS}
    for var, info in all_vars.items():
        if check_filter and check_filter.lower() not in var.lower():
            continue
        value = os.environ.get(var, "")
        if value:
            status[var] = "set"
        elif info["required"]:
            errors.append(f"MISSING {var}: {info['description']}")
            status[var] = "missing_required"
        else:
            warnings.append(f"Optional {var} not set: {info['description']}")
            status[var] = "missing_optional"

    if errors:
        print("[ERROR] Required API keys missing:")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print("[WARN] Optional API keys not set:")
        for w in warnings:
            print(f"  - {w}")
    if not errors and not warnings:
        print("[OK] All API keys validated.")

    return {"status": status, "errors": errors, "warnings": warnings}


def get_key(name):
    _load_dotenv()
    return os.environ.get(name, "")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate API keys for macro skills")
    parser.add_argument("--check", type=str, help="Filter by variable name substring")
    parser.add_argument("--get", type=str, help="Get a specific key value (masked)")
    args = parser.parse_args()

    if args.get:
        val = get_key(args.get)
        if val:
            print(f"{args.get}={val[:4]}...{val[-4:]}")
        else:
            print(f"{args.get} not set")
    else:
        result = validate(args.check)
        has_errors = bool(result["errors"])
        sys.exit(1 if has_errors else 0)
