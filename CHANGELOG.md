# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
