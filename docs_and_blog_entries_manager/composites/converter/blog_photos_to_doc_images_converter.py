from blogs.domain.entity import PhotoEntries
from blogs.domain.entity import PhotoEntry
from blogs.infrastructure.image import ImageDownLoader
from docs.domain.value import DocImage
from files.value import DirectoryPath


class BlogPhotosToDocImagesConverter:
    def __init__(self, image_downloader: ImageDownLoader):
        self.__image_downloader = image_downloader

    def convert_to_dict(self, photo_entries: PhotoEntries, doc_entry_dir_path: DirectoryPath) \
            -> dict[PhotoEntry, DocImage]:
        photo_entry_to_doc_image: dict[PhotoEntry, DocImage] = {}
        for blog_image in photo_entries.items:
            image_data: bytes = self.__image_downloader.run(blog_image.image_url)
            doc_image = DocImage(doc_entry_dir_path, blog_image.image_filename, image_data)
            photo_entry_to_doc_image[blog_image] = doc_image
        return photo_entry_to_doc_image

    def convert(self, photo_entries: PhotoEntries, doc_entry_dir_path: DirectoryPath) -> list[DocImage]:
        return list(self.convert_to_dict(photo_entries, doc_entry_dir_path).values())
