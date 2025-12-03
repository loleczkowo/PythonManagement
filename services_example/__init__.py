from .registry import services

from . import basic_service
from . import multiple_services
from . import machine_specific

__all__ = [
    "services", "basic_service", "multiple_services", "machine_specific"
]
