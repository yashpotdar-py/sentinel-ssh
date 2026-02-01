from sentinel.ingest import stream_ssh_logs
from sentinel.parser import parse_ssh_log
from sentinel.detector import process_event
from sentinel.responder import block_ip, unblock_expired
from sentinel.config import load_config


def main():
    config = load_config()
    allowlist = config["allowlist"]
    block_duration = config["ssh"]["block_duration_seconds"]

    for line in stream_ssh_logs():
        event = parse_ssh_log(line)
        if not event:
            continue

        alert = process_event(event)
        if alert:
            block_ip(alert["ip"], block_duration, allowlist)

        unblock_expired()


if __name__ == "__main__":
    main()
