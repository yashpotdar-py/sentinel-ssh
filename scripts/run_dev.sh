#!/usr/bin/env bash
set -e

sudo python3 - << 'EOF'
from sentinel.ingest import stream_ssh_logs
from sentinel.parser import parse_ssh_log
from sentinel.detector import process_event
from sentinel.responder import block_ip, unblock_expired
from sentinel.config import load_config

config = load_config()
ALLOWLIST = config["allowlist"]
BLOCK_DURATION = config["ssh"]["block_duration_seconds"]

for line in stream_ssh_logs():
    event = parse_ssh_log(line)
    if not event:
        continue

    alert = process_event(event)
    if alert:
        print("BLOCKING:", alert["ip"])
        block_ip(alert["ip"], BLOCK_DURATION, ALLOWLIST)

    unblock_expired()
EOF
