# sentinel/parser.py

"""
Log parsing logic.
Extracts structured events (login success, failure, invalid user) from raw log lines.
"""

# SSH log parser: extract structured events from log lines
import re  # For regular expressions
import logging
from typing import Optional, Dict  # For type hints

logger = logging.getLogger(__name__)

# Regex for failed password attempts (may include 'invalid user')
FAILED_PASSWORD = re.compile(
    r"Failed password for (invalid user )?(?P<user>\S+) from (?P<ip>\S+)"
)

# Regex for successful publickey authentication
ACCEPTED_PUBLICKEY = re.compile(
    r"Accepted publickey for (?P<user>\S+) from (?P<ip>\S+)"
)

# Regex for invalid user attempts
INVALID_USER = re.compile(r"Invalid user (?P<user>\S+) from (?P<ip>\S+)")


def parse_ssh_log(line: str) -> Optional[Dict]:
    """
    Parse a single SSH log line into a structured event dict.

    Args:
        line (str): A single line from the SSH log.

    Returns:
        dict: Structured event info (event type, username, ip, raw line), or None if not matched.
    """
    # Only process lines related to sshd
    if "sshd" not in line:
        return None

    # Check for successful publickey authentication
    if match := ACCEPTED_PUBLICKEY.search(line):
        logger.debug("Computed auth_success for %s", match.group('user'))
        return {
            "event": "auth_success",  # Successful login
            "username": match.group("user"),
            "ip": match.group("ip"),
            "raw": line,  # Original log line
        }

    # Check for failed password attempt
    if match := FAILED_PASSWORD.search(line):
        logger.debug(
            "Computed auth_failed for %s from %s",
            match.group('user'), match.group('ip')
        )
        return {
            "event": "auth_failed",  # Failed login
            "username": match.group("user"),
            "ip": match.group("ip"),
            "raw": line,
        }

    # Check for invalid user attempt
    if match := INVALID_USER.search(line):
        logger.debug(
            "Computed invalid_user for %s from %s",
            match.group('user'), match.group('ip')
        )
        return {
            "event": "invalid_user",  # Login attempt for non-existent user
            "username": match.group("user"),
            "ip": match.group("ip"),
            "raw": line,
        }

    # Not a relevant SSH event
    return None
