__all__ = (
    "FilesystemCompressionManager",
)

_os = None
_re = None
_tempfile = None
_zipfile = None
_pathlib = None
_FilesystemCompressionManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _FilesystemCompressionManager

    class __FilesystemCompressionManager:
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
            global _os
            global _re
            global _tempfile
            global _zipfile
            global _pathlib

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _os = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="os",
                )
            )
            _re = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="re",
                )
            )
            _tempfile = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="tempfile",
                )
            )
            _zipfile = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="zipfile",
                )
            )            
            _pathlib = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="pathlib",
                )
            )

            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            return True

        def shutdown(self):
            return True

        def get_zip_format_compression(
            self,
            value,
        ):
            if not isinstance(value, (str)):
                raise ValueError("'value' must be a string")

            match value.lower():
                case "store" | "stored" | "none":
                    result = _zipfile().ZIP_STORED

                case "deflate" | "deflated":
                    result = _zipfile().ZIP_DEFLATED

                case "bz2" | "bzip2":
                    result = _zipfile().ZIP_BZIP2

                case "lzma" | "xz":
                    result = _zipfile().ZIP_LZMA

                case _:
                    result = ""

            return result

        def extract_path(
            self,
            archive_path,
            destination_path,
            overwrite=False,
        ):
            if not isinstance(archive_path, (str, _pathlib().Path)):
                raise TypeError("")

            if not isinstance(destination_path, (str, _pathlib().Path)):
                raise TypeError("")

            if not isinstance(overwrite, (bool)):
                raise TypeError("")

            fs_archive_path = _pathlib().Path(archive_path)
            fs_destination_path = _pathlib().Path(
                destination_path,
            ).resolve()

            fs_destination_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            with _zipfile().ZipFile(
                fs_archive_path,
                "r",
            ) as archive:
                for member in archive.infolist():
                    target = (
                        fs_destination_path
                        / member.filename
                    ).resolve()

                    if (
                        fs_destination_path not in target.parents
                        and target != fs_destination_path
                    ):
                        raise ValueError("")

                    if not overwrite and target.exists():
                        continue

                    archive.extract(
                        member,
                        fs_destination_path,
                    )

            return True

        def compress_paths(self, **kwargs):
            if not isinstance(kwargs, object) or not kwargs:
                raise ValueError("")

            input_filesystem_paths = kwargs.get("input_filesystem_paths", ())
            output_filesystem_paths = kwargs.get("output_filesystem_paths", ())
            excluded_filesystem_paths = kwargs.get("excluded_filesystem_paths", ())
            input_regex_patterns = kwargs.get("input_regex_patterns", ())
            excluded_regex_patterns = kwargs.get("excluded_regex_patterns", ())
            compression_format = kwargs.get("format", "zip")
            compression_type = kwargs.get("type", "deflated")
            compression_level = kwargs.get("level", 6)
            is_zip_64_allowed = kwargs.get("is_zip_64_allowed", True)
            is_timestamp_strict = kwargs.get("is_timestamp_strict", True)

            if not input_filesystem_paths:
                raise ValueError("")

            if not output_filesystem_paths:
                raise ValueError("")

            def normalize(value):
                if isinstance(value, (str, _pathlib().Path)):
                    return (value,)
                return tuple(value)

            input_filesystem_paths = normalize(input_filesystem_paths)
            output_filesystem_paths = normalize(output_filesystem_paths)
            excluded_filesystem_paths = normalize(excluded_filesystem_paths)
            input_regex_patterns = normalize(input_regex_patterns)
            excluded_regex_patterns = normalize(excluded_regex_patterns)

            if len(input_filesystem_paths) != len(output_filesystem_paths):
                raise ValueError("")

            if not isinstance(compression_format, str):
                return False

            if compression_format.lower() != "zip":
                return False

            if not isinstance(compression_type, str):
                return False

            normalized_type = compression_type.lower()
            compression_method = (
                self.get_zip_format_compression(
                    normalized_type
                )
            )

            if not compression_method:
                return False

            if (
                not isinstance(compression_level, int)
                or isinstance(compression_level, bool)
            ):
                return False

            if not isinstance(is_zip_64_allowed, bool):
                return False

            if not isinstance(is_timestamp_strict, bool):
                return False

            input_patterns = tuple(
                _re().compile(pattern) for pattern in input_regex_patterns
            )
            excluded_patterns = tuple(
                _re().compile(pattern) for pattern in excluded_regex_patterns
            )

            def absolute_path(value):
                return _pathlib().Path(_os().path.abspath(_os().fspath(value)))

            def is_within(path, parent):
                return path == parent or path.is_relative_to(parent)

            current_path = absolute_path(_pathlib().Path.cwd())
            excluded_paths = {
                current_path,
                *(absolute_path(path) for path in excluded_filesystem_paths),
            }

            operations = []

            for input_path, output_path in zip(
                input_filesystem_paths,
                output_filesystem_paths,
            ):
                source = absolute_path(input_path)
                destination = absolute_path(output_path)

                if not source.exists() and not source.is_symlink():
                    return False

                if source.is_symlink():
                    return False

                if not source.is_file() and not source.is_dir():
                    return False

                if destination.exists() or destination.is_symlink():
                    return False

                if source == destination:
                    return False

                if source.is_dir() and is_within(destination, source):
                    return False

                if any(is_within(source, excluded) for excluded in excluded_paths):
                    return False

                selected_files = []

                if source.is_dir():
                    for path in source.rglob("*"):
                        if path.is_symlink() or not path.is_file():
                            continue

                        absolute_file_path = absolute_path(path)

                        if any(
                            is_within(absolute_file_path, excluded)
                            for excluded in excluded_paths
                        ):
                            continue

                        relative_path = path.relative_to(source).as_posix()

                        if input_patterns and not any(
                            pattern.search(relative_path)
                            for pattern in input_patterns
                        ):
                            continue

                        if any(
                            pattern.search(relative_path)
                            for pattern in excluded_patterns
                        ):
                            continue

                        selected_files.append((path, relative_path))

                else:
                    relative_path = source.name

                    if input_patterns and not any(
                        pattern.search(relative_path)
                        for pattern in input_patterns
                    ):
                        continue

                    if any(
                        pattern.search(relative_path)
                        for pattern in excluded_patterns
                    ):
                        continue

                    selected_files.append((source, relative_path))

                operations.append((destination, selected_files))

            for destination, selected_files in operations:
                destination.parent.mkdir(parents=True, exist_ok=True)

                temporary_path = None

                try:
                    with _tempfile().NamedTemporaryFile(
                        dir=destination.parent,
                        prefix=f".{destination.name}.",
                        suffix=".tmp",
                        delete=False,
                    ) as temporary_file:
                        temporary_path = _pathlib().Path(temporary_file.name)

                    with _zipfile().ZipFile(
                        temporary_path,
                        mode="w",
                        compression=compression_method,
                        compresslevel=(
                            compression_level,
                        ),
                        allowZip64=is_zip_64_allowed,
                        strict_timestamps=is_timestamp_strict,
                    ) as archive:
                        for source, archive_name in selected_files:
                            archive.write(source, arcname=archive_name)

                    if destination.exists() or destination.is_symlink():
                        return False

                    _os().replace(temporary_path, destination)
                    temporary_path = None

                finally:
                    if temporary_path is not None:
                        try:
                            temporary_path.unlink()
                        except OSError:
                            pass

            return True
            

    _FilesystemCompressionManager = __FilesystemCompressionManager
    _allocate = lambda: None


def FilesystemCompressionManager():
    if _FilesystemCompressionManager is None:
        _allocate()

    return _FilesystemCompressionManager


# FilesystemCompressionManager()
