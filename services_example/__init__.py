from core.logs import log, QINFO

from . import basic_service
from . import multiple_services
from . import machine_specific

from .registry import services

services_names = "\n".join([service.name for service in services])
log(QINFO, f"Current services: \n{services_names}")

__all__ = [
    "services", "basic_service", "multiple_services", "machine_specific"
]
