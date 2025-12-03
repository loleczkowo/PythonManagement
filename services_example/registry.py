from service import Service

services: list[Service] = []


def register(service):
    services.append(service)
