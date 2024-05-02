import base64


def read_b64(picture_file_path: str) -> str:
    with open(picture_file_path, 'rb') as f:
        pic_data = f.read()
    return base64.b64encode(pic_data).decode('utf-8')
