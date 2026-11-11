from __future__ import annotations

from typing import Any

__all__ = (
    "DependencyManager"
)

_sys: Any = None
_types: Any = None
_shlex: Any = None
_shutil: Any = None
_pathlib: Any = None
_argparse: Any = None
_subprocess: Any = None
_collections: Any = None
_importlib_util: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports

    global _sys
    global _shlex
    global _shutil
    global _pathlib
    global _argparse
    global _subprocess
    global _collections
    global _importlib_util

    import argparse
    import collections
    import importlib.util
    import pathlib
    import shlex
    import shutil
    import subprocess  # nosec B404
    import sys

    _sys = sys
    _shlex = shlex
    _shutil = shutil
    _pathlib = pathlib
    _argparse = argparse
    _subprocess = subprocess
    _collections = collections
    _importlib_util = importlib.util

    _handle_dynamic_imports = lambda: None


class DependencyManager:
    _singleton: Any = None

    def __init__(self) -> None:
        _handle_dynamic_imports()

    @classmethod
    def singleton(cls) -> Any:
        if not cls._singleton:
            cls._singleton = DependencyManager()

        return (
            cls._singleton
        )

    # def read_system_std_error(self) -> Any:
    #     return _sys.stderr

    # def read_console_arguments(self) -> tuple[str, ...]:
    #     return tuple(_sys.argv[1:])

    # def split_string_to_tuple(self, **kwargs: Any) -> tuple[str, ...]:
    #     if not kwargs:
    #         return tuple()

    #     value: str = (kwargs.get("value", "") or "")
    #     if not value:
    #         return tuple()

    #     return (
    #         _shlex.split(
    #             value
    #         ),
    #     )

    def convert_filesystem_path(self, **kwargs: Any) -> str:
        if not kwargs:
            return ""

        targets: tuple[str, ...] = (kwargs.get("targets", tuple()) or tuple())
        return str(_pathlib.Path(*targets))

    # def create_filesystem_path(self, **kwargs: Any) -> bool:
    #     if not kwargs:
    #         return False

    #     target: str = (kwargs.get("target", "") or "")
    #     if not target:
    #         return False

    #     _pathlib.Path(target).mkdir(parents=True, exist_ok=True)
    #     return True

    # def remove_filesystem_path(self, **kwargs: Any) -> bool:
    #     if not kwargs:
    #         return False

    #     target: str = (kwargs.get("target", "") or "")
    #     if not target:
    #         return False

    #     _shutil.rmtree(_pathlib.Path(target))
    #     return True

    # def move_filesystem_path(self, **kwargs: Any) -> bool:
    #     if not kwargs:
    #         return False

    #     source: str = (kwargs.get("source", "") or "")
    #     if not source:
    #         return False

    #     target: str = (kwargs.get("target", "") or "")
    #     if not target:
    #         return False

    #     _shutil.move(str(_pathlib.Path(source)), str(_pathlib.Path(target)))
    #     return True

    # def copy_filesystem_folder(self, **kwargs: Any) -> bool:
    #     if not kwargs:
    #         return False

    #     source: str = (kwargs.get("source", "") or "")
    #     if not source:
    #         return False

    #     target: str = (kwargs.get("target", "") or "")
    #     if not target:
    #         return False

    #     _shutil.copytree(str(_pathlib.Path(source)), str(_pathlib.Path(target)))
    #     return True

    # def copy_filesystem_file(self, **kwargs: Any) -> bool:
    #     if not kwargs:
    #         return False

    #     source: str = (kwargs.get("source", "") or "")
    #     if not source:
    #         return False

    #     target: str = (kwargs.get("target", "") or "")
    #     if not target:
    #         return False

    #     _shutil.copy2(str(_pathlib.Path(source)), str(_pathlib.Path(target)))
    #     return True

    def read_filesystem_path_type(self) -> _pathlib.Path:
        value: Any = _pathlib.Path

        return (
            value
        )

    def setup_console_parser(self, **kwargs: Any) -> Any:
        if not kwargs:
            return {}

        list_properties: tuple[str, ...] = (
            kwargs.get("list_properties", tuple()) or tuple()
        )
        keyword_properties: dict[str, Any] = (
            kwargs.get("keyword_properties", {}) or {}
        )

        console: Any = _argparse.ArgumentParser(
            *list_properties,
            **keyword_properties
        )

        return console

    def setup_console_command_parser(self, **kwargs: Any) -> Any:
        if not kwargs:
            return {}

        console: Any = (kwargs.get("console", {}) or {})
        if not console:
            return {}

        list_properties: tuple[str, ...] = (
            kwargs.get("list_properties", tuple()) or tuple()
        )
        keyword_properties: dict[str, Any] = (
            kwargs.get("keyword_properties", {}) or {}
        )

        command_subparsers = console.add_subparsers(
            *list_properties,
            **keyword_properties
        )

        return command_subparsers

    def setup_console_sub_command_parser(self, **kwargs: Any) -> Any:
        if not kwargs:
            return {}

        console: Any = (kwargs.get("console", {}) or {})
        if not console:
            return {}

        list_properties: tuple[str, ...] = (
            kwargs.get("list_properties", tuple()) or tuple()
        )
        keyword_properties: dict[str, Any] = (
            kwargs.get("keyword_properties", {}) or {}
        )

        command_parser = console.add_parser(
            *list_properties,
            **keyword_properties
        )

        return command_parser

    def setup_console_command_argument(self, **kwargs: Any) -> bool:
        if not kwargs:
            return False

        console: Any = (kwargs.get("console", {}) or {})
        if not console:
            return False

        list_properties: tuple[str, ...] = (
            kwargs.get("list_properties", tuple()) or tuple()
        )
        keyword_properties: dict[str, Any] = (
            kwargs.get("keyword_properties", {}) or {}
        )

        console.add_argument(
            *list_properties,
            **keyword_properties
        )

        return True

    def setup_console_command_method_handler(self, **kwargs: Any) -> bool:
        if not kwargs:
            return False

        console: Any = (kwargs.get("console", {}) or {})
        if not console:
            return False

        keyword_properties: dict[str, Any] = (
            kwargs.get("keyword_properties", {}) or {}
        )

        console.set_defaults(
            **keyword_properties
        )

        return True

    def run_subprocess(self, **kwargs: Any) -> Any:
        if not kwargs:
            return {}

        command_list: tuple[str, ...] = (
            kwargs.get("command_list", tuple()) or tuple()
        )
        if not command_list:
            return {}

        output: Any = ( # nosec B603
            _subprocess.run(
                command_list,
                check=False,
                shell=False,
            )
        )

        return (
            output
        )

    def read_subprocess_result_return_code(self, **kwargs: Any) -> Any:
        if not kwargs:
            return {}

        result: Any = (kwargs.get("result", {}) or {})

        return int(
            result.returncode
        )

    def read_working_console_filesystem_path(self) -> str:
        output: str = str(
            _pathlib.Path.cwd()
        )

        return output

    # def read_entry_script_filesystem_path(self) -> str:
    #     output: str = str(
    #         _pathlib.Path(_sys.argv[0]).resolve()
    #     )

    #     return output

    def read_entry_script_folder_path(self) -> str:
        output: str = str(
            _pathlib.Path(_sys.argv[0]).resolve().parent
        )

        return output

    def import_modules(
        self,
        **kwargs: Any,
    ) -> tuple[Any, ...]:
        target_filesystem_path: str = kwargs.get("target_filesystem_path", "") or ""
        if not target_filesystem_path:
            return tuple()

        excluded_filesystem_paths: tuple[str, ...] = (
            kwargs.get("excluded_filesystem_paths", tuple()) or tuple()
        )

        is_recursive: bool = kwargs.get("is_recursive", True)
        folder_path: _pathlib.Path = _pathlib.Path(
            (_pathlib.Path.cwd() / target_filesystem_path).resolve()
        )
        excluded_paths: Any = {
            (folder_path / path).resolve()
            for path in excluded_filesystem_paths
        }

        modules: list[Any] = []

        file_paths: Any = (
            folder_path.rglob("*.py")
            if is_recursive
            else folder_path.glob("*.py")
        )

        for file_path in sorted(file_paths):
            resolved_file_path = file_path.resolve()

            if resolved_file_path in excluded_paths:
                continue

            if any(
                path in excluded_paths
                for path in resolved_file_path.parents
            ):
                continue

            relative_path = file_path.relative_to(folder_path)

            if file_path.name == "__init__.py":
                module_parts = relative_path.parent.parts
            else:
                module_parts = (*relative_path.parent.parts, file_path.stem)

            if not module_parts:
                continue

            module_name = ".".join(module_parts)
            spec = _importlib_util.spec_from_file_location(module_name, file_path)

            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module from {file_path}")

            module = _importlib_util.module_from_spec(spec)
            _sys.modules[module_name] = module

            try:
                spec.loader.exec_module(module)

            except BaseException:
                _sys.modules.pop(module_name, None)
                raise

            modules.append(module)

        return tuple(modules)
