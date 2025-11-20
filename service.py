from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union
from config import VENVS_DIR
from subprocess import Popen


@dataclass(frozen=True)
class VenvSpec:
    # If 'dir' is set -> explicit mode; if None -> auto mode.
    name: str
    requirements: Path = None
    dir: Optional[Path] = None
    base_python: Optional[Path] = None
    fingerprint_name: str = ".venv_fingerprint.json"

    def is_explicit(self):
        return self.dir is not None

    def resolve_dir(self) -> Path:
        # Explicit: <dir>/<name>
        # Auto: %LOCALAPPDATA%/PythonManagement/venvs/<name>
        if self.is_explicit():
            return (self.dir / self.name).resolve()  # type: ignore[union-attr]
        return VENVS_DIR / self.name

    def python_exe(self) -> Path:
        vdir = self.resolve_dir()
        return vdir / "Scripts" / "python.exe"


@dataclass(frozen=True)
class Service:
    name: str
    cwd: Path
    entry: str                      # "main.py" or "pkg.module:main"
    venv: VenvSpec
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    log_output: bool = True  # logs output to file


@dataclass()
class ServiceStatus:
    service: Service
    status: Optional[Union[bool, Popen]] = None
    # None  = not started
    # False = crash
    # proc  = running processor
