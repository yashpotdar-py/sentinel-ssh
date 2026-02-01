# sentinel-ssh

Sentinel-SSH is a lightweight SSH intrusion detection and response service designed for single-host Linux systems.

It detects brute-force and enumeration attempts using SSH authentication logs and applies temporary firewall blocks using UFW.

## Why this exists
Fail2Ban is powerful but opaque. Sentinel-SSH was built to:
- understand SSH attack signals at a low level
- experiment with detection logic safely
- provide explainable, inspectable behavior

## Architecture
journald → parser → detector → responder → UFW

## Detection Logic
- Sliding time window
- Per-IP state tracking
- Conservative thresholds to avoid false positives

## Safety Guarantees
- Explicit allowlist
- Temporary blocks only
- Automatic unblock
- No permanent firewall changes

## Limitations
- Single-host only
- In-memory state
- No persistence across reboot (by design)

## Status
v1 frozen. Stable for home-lab and learning use.
