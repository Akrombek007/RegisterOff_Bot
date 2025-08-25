from file_service.hemis_file import hemis_file_path_


async def main():
    path = await hemis_file_path_("hemis_info")
    print(path)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())