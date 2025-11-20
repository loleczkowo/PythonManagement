from service import Service, VenvSpec
from pathlib import Path
from .registry import register


project_dir = Path(r"D:\Szymon\OneDrive\programy_2025\OldPCMessages")
oldpcmessages_venv = VenvSpec("oldpcmessages", project_dir/"requirements.txt")


register(Service(
    "notifications_popup",
    project_dir,
    "NOTIFICATIONS.py",
    oldpcmessages_venv,
))

register(Service(
    "discord_notifications_popup",
    project_dir / "discord_notifications",
    "main.py",
    oldpcmessages_venv,
))

register(Service(
    "sys_info_popup",
    project_dir,
    "SYS_INFO.py",
    oldpcmessages_venv,
))
