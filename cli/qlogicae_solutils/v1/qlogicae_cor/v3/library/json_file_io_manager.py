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

    class __JsonFileIoManager:
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

            global _json
            global _pathlib
            global _JsonIoDataManager
            global _TextEncodingDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _json = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="json",
                )
            )
            _pathlib = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="pathlib",
                )
            )
            _JsonIoDataManager = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="qlogicae_cor.v3.library.json_io_data_manager",
                    member="JsonIoDataManager",
                    is_member_callable=True,
                )
            )
            _TextEncodingDataManager = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="qlogicae_cor.v3.library.text_encoding_manager",
                    member="TextEncodingDataManager",
                    is_member_callable=True,
                )
            )
            
            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
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
                        .get_singleton()
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
                    .get_singleton()
            )
            text_encoding_manager = (
                _TextEncodingDataManager()
                    .get_singleton()
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
