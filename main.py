import shutil
import atexit
import socketserver
from api.http import WebServer
from service import ServiceStatus
from services import services
from core.logs import log, INFO, QINFO, ERROR
from core.venv_utils import venv_check
from core.service_utils import run_service, close_all
from config import SERVICE_LOG_DIR, API_PORT
from globals import Globals as G

# main system;

# startup;

# venv check
# for service in services:
#   if old fingerprint: del venv
#   if no vevn: create venv

# main start
# for service in services:
#   if no logs and logs dir; del logs dir
#   if logs and no logs dir; create logs dir
#   run service

# main loop;
# for service in services:
#   if service == crash: notify user
#   allow user to stop/restart/start services somehow

log(INFO, "----- script is starting -----")
atexit.register(close_all)

log(INFO, "-- venv check on all services")
for service in services:
    log(QINFO, f"checking venv from service {service.name}")
    venv_check(service)
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
            log(ERROR, f"error while removing log dir for {service.name}\n{e}")
    log(QINFO, f"starting {service.name}")
    G.service_status[service.name] = ServiceStatus(service, None)
    run_service(service)


log(INFO, "-- running the main loop")
with socketserver.TCPServer(("127.0.0.1", API_PORT), WebServer) as httpd:
    httpd.serve_forever()
log(INFO, "-- closing all services")
close_all()
log(INFO, "-- goodbye")
