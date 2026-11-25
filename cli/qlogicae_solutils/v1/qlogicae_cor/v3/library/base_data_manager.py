__all__ = (
    "BaseDataManager",
)

_BaseDataManager = None
_ExternalDependencyManager = None

_PluginDataManager = None


def _allocate():
    global _allocate
    global _BaseDataManager

    from .abstract_manager import AbstractManager

    class __BaseDataManager(AbstractManager()):
        __slots__ = (
            "_root_key_path",
        )

        def __init__(self, root_key_path):
            self.base_construct(root_key_path)

        @property
        def root_key_path(self):
            return self._root_key_path

        @root_key_path.setter
        def root_key_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

            self._root_key_path = value

        def base_construct(self, root_key_path):
            global _ExternalDependencyManager
            global _PluginDataManager
            
            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _PluginDataManager = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_data_manager",
                        member="PluginDataManager",
                        is_member_callable=True,
                    )
            )

            self._root_key_path = (
                root_key_path
            )

            return True

        def base_setup_plugin_data(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            plugin_data_manager = (
                _PluginDataManager()
                    .read_singleton()
            )

            return (
                plugin_data_manager
                    .setup_plugin_data(kwargs)
            )

        def read_callback(self, callback_name):
            data = (
                self.read_one_data(
                        (callback_name,)
                    )
            )

            return (
                data
            )

        def read_all_data(
            self
        ):
            data = (
                _PluginDataManager()
                    .read_singleton()
                    .read_all_data(
                        self._root_key_path
                    )
            )

            return (
                data
            )

        def read_one_data(
            self,
            key_path,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            data = (
                _PluginDataManager()
                    .read_singleton()
                    .read_one_data(
                        self._root_key_path,
                        key_path
                    )
            )

            return (
                data
            )

        def write_all_data(
            self,
            value
        ):
            result = True
            result = (
                _PluginDataManager()
                    .read_singleton()
                    .write_all_data(
                        self._root_key_path,
                        value
                    ) and result
            )

            return (
                result
            )

        def write_one_data(
            self,
            key_path,
            value,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            result = True
            result = (
                _PluginDataManager()
                    .read_singleton()
                    .write_one_data(
                        self._root_key_path,
                        key_path,
                        value
                    ) and result
            )

            return (
                result
            )

        def remove_one_data(
            self,
            key_path,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            result = True
            result = (
                _PluginDataManager()
                    .read_singleton()
                    .remove_one_data(
                        self._root_key_path,
                        key_path,
                    ) and result
            )

            return (
                result
            )

        def remove_all_data(
            self,
        ):
            result = True
            result = (
                _PluginDataManager()
                    .read_singleton()
                    .remove_all_data(
                        self._root_key_path,
                    ) and result
            )

            return (
                result
            )


    _BaseDataManager = __BaseDataManager
    _allocate = lambda: None


def BaseDataManager():
    if _BaseDataManager is None:
        _allocate()

    return _BaseDataManager
