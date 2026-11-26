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
            "_main_root_key_path",
            "_sub_root_key_path",
        )

        def __init__(self, kwargs):
            self.base_construct(kwargs)

        @property
        def main_root_key_path(self):
            return self._main_root_key_path

        @main_root_key_path.setter
        def main_root_key_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

            self._main_root_key_path = value

        @property
        def sub_root_key_path(self):
            return self._sub_root_key_path

        @sub_root_key_path.setter
        def sub_root_key_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

            self._sub_root_key_path = value

        def read_root_key_path(self):
            return (
                f"{self._main_root_key_path}_{self._sub_root_key_path}"
            )

        def base_construct(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")         
                
            global _ExternalDependencyManager   

            if not _ExternalDependencyManager:            
                from .external_dependency_manager import ExternalDependencyManager

                global _PluginDataManager
                
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

            self._main_root_key_path = (
                kwargs.get(
                    "main_root_key_path",
                    "qlogicae_cor_v3"
                ) or "qlogicae_cor_v3"
            )
            self._sub_root_key_path = (
                kwargs.get(
                    "sub_root_key_path",
                    "base"
                ) or "base"
            )

            return True

        def base_setup_plugin_data(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            plugin_data_manager = (
                _PluginDataManager()
                    .read_singleton()
            )

            data = (
                kwargs.get("data", {}) or {}
            )
            root_key_path = (
                kwargs.get(
                    "root_key_path",
                    self.read_root_key_path()
                ) or self.read_root_key_path()
            )
            layer = (
                kwargs.get("layer", 0)
            )
            is_default_data_enabled = (
                kwargs.get("is_default_data_enabled", True)
            )
            default_data = (
                {
                    "callbacks": {
                        "on_pre_setup": None,
                        "on_post_setup": None,
                        "on_pre_run": None,
                        "on_post_run": None,
                        "on_pre_shutdown": None,
                        "on_post_shutdown": None,
                    }
                }
                if is_default_data_enabled
                else {}
            )

            return (
                plugin_data_manager
                    .setup_plugin_data({
                        "root_key_path": root_key_path,
                        "layer": layer,
                        "data": {
                            **default_data,
                            **data,
                        }
                    })
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
                        self.read_root_key_path()
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
                        self.read_root_key_path(),
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
                        self.read_root_key_path(),
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
                        self.read_root_key_path(),
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
                        self.read_root_key_path(),
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
                        self.read_root_key_path(),
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
