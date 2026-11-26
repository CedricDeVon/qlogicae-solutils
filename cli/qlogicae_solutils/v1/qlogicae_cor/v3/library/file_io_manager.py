__all__ = (
    "FileIoManager",
)

_TextEncodingDataManager = None
_ExternalDependencyManager = None

_pathlib = None
_FileIoManager = None


def _allocate():
    global _allocate
    global _FileIoManager

    from .abstract_manager import AbstractManager

    class __FileIoManager(AbstractManager()):        
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager
                
                global _pathlib
                global _TextEncodingDataManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _pathlib = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="pathlib",
                    )
                )
                _TextEncodingDataManager = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.text_encoding_data_manager",
                        member="TextEncodingDataManager",
                        is_member_callable=True,
                    )
                )

            return True

        def read_file(self, file_path):
            path = _pathlib().Path(file_path)

            with path.open(
                mode="r",
                encoding=_TextEncodingDataManager()
                    .read_singleton()
                    .read_selected_encoding_type(),
            ) as file:
                return file.read() or ""

        def write_file(self, file_path, data):
            path = _pathlib().Path(file_path)

            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with path.open(
                mode="w",
                encoding=_TextEncodingDataManager()
                    .read_singleton()
                    .read_selected_encoding_type(),
            ) as file:
                file.write(str(data))

            return True


    _FileIoManager = __FileIoManager
    _allocate = lambda: None


def FileIoManager():
    if _FileIoManager is None:
        _allocate()

    return _FileIoManager


# FileIoManager()
