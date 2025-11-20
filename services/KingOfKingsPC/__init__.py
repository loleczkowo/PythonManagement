from core.utils import pc_id
from core.logs import log, QINFO
from ..registry import register
from .status_raspberrypipico import service_status_raspberrypipico


if pc_id() == "KoKpc":
    log(QINFO, "Detected PC `King of Kings PC` including its services")
    register(service_status_raspberrypipico)
