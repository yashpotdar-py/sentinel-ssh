# sentinel/state.py

"""
Event state tracking.
Keeps track of events per IP within a sliding time window.
"""

import time  # For timestamps
import logging
from collections import defaultdict, deque  # For efficient IP tracking

logger = logging.getLogger(__name__)

class EventState:
    """
    Tracks the number of events (e.g., failed logins) per IP address within a sliding time window.
    Uses a deque to maintain timestamps and automatically expire old ones.
    """

    def __init__(self, window_seconds: int = 60):
        """
        Initialize the event state tracker.

        Args:
            window_seconds (int): Time window in seconds to track events (default 60).
        """
        self.window = window_seconds  # Sliding window duration
        self.events = defaultdict(deque)  # IP -> deque of timestamps
        logger.debug("Initialized EventState with window=%ss", window_seconds)

    def get_count(self, ip: str) -> int:
        """Return the current count for an IP without modifying state."""
        return len(self.events[ip])
        """
        Record a new event for the given IP and return the current count in the window.

        Args:
            ip (str): The IP address to record the event for.

        Returns:
            int: Number of events for this IP in the current window.
        """
        now = time.time()  # Current timestamp
        dq = self.events[ip]  # Get or create deque for this IP
        dq.append(now)  # Add new timestamp

        # Remove timestamps older than the window
        cleaned = 0
        while dq and now - dq[0] > self.window:
            dq.popleft()
            cleaned += 1

        if cleaned > 0:
            logger.debug("Expired %d old events for %s", cleaned, ip)

        count = len(dq)
        logger.debug("Recorded event for %s. Count in window: %d", ip, count)
        return count  # Return count of events in window

    def get_count(self, ip: str) -> int:
        """Return the current count for an IP without modifying state."""
        return len(self.events[ip])
