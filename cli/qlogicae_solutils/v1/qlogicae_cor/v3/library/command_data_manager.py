__all__ = (
    "CommandDataManager",
)

_CommandDataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _CommandDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __CommandDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "command"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "is_parser_enabled": False,
                        "parser_options": {
                            "args": (),
                            "kwargs": {
                                "prog": "name",
                                "description": "description",
                                "add_help": True,
                                "allow_abbrev": True,
                            },
                            "commands": [],
                            "subparsers": {
                                "args": (),
                                "kwargs": {
                                    "dest": "command",
                                    "required": True,
                                    "title": "commands",
                                    "description": None,
                                    "metavar": "",
                                },
                            },
                        },
                        "functions": {},
                    }                  
                })
            )

        def read_functions(self):
            return (
                self.read_one_data(
                    ("functions",)
                )
            )

        def read_parser_options(self):
            return (
                self.read_one_data(
                    ("parser_options",)
                )
            )


    _CommandDataManager = __CommandDataManager
    _allocate = lambda: None


def CommandDataManager():
    if _CommandDataManager is None:
        _allocate()

    return _CommandDataManager
