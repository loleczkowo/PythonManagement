import subprocess
import shutil
from globals import Globals as G
from core.service_utils import run_service
from config import SERVICE_LOG_DIR
from core.venv_utils import venv_check
from service import ServiceStatus
from services import services
from core.logs import log, INFO, QINFO, ERROR, WARNING


def check_all():
    log(INFO, "-- venv check on all services")
    for service in services:
        log(QINFO, f"checking venv from service {service.name}")
        venv_check(service)


def start_all():
    log(INFO, "-- starting all services")
    for service in services:
        log_path = SERVICE_LOG_DIR / service.name
        if service.log_output:
            if not log_path.is_dir():
                log(INFO, f"creating log dir for {service.name}")
                log_path.mkdir(parents=True)
        else:
            try:
                if log_path.is_dir():
                    log(INFO, f"removing log dir for {service.name}")
                    shutil.rmtree(log_path)
            except Exception as e:
                log(ERROR,
                    f"error while removing log dir for {service.name}\n{e}")
        log(QINFO, f"starting {service.name}")
        G.service_status[service.name] = ServiceStatus(service, None)
        run_service(service)


def close_all():
    log(INFO, "-- closing all services")
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
