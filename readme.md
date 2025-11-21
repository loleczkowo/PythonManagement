# NOTE
**This is mostly a private project. Therefore many configs were set to me  
You can edit this as much as you want.**  
This project is a "python service manager", It auto generates needed venv's and starts apps.  
It also host a small interface *(if you know how to use js or html please clean up the shitty AI code)*  
Almost all of this code is written by hand. AI was **ONLY** used for everything in `ui/`, elsewere it was only used as a reshearch tool.

## ADD NEW SERVICE:
1. add a new file to `services/`
2. in the file define the `VenvSpec` and `Service`
3. use `register(your_service)` on your service
4. to `__init__.py` add `from * import your_file.py`
## default config
- logs in `%localappdata%/PythonManagement/logs`
- IGNORE_API_LOGS (ignores logs from API and WEB reccomended for debug) `TRUE`
- service logs in `%localappdata%/PythonManagement/service_logs/servicename`
- service venvs in `%localappdata%/PythonManagement/venvs/venvname`
- api port `52481`
- web ui path is `Appdir/ui/`
## how to use
Use `start_python_managment.bat` to run the program.  
When venvs break use `delete_all_venvs.bat` to reinstall all venvs

### API Endpoints
| HTTP Verbs | Endpoints | Action |
|---|---|---|
| GET        | /api/status   | Get running/stopped state of all services        |
| GET        | /api/logs   | Get last 100 global log lines                    |
| GET        | /api/service_logs/{name}  | Get last 100 log lines for a specific service  |
| POST       | /api/start/{name}  | Start a service         |
| POST       | /api/stop/{name}    | Stop a service                |
| POST       | /api/shutdown | Shutdowns the script manager

```json
GET /api/status
Returns:
{ [ "service": true|false ], ...}
```

```json
GET /api/logs
Returns:
{ "lines": [...] }
```

```json
GET /api/service_logs/{name}
Returns:
{ "lines": [...] }
Errors:
{ "error": "log_not_found" } (404)
```

```json
POST /api/start/{name}
Returns:
{ "status": "started" }
{ "status": "already_running" }
Errors:
{ "error": "service_not_found" } (404)
{ "status": "start_failed" } (500)
```

```json
POST /api/stop/{name}
Returns:
{ "status": "stopped" }
{ "status": "already_stopped" }
Errors:
{ "error": "service_not_found" } (404)
```

```json
POST /api/shutdown
Returns:
{ "ok": "shutdown" }
```

---
*-App made by loleczkowo*  