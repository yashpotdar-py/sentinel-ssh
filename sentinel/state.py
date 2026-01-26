# Track SSH events per IP within a time window
import time  # For timestamps
from collections import defaultdict, deque  # For efficient IP tracking


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

    def record(self, ip: str) -> int:
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
        while dq and now - dq[0] > self.window:
            dq.popleft()

        return len(dq)  # Return count of events in window
