# Threat Model

## Asset
- SSH access to the host `miriel`

## Adversary
- Internet-based attackers performing:
  - Brute-force login attempts
  - Username enumeration
  - Credential stuffing

## Attack Signals (Initial)
- Repeated failed SSH authentication attempts
- Attempts for non-existent users
- High-frequency attempts from a single IP

## Out of Scope
- Zero-day SSH daemon exploits
- Insider threats
- Physical access

## Response Philosophy
- Prefer false negatives over false positives
- Never block trusted subnets
- All actions must be reversible
