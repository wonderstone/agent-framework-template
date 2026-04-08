# Strict Adoption Verification Packet

- Generated at: [generated-at]
- Repository root: [repository-root]
- Manifest schema version: [manifest-schema-version]
- Audit version: [audit-version]
- Adoption verdict: [fully-adopted | partially-adopted | design-only-upgrade-path-kept]

## Verdict Summary

- [Short summary of why this verdict was reached.]

## Mechanism Coverage

| Mechanism ID | Status | Required coverage | Missing required paths | Notes |
|---|---|---|---|---|
| [mechanism-id] | [kept | downgraded | design-only-upgrade-path-kept | missing | unknown-mechanism] | [N/M paths present] | [missing paths or `none`] | [short note] |

## Validation Evidence

| Label | Path | Present | Notes |
|---|---|---|---|
| [validation-label] | [path] | [yes / no] | [what this evidence proves] |

## Independent Review Evidence

| Reviewer | Path | Present | Notes |
|---|---|---|---|
| [reviewer-name] | [path] | [yes / no] | [what this review contributes] |

## Contract Notes

- Required mechanism IDs: [comma-separated mechanism ids]
- Require independent review for: [comma-separated verdicts or `none`]
- Verification packet path: [verification-packet-path]

## Notes

- This packet is an attestation artifact, not canonical proof that a repository's runtime behavior is semantically correct in every scenario.
- `fully-adopted` requires both mechanism coverage and the evidence gates declared by the manifest contract.