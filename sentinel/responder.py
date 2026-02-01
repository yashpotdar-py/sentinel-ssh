# SSH responder: block suspicious IPs using UFW firewall
import subprocess  # To run system commands like ufw
import time  # For timestamps and expiration
import ipaddress  # For IP/network validation
import logging
from typing import List  # Type hint for lists

from sentinel.ui import red, green

logger = logging.getLogger(__name__)

# Global dict: IP -> expiration timestamp
blocked_ips = {}


def ip_in_allowlist(ip: str, allowlist: List[str]) -> bool:
    """
    Check if an IP is in the allowlist (supports CIDR notation).

    Args:
        ip (str): IP address to check.
        allowlist (List[str]): List of allowed IPs/networks.

    Returns:
        bool: True if IP is allowed, False otherwise.
    """
    ip_obj = ipaddress.ip_address(ip)  # Parse IP
    for entry in allowlist:
        net = ipaddress.ip_network(entry, strict=False)  # Parse network
        if ip_obj in net:
            return True
    return False


def block_ip(ip: str, duration: int, allowlist: List[str]):
    """
    Block an IP using UFW if not already blocked and not in allowlist.

    Args:
        ip (str): IP to block.
        duration (int): Block duration in seconds.
        allowlist (List[str]): IPs/networks to never block.
    """
    if ip in blocked_ips:  # Already blocked
        logger.debug(f"Skipping block for {ip} (already blocked)")
        return

    if ip_in_allowlist(ip, allowlist):  # Skip allowed IPs
        logger.warning(f"Skipping block for {ip} (in allowlist)")
        return

    # Add UFW deny rule for SSH (port 22)
    logger.info(f"Blocking {ip} for {duration} seconds via UFW")
    try:
        subprocess.run(["ufw", "deny", "from", ip, "to", "any", "port", "22"], check=True)
        # Record expiration time
        blocked_ips[ip] = time.time() + duration
        print(red(f"[BLOCK] SSH brute-force detected from {ip}"), flush=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to execute UFW command: {e}")


def unblock_expired():
    """
    Remove expired blocks from UFW and the tracking dict.
    """
    now = time.time()
    # Find expired IPs
    expired = [ip for ip, until in blocked_ips.items() if until < now]

    for ip in expired:
        # Remove UFW rule
        logger.info(f"Unblocking {ip} (expired)")
        try:
            subprocess.run(
                ["ufw", "delete", "deny", "from", ip, "to", "any", "port", "22"], check=True
            )
            # Remove from tracking
            del blocked_ips[ip]
            print(green(f"[UNBLOCK] Cooldown expired for {ip}"), flush=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to remove UFW rule for {ip}: {e}")

