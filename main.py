import atexit
import socketserver
from api.http import WebServer
from core.logs import log, INFO
from core.console_input import ConsoleInput
from config import API_PORT
from main_functions import check_all, start_all, close_all

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
check_all()
start_all()
log(INFO, "-- running the main loop")
log(INFO, "- ConsoleInput thread start")
console_input = ConsoleInput()
console_input.start_thread()

with socketserver.TCPServer(("127.0.0.1", API_PORT), WebServer) as httpd:
    httpd.serve_forever()

close_all()
console_input.running = False
log(INFO, "-- goodbye")
