from pathlib import Path
import os

DIR = Path(__file__).parent
local = os.environ["LOCALAPPDATA"] or str(Path.home() / "AppData" / "Local")
APP_DATA_DIR = Path(local) / "PythonManagement"

VENVS_DIR = APP_DATA_DIR / "venvs"

LOG_RETENTION_DAYS = 3
LOG_DIR = APP_DATA_DIR / "logs"
IGNORE_API_LOGS = True  # ussaly they spam the whole logs, use for debug

SERVICE_LOG_RETENTION_DAYS = 3
SERVICE_LOG_DIR = APP_DATA_DIR / "service_logs"

API_PORT = 52481
WEB_UI_DIR = DIR / "ui"
