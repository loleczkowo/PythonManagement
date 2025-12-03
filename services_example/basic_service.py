from pathlib import Path
from service import Service, VenvSpec
from .registry import register

project_dir = Path("path/to/example_project")

venv = VenvSpec(
    "example_env",
    project_dir / "requirements.txt"
)

example_service = Service(
    "example_service",
    project_dir,
    "main.py",
    venv,
)

register(example_service)
