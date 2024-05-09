from typing import List

from domain.blogs.entity.photo.photo_entries import PhotoEntries
from domain.docs.entity.image.doc_image import DocImage
from infrastructure.hatena.image.image_downloader import ImageDownLoader


class PhotoEntriesToDocImagesConverter:
    def __init__(self, image_downloader: ImageDownLoader):
        self.__image_downloader = image_downloader

    def execute(self, photo_entries: PhotoEntries, doc_entry_dir_path):
        doc_images: List[DocImage] = []
        for blog_image in photo_entries.items:
            image_data: bytes = self.__image_downloader.run(blog_image.image_url)
            doc_image = DocImage(doc_entry_dir_path, blog_image.image_filename, image_data)
            doc_images.append(doc_image)
        return doc_images
