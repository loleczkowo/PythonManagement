import pathlib


def pc_id():
    p = pathlib.Path.home() / '.pc'
    if not p.exists():
        return None
    return p.read_text().strip()
