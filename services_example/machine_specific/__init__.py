from core.utils import pc_id
from ..registry import register
from .machine_service import machine_service
from core.logs import log, QINFO

if pc_id() == "ExampleMachine":
    log(QINFO, "Using example machine-specific services")
    register(machine_service)
