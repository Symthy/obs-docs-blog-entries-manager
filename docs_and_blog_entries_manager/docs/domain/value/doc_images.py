from .doc_image import DocImage


class DocImages:
    def __init__(self, images: list[DocImage]):
        self.__images = images

    @property
    def items(self) -> list[DocImage]:
        return self.__images
