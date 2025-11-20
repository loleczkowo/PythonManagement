import os
import subprocess
import threading
from pathlib import Path
from globals import Globals as G
from service import Service
from .logs import service_log, log, ERROR, WARNING, QINFO


def reader(pipe, service: Service):
    for raw in iter(pipe.readline, b''):
        line = raw.decode('utf-8', errors='replace').rstrip('\r\n')
        service_log(service, line)
    pipe.close()


def run_script(
    service: Service,
    python_path: Path,
    project_path: Path,
    entry: str,
    args: list = None,
    env_varibles: dict = None
):
    if args is None:
        args = []
    if entry.endswith(".py"):
        cmd = [str(python_path), "-u",
               str((project_path/entry).resolve()), *args]
    else:
        cmd = [str(python_path), "-u", "-m", entry, *args]
    env = dict(os.environ)
    if env_varibles:
        env.update(env_varibles)

    service_log(service, "--- SERVICE AUTO STARTUP MESSAGE ---")
    NO_WINDOW = 0x08000000
    proc = subprocess.Popen(
        cmd,
        cwd=str(project_path),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
        close_fds=True,
        creationflags=NO_WINDOW
    )
    threading.Thread(
        target=reader,
        args=(proc.stdout, service),
        daemon=True
    ).start()
    threading.Thread(
        target=reader,
        args=(proc.stderr, service),
        daemon=True
    ).start()
    G.service_status[service.name].status = proc
    proc.wait()
    G.service_status[service.name].status = False


def run_service(service: Service):
    if service.entry.endswith(".py"):
        file_path = service.cwd / service.entry
        if not file_path.is_file():
            log(ERROR, f"{file_path} from {service.name} does not exist")
            G.service_status[service.name].status = False
            return False
    t = threading.Thread(
        target=run_script, args=(
            service, service.venv.python_exe(), service.cwd,
            service.entry, service.args, service.env,
        ), daemon=True
    )
    t.start()
    return t


def stop_service(service: Service):
    status = G.service_status[service.name].status
    if not isinstance(status, subprocess.Popen):
        return False
    log(QINFO, f"shutting down {service.name}")
    status.terminate()
    return True


def close_all():
    for name, service_status in G.service_status.items():
        status = service_status.status
        if status is None:
            log(WARNING, f"cannot shutdown {name} because its starting")
            continue  # starting?
        if status is False:
            continue  # already dead
        if not isinstance(status, subprocess.Popen):
            continue  # something else
        # running
        log(QINFO, f"shutting down {name}")
        status.terminate()
        service_status.status = None
