from common.constants import DOCS_DIR_PATH
from docs.domain.value import DocEntryId
from entries.domain.entity import CategoryTreeDefinition
from entries.domain.value import CategoryPath
from files.value import DirectoryPath


class AllDocumentPathResolver:
    def __init__(self, category_tree_def: CategoryTreeDefinition, doc_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__doc_root_dir_path = doc_dir_path
        self.__category_tree_def = category_tree_def

    def resolve(self) -> dict[DocEntryId, str]:
        all_category_paths: list[CategoryPath] = self.__category_tree_def.all_category_paths
        dir_paths = list(
            map(lambda path: self.__doc_root_dir_path.add_dir(path.value), all_category_paths))

        doc_id_to_path = {}
        for dir_path in dir_paths:
            doc_file_paths = dir_path.get_file_paths_in_target_dir()
            doc_id_to_path |= dict(
                map(lambda file_path: (DocEntryId(file_path.get_created_file_time()), file_path), doc_file_paths))
        return doc_id_to_path
