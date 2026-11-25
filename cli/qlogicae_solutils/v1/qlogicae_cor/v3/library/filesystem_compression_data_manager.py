__all__ = (
    "FilesystemCompressionDataManager",
)

_ExternalDependencyManager = None
_FilesystemCompressionDataManager = None

_zipfile = None
_PluginDataManager = None


def _allocate():
    global _allocate
    global _FilesystemCompressionDataManager

    class __FilesystemCompressionDataManager:
        __slots__ = (
            "_root_key_path",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def root_key_path(self):
            return self._root_key_path

        @root_key_path.setter
        def root_key_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

            self._root_key_path = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _zipfile

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _zipfile = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="zipfile",
                )
            )        

            self._root_key_path = (
                "qlogicae_cor_v3_filesystem_compression"
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            return True

        def setup_plugin_data(self):
            global _PluginDataManager

            _PluginDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_data_manager",
                        member="PluginDataManager",
                        is_member_callable=True,
                    )
            )

            plugin_data_manager = (
                _PluginDataManager()
                    .get_singleton()
            )

            return (
                plugin_data_manager
                    .setup_plugin_data({
                        "root_key_path": self._root_key_path,
                        "layer": 0,
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

        def read_all_data(
            self
        ):
            data = (
                _PluginDataManager()
                    .get_singleton()
                    .read_all_data(
                        self._root_key_path
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
                    .get_singleton()
                    .read_one_data(
                        self._root_key_path,
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
                    .get_singleton()
                    .write_all_data(
                        self._root_key_path,
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
                    .get_singleton()
                    .write_one_data(
                        self._root_key_path,
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
                    .get_singleton()
                    .remove_one_data(
                        self._root_key_path,
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
                    .get_singleton()
                    .remove_all_data(
                        self._root_key_path,
                    ) and result
            )

            return (
                result
            )


    _FilesystemCompressionDataManager = __FilesystemCompressionDataManager
    _allocate = lambda: None


def FilesystemCompressionDataManager():
    if _FilesystemCompressionDataManager is None:
        _allocate()

    return _FilesystemCompressionDataManager
