__all__ = (
    "PluginManager",
)

_PluginManager = None
_ExternalDependencyManager = None

_PluginDataManager = None


def _allocate():
    global _allocate
    global _PluginManager

    class __PluginManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
            
            global _PluginDataManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

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

            return True

        def setup(
            self, kwargs,
        ):        
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            return True

        def run(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            plugin_data_manager = (
                _PluginDataManager()
                    .read_singleton()
            )

            plugin_data_manager.setup(
                kwargs
            )

            plugin_items = (
                plugin_data_manager
                    .plugin_items
            )

            if not plugin_items:
                return True

            is_setup_enabled = (
                kwargs.get("is_setup_enabled", True)
            )
            if not isinstance(is_setup_enabled, (bool)):
                raise TypeError("")

            is_run_enabled = (
                kwargs.get("is_run_enabled", True)
            )
            if not isinstance(is_run_enabled, (bool)):
                raise TypeError("")

            is_shutdown_enabled = (
                kwargs.get("is_shutdown_enabled", False)
            )
            if not isinstance(is_shutdown_enabled, (bool)):
                raise TypeError("")

            result = True

            if is_setup_enabled:
                result = (
                    self.setup_plugins() and result
                )

            if is_run_enabled:
                result = (
                    self.run_plugins() and result
                )

            if is_shutdown_enabled:
                result = (
                    self.shutdown_plugins() and result
                )

            return result
    
        def setup_plugins(self):
            return (
                self.run_method_plugins(
                    self.setup_plugin
                )
            )

        def run_plugins(self):            
            return (
                self.run_method_plugins(
                    self.run_plugin
                )
            )

        def shutdown_plugins(self):
            return (
                self.run_method_plugins(
                    self.shutdown_plugin,
                    is_reversed=True,
                )
            )

        def run_method_plugins(
            self,
            callback,
            is_reversed=False,
        ):
            if not callable(callback):
                raise TypeError("")

            if not isinstance(is_reversed, (bool)):
                raise TypeError("")
            

            plugin_data_manager = (
                _PluginDataManager().read_singleton()
            )
            plugin_items = (
                plugin_data_manager
                    .read_plugin_items()
            )
            if not plugin_items:
                return True

            result = True
            plugin_items = (
                reversed(plugin_items)
                if is_reversed
                else plugin_items
            )

            for plugin_item in plugin_items:

                if not plugin_item:
                    raise TypeError("")

                result = (
                    callback(
                        plugin_item
                    )
                )

 
            return result

        def setup_plugin(
            self,
            plugin_item,
        ):
            if not plugin_item:
                raise TypeError("")
                
            return (
                self.run_optional_plugin_method(
                    plugin_item,
                    "setup_plugin"
                )
            )

        def run_plugin(
            self,
            plugin_item,
        ):
            if not plugin_item:
                raise TypeError("")

            return (
                self.run_optional_plugin_method(
                    plugin_item,
                    "run_plugin"
                )
            )

        def shutdown_plugin(
            self,
            plugin_item,
        ):
            if not plugin_item:
                raise TypeError("")

            return (
                self.run_optional_plugin_method(
                    plugin_item,
                    "shutdown_plugin"
                )
            )

        def run_optional_plugin_method(
            self,            
            plugin_item,
            method_name,
        ):
            if not plugin_item:
                raise TypeError("")

            if not isinstance(method_name, (str)):
                raise TypeError("")


            result = True
            plugin_method = (
                getattr(
                    plugin_item,
                    method_name,
                    None
                ) or None
            )

            if plugin_method:
                if not callable(plugin_method):
                    raise TypeError("")
                
                result = (
                    plugin_method() and result
                )

            return (
                result
            )


    _PluginManager = __PluginManager
    _allocate = lambda: None


def PluginManager():
    if _PluginManager is None:
        _allocate()

    return _PluginManager

# PluginManager()
