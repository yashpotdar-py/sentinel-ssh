# sentinel-ssh 🛡️

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

```

journald → parser → detector → responder → UFW

````

- `journald` is the source of truth  
- the parser extracts signal  
- the detector tracks behavior over time  
- the responder enforces consequences  

No dashboards. No databases. Just decisions.

---

## ✨ Features

- **Real-time detection**  
  Streams logs directly from `journalctl`. No polling files like a peasant.

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
   git clone https://github.com/yashpotdar-py/sentinel-ssh.git
   cd sentinel-ssh
````

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

