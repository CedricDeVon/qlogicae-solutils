__all__ = (
    "BasePluginManager",
)

_BasePluginManager = None

def _allocate():
    global _allocate
    global _BasePluginManager

    from .abstract_manager import AbstractManager        

    class __BasePluginManager(AbstractManager()):
        __slots__ = (
            "_data_manager",
        )

        def base_construct(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            data_manager = (
                kwargs.get(
                    "data_manager",
                    None
                ) or None
            )
            if not isinstance(data_manager, (object)):
                raise TypeError("")

            self._data_manager = (
                data_manager
            )

            return True

        def export_plugin(self):
            if not self._data_manager:
                raise TypeError("")

            data_manager = (
                self._data_manager()
                    .read_singleton()
            )            

            on_pre_export = (
                data_manager.read_callback(
                    "on_pre_export"
                )
            )
            if callable(on_pre_export):
                on_pre_export()

            self.on_export_plugin()
            plugin_data = (
                data_manager
                    .setup_plugin_data()
            )

            on_post_export = (
                data_manager.read_callback(
                    "on_post_export"
                )
            )
            if callable(on_post_export):
                on_post_export()


            return (
                plugin_data
            )

        def setup_plugin(self):
            data_manager = (
                self._data_manager()
                    .read_singleton()
            )

            result = True
            on_pre_setup = (
                data_manager.read_callback(
                    "on_pre_setup"
                )
            )
            if callable(on_pre_setup):
                result = on_pre_setup() and result

            result = (
                self.on_setup_plugin() and result
            )

            on_post_setup = (
                data_manager.read_callback(
                    "on_post_setup"
                )
            )
            if callable(on_post_setup):
                result = on_post_setup() and result

            return result

        def run_plugin(self):       
            data_manager = (
                self._data_manager()
                    .read_singleton()
            )

            result = True            
            on_pre_run = (
                data_manager.read_callback(
                    "on_pre_run"
                )
            )
            if callable(on_pre_run):
                result = on_pre_run() and result

            result = (
                self.on_run_plugin() and result
            )

            on_post_run = (
                data_manager.read_callback(
                    "on_post_run"
                )
            )
            if callable(on_post_run):
                result = on_post_run() and result

            return result

        def shutdown_plugin(self):     
            data_manager = (
                self._data_manager()
                    .read_singleton()
            )

            result = True            
            on_pre_shutdown = (
                data_manager.read_callback(
                    "on_pre_shutdown"
                )
            )
            if callable(on_pre_shutdown):
                result = on_pre_shutdown() and result

            result = (
                self.on_shutdown_plugin() and result
            )

            on_post_shutdown = (
                data_manager.read_callback(
                    "on_post_shutdown"
                )
            )
            if callable(on_post_shutdown):
                result = on_post_shutdown() and result

            return result

        def on_export_plugin(self):
            result = True
            return result

        def on_setup_plugin(self):
            result = True
            return result

        def on_run_plugin(self):            
            result = True
            return result

        def on_shutdown_plugin(self):            
            result = True
            return result


    _BasePluginManager = __BasePluginManager
    _allocate = lambda: None


def BasePluginManager():
    if _BasePluginManager is None:
        _allocate()

    return _BasePluginManager
