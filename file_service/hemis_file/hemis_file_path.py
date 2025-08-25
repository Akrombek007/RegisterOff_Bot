from os.path import join, dirname
from os import listdir


BASE_DIR = dirname(__file__)

async def hemis_file_path_(folder_name: str):
    folder_path = join(BASE_DIR, folder_name)
    return sorted([
        join(folder_path, f)
        for f in listdir(folder_path)
        if f.endswith(".png")
    ])