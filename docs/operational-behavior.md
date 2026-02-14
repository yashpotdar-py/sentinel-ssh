# Operational Behavior

This document explains how Sentinel-SSH behaves in production.

## Ban Lifecycle

### 1. Detection Phase

Sentinel monitors SSH authentication logs in real-time via `journalctl`.

When a failed authentication attempt is detected:
1. The IP address is extracted
2. The failure is recorded with a timestamp
3. The failure count for that IP is incremented

### 2. Threshold Check

After each failed attempt, Sentinel checks:

```
if failed_attempts >= block_threshold:
    initiate_ban()
```

**Default threshold:** 5 failed attempts

The threshold is configurable in `config/sentinel.yaml`.

### 3. Allowlist Check

Before issuing a ban, Sentinel verifies the IP is not in the allowlist.

**Allowlisted IPs never trigger bans**, regardless of failure count.

This prevents you from locking yourself out (unless you really try).

### 4. Ban Execution

If the IP passes threshold and is not allowlisted:

1. Sentinel issues a UFW deny rule: `ufw deny from <IP>`
2. The ban is recorded in internal state
3. Metrics are incremented:
   - `bans_total` +1
   - `active_bans` +1
   - `unique_attacker_ips_total` +1 (if first ban for this IP)
   - `last_ban_timestamp` = current time

### 5. Ban Expiry

Bans are **temporary** by default.

After `block_duration_seconds` (default: 300 = 5 minutes):

1. Sentinel removes the UFW deny rule
2. The IP is removed from internal state
3. Metrics are updated:
   - `active_bans` -1

The IP can potentially be re-banned if it continues attacking.

## Threshold Logic

Sentinel uses a **sliding time window** to track failures.

### Time Window

Failures older than the time window are automatically discarded.

This prevents "1 failed attempt per day for 5 days" from triggering a ban.

### Failure Tracking

Each failed attempt is timestamped and stored per-IP.

When checking the threshold:
1. Old failures (outside the time window) are purged
2. Remaining failures are counted
3. If count >= threshold, ban is triggered

### State Reset

When an IP is banned:
- The failure count **is not reset**
- The failure history remains in memory
- Upon unban, if the IP attacks again, it starts from scratch

This is intentional. We're not rehabilitating attackers.

## Firewall Behavior

### What Bans Block

UFW deny rules block **new incoming connections** from the banned IP.

This includes:
- New TCP handshakes
- New SSH connection attempts
- Any new traffic from that IP

### What Bans Do NOT Block

**Active SSH sessions are not terminated.**

If an attacker has an active SSH session when they get banned, that session continues until:
- The attacker disconnects
- The session times out
- sshd terminates it for other reasons

**Why?**

Because Sentinel controls the firewall, not the SSH daemon.

Terminating active sessions requires killing processes or modifying kernel state, which introduces risk and complexity.

Sentinel is a **bouncer**, not an **assassin**.

### Firewall Rule Placement

Sentinel issues UFW commands, which add rules to the firewall ruleset.

The exact placement depends on your existing UFW configuration.

**Best practice:** Run Sentinel on a system with minimal UFW customization.

## Known Limitations

### 1. No Session Termination

Bans only prevent new connections. Active sessions persist.

**Mitigation:** Use short SSH session timeouts in `sshd_config`.

### 2. No IP Spoofing Detection

Sentinel trusts the source IP in logs.

If an attacker spoofs IPs, Sentinel will ban the spoofed IPs, not the real attacker.

**Mitigation:** Use network-level anti-spoofing (BCP 38, uRPF).

### 3. Metrics Reset on Restart

All metrics are in-memory and ephemeral.

**Mitigation:** Use Prometheus for historical data.

### 4. No Distributed Coordination

Sentinel runs per-host. Multiple hosts do not share state.

**Mitigation:** Run Sentinel on each host. Or use a centralized IDS if you need coordination.

### 5. Log Parsing Brittleness

Sentinel parses logs via regex.

If systemd or sshd changes log format, detection may break.

**Mitigation:** Monitor `ssh_failed_attempts_total`. If it stops incrementing during attacks, check logs manually.

### 6. No Rate Limiting

Sentinel does not rate-limit its own UFW operations.

If you're under attack from 10,000 IPs simultaneously, Sentinel will issue 10,000 UFW commands.

**Mitigation:** Don't expose SSH to the entire internet. Use a VPN or bastion host.

## Troubleshooting

### "I'm locked out"

Check your allowlist in `config/sentinel.yaml`.

If you're banned and not allowlisted:
1. Access the server via console (or another IP)
2. Manually remove the UFW rule: `ufw delete deny from <IP>`
3. Add your IP to the allowlist
4. Restart Sentinel

### "Bans aren't happening"

Check:
1. Is Sentinel running? `systemctl status sentinel-ssh`
2. Are logs being ingested? Check Sentinel output
3. Are failed attempts being parsed? Check `ssh_failed_attempts_total`
4. Is the threshold set correctly? Check `config/sentinel.yaml`
5. Is the attacker IP allowlisted? Check `config/sentinel.yaml`

### "Metrics aren't updating"

Check:
1. Is the metrics server running? `curl http://127.0.0.1:9105/metrics`
2. Is Sentinel actually processing logs?
3. Are there any errors in Sentinel logs?

The metrics server is designed to fail silently, so a crash won't stop Sentinel.

### "Unbans aren't happening"

Check:
1. Is Sentinel still running?
2. Are there errors in the logs?
3. Is UFW actually applying the rules? Run `ufw status`

If Sentinel crashes, scheduled unbans will not execute.

Restart Sentinel and manually clean up UFW rules if needed.

## Best Practices

1. **Always configure an allowlist.** Your IP, your VPN, your bastion host.
2. **Monitor metrics.** If `ssh_failed_attempts_total` stops incrementing, something is wrong.
3. **Use short ban durations** (5-10 minutes) unless you have a specific reason.
4. **Run Sentinel as a systemd service** for automatic restarts and logging.
5. **Test before deploying.** Lock yourself out in a VM first, not production.
6. **Keep logs.** Sentinel logs to stdout. Capture them with journald or syslog.

## Summary

Sentinel-SSH is designed to be simple, safe, and observable.

It detects brute-force attacks, bans offending IPs temporarily, and exposes metrics for monitoring.

It does not terminate sessions, persist state, or coordinate across hosts.

Know the limitations. Work within them. Don't deploy this on the NSA's SSH server.
