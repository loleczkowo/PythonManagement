from service import Service, VenvSpec
from pathlib import Path
from .registry import register


background_venv = VenvSpec(
    "fun_background",
    Path(r"D:\Szymon\OneDrive\programy_2025\fun_background\requirements.txt")
)


register(
    Service(
        "fun_background",
        Path(r"D:\Szymon\OneDrive\programy_2025\fun_background"),
        "fuckpolish.py",
        background_venv,
        log_output=False  # there is no output
    )
)
