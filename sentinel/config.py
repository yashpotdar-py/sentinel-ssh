import yaml
import logging
from pathlib import Path
from typing import Dict, Any

# Configure module-level logger
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent.parent / "config" / "sentinel.yaml"


def load_config() -> Dict[str, Any]:
    """
    Load the application configuration from the YAML file.

    This function locates the 'sentinel.yaml' file relative to the project structure
    and parses it.

    Returns:
        Dict[str, Any]: The configuration dictionary.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        yaml.YAMLError: If the config file is invalid.
    """
    try:
        logger.debug(f"Loading configuration from {CONFIG_PATH}")
        with open(CONFIG_PATH) as f:
            config = yaml.safe_load(f)
            logger.info("Configuration loaded successfully.")
            return config
    except FileNotFoundError:
        logger.critical(f"Configuration file not found at {CONFIG_PATH}")
        raise
    except yaml.YAMLError as e:
        logger.critical(f"Failed to parse configuration file: {e}")
        raise
