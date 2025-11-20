from service import Service, VenvSpec
from pathlib import Path

path = Path(r"D:\Szymon\OneDrive\Python\show_status_raspberrypipico")

service_status_raspberrypipico = Service(
    "KoKpc_status_raspberrypipico",
    path,
    "main.py",
    VenvSpec("KoKpc_status_raspberrypipico", path/"requirements.txt")
)
