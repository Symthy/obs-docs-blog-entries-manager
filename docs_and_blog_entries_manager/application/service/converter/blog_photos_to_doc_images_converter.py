from domain.blogs.entity.photo.photo_entries import PhotoEntries
from domain.blogs.entity.photo.photo_entry import PhotoEntry
from domain.docs.entity.image.doc_image import DocImage
from infrastructure.hatena.image.image_downloader import ImageDownLoader


class BlogPhotosToDocImagesConverter:
    def __init__(self, image_downloader: ImageDownLoader):
        self.__image_downloader = image_downloader

    def convert_to_dict(self, photo_entries: PhotoEntries, doc_entry_dir_path: str) -> dict[PhotoEntry, DocImage]:
        photo_entry_to_doc_image: dict[PhotoEntry, DocImage] = {}
        for blog_image in photo_entries.items:
            image_data: bytes = self.__image_downloader.run(blog_image.image_url)
            doc_image = DocImage(doc_entry_dir_path, blog_image.image_filename, image_data)
            photo_entry_to_doc_image[blog_image] = doc_image
        return photo_entry_to_doc_image

    def convert(self, photo_entries: PhotoEntries, doc_entry_dir_path: str) -> list[DocImage]:
        return list(self.convert_to_dict(photo_entries, doc_entry_dir_path).values())
