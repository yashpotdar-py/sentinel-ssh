# Release Notes: Sentinel-SSH v1.1.0

**Release Date:** February 14, 2026

---

## Overview

This release elevates Sentinel-SSH from a reactive security script to an **observable system service**.

The focus of v1.1.0 was **correctness, determinism, and operational clarity**.

---

## What Changed

### Observability

Sentinel-SSH now exposes internal metrics via a Prometheus-compatible HTTP endpoint.

This was not added because "everyone has metrics now."

It was added because operating security software without visibility is reckless.

You should know:
- Is Sentinel running?
- How many attacks are happening?
- Are bans being issued?
- Are unbans happening on schedule?

Now you can. `http://127.0.0.1:9105/metrics`

### Metrics Semantics

The metrics system is intentionally minimal:

- **No external dependencies.** No Prometheus client library. No protobuf.
- **In-memory only.** No disk. No persistence. Metrics reset on restart.
- **Localhost-only.** No authentication. No TLS. Scrape it locally or don't.
- **Fail-safe.** Metrics failures never crash Sentinel.

The implementation is ~50 lines of Python. It works. It's boring. That's the point.

### Security Model

Metrics endpoint security is intentionally minimal:

- **Localhost-only binding**: Metrics server binds to `127.0.0.1:9105` exclusively
- **No authentication**: Not needed for localhost-only services
- **No TLS**: Not needed for localhost-only traffic
- **No external exposure**: Firewall should block external access by default

**If remote scraping is required**: Use SSH port forwarding or VPN. The metrics endpoint is not designed for direct external exposure.

This is a deliberate design choice, not a limitation.

### Documentation

Real documentation was written.

Not "updated README with vague promises."

Actual technical documentation:

- **architecture.md**: Component flow, design principles, operational characteristics
- **metrics.md**: Metric types, semantics, failure modes, query examples
- **operational-behavior.md**: Ban lifecycle, threshold logic, known limitations

These documents are for operators who need to understand what Sentinel is doing and why.

---

## What Was NOT Added

### No Dashboards

Sentinel does not ship Grafana dashboards.

You know your environment. You know what matters. Build your own.

### No Alerting

Sentinel emits metrics. Prometheus handles alerting.

Separation of concerns.

### No Historical Storage

Metrics are ephemeral. Prometheus is your time-series database.

Sentinel is not a database.

### No Machine Learning

Sentinel intentionally avoids heuristic or ML-based detection.

The focus is deterministic threshold-based logic. This ensures:
- Predictable behavior
- No training data requirements
- No false positives from model drift
- Transparent decision-making

Complexity is a security risk. Simple thresholds work.

---

## Why Metrics Matter

Security tools that provide no observability are black boxes.

You deploy them. You hope they work. You find out they don't when you're already compromised.

Metrics allow you to:

1. **Verify correct operation** – Is Sentinel detecting attacks?
2. **Detect failures** – Did Sentinel crash? Is log parsing broken?
3. **Track attack patterns** – Are attacks increasing? From how many IPs?
4. **Alert on anomalies** – No attacks in 24 hours? Maybe Sentinel is dead.

This is basic operational hygiene.

---

## Architectural Principles

The metrics implementation follows the same principles as the rest of Sentinel:

1. **Simplicity**: No dependencies, no complexity
2. **Safety**: Failures are isolated and non-fatal
3. **Transparency**: Metrics are self-documenting
4. **Determinism**: No sampling, no approximation

These are not flexible principles. They are load-bearing constraints.

---

## Known Limitations

Documented clearly because honesty > marketing:

1. **Metrics reset on restart** – Use Prometheus for historical data
2. **No per-IP metrics** – Sentinel tracks aggregates, not individual attackers
3. **No session termination** – Bans block new connections, not active sessions
4. **Localhost-only** – Remote scraping requires SSH tunneling or VPN

These are not bugs. They are design decisions.

---

## Migration Guide

### From v1.0.2 to v1.1.0

**No breaking changes.**

Sentinel v1.1.0 is fully backward-compatible with v1.0.x.

Your existing configuration will continue to work.

**What's new:**
- Metrics endpoint is automatically enabled on `127.0.0.1:9105`
- No configuration required
- No performance impact
- No new dependencies

**Optional:**
- Configure Prometheus to scrape the endpoint
- Build Grafana dashboards
- Set up alerts

But Sentinel will continue banning attackers whether you scrape metrics or not.

---

## Future Direction

Sentinel-SSH is intentionally minimal.

Future releases will focus on:

- **Correctness improvements** – Edge case fixes, better error handling
- **Performance optimization** – Efficient log parsing, state management
- **Documentation refinement** – Clearer operational guidance

**Not planned:**
- Feature bloat
- External dependencies
- Configuration complexity
- Machine learning

Sentinel does one thing. It will continue doing that one thing well.

---

## Acknowledgments

This release was driven by production usage and operator feedback.

Thanks to everyone who asked "how do I know if this is working?"

The answer is now: `curl http://127.0.0.1:9105/metrics`

---

## Upgrade Instructions

### Via Git

```bash
cd sentinel-ssh
git pull origin main
git checkout v1.1.0
pip install -e .
sudo systemctl restart sentinel-ssh
```

Verify metrics endpoint:

```bash
curl http://127.0.0.1:9105/metrics
```

You should see:

```
sentinel_up 1
ssh_failed_attempts_total 0
unique_attacker_ips_total 0
bans_total 0
active_bans 0
last_ban_timestamp 0
```

If you see that, you're good.

---

## Version Tag

```bash
git tag -a v1.1.0 -m "Sentinel-SSH v1.1.0: observability and metrics release"
git push origin v1.1.0
```

---

**This is a real release.**

Not "I pushed some commits."

Not "updated stuff."

A deliberate, documented, versioned release.

Treat it accordingly.
