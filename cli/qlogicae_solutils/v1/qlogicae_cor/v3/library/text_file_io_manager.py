__all__ = (
    "TextFileIoManager",
)

_TextFileIoManager = None
_ExternalDependencyManager = None

_pathlib = None
_TextEncodingDataManager = None


def _allocate():
    global _allocate
    global _TextFileIoManager

    from .abstract_manager import AbstractManager

    class __TextFileIoManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def read_file(self, file_path):
            path = _pathlib().Path(file_path)

            output_data = ""

            with path.open(
                mode="r",
                encoding=_TextEncodingDataManager().read_selected_encoding_type(),
            ) as file:
                output_data = file.read() or ""

            return output_data

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
                        member="TextEncodingManager",
                        is_member_callable=True,
                    )
                )

            return True

        def write_file(self, file_path, data):
            path = _pathlib().Path(file_path)

            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with path.open(
                mode="w",
                encoding=_TextEncodingDataManager().read_selected_encoding_type(),
            ) as file:
                file.write(str(data))

            return True

    _TextFileIoManager = __TextFileIoManager
    _allocate = lambda: None


def TextFileIoManager():
    if _TextFileIoManager is None:
        _allocate()

    return _TextFileIoManager


# TextFileIoManager()
