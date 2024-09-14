from docs.domain.datasource.interface import IDocumentReader, IDocumentMover, StoredDocEntriesLoader
from docs.domain.entity import DocEntry
from entries.domain.entity.category_tree_definition import CategoryTreeDefinition
from entries.domain.value import CategoryPath


class LocalDocOrganizerService:
    """
    documentフォルダ内の記事を記事のカテゴリパスに応じて整理(移動)
    """

    def __init__(self, category_tree_def: CategoryTreeDefinition,
                 document_file_mover: IDocumentMover,
                 document_file_reader: IDocumentReader,
                 stored_doc_entries_loader: StoredDocEntriesLoader):
        self.__category_tree_def = category_tree_def
        self.__document_file_mover = document_file_mover
        self.__document_file_reader = document_file_reader
        self.__stored_doc_entries_loader = stored_doc_entries_loader

    def organize(self):
        category_paths: list[CategoryPath] = self.__category_tree_def.all_category_paths
        # Todo: refactor
        for category_path in category_paths:
            doc_file_paths = self.__category_tree_def.get_file_paths(category_path)
            for doc_file_path in doc_file_paths:
                current_doc_entry: DocEntry = self.__document_file_reader.restore(doc_file_path)
                old_doc_entry: DocEntry = self.__stored_doc_entries_loader.load_entry(current_doc_entry.id)
                if not current_doc_entry.equals_path(old_doc_entry):
                    self.__document_file_mover.move(old_doc_entry.doc_file_path, current_doc_entry.doc_file_path)
