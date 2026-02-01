import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config" / "sentinel.yaml"


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)
