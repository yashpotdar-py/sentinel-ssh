#!/usr/bin/env bash
# Quick dev script: stream SSH logs using Python
set -e  # Exit on error

python3 - << 'EOF'
from sentinel.ingest import stream_ssh_logs  # Import the log streamer

for line in stream_ssh_logs():  # Print each log line as it arrives
    print(line)
EOF
