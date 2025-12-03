from pathlib import Path
from service import Service, VenvSpec
from .registry import register

app_dir = Path("path/to/application")

venv = VenvSpec(
    "application_env",
    app_dir / "requirements.txt"
)

register(Service(
    "app_worker",
    app_dir / "worker",
    "worker.py",
    venv,
))

register(Service(
    "app_api",
    app_dir / "api",
    "api.py",
    venv,
))

register(Service(
    "app_scheduler",
    app_dir / "scheduler",
    "scheduler.py",
    venv,
))
