import os
from typing import Optional

async def akademic_get_file_path(file_name: str, base_dir: Optional[str] = None) -> Optional[str]:
    if base_dir is None:
        base_dir = os.path.dirname(__file__)
    for root, dirs, files in os.walk(base_dir):
        if file_name in files:
            return os.path.join(root, file_name)
    return None