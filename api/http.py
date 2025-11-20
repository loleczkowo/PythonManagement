import json
import os
from http.server import BaseHTTPRequestHandler
import threading
from urllib.parse import urlparse
from globals import Globals as G
from core.service_utils import run_service, stop_service
from subprocess import Popen
from core.logs import log, INFO, get_logs, get_service_logs
from config import WEB_UI_DIR


class WebServer(BaseHTTPRequestHandler):
    def _send(self, data, status=200, log_data=True):
        if log_data:
            log(INFO, f"RESPONSE::{status};\n{data}", is_api=True)
        else:
            log(INFO, f"RESPONSE::{status}", is_api=True)
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path):
        if not os.path.isfile(path):
            self.send_error(404)
            return
        path = str(path)
        log(INFO, f"FILESEND::{path}", is_api=True)
        if path.endswith(".html"):
            mime = "text/html"
        elif path.endswith(".js"):
            mime = "application/javascript"
        elif path.endswith(".css"):
            mime = "text/css"
        else:
            mime = "application/octet-stream"
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        log(INFO, f"GET::{parsed.path}", is_api=True)
        # UI
        path = parsed.path
        if path.startswith("/api/"):
            self._handle_api_get(path)
            return
        if path.endswith("/"):
            self._send_file(WEB_UI_DIR / path.lstrip("/") / "index.html")
            return
        self._send_file(WEB_UI_DIR / path.lstrip("/"))

    def _handle_api_get(self, path: str):
        parsed = urlparse(path)
        parts = parsed.path.split("/")
        if parsed.path == "/api/health":
            self._send({"ok": True})
            return

        if parsed.path == "/api/status":
            data = {}
            for name, servicestatus in G.service_status.items():
                status = servicestatus.status
                if status is None:
                    data[name] = True
                elif status is False:
                    data[name] = False
                elif isinstance(status, Popen):
                    data[name] = True
            self._send(data)
            return

        if parsed.path == "/api/logs":
            # last 100 logs
            self._send({"lines": get_logs(100)}, log_data=False)
            return

        if parts[:3] == ["", "api", "service_logs"] and len(parts) == 4:
            # last 100 service logs
            lines = get_service_logs(parts[3], 100)
            if not lines:
                self._send({"error": "log_not_found"}, 404)
            self._send({"lines": lines},
                       log_data=False)
            return

        self._send({"error": "not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        log(INFO, f"POST::{parsed.path}", is_api=True)
        parts = parsed.path.split("/")

        if parsed.path == "/api/shutdown":
            log(INFO, "SHUTDOWN")
            self._send({"ok": "shutdown"})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return

        if parts[:3] == ["", "api", "start"] and len(parts) == 4:
            if parts[3] not in G.service_status:
                self._send({"error": "service_not_found"}, 404)
                return
            if not G.service_status[parts[3]].status is False:
                self._send({"status": "already_running"})
                return
            result = run_service(G.service_status[parts[3]].service)
            if result is False:
                self._send({"status": "start_failed"}, 500)
                return
            self._send({"status": "started"})
            return

        if parts[:3] == ["", "api", "stop"] and len(parts) == 4:
            if parts[3] not in G.service_status:
                self._send({"error": "service_not_found"}, 404)
                return
            if G.service_status[parts[3]].status is False:
                self._send({"status": "already_stopped"})
                return
            stop_service(G.service_status[parts[3]].service)
            self._send({"status": "stopped"})
            return

        self._send({"error": "not found"}, 404)

    def log_message(self, format, *args):
        pass
