__all__ = (
    "FilesystemCompressionDataManager",
)

_ExternalDependencyManager = None
_FilesystemCompressionDataManager = None

_zipfile = None


def _allocate():
    global _allocate
    global _FilesystemCompressionDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __FilesystemCompressionDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "filesystem_compression"
            })

            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _zipfile
    
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _zipfile = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="zipfile",
                    )
                )        

            return True

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "zip_compression_types": {
                            "store": _zipfile().ZIP_STORED,
                            "stored": _zipfile().ZIP_STORED,
                            "none": _zipfile().ZIP_STORED,
                            "deflate": _zipfile().ZIP_DEFLATED,
                            "deflated": _zipfile().ZIP_DEFLATED,
                            "bz2": _zipfile().ZIP_BZIP2,
                            "bzip2": _zipfile().ZIP_BZIP2,
                            "lzma": _zipfile().ZIP_LZMA,
                            "xz": _zipfile().ZIP_LZMA,
                        }
                    }                  
                })
            )

        def read_zip_compression_type(self, compression_format):
            return (
                self.read_one_data(
                    ("zip_compression_types", compression_format,),
                )
            )


    _FilesystemCompressionDataManager = __FilesystemCompressionDataManager
    _allocate = lambda: None


def FilesystemCompressionDataManager():
    if _FilesystemCompressionDataManager is None:
        _allocate()

    return _FilesystemCompressionDataManager
