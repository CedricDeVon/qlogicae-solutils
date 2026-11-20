__all__ = (
    "FilesystemManager",
)

_os = None
_re = None
_shutil = None
_pathlib = None
_FilesystemManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _FilesystemManager

    class __FilesystemManager:
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
            global _shutil
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
            _shutil = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="shutil",
                )
            )
            _pathlib = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="pathlib",
                )
            )

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True

        def throw_if_filesystem_path_invalid(self, value):
            if not isinstance(value, (str, _pathlib().Path)):
                raise ValueError("'value' must either be a string or Path")

            path = _pathlib().Path(value)

            if not path.exists():
                raise ValueError(
                    f"filesystem path '{path}' is invalid"
                )

            return False

        def throw_if_file_path_invalid(self, value):
            if not isinstance(value, (str, _pathlib().Path)):
                raise ValueError("'value' must either be a string or Path")

            path = _pathlib().Path(value)

            if not path.is_file():
                raise ValueError(
                    f"file path '{path}' is invalid"
                )

            return False

        def throw_if_folder_path_invalid(self, value):
            if not isinstance(value, (str, _pathlib().Path)):
                raise ValueError("'value' must either be a string or Path")

            path = _pathlib().Path(value)

            if not path.is_dir():
                raise ValueError(
                    f"folder path '{path}' is invalid"
                )

            return False

        def is_filesystem_path_valid(self, value):
            if not isinstance(value, (str, _pathlib().Path)):
                raise ValueError("'value' must either be a string or Path")

            result = _pathlib().Path(value).exists()
            return result

        def is_file_path_valid(self, value):
            if not isinstance(value, (str, _pathlib().Path)):
                raise ValueError("'value' must either be a string or Path")

            result = _pathlib().Path(value).is_file()
            return result

        def is_folder_path_valid(self, value):
            if not isinstance(value, (str, _pathlib().Path)):
                raise ValueError("'value' must either be a string or Path")

            result = _pathlib().Path(value).is_dir()
            return result

        def create_files(self, **kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("'kwargs' must be defined")

            target_filesystem_paths = kwargs.get(
                "target_filesystem_paths",
                ()
            ) or ()
            content = kwargs.get("content", "") or ""
            is_overwrite_enabled = kwargs.get(
                "is_overwrite_enabled",
                False
            )
            encoding = kwargs.get(
                "encoding",
                "utf-8"
            ) or "utf-8"

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            if not isinstance(content, str):
                raise TypeError("'content' must be a string")

            if not isinstance(is_overwrite_enabled, bool):
                raise TypeError("'is_overwrite_enabled' must be a boolean")

            for target_filesystem_path in target_filesystem_paths:
                if not target_filesystem_path:
                    raise TypeError("'is_overwrite_enabled' must be a boolean")

                path = _pathlib().Path(target_filesystem_path)

                path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                if path.exists() and not is_overwrite_enabled:
                    continue

                path.write_text(
                    content,
                    encoding=encoding
                )
            
            return True

        def create_folders(self, **kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("'kwargs' must be defined")

            target_filesystem_paths = kwargs.get(
                "target_filesystem_paths",
                ()
            ) or ()

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            for target_filesystem_path in target_filesystem_paths:
                if not target_filesystem_path:
                    continue
                    
                _pathlib().Path(target_filesystem_path).mkdir(
                    parents=True,
                    exist_ok=True
                )
            
            return True

        def remove_paths(self, **kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("'kwargs' must be defined")

            target_filesystem_paths = kwargs.get("target_filesystem_paths", ()) or ()
            target_regex_patterns = kwargs.get("target_regex_patterns", ()) or ()
            excluded_filesystem_paths = kwargs.get("excluded_filesystem_paths", ()) or ()
            excluded_regex_patterns = kwargs.get("excluded_regex_patterns", ()) or ()

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            def normalize(value):
                if isinstance(value, (str, _pathlib().Path)):
                    return (value,)
                return tuple(value)

            target_filesystem_paths = normalize(target_filesystem_paths)
            target_regex_patterns = normalize(target_regex_patterns)
            excluded_filesystem_paths = normalize(excluded_filesystem_paths)
            excluded_regex_patterns = normalize(excluded_regex_patterns)

            target_patterns = tuple(_re().compile(pattern) for pattern in target_regex_patterns)
            excluded_patterns = tuple(_re().compile(pattern) for pattern in excluded_regex_patterns)

            def absolute_path(value):
                return _pathlib().Path(_os().path.abspath(_os().fspath(value)))

            current_path = absolute_path(_pathlib().Path.cwd())
            excluded_paths = {
                current_path,
                *(absolute_path(path) for path in excluded_filesystem_paths),
            }

            def is_within(path, parent):
                return path == parent or path.is_relative_to(parent)

            def is_excluded(path, root):
                if any(is_within(path, excluded) for excluded in excluded_paths):
                    return True

                if any(is_within(excluded, path) for excluded in excluded_paths):
                    return True

                relative_path = path.relative_to(root).as_posix()

                return any(
                    pattern.search(relative_path)
                    for pattern in excluded_patterns
                )

            def remove_path(path, root, inherited_selection=False):
                if is_excluded(path, root):
                    return False

                relative_path = path.relative_to(root).as_posix()

                is_selected = (
                    inherited_selection
                    or not target_patterns
                    or any(pattern.search(relative_path) for pattern in target_patterns)
                )

                if path.is_symlink() or not path.is_dir():
                    if is_selected:
                        path.unlink()
                        return True
                    return False

                is_modified = False

                for child in path.iterdir():
                    if remove_path(child, root, is_selected):
                        is_modified = True

                if is_selected or is_modified:
                    try:
                        path.rmdir()
                        return True
                    except OSError:
                        pass

                return is_modified

            for target in target_filesystem_paths:
                root = absolute_path(target)

                if not root.exists() and not root.is_symlink():
                    continue

                if any(is_within(root, excluded) for excluded in excluded_paths):
                    continue

                if any(is_within(excluded, root) for excluded in excluded_paths):
                    if root.is_dir() and not root.is_symlink():
                        for child in root.iterdir():
                            remove_path(child, root, False)
                        continue
                    continue

                remove_path(root, root)

            return True

        def move_path(self, **kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("'kwargs' must be defined")

            input_filesystem_path = kwargs.get("input_filesystem_path", "") or ""
            output_filesystem_path = kwargs.get("output_filesystem_path", "") or ""
            input_regex_patterns = kwargs.get("input_regex_patterns", ()) or ()

            if not input_filesystem_path:
                raise ValueError("'input_filesystem_path' must be defined")

            if not output_filesystem_path:
                raise ValueError("'output_filesystem_path' must be defined")

            if isinstance(input_regex_patterns, str):
                input_regex_patterns = (input_regex_patterns,)

            source = _pathlib().Path(_os().path.abspath(_os().fspath(input_filesystem_path)))
            destination = _pathlib().Path(_os().path.abspath(_os().fspath(output_filesystem_path)))

            if not source.exists() and not source.is_symlink():
                return False

            if source == destination:
                return False

            patterns = tuple(_re().compile(pattern) for pattern in input_regex_patterns)

            if not patterns:
                if source.is_dir() and not source.is_symlink():
                    if destination.is_relative_to(source):
                        return False

                if destination.exists() or destination.is_symlink():
                    return False

                destination.parent.mkdir(parents=True, exist_ok=True)
                _shutil().move(str(source), str(destination))
                return True

            if not source.is_dir() or source.is_symlink():
                return False

            if destination.is_relative_to(source):
                return False

            if destination.exists() and not destination.is_dir():
                return False

            selected_paths = []

            for path in source.rglob("*"):
                relative_path = path.relative_to(source).as_posix()

                if any(pattern.search(relative_path) for pattern in patterns):
                    selected_paths.append(path)

            selected_paths.sort(key=lambda path: (len(path.parts), path.as_posix()))

            filtered_paths = []

            for path in selected_paths:
                if any(path.is_relative_to(parent) for parent in filtered_paths):
                    continue
                filtered_paths.append(path)

            operations = []

            for path in filtered_paths:
                relative_path = path.relative_to(source)
                target = destination / relative_path

                if target.exists() or target.is_symlink():
                    return False

                operations.append((path, target))

            for path, target in operations:
                target.parent.mkdir(parents=True, exist_ok=True)
                _shutil().move(str(path), str(target))

            for path in sorted(
                source.rglob("*"),
                key=lambda item: len(item.parts),
                reverse=True,
            ):
                if path.is_dir() and not path.is_symlink():
                    try:
                        path.rmdir()
                    except OSError:
                        pass

            try:
                source.rmdir()
            except OSError:
                pass

            return True

        def copy_paths(self, **kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("'kwargs' must be defined")

            input_filesystem_paths = kwargs.get("input_filesystem_paths", ()) or ()
            output_filesystem_paths = kwargs.get("output_filesystem_paths", ()) or ()
            input_regex_patterns = kwargs.get("input_regex_patterns", ()) or ()

            if not input_filesystem_paths:
                raise ValueError("'input_filesystem_paths' must be defined")

            if not output_filesystem_paths:
                raise ValueError("'output_filesystem_paths' must be defined")

            def normalize(value):
                if isinstance(value, (str, _pathlib().Path)):
                    return (value,)
                return tuple(value)

            input_filesystem_paths = normalize(input_filesystem_paths)
            output_filesystem_paths = normalize(output_filesystem_paths)
            input_regex_patterns = normalize(input_regex_patterns)

            if len(input_filesystem_paths) != len(output_filesystem_paths):
                raise ValueError(
                    "'input_filesystem_paths' and 'output_filesystem_paths' "
                    "must contain the same number of paths"
                )

            patterns = tuple(_re().compile(pattern) for pattern in input_regex_patterns)

            def copy_item(source, destination):
                if destination.exists() or destination.is_symlink():
                    raise FileExistsError(str(destination))

                destination.parent.mkdir(parents=True, exist_ok=True)

                if source.is_symlink():
                    _os().symlink(_os().readlink(source), destination)
                elif source.is_dir():
                    _shutil().copytree(source, destination, symlinks=True)
                else:
                    _shutil().copy2(source, destination, follow_symlinks=False)

            operations = []

            for input_path, output_path in zip(
                input_filesystem_paths,
                output_filesystem_paths,
            ):
                source = _pathlib().Path(_os().path.abspath(_os().fspath(input_path)))
                destination = _pathlib().Path(_os().path.abspath(_os().fspath(output_path)))

                if not source.exists() and not source.is_symlink():
                    return False

                if source == destination:
                    return False

                if source.is_dir() and not source.is_symlink():
                    if destination.is_relative_to(source):
                        return False

                    if source.is_relative_to(destination):
                        return False

                    if not patterns:
                        operations.append((source, destination, True))
                        continue

                    selected_paths = []

                    for path in source.rglob("*"):
                        relative_path = path.relative_to(source).as_posix()

                        if any(pattern.search(relative_path) for pattern in patterns):
                            selected_paths.append(path)

                    selected_paths.sort(
                        key=lambda path: (len(path.parts), path.as_posix())
                    )

                    filtered_paths = []

                    for path in selected_paths:
                        if any(path.is_relative_to(parent) for parent in filtered_paths):
                            continue
                        filtered_paths.append(path)

                    for path in filtered_paths:
                        target = destination / path.relative_to(source)
                        operations.append((path, target, path.is_dir() and not path.is_symlink()))

                else:
                    if patterns:
                        return False

                    operations.append((source, destination, False))

            for source, destination, is_directory in operations:
                if destination.exists() or destination.is_symlink():
                    return False

                if is_directory:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    _shutil().copytree(source, destination, symlinks=True)
                else:
                    copy_item(source, destination)

            return True

        def list_paths(self, **kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise ValueError("'kwargs' must be defined")

            target_filesystem_paths = kwargs.get(
                "target_filesystem_paths",
                ()
            ) or ()
            target_regex_patterns = kwargs.get(
                "target_regex_patterns",
                ()
            ) or ()

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            if isinstance(target_filesystem_paths, str):
                target_filesystem_paths = (target_filesystem_paths,)

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            compiled_patterns = tuple(
                _re().compile(pattern)
                for pattern in target_regex_patterns
            )

            results = set()
            for target_filesystem_path in target_filesystem_paths:
                root = _pathlib().Path(target_filesystem_path)

                if not root.exists() and not root.is_symlink():
                    continue

                if root.is_file() or root.is_symlink():
                    if not compiled_patterns or any(
                        pattern.search(root.name)
                        for pattern in compiled_patterns
                    ):
                        results.push(root)
                    continue

                for path in sorted(root.rglob("*")):
                    relative_path = path.relative_to(root).as_posix()

                    if compiled_patterns and not any(
                        pattern.search(relative_path)
                        for pattern in compiled_patterns
                    ):
                        continue

                    results.push(root)

            return results
            
        


    _FilesystemManager = __FilesystemManager
    _allocate = lambda: None


def FilesystemManager():
    if _FilesystemManager is None:
        _allocate()

    return _FilesystemManager


# FilesystemManager()

# def clean_filesystem_path(self, value):
#     if not isinstance(value, (str, _pathlib().Path)):
#         raise ValueError("'value' must either be a string or Path")

#     directory = _pathlib().Path(value).resolve()

#     protected_paths = {
#         _pathlib().Path(""),
#         _pathlib().Path("/"),
#         _pathlib().Path.home(),
#     }

#     if directory in protected_paths:
#         raise ValueError(
#             f"folder path '{value}' is protected"
#         )

#     if not directory.exists():
#         return True

#     if not directory.is_dir():
#         raise ValueError(
#             f"file path '{value}' is not a folder"
#         )

#     for item in directory.iterdir():
#         if item.is_file() or item.is_symlink():
#             item.unlink()

#         elif item.is_dir():
#             _shutil().rmtree(item)

#     return True

# def copy_filesystem_path(
#     self,
#     first_path,
#     second_path,
# ):
#     if not isinstance(first_path, (str, _pathlib().Path)):
#         raise ValueError("'first_path' must either be a string or Path")

#     if not isinstance(second_path, (str, _pathlib().Path)):
#         raise ValueError("'second_path' must either be a string or Path")

#     fs_first_path = _pathlib().Path(first_path)
#     fs_second_path = _pathlib().Path(second_path)

#     if fs_first_path.is_dir():
#         _shutil().copytree(
#             fs_first_path,
#             fs_second_path,
#             dirs_exist_ok=True,
#         )

#     elif fs_first_path.is_file():
#         fs_second_path.parent.mkdir(
#             parents=True,
#             exist_ok=True,
#         )

#         _shutil().copy2(
#             fs_first_path,
#             fs_second_path,
#         )

#     else:
#         return False

#     return True

# def move_filesystem_path(
#     self,
#     first_path,
#     second_path,
# ):
#     if not isinstance(first_path, (str, _pathlib().Path)):
#         raise ValueError("'first_path' must either be a string or Path")

#     if not isinstance(second_path, (str, _pathlib().Path)):
#         raise ValueError("'second_path' must either be a string or Path")

#     source = _pathlib().Path(first_path)
#     destination = _pathlib().Path(second_path)

#     destination.parent.mkdir(
#         parents=True,
#         exist_ok=True,
#     )

#     _shutil().move(
#         str(source),
#         str(destination),
#     )

#     return True

# def rename_filesystem_entity(
#     self,
#     source,
#     destination,
# ):
#     if not isinstance(source, (str, _pathlib().Path)):
#         raise ValueError("'source' must either be a string or Path")

#     if not isinstance(destination, (str, _pathlib().Path)):
#         raise ValueError("'destination' must either be a string or Path")

#     _pathlib().Path(source).rename(destination)

#     return True

# def setup_filesystem_tree_path(self, directory):
#     if not isinstance(directory, (str, _pathlib().Path)):
#         raise ValueError("'directory' must either be a string or Path")

#     _pathlib().Path(directory).mkdir(
#         parents=True,
#         exist_ok=True,
#     )

#     return True
