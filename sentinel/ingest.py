# I'm learning how to work with subprocesses and log streaming in Python.
# This file is about reading SSH logs in real time from systemd's journal.

import subprocess  # To run system commands from Python
import logging
from typing import Iterator  # For type hinting a generator of log lines

logger = logging.getLogger(__name__)

def stream_ssh_logs() -> Iterator[str]:
    """
    Streams SSH logs from journald in real time.

    This function uses subprocess to call 'journalctl' and follows the SSH service logs as they happen.
    It's read-only: it doesn't change any system state, just reads logs.

    Returns:
        Iterator[str]: Each line from the SSH log, as a string (stripped of whitespace).
    """
    # The command to run: journalctl -u ssh -f -o short
    # -u ssh: only logs for the ssh service
    # -f: follow (like tail -f)
    # -o short: short output format
    cmd = [
        "journalctl",      # journalctl is the systemd log viewer
        "-u", "ssh",       # -u specifies the unit (ssh service)
        "-f",              # -f means follow new log entries
        "-o", "short"      # -o short gives a compact output
    ]

    logger.info(f"Starting log stream with command: {' '.join(cmd)}")

    # Start the subprocess to run the command above
    # stdout=subprocess.PIPE: capture the output so we can read it in Python
    # stderr=subprocess.PIPE: also capture errors (not used here, but good practice)
    # text=True: get strings instead of bytes
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except FileNotFoundError:
        logger.critical("Has journalctl been installed? Cannot find the executable.")
        return
    
    # If for some reason stdout isn't available, just return (nothing to yield)
    if not process.stdout:
        logger.error("Failed to Capture stdout from journalctl")
        return

    # Read each line as it comes in from the log
    for line in process.stdout:
        # Remove any leading/trailing whitespace (like newlines)
        if line.strip():
            yield line.strip()  # yield returns the line to whoever called this function

    # Note: This function is a generator! It doesn't return all lines at once,
    # but gives them one by one as they arrive.
