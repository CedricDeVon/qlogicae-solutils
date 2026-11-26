__all__ = (
    "FilesystemMetadataDataManager",
)

_ExternalDependencyManager = None
_FilesystemMetadataDataManager = None


def _allocate():
    global _allocate
    global _FilesystemMetadataDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __FilesystemMetadataDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "filesystem_metadata"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "property_names": {
                            "path",
                            "name",
                            "type",
                            "size",
                            "permissions",
                            "mode",
                            "owner_id",
                            "group_id",
                            "hard_links",
                            "device_id",
                            "inode",
                            "created_at",
                            "changed_at",
                            "modified_at",
                            "accessed_at",
                        },
                    }                  
                })
            )

        def read_property_names(self):
            return (
                self.read_one_data(
                    ("property_names",),
                )
            )


    _FilesystemMetadataDataManager = __FilesystemMetadataDataManager
    _allocate = lambda: None


def FilesystemMetadataDataManager():
    if _FilesystemMetadataDataManager is None:
        _allocate()

    return _FilesystemMetadataDataManager
