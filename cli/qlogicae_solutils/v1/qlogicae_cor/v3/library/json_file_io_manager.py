__all__ = (
    "JsonFileIoManager",
)

_JsonFileIoManager = None
_ExternalDependencyManager = None

_json = None
_pathlib = None
_JsonIoDataManager = None
_TextEncodingDataManager = None


def _allocate():
    global _allocate
    global _JsonFileIoManager

    from .abstract_manager import AbstractManager

    class __JsonFileIoManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _json
                global _pathlib
                global _JsonIoDataManager
                global _TextEncodingDataManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _json = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="json",
                    )
                )
                _pathlib = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="pathlib",
                    )
                )
                _JsonIoDataManager = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.json_io_data_manager",
                        member="JsonIoDataManager",
                        is_member_callable=True,
                    )
                )
                _TextEncodingDataManager = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.text_encoding_manager",
                        member="TextEncodingDataManager",
                        is_member_callable=True,
                    )
                )
                
            return True

        def read_file(self, file_path):
            if not isinstance(file_path, (str, _pathlib().Path)):
                raise TypeError("")

            path = _pathlib().Path(file_path)

            output_data = {}

            with path.open(
                mode="r",
                encoding=(
                    _TextEncodingDataManager()
                        .read_singleton()
                        .read_selected_encoding_type()
                ),
            ) as file:
                output_data = _json().load(file) or {}

            return output_data

        def write_file(self, file_path, data):
            if not isinstance(file_path, (str, _pathlib().Path)):
                raise TypeError("")

            path = _pathlib().Path(file_path)

            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            json_io_data_manager = (
                _JsonIoDataManager()
                    .read_singleton()
            )
            text_encoding_manager = (
                _TextEncodingDataManager()
                    .read_singleton()
            )

            with path.open(
                mode="w",
                encoding=(
                    text_encoding_manager
                        .read_selected_encoding_type()
                ),
            ) as file:
                _json().dump(
                    data,
                    file,
                    indent=(
                        json_io_data_manager
                            .read_indent_count()
                    ),
                    ensure_ascii=(
                        json_io_data_manager
                            .read_is_ascii_format_enabled()
                    ),
                    sort_keys=(
                        json_io_data_manager
                            .read_is_key_sortable()
                    ),
                )

            return True


    _JsonFileIoManager = __JsonFileIoManager
    _allocate = lambda: None


def JsonFileIoManager():
    if _JsonFileIoManager is None:
        _allocate()

    return _JsonFileIoManager


# JsonFileIoManager()
