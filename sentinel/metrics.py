import threading

_lock = threading.Lock()

_counters = {
    "ssh_failed_attempts_total": 0,
    "unique_attacker_ips_total": 0,
    "bans_total": 0,
}

_gauges = {
    "sentinel_up": 0,
    "active_bans": 0,
    "last_ban_timestamp": 0,
}


def inc_counter(name: str, value: int = 1) -> None:
    with _lock:
        if name not in _counters:
            raise KeyError(f"Unknown counter: {name}")
        _counters[name] += value


def set_gauge(name: str, value: int) -> None:
    with _lock:
        if name not in _gauges:
            raise KeyError(f"Unknown gauge: {name}")
        _gauges[name] = value


def get_snapshot() -> dict:
    with _lock:
        return {
            **_counters,
            **_gauges,
        }


def render() -> str:
    snapshot = get_snapshot()
    lines = []

    for key, value in snapshot.items():
        lines.append(f"{key} {value}")

    return "\n".join(lines) + "\n"
