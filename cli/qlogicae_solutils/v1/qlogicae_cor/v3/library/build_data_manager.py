__all__ = (
    "BuildDataManager",
)

_BuildDataManager = None

def _allocate():
    global _allocate
    global _BuildDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __BuildDataManager(BaseDataManager()):
        _singleton = None

        def __init__(self):
            super().__init__("qlogicae_cor_v3_build")

        @classmethod
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def setup_plugin_data(self):
            return (
                super()
                    .setup_plugin_data({
                        "root_key_path": self._root_key_path,
                        "layer": 0,
                        "data": (
                            {
                                "company_name": "",
                                "project_name": "",
                                "project_description": "",
                                "brand_base_name": "",
                                "brand_source_name": "",
                                "current_version_label": "",
                                "current_active_major_version_label": "",
                                "callbacks": {
                                    "on_pre_setup": None,
                                    "on_post_setup": None,
                                    "on_pre_run": None,
                                    "on_post_run": None,
                                    "on_pre_shutdown": None,
                                    "on_post_shutdown": None,
                                },
                            }
                        )
                    })
            )

        def read_company_name(self):
            return (
                self.read_one_data(
                    ("company_name"),
                ) or ""
            )

        def read_project_name(self):
            return (            
                self.read_one_data(
                    ("project_name"),
                ) or ""
            )

        def read_project_description(self):
            return (            
                self.read_one_data(
                    ("project_description"),
                ) or ""
            )

        def read_brand_base_name(self):
            return (            
                self.read_one_data(
                    ("brand_base_name"),
                ) or ""
            )

        def read_brand_source_name(self):
            return (            
                self.read_one_data(
                    ("brand_source_name"),
                ) or ""
            )

        def read_current_version_label(self):
            return (            
                self.read_one_data(
                    ("current_version_label"),
                ) or ""
            )

        def read_current_active_major_version_label(self):
            return (            
                self.read_one_data(
                    ("current_active_major_version_label"),
                ) or ""
            )


    _BuildDataManager = __BuildDataManager
    _allocate = lambda: None


def BuildDataManager():
    if _BuildDataManager is None:
        _allocate()

    return _BuildDataManager
