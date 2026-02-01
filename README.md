# sentinel-ssh 🛡️

> "If you come at the king, you best not miss." - Omar Little (and probably your server running this)

**Sentinel-SSH** is a lightweight, no-nonsense SSH intrusion detection and response system. It watches your `journald` logs like a hawk, detects brute-force attempts from scripts written by bored teenagers, and politely asks `ufw` to show them the door.

It's designed for single-host Linux systems where you want actual visibility into what's happening, rather than trusting a black box.

## 🧐 Why?

Look, `Fail2Ban` is great. Use it if you want. But it's also a massive labyrinth of regex and configuration that I didn't feel like debugging at 3 AM.

I built Sentinel-SSH because I wanted:
1.  **Transparency**: I want to know *exactly* why an IP was blocked.
2.  **Safety**: No permanent firewall rule clutter. Verify, block, cool down, release.
3.  **Control**: Python is easier to read than jail.conf.
4.  **Fun**: Writing my own security tools makes me feel like a hacker in a movie.

## 🏗️ Architecture

It's stupidly simple, which is a feature:

`journald` (source of truth) → `parser` (regex magic) → `detector` (state tracking) → `responder` (the bouncer) → `UFW` (the wall)

## ✨ Features

-   **Real-time Detection**: Streams logs directly from `journalctl`. No polling files like a peasant.
-   **Smart-ish Detection**: Uses a sliding time window to track failed attempts.
-   **Temporary Blocks**: Blocks IPs for a configurable duration (default: 5 mins). Just enough to annoy them into moving to a softer target.
-   **Safety First**: Built-in allowlist prevents you from locking yourself out (unless you try really hard).
-   **Clean Code**: Fully type-hinted, documented, and written by someone who actually cares about readability.

## 🚀 Usage

### Prerequisites

-   Linux (duh)
-   `python3` (>= 3.8)
-   `ufw` (Uncomplicated Firewall)
-   `systemd` (Sorry, sysvinit purists)

### Installation

1.  Clone this repo.
    ```bash
    git clone https://github.com/yashpotdar-py/sentinel-ssh.git
    cd sentinel-ssh
    ```

2.  Install dependencies.
    ```bash
    pip install -e .
    ```

3.  Configure your allowlist in `config/sentinel.yaml`. **DO THIS or risk locking yourself out.**

4.  Run it.
    ```bash
    # Needs root because it touches the firewall
    sudo python3 -m sentinel.main
    ```

## 🛠️ Configuration

Check `config/sentinel.yaml`. It's YAML. You know how to read YAML.

```yaml
ssh:
  block_duration_seconds: 300  # 5 minutes of shame

allowlist:
  - "192.168.1.0/24"      # Your home network
  - "10.0.0.5"            # That one trusted jumpbox
```

## ⚠️ Disclaimer

I am a developer, not a lawyer or your CISO. This tool interacts with your firewall. While I've made it as safe as possible (temporary blocks, allowlists), running code as root carries risks. 

**Use common sense.** Don't run this on a production database server handling millions of dollars without testing it first.

## 🤝 Contributing

Found a bug? Want to make the regex tighter? PRs are welcome. Just keep the code clean and the commit messages funny.

## 📝 License

MIT. Do whatever you want with it. Just don't blame me if you block Googlebot.

---
*Built with ☕ and paranoia by [Yash Potdar](https://github.com/yashpotdar-py).*
