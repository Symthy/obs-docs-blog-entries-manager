from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.entry_date_time import EntryDateTime
from files import text_file, file_system, image_file


class DocumentFileAccessor:
    def __init__(self, document_root_dir_path):
        self.__document_root_dir_path = document_root_dir_path

    def save_doc_set(self, doc_entry_dir_path: str, title: str, content: DocContent,
                     images: DocImages) -> DocEntryId:
        doc_file_path = file_system.join_path(doc_entry_dir_path, f'{title}.md')
        text_file.write_file(doc_file_path, content.value)
        for image in images.items:
            image_file.write(image.file_path, image.image_data)
        created_date_time = EntryDateTime(file_system.get_created_file_time(doc_file_path))
        return DocEntryId(created_date_time.to_str_with_num_sequence())

    def load(self, doc_file_path: str) -> DocContent:
        content: str = text_file.read_file(file_system.join_path(doc_file_path))
        doc_dir_path = file_system.get_dir_path_from_file_path(doc_file_path)
        return DocContent(content, doc_dir_path)

    def __build_file_path(self, doc_file_path: str) -> str:
        return file_system.join_path(self.__document_root_dir_path, doc_file_path)
