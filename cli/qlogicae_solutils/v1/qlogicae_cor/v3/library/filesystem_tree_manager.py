__all__ = (
    "FilesystemTreeManager",
)

_pathlib = None
_FileEntityFilesystemTreeSetupOptions = None
_FolderEntityFilesystemTreeSetupOptions = None
_FilesystemTreeManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _FilesystemTreeManager

    class __FilesystemTreeManager:
        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
            global _pathlib
            global _FileEntityFilesystemTreeSetupOptions
            global _FolderEntityFilesystemTreeSetupOptions

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _pathlib = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="pathlib",
                )
            )
            _FileEntityFilesystemTreeSetupOptions = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="qlogicae_cor.v3.library.file_entity_filesystem_tree_setup_options",
                    member="FileEntityFilesystemTreeSetupOptions",
                    is_member_callable=True,
                )
            )
            _FolderEntityFilesystemTreeSetupOptions = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="qlogicae_cor.v3.library.folder_entity_filesystem_tree_setup_options",
                    member="FolderEntityFilesystemTreeSetupOptions",
                    is_member_callable=True,
                )
            )

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True

        def setup_filesystem_tree(
            self,
            parent_path,
            entities,
        ):
            if not isinstance(parent_path, (str, _pathlib().Path)):
                raise ValueError("'parent_path' must either be a string or Path")

            if not isinstance(entities, (tuple, list)):
                raise ValueError(
                    "'entities' must be a tuple or list"
                )

            path = _pathlib().Path(parent_path)

            if not path.exists():
                raise ValueError(
                    f"filesystem path '{path}' is invalid"
                )

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
                    raise ValueError(
                        f"'entities[]' must be either "
                        "FolderEntityFilesystemTreeSetupOptions' or "
                        "FileEntityFilesystemTreeSetupOptions'"
                    )

            return True

        def _setup_filesystem_tree(
            self,
            parent_path,
            options,
        ):
            if not isinstance(parent_path, (str, _pathlib().Path)):
                raise ValueError("'parent_path' must either be a string or Path")

            if not isinstance(options, (_FolderEntityFilesystemTreeSetupOptions())):
                raise ValueError(
                    "'options' must be a 'FolderEntityFilesystemTreeSetupOptions'"
                )

            path = _pathlib().Path(parent_path)

            if not path.exists():
                raise ValueError(
                    f"filesystem path '{path}' is invalid"
                )

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
