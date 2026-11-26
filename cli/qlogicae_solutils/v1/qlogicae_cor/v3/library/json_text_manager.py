__all__ = (
    "JsonTextManager",
)

_JsonTextManager = None
_ExternalDependencyManager = None

_json = None
_JsonIoDataManager = None


def _allocate():
    global _allocate
    global _JsonTextManager

    from .abstract_manager import AbstractManager

    class __JsonTextManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager


            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _json
                global _JsonIoDataManager
                    
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _json = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="json",
                    )
                )
                _JsonIoDataManager = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.json_io_data_manager",
                        member="JsonIoDataManager",
                        is_member_callable=True,
                    )
                )

            return True

        def is_valid(self, value):
            _json().loads(value)

            return True

        def convert_to_object(self, value):
            return _json().loads(value)

        def convert_to_string(self, value):
            json_io_data_manager = (
                _JsonIoDataManager().read_singleton()
            )

            result = _json().dumps(
                value,
                indent=(
                    json_io_data_manager
                        .read_indent_count()
                ),
                ensure_ascii=(
                    json_io_data_manager
                        .read_is_ascii_format_enabled()
                ),
            )

            return result

    _JsonTextManager = __JsonTextManager
    _allocate = lambda: None


def JsonTextManager():
    if _JsonTextManager is None:
        _allocate()

    return _JsonTextManager


# JsonTextManager()
