import os
from pathlib import Path


def pc_id():
    p = Path.home() / '.pc'
    if not p.exists():
        return None
    return p.read_text().strip()


def get_app_data_dir():
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA")
        if not base:
            base = Path.home() / "AppData" / "Local"
    else:
        base = os.environ.get("XDG_DATA_HOME")
        if not base:
            base = Path.home() / ".local" / "share"
    return Path(base)


APP_DATA_DIR = get_app_data_dir()
