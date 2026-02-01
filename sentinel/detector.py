# sentinel/detector.py

"""
SSH brute force detector logic.
Monitors failed logins and flags suspicious IPs based on thresholds.
"""

import logging
from sentinel.state import EventState  # Import the event state tracker

# Global state for tracking events per IP in a 60-second window
state = EventState(window_seconds=60)
THRESHOLD = 5  # Flag IP if 5+ failed attempts in window
logger = logging.getLogger(__name__)

def process_event(event: dict) -> dict | None:
    """
    Process a parsed SSH event and detect potential brute force attacks.

    Args:
        event (dict): Parsed event from parser.py (e.g., auth_failed, invalid_user).

    Returns:
        dict: Alert info if threshold exceeded (IP, count, reason), else None.
    """
    # Only care about failed auth events
    if event["event"] not in ("auth_failed", "invalid_user"):
        return None

    # Record the event and get current count for this IP
    count = state.record(event["ip"])
    logger.debug("Event for %s recorded. Current count: %d", event['ip'], count)

    # If count exceeds threshold, flag as suspected brute force
    if count >= THRESHOLD:
        logger.warning("Threshold exceeded for %s (count: %d)", event['ip'], count)
        return {
            "ip": event["ip"],
            "count": count,
            "reason": "ssh_bruteforce_suspected"
        }

    # No alert needed
    return None
