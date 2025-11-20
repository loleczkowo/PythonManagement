import hashlib
import subprocess
import sys
import json
import shutil
from .logs import log, INFO, QINFO, SUCCESS
from service import Service


def _fingerprint(service: Service):
    venv = service.venv
    python_exe = venv.python_exe()
    h = hashlib.sha256()
    h.update(str(python_exe).encode("utf-8"))
    req = venv.requirements
    if req:
        req_path = req if req.is_absolute() else (service.cwd / req)
        if req_path.is_file():
            h.update(req_path.read_bytes())
        elif req_path.is_dir():
            for p in sorted(req_path.rglob("*")):
                if p.is_file():
                    h.update(p.read_bytes())
    return h.hexdigest()


def _install_requirements(service: Service):
    req = service.venv.requirements
    if not req:
        return
    if not req.exists():
        return
    log(QINFO, f" | installing requirements from {str(req)}")
    python = service.venv.python_exe()

    subprocess.call(
        [str(python), "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call(
        [str(python), "-m", "pip", "install", "-r", str(req)])


def venv_check(service: Service):
    venv = service.venv
    vdir = venv.resolve_dir()
    fingerprint_file = vdir / venv.fingerprint_name

    new_fingerprint = {"hash": _fingerprint(service)}

    old_fingerprint = None
    if fingerprint_file.exists():
        try:
            old_fingerprint = json.loads(
                fingerprint_file.read_text(encoding="utf-8"))
        except Exception:
            old_fingerprint = None

    needs_rebuild = not vdir.exists() or old_fingerprint != new_fingerprint

    if needs_rebuild:
        log(INFO, f"building venv `{venv.name}`")
        if vdir.exists():
            log(QINFO, " | deleting old venv")
            shutil.rmtree(vdir)
            log(QINFO, " | building new venv")

        base = str(venv.base_python or sys.executable)
        subprocess.check_call([base, "-m", "venv", str(vdir)])
        _install_requirements(service)
        log(QINFO, f" | building new fingerprint at {str(fingerprint_file)}")
        fingerprint_file.parent.mkdir(parents=True, exist_ok=True)
        fingerprint_file.write_text(
            json.dumps(new_fingerprint, indent=2), encoding="utf-8")

        log(SUCCESS, f" \\ venv built: {vdir}")
    else:
        log(INFO, f"venv {venv.name} up-to-date")
