from service import ServiceStatus


class Globals:
    service_status: dict[str, ServiceStatus] = {}
    stop_logging_to_console: bool = False
