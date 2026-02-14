# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-14

### Added
- **Metrics**: Prometheus-compatible metrics exporter
- **Metrics**: Internal metrics system with thread-safe counters and gauges
- **Metrics**: HTTP `/metrics` endpoint on localhost:9105
- **Metrics**: Exported metrics include:
  - `sentinel_up`: Service health indicator
  - `ssh_failed_attempts_total`: Total authentication failures
  - `unique_attacker_ips_total`: Distinct IPs crossing threshold
  - `bans_total`: Total firewall bans issued
  - `active_bans`: Current active ban count
  - `last_ban_timestamp`: Most recent ban timestamp
- **Docs**: Added `docs/architecture.md` with component flow diagram
- **Docs**: Added `docs/metrics.md` with detailed metric semantics
- **Docs**: Added `docs/operational-behavior.md` with ban lifecycle and limitations
- **README**: Added "Observability" section documenting metrics
- **README**: Added "Operational Model" section explaining ban behavior
- **README**: Added "Prometheus Integration" section with scrape config examples

### Changed
- **Metrics**: Improved unique attacker tracking to count distinct threshold-triggering IPs
- **Metrics**: Metrics server runs as daemon thread (non-blocking)
- **Docs**: Documented firewall behavior and active session semantics

## [1.0.2] - 2026-02-01

### Fixed
- **Linting**: Fixed a bunch of pylint errors.
    - Added module docstrings (because apparently `__init__.py` isn't enough).
    - Switched to lazy % formatting for logging (f-strings in logging are a sin, apparently).
    - Added explicit encoding to `open()`.
    - Fixed some import order sorting.
- **CI**: Raised pylint score from ~7.5 to hopefully 10.0 (or at least >8.0).

## [1.0.1] - 2026-02-01

### Fixed
- **CI**: Fixed a typo in the workflow where I tried to install a Flash player (`ruffle`) instead of a python linter (`ruff`). My bad.

## [1.0.0] - 2026-02-01

### Added
- **Core**: Initial release of Sentinel-SSH. It actually works.
- **Detector**: Brute-force detection with sliding window state tracking.
- **Responder**: UFW integration for temporary blocking.
- **Config**: YAML-based configuration because hardcoding constants is for amateurs.
- **Docs**: Comprehensive README that explains why this exists (spite).

### Changed
- **Logging**: Replaced `print` statements with actual `logging` because we live in a society.
- **Project Structure**: Organized into a proper Python package.

### Fixed
- **Bugs**: Probably many, but I haven't found them yet.
