# Sentinel-SSH v1 Freeze

## Included
- Journald-based SSH log ingestion
- Structured parsing of auth events
- Sliding-window brute-force detection
- UFW-based automated blocking
- Allowlist protection
- Automatic unblock
- systemd persistence

## Explicitly Excluded
- Dashboards
- External alerts
- Persistent block storage
- Distributed deployment
- Machine learning

## Rationale
v1 prioritizes correctness, explainability, and safety over features.
