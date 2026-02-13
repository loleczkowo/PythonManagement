from pathlib import Path
from core.utils import get_app_data_dir

DIR = Path(__file__).parent
APP_DATA_DIR = get_app_data_dir() / "PythonManagement"

VENVS_DIR = APP_DATA_DIR / "venvs"

LOG_RETENTION_DAYS = 3
LOG_DIR = APP_DATA_DIR / "logs"
LOG_TO_CONSOLE = True
IGNORE_API_LOGS = True  # ussaly they spam the whole logs, use for debug

SERVICE_LOG_RETENTION_DAYS = 3
SERVICE_LOG_DIR = APP_DATA_DIR / "service_logs"

API_PORT = 52481
WEB_UI_DIR = DIR / "ui"
