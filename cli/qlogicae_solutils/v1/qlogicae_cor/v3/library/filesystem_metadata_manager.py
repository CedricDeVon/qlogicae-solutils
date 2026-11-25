__all__ = (
    "FilesystemMetadataManager",
)

_FilesystemMetadataManager = None
_ExternalDependencyManager = None

_re = None
_json = None
_stat = None
_pathlib = None
_datetime = None
_FilesystemMetadata = None
_FilesystemMetadataDataManager = None


def _allocate():
    global _allocate
    global _FilesystemMetadataManager

    class __FilesystemMetadataManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _re
            global _json
            global _stat
            global _pathlib
            global _datetime
            global _FilesystemMetadata
            global _FilesystemMetadataDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _datetime = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="datetime",
                )
            )
            _json = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="json",
                )
            )
            _re = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="re",
                )
            )
            _stat = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="stat",
                )
            )
            _pathlib = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="pathlib",
                )
            )
            _FilesystemMetadata = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.filesystem_metadata",
                    member="FilesystemMetadata",
                    is_member_callable=True
                )
            )
            _FilesystemMetadataDataManager = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.filesystem_metadata_data_manager",
                        member="FilesystemMetadataDataManager",
                        is_member_callable=True,
                    )
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
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

        def read_data(
            self,
            target_filesystem_path,
            target_regex_patterns,
            properties,
        ):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("")
        
            if not target_filesystem_path:
                raise ValueError("")

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            if isinstance(properties, str):
                properties = (properties,)            

            if properties:
                filesystem_metadata_data_manager = (
                    _FilesystemMetadataDataManager()
                        .read_singleton()
                )
                property_names = (
                    filesystem_metadata_data_manager
                        .read_property_names()
                )

                invalid_properties = set(properties) - property_names

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

        def read_size(
            self,
            target_filesystem_paths,
            target_regex_patterns,
        ):
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

            return total_size

        def run_filesystem_count_command(self,
            target_filesystem_paths,
            target_regex_patterns,
        ):
            if not isinstance(kwargs, object) or not kwargs:
                raise ValueError("")

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
