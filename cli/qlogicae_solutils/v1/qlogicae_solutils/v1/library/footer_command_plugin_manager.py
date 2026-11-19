__all__ = (
    "FooterCommandPluginManager",
)


_FooterCommandPluginManager = None


def _allocate():
    global _allocate
    global _FooterCommandPluginManager

    class __FooterCommandPluginManager:
        __slots__ = (
            "_plugin_exports",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def plugin_exports(self):
            return self._plugin_exports


        @plugin_exports.setter
        def plugin_exports(self, value):
            if not isinstance(value, dict):
                raise ValueError(
                    "'plugin_exports' must be a dictionary"
                )

            self._plugin_exports = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):            
            self._plugin_exports = {
                "object_merge": {
                    "level": 100
                },
                "qlogicae": {
                    "cliq": {
                        "v1": {    
                            "command": {
                                "options": {
                                    "commands": [
                                        {
                                            "name": "",
                                            "args": (),
                                            "kwargs": { "help": "", },
                                        },
                                    ],
                                },
                            },
                        }
                    }
                }
            }

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True


    _FooterCommandPluginManager = __FooterCommandPluginManager
    _allocate = lambda: None


def FooterCommandPluginManager():
    if _FooterCommandPluginManager is None:
        _allocate()

    return _FooterCommandPluginManager

