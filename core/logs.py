from dataclasses import dataclass
import datetime
from config import (LOG_DIR, LOG_RETENTION_DAYS,
                    SERVICE_LOG_DIR, SERVICE_LOG_RETENTION_DAYS,
                    IGNORE_API_LOGS)
from service import Service


@dataclass
class LogType:
    name: str


QINFO = LogType("Qinfo")  # quiet-log.
INFO = LogType("INFO")
WARNING = LogType("WARNING")
ERROR = LogType("ERROR")
CRITICAL = LogType("CRITICAL")
SUCCESS = LogType("SUCCESS")

_TYPE_WIDTH = max(len(t.name) for t in [
    INFO, WARNING, ERROR, CRITICAL, SUCCESS
    ])
_SPACE_PAD = " " * _TYPE_WIDTH

LOG_DIR.mkdir(parents=True, exist_ok=True)


def _plain_log(log_text: str, to_file: bool = True):
    print(log_text)
    if not to_file:
        return
    today = datetime.date.today().isoformat()
    log_file = LOG_DIR / f"{today}.log"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(log_text + "\n")
    cutoff = datetime.datetime.now() - datetime.timedelta(
        days=LOG_RETENTION_DAYS)
    for path in LOG_DIR.glob("*.log"):
        try:
            date_str = path.stem
            file_date = datetime.datetime.fromisoformat(date_str)
        except Exception:
            continue
        if file_date < cutoff:
            path.unlink()


def get_logs(last: int):
    today = datetime.date.today().isoformat()
    log_file = LOG_DIR / f"{today}.log"
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[-int(last):]


def log(log_type: LogType, message: str, to_file: bool = True, is_api=False):
    if is_api and IGNORE_API_LOGS:
        return
    lines = message.split("\n")
    header = f"{log_type.name.ljust(_TYPE_WIDTH)} || {lines[0]}"

    if len(lines) > 1:
        ind = f"{_SPACE_PAD}  | "
        body = "\n".join(f"{ind}{lins}" for lins in lines[1:])
        _plain_log(f"{header}\n{body}", to_file)
    else:
        _plain_log(header, to_file)


def service_log(service: Service, log_message: str):
    if not service.log_output:
        return
    today = datetime.date.today().isoformat()
    service_log_dir = SERVICE_LOG_DIR / service.name
    log_file = service_log_dir / f"{today}.log"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(log_message + "\n")

    cutoff = datetime.datetime.now() - datetime.timedelta(
        days=SERVICE_LOG_RETENTION_DAYS)
    for path in service_log_dir.glob("*.log"):
        try:
            date_str = path.stem
            file_date = datetime.datetime.fromisoformat(date_str)
        except Exception:
            continue
        if file_date < cutoff:
            path.unlink()


def get_service_logs(service_name: str, last: int):
    today = datetime.date.today().isoformat()
    service_log_dir = SERVICE_LOG_DIR / service_name
    log_file = service_log_dir / f"{today}.log"
    if not log_file.exists():
        return
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[-int(last):]
