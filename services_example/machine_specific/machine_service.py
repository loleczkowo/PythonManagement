from pathlib import Path
from service import Service, VenvSpec

root = Path("path/to/machine_specific_project")

machine_service = Service(
    "example_machine_service",
    root,
    "main.py",
    VenvSpec("example_machine_env", root / "requirements.txt")
)
