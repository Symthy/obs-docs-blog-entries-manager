def get_file_name(file_path: str) -> str:
    return file_path.rsplit('/', 1)[1]
