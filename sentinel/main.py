import logging
import sys
from sentinel.ingest import stream_ssh_logs
from sentinel.parser import parse_ssh_log
from sentinel.detector import process_event
from sentinel.responder import block_ip, unblock_expired
from sentinel.config import load_config
from sentinel.banner import BANNER

# Configure basic logging for the entire application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

print(BANNER, flush=True)


def main():
    """
    Main entry point for the Sentinel-SSH service.

    Orchestrates the log streaming, parsing, detection, and response loop.
    It loads configuration, sets up the block/allow lists, and enters an infinite loop
    processing SSH logs from systemd.
    """
    try:
        config = load_config()
    except Exception as e:
        logger.critical(f"Failed to load config: {e}")
        sys.exit(1)

    allowlist = config.get("allowlist", [])
    
    # Get block duration, default to 300 seconds (5 minutes) if not set
    block_duration = config.get("ssh", {}).get("block_duration_seconds", 300)
    
    logger.info("Sentinel-SSH starting up...")
    logger.info(f"Block duration: {block_duration}s")
    logger.info(f"Allowlist: {allowlist}")

    try:
        for line in stream_ssh_logs():
            event = parse_ssh_log(line)
            if not event:
                continue

            alert = process_event(event)
            if alert:
                block_ip(alert["ip"], block_duration, allowlist)

            unblock_expired()
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
