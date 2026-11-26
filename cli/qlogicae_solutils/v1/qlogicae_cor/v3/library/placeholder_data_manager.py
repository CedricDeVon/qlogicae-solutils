__all__ = (
    "PlaceholderDataManager",
)

_ExternalDependencyManager = None
_PlaceholderDataManager = None


def _allocate():
    global _allocate
    global _PlaceholderDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __PlaceholderDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "placeholder"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "none": "None",
                        "not_a_number": "NaN",
                        "redacted": "REDACTED",
                        "expunged": "EXPUNGED",
                        "censored": "CENSORED",
                    }                  
                })
            )

        def read_none(self):
            return (
                self.read_one_data(
                    ("none",),
                ) or "None"
            )

        def read_not_a_number(self):
            return (
                self.read_one_data(
                    ("not_a_number",),
                ) or "NaN"
            )

        def read_redacted(self):
            return (
                self.read_one_data(
                    ("redacted",),
                ) or "REDACTED"
            )

        def read_expunged(self):
            return (
                self.read_one_data(
                    ("expunged",),
                ) or "EXPUNGED"
            )

        def read_censored(self):
            return (
                self.read_one_data(
                    ("censored",),
                ) or "CENSORED"
            )


    _PlaceholderDataManager = __PlaceholderDataManager
    _allocate = lambda: None


def PlaceholderDataManager():
    if _PlaceholderDataManager is None:
        _allocate()

    return _PlaceholderDataManager
