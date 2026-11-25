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

        def __init__(self):
            self.base_construct()

        def base_construct(self):
            self._data_manager = None

            return True

        def export_plugin(self):
            if not self._data_manager:
                raise TypeError("")

            data_manager = (
                self._data_manager()
                    .read_singleton()
            )

            return (
                data_manager
                    .setup_plugin_data()
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
                self.setup_plugin_hook() and result
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
                self.run_plugin_hook() and result
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
                self.shutdown_plugin_hook() and result
            )

            on_post_shutdown = (
                data_manager.read_callback(
                    "on_post_shutdown"
                )
            )
            if callable(on_post_shutdown):
                result = on_post_shutdown() and result

            return result

        def setup_plugin_hook(self):
            result = True
            return result

        def run_plugin_hook(self):            
            result = True
            return result

        def shutdown_plugin_hook(self):            
            result = True
            return result


    _BasePluginManager = __BasePluginManager
    _allocate = lambda: None


def BasePluginManager():
    if _BasePluginManager is None:
        _allocate()

    return _BasePluginManager
