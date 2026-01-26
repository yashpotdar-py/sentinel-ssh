#!/usr/bin/env bash
set -e

python3 - << 'EOF'
from sentinel.ingest import stream_ssh_logs
from sentinel.parser import parse_ssh_log
from sentinel.detector import process_event

for line in stream_ssh_logs():
    event = parse_ssh_log(line)
    if not event:
        continue

    alert = process_event(event)
    if alert:
        print("ALERT:", alert)
EOF
