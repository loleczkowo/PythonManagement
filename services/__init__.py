from core.logs import log, QINFO
from . import background
from . import oldpcmessages
from . import KingOfKingsPC
from .registry import services

services_names = "\n".join([service.name for service in services])
log(QINFO, f"Current services: \n{services_names}")
__all__ = [
    "services",
    "background", "oldpcmessages",
    "KingOfKingsPC"]
