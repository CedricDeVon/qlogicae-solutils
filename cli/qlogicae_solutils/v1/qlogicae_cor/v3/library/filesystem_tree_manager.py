__all__ = (
    "FilesystemTreeManager",
)

_FilesystemTreeManager = None
_ExternalDependencyManager = None

_pathlib = None
_FileEntityFilesystemTreeSetupOptions = None
_FolderEntityFilesystemTreeSetupOptions = None


def _allocate():
    global _allocate
    global _FilesystemTreeManager

    from .abstract_manager import AbstractManager

    class __FilesystemTreeManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _pathlib
                global _FileEntityFilesystemTreeSetupOptions
                global _FolderEntityFilesystemTreeSetupOptions

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _pathlib = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="pathlib",
                    )
                )
                _FileEntityFilesystemTreeSetupOptions = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.file_entity_filesystem_tree_setup_options",
                        member="FileEntityFilesystemTreeSetupOptions",
                        is_member_callable=True,
                    )
                )
                _FolderEntityFilesystemTreeSetupOptions = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.folder_entity_filesystem_tree_setup_options",
                        member="FolderEntityFilesystemTreeSetupOptions",
                        is_member_callable=True,
                    )
                )

            return True

        def setup_filesystem_tree(
            self,
            parent_path,
            entities,
        ):
            if not isinstance(parent_path, (str, _pathlib().Path)):
                raise ValueError("")

            if not isinstance(entities, (tuple, list)):
                raise ValueError("")

            path = _pathlib().Path(parent_path)

            if not path.exists():
                raise ValueError("")

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

            for entity in entities:
                if entity is None:
                    continue

                entity_path = path / entity.name

                if isinstance(
                    entity,
                    _FolderEntityFilesystemTreeSetupOptions(),
                ):
                    entity_path.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    self._setup_filesystem_tree(
                        entity_path,
                        entity,
                    )

                elif isinstance(
                    entity,
                    _FileEntityFilesystemTreeSetupOptions(),
                ):
                    if not entity_path.exists():
                        entity_path.write_text(
                            entity.content,
                            encoding=entity.encoding,
                        )

                else:
                    raise ValueError("")

            return True

        def _setup_filesystem_tree(
            self,
            parent_path,
            options,
        ):
            if not isinstance(parent_path, (str, _pathlib().Path)):
                raise ValueError("")

            if not isinstance(options, (_FolderEntityFilesystemTreeSetupOptions())):
                raise ValueError("")

            path = _pathlib().Path(parent_path)

            if not path.exists():
                raise ValueError("")

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

            for entity in options.entities or []:
                entity_path = path / entity.name

                if isinstance(
                    entity,
                    _FolderEntityFilesystemTreeSetupOptions(),
                ):
                    entity_path.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    self._setup_filesystem_tree(
                        entity_path,
                        entity,
                    )

                elif isinstance(
                    entity,
                    _FileEntityFilesystemTreeSetupOptions(),
                ):
                    if not entity_path.exists():
                        entity_path.write_text(
                            entity.content,
                            encoding=entity.encoding,
                        )


    _FilesystemTreeManager = __FilesystemTreeManager
    _allocate = lambda: None


def FilesystemTreeManager():
    if _FilesystemTreeManager is None:
        _allocate()

    return _FilesystemTreeManager


# FilesystemTreeManager()
