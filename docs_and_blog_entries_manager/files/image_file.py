import base64

from files.value.file_path import FilePath


def read_b64(picture_file_path: FilePath) -> str:
    with open(picture_file_path.value, 'rb') as f:
        pic_data: bytes = f.read()
    return base64.b64encode(pic_data).decode('utf-8')


def encode_base64(image_data: bytes) -> str:
    return base64.b64encode(image_data).decode('utf-8')


def write(file_path: FilePath, image_data: bytes):
    with open(file_path.value, "wb") as f:
        f.write(image_data)
