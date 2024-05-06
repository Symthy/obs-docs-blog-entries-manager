from typing import List

from domain.docs.entity.image.doc_image import DocImage


class DocImages:
    def __init__(self, images: List[DocImage]):
        self.__images = images

    @property
    def items(self) -> List[DocImage]:
        return self.__images
