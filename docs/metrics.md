# Metrics

Sentinel-SSH v1.1.0 introduces a Prometheus-compatible metrics exporter.

## Why Metrics?

Because "trust me, it's running" isn't observability.

Metrics allow you to:
- Verify Sentinel is actually running
- Track attack patterns over time
- Alert on anomalous behavior
- Build dashboards for that sweet, sweet dopamine hit

## Design Decisions

### In-Memory Only

Metrics are stored in-memory and reset on restart.

**Why?**
- Simplicity. No database, no disk I/O, no corruption.
- Ephemeral state matches operational reality.
- Sentinel is not a time-series database.

If you want historical data, that's what Prometheus is for.

### Exporter-Style

Sentinel exposes a scrape endpoint. It does not push metrics anywhere.

**Why?**
- Follows Prometheus conventions.
- No external dependencies.
- Works offline.

### Localhost-Only

The metrics server binds to `127.0.0.1:9105`.

**Why?**
- Security. No authentication = no external exposure.
- Simplicity. Prometheus should run on the same host.
- Intent. This is for operators, not attackers.

If you need remote scraping, use SSH port forwarding or VPN. Not my problem.

## Metric Types

### Counters

Monotonically increasing values that reset on restart.

- `ssh_failed_attempts_total`: Total failed SSH authentication attempts observed
- `unique_attacker_ips_total`: Number of distinct IPs that crossed the threshold during runtime
- `bans_total`: Total number of firewall bans issued

**Use cases:** Rate calculations, trend analysis

### Gauges

Point-in-time values that can go up or down.

- `sentinel_up`: 1 if running, 0 otherwise
- `active_bans`: Current number of active bans
- `last_ban_timestamp`: Unix timestamp of most recent ban

**Use cases:** Current state monitoring, alerting

## Semantics

### `ssh_failed_attempts_total`

Incremented for every failed SSH authentication attempt parsed from the logs.

**Includes:**
- Invalid usernames
- Wrong passwords
- Key mismatches

**Excludes:**
- Connection timeouts
- Non-authentication failures

### `unique_attacker_ips_total`

Incremented when an IP crosses the brute-force threshold for the first time during the current runtime.

**Important:** Does not increment again if the same IP is unbanned and re-banned.

This metric answers: "How many distinct IPs have triggered a ban decision?"

### `bans_total`

Incremented every time a UFW deny rule is issued.

**Important:** Counts ban events, not unique IPs. If an IP is banned twice, it increments twice.

### `active_bans`

The current count of IPs with active firewall bans.

Decremented when bans expire and are removed.

### `last_ban_timestamp`

Unix timestamp (seconds since epoch) of the most recent ban.

Useful for alerting on "no recent bans" (indicating either no attacks or Sentinel failure).

## Known Limitations

- **No persistence**: Metrics reset on restart
- **No historical labels**: Metrics do not track individual IPs
- **No pre-aggregation**: Rate calculations happen in Prometheus
- **Thread-safe but simple**: Basic locking, no fancy concurrency

## Failure Modes

The metrics server runs in a daemon thread and is designed to fail silently.

**If the metrics server crashes:**
- Sentinel continues operating normally
- Bans still happen
- You just can't observe it

**If scraping fails:**
- Metrics continue accumulating
- Next scrape will have fresh data

Metrics are nice-to-have, not critical path.

## Example Prometheus Queries

### Attack rate over last 5 minutes
```promql
rate(ssh_failed_attempts_total[5m])
```

### Total bans issued
```promql
bans_total
```

### Average ban duration
```promql
(time() - last_ban_timestamp) / 60
```

### Is Sentinel running?
```promql
sentinel_up == 1
```

## Endpoint Specification

**URL:** `http://127.0.0.1:9105/metrics`

**Method:** GET

**Response Format:**
```
sentinel_up 1
ssh_failed_attempts_total 42
unique_attacker_ips_total 3
bans_total 3
active_bans 2
last_ban_timestamp 1739491234
```

Plain text. One metric per line. No comments. No help text. No types.

It's minimal. It works.
