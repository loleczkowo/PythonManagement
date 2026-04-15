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

def read_env_file(path: Path):
    env = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip("'\"")
    return env

APP_DATA_DIR = get_app_data_dir()
