__all__ = (
    "PythonModuleManager",
)

_PythonModuleManager = None
_ExternalDependencyManager = None

_sys = None
_pathlib = None
_importlib_util = None


def _allocate():
    global _allocate
    global _PythonModuleManager

    from .abstract_manager import AbstractManager

    class __PythonModuleManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _sys
                global _pathlib
                global _importlib_util

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _sys = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="sys",
                    )
                )
                _pathlib = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="pathlib",
                    )
                )
                _importlib_util = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="importlib.util",
                    )
                )

            return True

        def read_imported_modules(
            self,
            target_filesystem_paths,
            is_recursive=True,
        ):
            if not isinstance(target_filesystem_paths, (tuple, list)):
                raise TypeError("")

            if not isinstance(is_recursive, (bool)):
                raise TypeError("")

            if not target_filesystem_paths:
                return tuple()

            folder_paths = tuple(
                dict.fromkeys(
                    (
                        _pathlib().Path.cwd() / path
                    ).resolve()
                    for path in target_filesystem_paths
                )
            )

            modules = []
            imported_file_paths = set()

            for folder_path in folder_paths:
                if not folder_path.is_dir():
                    continue

                file_paths = (
                    folder_path.rglob("*.py")
                    if is_recursive
                    else folder_path.glob("*.py")
                )

                for file_path in sorted(file_paths):
                    resolved_file_path = file_path.resolve()

                    if resolved_file_path in imported_file_paths:
                        continue

                    imported_file_paths.add(resolved_file_path)

                    relative_path = file_path.relative_to(folder_path)

                    if file_path.name == "__init__.py":
                        module_parts = relative_path.parent.parts
                    else:
                        module_parts = (
                            *relative_path.parent.parts,
                            file_path.stem,
                        )

                    if not module_parts:
                        continue

                    module_name = ".".join(module_parts)

                    spec = _importlib_util().spec_from_file_location(
                        module_name,
                        file_path,
                    )

                    if spec is None or spec.loader is None:
                        raise ImportError("")

                    module = _importlib_util().module_from_spec(spec)

                    _sys().modules[module_name] = module

                    try:
                        spec.loader.exec_module(module)

                    except BaseException:
                        _sys().modules.pop(module_name, None)
                        raise

                    modules.append(module)

            return tuple(modules)

        def read_loaded_modules(self):
            return (
                module_name
                for module_name in _sys().modules
            )


    _PythonModuleManager = __PythonModuleManager
    _allocate = lambda: None


def PythonModuleManager():
    if _PythonModuleManager is None:
        _allocate()

    return _PythonModuleManager


# PythonModuleManager()
