# SSH responder: block suspicious IPs using UFW firewall
import subprocess  # To run system commands like ufw
import time  # For timestamps and expiration
import ipaddress  # For IP/network validation
from typing import List  # Type hint for lists

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
        return

    if ip_in_allowlist(ip, allowlist):  # Skip allowed IPs
        return

    # Add UFW deny rule for SSH (port 22)
    subprocess.run(["ufw", "deny", "from", ip, "to", "any", "port", "22"], check=True)

    # Record expiration time
    blocked_ips[ip] = time.time() + duration


def unblock_expired():
    """
    Remove expired blocks from UFW and the tracking dict.
    """
    now = time.time()
    # Find expired IPs
    expired = [ip for ip, until in blocked_ips.items() if until < now]

    for ip in expired:
        # Remove UFW rule
        subprocess.run(
            ["ufw", "delete", "deny", "from", ip, "to", "any", "port", "22"], check=True
        )
        # Remove from tracking
        del blocked_ips[ip]
