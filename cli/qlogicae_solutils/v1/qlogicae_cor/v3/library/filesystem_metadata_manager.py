__all__ = (
    "FilesystemMetadataManager",
)

_datetime = None
_json = None
_re = None
_stat = None
_pathlib = None
_FilesystemMetadata = None
_FilesystemMetadataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _FilesystemMetadataManager

    class __FilesystemMetadataManager:
        __slots__ = (
            "_property_names",
            "_size_units",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
            global _pathlib
            global _datetime
            global _json
            global _re
            global _stat
            global _FilesystemMetadata

            _.external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _datetime = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="datetime",
                )
            )
            _json = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="json",
                )
            )
            _re = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="re",
                )
            )
            _stat = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="stat",
                )
            )
            _pathlib = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="pathlib",
                )
            )
            _FilesystemMetadata = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="qlogicae_cor.v3.library.filesystem_metadata",
                    member="FilesystemMetadata",
                    is_member_callable=True
                )
            )

            self._property_names = {
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
            }

            self._size_units = {
                "b": 1 / 8,
                "bit": 1 / 8,
                "bits": 1 / 8,
                "B": 1,
                "byte": 1,
                "bytes": 1,
                "kb": 1000 / 8,
                "kilobit": 1000 / 8,
                "kilobits": 1000 / 8,
                "kB": 1000,
                "kilobyte": 1000,
                "kilobytes": 1000,
                "Mb": 1000 ** 2 / 8,
                "megabit": 1000 ** 2 / 8,
                "megabits": 1000 ** 2 / 8,
                "MB": 1000 ** 2,
                "megabyte": 1000 ** 2,
                "megabytes": 1000 ** 2,
                "Gb": 1000 ** 3 / 8,
                "gigabit": 1000 ** 3 / 8,
                "gigabits": 1000 ** 3 / 8,
                "GB": 1000 ** 3,
                "gigabyte": 1000 ** 3,
                "gigabytes": 1000 ** 3,
                "Tb": 1000 ** 4 / 8,
                "terabit": 1000 ** 4 / 8,
                "terabits": 1000 ** 4 / 8,
                "TB": 1000 ** 4,
                "terabyte": 1000 ** 4,
                "terabytes": 1000 ** 4,
                "Pb": 1000 ** 5 / 8,
                "petabit": 1000 ** 5 / 8,
                "petabits": 1000 ** 5 / 8,
                "PB": 1000 ** 5,
                "petabyte": 1000 ** 5,
                "petabytes": 1000 ** 5,
                "Kib": 1024 / 8,
                "kibibit": 1024 / 8,
                "kibibits": 1024 / 8,
                "KiB": 1024,
                "kibibyte": 1024,
                "kibibytes": 1024,
                "Mib": 1024 ** 2 / 8,
                "mebibit": 1024 ** 2 / 8,
                "mebibits": 1024 ** 2 / 8,
                "MiB": 1024 ** 2,
                "mebibyte": 1024 ** 2,
                "mebibytes": 1024 ** 2,
                "Gib": 1024 ** 3 / 8,
                "gibibit": 1024 ** 3 / 8,
                "gibibits": 1024 ** 3 / 8,
                "GiB": 1024 ** 3,
                "gibibyte": 1024 ** 3,
                "gibibytes": 1024 ** 3,
                "Tib": 1024 ** 4 / 8,
                "tebibit": 1024 ** 4 / 8,
                "tebibits": 1024 ** 4 / 8,
                "TiB": 1024 ** 4,
                "tebibyte": 1024 ** 4,
                "tebibytes": 1024 ** 4,
                "Pib": 1024 ** 5 / 8,
                "pebibit": 1024 ** 5 / 8,
                "pebibits": 1024 ** 5 / 8,
                "PiB": 1024 ** 5,
                "pebibyte": 1024 ** 5,
                "pebibytes": 1024 ** 5,
            }

            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True
                
            return True

        def shutdown(self):
            return True

        def read_metadata(
            self,
            filesystem_path,
        ):
            if not isinstance(filesystem_path, (str, _pathlib().Path)):
                raise ValueError("")

            stat = _pathlib().Path(filesystem_path).stat()

            return _FilesystemMetadata()(
                mode=stat.st_mode,
                inode=stat.st_ino,
                device=stat.st_dev,
                hard_links=stat.st_nlink,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                access_time=stat.st_atime,
                modification_time=stat.st_mtime,
                status_change_time=stat.st_ctime,
            )

        def read_data(self, **kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("")
        
            target_filesystem_path = kwargs.get(
                "target_filesystem_path"
            )
            target_regex_patterns = kwargs.get(
                "target_regex_patterns",
                ()
            )
            properties = kwargs.get(
                "properties",
                ()
            )

            if not target_filesystem_path:
                raise ValueError("")

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            if isinstance(properties, str):
                properties = (properties,)            

            if properties:
                invalid_properties = set(properties) - self._property_names

                if invalid_properties:
                    raise ValueError("")

            root = _pathlib().Path(target_filesystem_path)

            if not root.exists() and not root.is_symlink():
                return False

            compiled_patterns = tuple(
                _re().compile(pattern)
                for pattern in target_regex_patterns
            )

            if root.is_file() or root.is_symlink():
                paths = (root,)
            else:
                paths = (root, *root.rglob("*"))

            results = []

            for path in paths:
                if path != root:
                    relative_path = path.relative_to(root).as_posix()

                    if compiled_patterns and not any(
                        pattern.search(relative_path)
                        for pattern in compiled_patterns
                    ):
                        continue

                metadata = path.lstat()
                mode = metadata.st_mode

                if _stat().S_ISLNK(mode):
                    filesystem_type = "symlink"
                elif _stat().S_ISDIR(mode):
                    filesystem_type = "directory"
                elif _stat().S_ISREG(mode):
                    filesystem_type = "file"
                elif _stat().S_ISFIFO(mode):
                    filesystem_type = "fifo"
                elif _stat().S_ISSOCK(mode):
                    filesystem_type = "socket"
                elif _stat().S_ISCHR(mode):
                    filesystem_type = "character_device"
                elif _stat().S_ISBLK(mode):
                    filesystem_type = "block_device"
                else:
                    filesystem_type = "unknown"

                created_timestamp = getattr(
                    metadata,
                    "st_birthtime",
                    None
                )

                if created_timestamp is None:
                    created_timestamp = getattr(
                        metadata,
                        "st_ctime",
                        None
                    )

                entry = {
                    "path": str(path),
                    "name": path.name,
                    "type": filesystem_type,
                    "size": metadata.st_size,
                    "permissions": _stat().filemode(mode),
                    "mode": oct(mode),
                    "owner_id": getattr(metadata, "st_uid", None),
                    "group_id": getattr(metadata, "st_gid", None),
                    "hard_links": getattr(metadata, "st_nlink", None),
                    "device_id": getattr(metadata, "st_dev", None),
                    "inode": getattr(metadata, "st_ino", None),
                    "created_at": (
                        _datetime().datetime.fromtimestamp(
                            created_timestamp,
                            tz=_datetime().timezone.utc
                        ).isoformat()
                        if created_timestamp is not None
                        else None
                    ),
                    "changed_at": (
                        _datetime().datetime.fromtimestamp(
                            metadata.st_ctime,
                            tz=_datetime().timezone.utc
                        ).isoformat()
                        if created_timestamp is None
                        and hasattr(metadata, "st_ctime")
                        else None
                    ),
                    "modified_at": _datetime().datetime.fromtimestamp(
                        metadata.st_mtime,
                        tz=_datetime().timezone.utc
                    ).isoformat(),
                    "accessed_at": _datetime().datetime.fromtimestamp(
                        metadata.st_atime,
                        tz=_datetime().timezone.utc
                    ).isoformat(),
                }

                if properties:
                    entry = {
                        property_name: entry[property_name]
                        for property_name in properties
                    }

                results.append(entry)

            return tuple(
                _json().dumps(
                    results,
                    indent=4,
                    ensure_ascii=False
                )
            )

        def read_size(self, **kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("")

            target_filesystem_paths = kwargs.get(
                "target_filesystem_paths",
                ()
            ) or ()
            target_regex_patterns = kwargs.get(
                "target_regex_patterns",
                ()
            ) or ()
            unit = kwargs.get("unit", "B") or "B"

            if not target_filesystem_paths:
                raise ValueError("")

            if isinstance(target_filesystem_paths, str):
                target_filesystem_paths = (target_filesystem_paths,)

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            if unit not in self._size_units:
                raise ValueError("")

            compiled_patterns = tuple(
                _re().compile(pattern)
                for pattern in target_regex_patterns
            )

            total_size = 0

            for target_filesystem_path in target_filesystem_paths:
                root = _pathlib().Path(target_filesystem_path)

                if not root.exists() and not root.is_symlink():
                    continue

                if root.is_symlink():
                    continue

                if root.is_file():
                    if not compiled_patterns or any(
                        pattern.search(root.name)
                        for pattern in compiled_patterns
                    ):
                        total_size += root.stat().st_size

                    continue

                for path in root.rglob("*"):
                    if path.is_symlink() or not path.is_file():
                        continue

                    relative_path = path.relative_to(root).as_posix()

                    if compiled_patterns and not any(
                        pattern.search(relative_path)
                        for pattern in compiled_patterns
                    ):
                        continue

                    total_size += path.stat().st_size

            result = total_size / self._size_units.get(
                unit,
                1
            ) or 1

            return result

        def run_filesystem_count_command(self, **kwargs):
            if not isinstance(kwargs, object) or not kwargs:
                raise ValueError("")

            target_filesystem_paths = kwargs.get(
                "target_filesystem_paths",
                ()
            ) or ()
            target_regex_patterns = kwargs.get(
                "target_regex_patterns",
                ()
            ) or ()

            if not target_filesystem_paths:
                raise ValueError("")

            if isinstance(target_filesystem_paths, str):
                target_filesystem_paths = (target_filesystem_paths,)

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            compiled_patterns = tuple(
                _re().compile(pattern)
                for pattern in target_regex_patterns
            )

            total_count = 0

            for target_filesystem_path in target_filesystem_paths:
                root = _pathlib().Path(target_filesystem_path)

                if not root.exists() and not root.is_symlink():
                    continue

                if root.is_file() or root.is_symlink():
                    if not compiled_patterns or any(
                        pattern.search(root.name)
                        for pattern in compiled_patterns
                    ):
                        total_count += 1

                    continue

                for path in root.rglob("*"):
                    relative_path = path.relative_to(root).as_posix()

                    if compiled_patterns and not any(
                        pattern.search(relative_path)
                        for pattern in compiled_patterns
                    ):
                        continue

                    total_count += 1

            return total_count


    _FilesystemMetadataManager = __FilesystemMetadataManager
    _allocate = lambda: None


def FilesystemMetadataManager():
    if _FilesystemMetadataManager is None:
        _allocate()

    return _FilesystemMetadataManager


# FilesystemMetadataManager()
