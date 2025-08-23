from os.path import join, dirname


async def hemis_file_path_(name: str):
    return join(dirname(__file__), name)