#!/usr/bin/env bash
# Quick dev script: stream SSH logs using Python
set -e  # Exit on error

python3 - << 'EOF'
from sentinel.ingest import stream_ssh_logs  # Import the log streamer
from sentinel.parser import parse_ssh_log  # Import the log parser

for line in stream_ssh_logs():  # Print each log line as it arrives
    event = parse_ssh_log(line)  # Parse the log line
    if event:  # If parsing was successful
        print(line)
EOF
