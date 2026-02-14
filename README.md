# sentinel-ssh 🛡️

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> "If you come at the king, you best not miss."  
> — Omar Little (and probably your server running this)

**Sentinel-SSH** is a lightweight, no-nonsense SSH intrusion detection and response system.

It watches your `journald` logs like a hawk, detects brute-force attempts from scripts written by bored teenagers, and politely asks `ufw` to show them the door.

Designed for single-host Linux systems where you want to actually *see* what’s happening, instead of trusting a black box and hoping for the best.

---

## 🧐 Why?

Look, **Fail2Ban is great**. You should use it if it fits your needs.

But it’s also a sprawling maze of regex, configs, and “why is this not triggering” moments that I didn’t feel like debugging at 3 AM.

I built Sentinel-SSH because I wanted:

1. **Transparency** – I want to know *exactly* why an IP was blocked.
2. **Safety** – No permanent firewall clutter. Verify → block → cool down → release.
3. **Control** – Python is easier to reason about than `jail.conf`.
4. **Fun** – Writing your own security tools makes you feel like a hacker in a movie. This is important.

---

## 🏗️ Architecture

It’s intentionally boring. That’s a feature.

```plaintext
journald → parser → detector → responder → UFW
```

- `journald` is the source of truth  
- the parser extracts signal  
- the detector tracks behavior over time  
- the responder enforces consequences  

No dashboards. No databases. Just decisions.

---

## ✨ Features

- **Real-time detection**  
  Streams logs directly from `journalctl`, avoiding file polling.

- **Smart-ish detection**  
  Sliding time window to catch brute-force and enumeration patterns.

- **Temporary blocks**  
  IPs are blocked for a configurable duration (default: 5 minutes).  
  Long enough to be annoying. Short enough to be safe.

- **Safety first**  
  Built-in allowlist so you don’t lock yourself out  
  (unless you *really* try).

- **Readable code**  
  Type-hinted, documented, and written with the assumption that future-you has feelings.

---

## 📊 Observability (v1.1.0+)

Because "it's working fine" is not a metric.

Sentinel-SSH exposes internal metrics via a local HTTP endpoint for Prometheus scraping.

By default, metrics are available at:

```
http://127.0.0.1:9105/metrics
```

This endpoint is localhost-only. No authentication. No TLS.  
It's designed to be scraped by Prometheus running on the same host.

### Exported Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `sentinel_up` | gauge | 1 if Sentinel is running, 0 otherwise |
| `ssh_failed_attempts_total` | counter | Total SSH authentication failures observed |
| `unique_attacker_ips_total` | counter | Number of distinct IPs that have crossed the brute-force threshold during runtime |
| `bans_total` | counter | Total number of firewall bans issued |
| `active_bans` | gauge | Number of currently active bans |
| `last_ban_timestamp` | gauge | Unix timestamp of most recent ban |

**Note:**
- Counters reset on service restart.
- `unique_attacker_ips_total` tracks unique threshold-triggering IPs during the current runtime.
- Firewall bans apply only to new connections. Existing SSH sessions are not terminated.

---

## 🚀 Usage

### Prerequisites

- Linux (duh)
- `python3` ≥ 3.8
- `ufw`
- `systemd`  
  (Sorry, sysvinit purists)

### Installation

1. Clone the repo:
    ```bash
    git clone https://github.com/yashpotdar-py/  sentinel-ssh.git
    cd sentinel-ssh
    ```
  
2. Install dependencies:
    ```bash
    pip install -e .
    ```

3. Configure your allowlist in `config/sentinel.yaml`.
   **Do this unless you enjoy locking yourself out.**

4. Run it:
    ```bash
    sudo python3 -m sentinel.main
     ```

---

## 🛠️ Configuration

See `config/sentinel.yaml`.
It’s YAML. You’ll manage.

```yaml
ssh:
  block_duration_seconds: 300  # 5 minutes of shame

allowlist:
  - "192.168.1.0/24"  # Home network
  - "10.0.0.5"        # That one trusted box
```

---

## 🧠 Operational Model

Sentinel-SSH works by:

1. Monitoring systemd SSH logs via `journalctl`.
2. Detecting repeated failed login attempts within a sliding time window.
3. Issuing UFW deny rules for offending IPs.
4. Automatically removing bans after a configurable duration.

**Important:**
- Bans block **new** incoming SSH connections.
- Active SSH sessions are **not** forcibly terminated.
- Detection is deterministic and threshold-based.
- Metrics are in-memory and reset on restart.

Think of it as a bouncer, not an assassin.

---

## 📡 Prometheus Integration

Example Prometheus scrape configuration:

```yaml
scrape_configs:
  - job_name: "sentinel-ssh"
    static_configs:
      - targets: ["127.0.0.1:9105"]
```

Grafana dashboards can be built using standard PromQL queries such as:

```promql
rate(ssh_failed_attempts_total[1m])
bans_total
active_bans
unique_attacker_ips_total
```

Or if you prefer suffering, you can just `curl http://127.0.0.1:9105/metrics` and read the raw output like it's 1995.

---

## ⚠️ Disclaimer

I am a developer, not your lawyer or CISO.

This tool runs as root and touches your firewall. While it’s designed to be safe (temporary blocks, allowlists, automatic cleanup), **running security code always carries risk**.

Use common sense.
Test it first.
Please don’t deploy this on a production server handling millions of dollars and then DM me.

---

## 🤝 Contributing

Found a bug? Want to tighten the regex? Improve detection logic?

PRs are welcome.
Just keep the code clean and the commit messages funny.

---

## 📝 License

MIT. Do whatever you want with it.

Just don’t blame me if you block Googlebot.

---

*Built with ☕, paranoia, and systemd by [Yash Potdar](https://github.com/yashpotdar-py).*

