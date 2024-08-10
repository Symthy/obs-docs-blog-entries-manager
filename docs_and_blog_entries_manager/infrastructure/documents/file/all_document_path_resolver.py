from common.constants import DOCS_DIR_PATH
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.entity.category_tree_definition import CategoryTreeDefinition
from domain.entries.values.category_path import CategoryPath
from files import file_system


class AllDocumentPathResolver:
    def __init__(self, category_tree_def: CategoryTreeDefinition, doc_dir_path: str = DOCS_DIR_PATH):
        self.__doc_root_dir_path = doc_dir_path
        self.__category_tree_def = category_tree_def

    def resolve(self) -> dict[DocEntryId, str]:
        doc_id_to_path = {}
        all_category_paths: list[CategoryPath] = self.__category_tree_def.all_category_paths
        dir_paths = list(
            map(lambda path: file_system.join_path(self.__doc_root_dir_path, path.value), all_category_paths))
        for dir_path in dir_paths:
            doc_file_paths = file_system.get_file_paths_in_target_dir(dir_path)
            doc_id_to_path |= dict(
                map(lambda path: (DocEntryId(file_system.get_created_file_time(path)), path), doc_file_paths))
        return doc_id_to_path
