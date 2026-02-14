# Architecture

Sentinel-SSH is a single-process Python application with a deliberately simple architecture.

## Components

### 1. Ingest (`ingest.py`)
Streams SSH authentication logs from `journalctl` in real-time.

- Uses `journalctl -f` to tail systemd journal
- Filters for sshd service logs
- Yields raw log lines to the parser

### 2. Parser (`parser.py`)
Extracts structured data from raw log lines.

- Identifies failed authentication attempts
- Extracts IP addresses and usernames
- Outputs structured events

### 3. Detector (`detector.py`)
Tracks behavior over time and decides when to act.

- Maintains sliding time window state
- Counts failed attempts per IP
- Triggers ban decision when threshold is exceeded
- Respects allowlist

### 4. Responder (`responder.py`)
Enforces firewall rules via UFW.

- Issues `ufw deny from <IP>` commands
- Schedules automatic unban after configured duration
- Verifies ban success and handles errors

### 5. Metrics (`metrics.py`)
In-memory metrics store.

- Thread-safe counters and gauges
- No external dependencies
- Simple snapshot-based collection

### 6. Metrics Server (`metrics_server.py`)
HTTP endpoint for Prometheus scraping.

- Runs on localhost:9105
- Exposes `/metrics` endpoint
- Daemon thread (non-blocking)

## Flow

```
journald → ingest → parser → detector → responder → ufw
                                 ↓
                              metrics
                                 ↓
                          /metrics endpoint
```

## Design Principles

- **No database**: State is in-memory and ephemeral
- **No external dependencies**: Uses system tools (journalctl, UFW)
- **Single process**: All components run in one Python process
- **Fail-safe**: Metrics failures never crash Sentinel
- **Deterministic**: No ML, no heuristics, just thresholds

## Configuration

All configuration is loaded from `config/sentinel.yaml`:

- `block_threshold`: Failed attempts before ban
- `block_duration_seconds`: How long bans last
- `allowlist`: IPs that are never banned

## Operational Characteristics

- **Startup**: Reads config, initializes state, starts metrics server, begins log ingestion
- **Runtime**: Processes logs continuously, maintains state, handles bans/unbans
- **Shutdown**: Graceful termination on SIGTERM/SIGINT
- **Metrics**: In-memory counters reset on restart

No persistence. No replay. What you see in the logs is what happened.
