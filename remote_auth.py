import time
import sys
import requests

CONTROL_URL = "https://raw.githubusercontent.com/Harsh7065/Linkharvest-releases/main/control.json"
TIMEOUT = 5
FAIL_CLOSED = False  # True = block the app if the check itself fails


def _parse_version(v: str):
    cleaned = (v or "").lstrip("vV").strip()
    parts = []
    for p in cleaned.split("."):
        digits = "".join(c for c in p if c.isdigit())
        parts.append(int(digits) if digits else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def check_authorization(current_version: str):
    """
    Returns (allowed: bool, message: str | None).
    Call this once at startup, before the main window is built.
    """
    try:
        bust = int(time.time())
        url = f"{CONTROL_URL}?_={bust}"
        
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        
        resp = requests.get(url, timeout=TIMEOUT, headers=headers)
        if resp.status_code != 200:
            return (not FAIL_CLOSED, None)

        data = resp.json()

        # Flexible boolean check (handles both boolean False and string "false")
        active_val = data.get("active", True)
        if isinstance(active_val, str):
            active_val = active_val.lower() not in ("false", "0", "no", "off")

        if not bool(active_val):
            return (False, data.get("message", "This app is no longer available."))

        min_version = str(data.get("min_version", ""))
        if min_version and _parse_version(current_version) < _parse_version(min_version):
            return (False, data.get(
                "message",
                f"A required update (v{min_version}+) is available. Please download the latest version."
            ))

        return (True, None)

    except (requests.RequestException, ValueError, KeyError):
        return (not FAIL_CLOSED, None)
