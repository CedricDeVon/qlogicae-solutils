from __future__ import annotations

import re
import sys
import shlex
import shutil
import argparse
import subprocess
from pathlib import Path
from collections.abc import Sequence


def parse_bool(value: str) -> bool:
    normalized = value.lower()

    if normalized not in {"true", "false"}:
        raise argparse.ArgumentTypeError(
            "Expected 'true' or 'false'."
        )

    return normalized == "true"


def normalize_path(value: str | Path) -> Path:
    return Path(value).resolve(strict=False)


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_unprotected_filesystem_paths(
    paths: Sequence[str | Path],
    protected_paths: Sequence[str],
) -> None:
    protected = [
        normalize_path(path)
        for path in protected_paths
    ]

    for value in paths:
        path = normalize_path(value)

        for protected_path in protected:
            if (
                is_within(path, protected_path)
                or is_within(protected_path, path)
            ):
                raise PermissionError(
                    f"Operation rejected: {value!s} overlaps "
                    f"protected path {protected_path!s}."
                )


def validate_sources(
    paths: Sequence[str],
    is_required: bool,
) -> list[Path]:
    result: list[Path] = []

    for value in paths:
        path = Path(value)

        if not path.exists() and not path.is_symlink():
            if is_required:
                raise FileNotFoundError(value)
            continue

        result.append(path)

    return result


def create_filesystem_path(
    paths: Sequence[str],
) -> None:
    for value in paths:
        path = Path(value)

        if path.exists():
            continue

    for value in paths:
        path = Path(value)

        if not path.exists():
            path.mkdir(parents=True, exist_ok=False)


def run_script(
    targets: Sequence[str],
    is_atmoic: bool,
) -> None:
    for target in targets:
        command = target.strip()

        if not command:
            raise ValueError("Commands must not be empty.")

        result = subprocess.run(
            shlex.split(command),
            check=False,
        )

        if result.returncode != 0:
            message = (
                f"Command failed with exit code "
                f"{result.returncode}: {target}"
            )

            if is_atmoic:
                print(
                    f"warning: {message}",
                    file=sys.stderr,
                )
                continue

            raise RuntimeError(message)


def remove_filesystem_path(
    included: Sequence[str],
    excluded: Sequence[str],
    is_recursive: bool,
) -> None:
    existing = validate_sources(included, False)
    validate_unprotected_filesystem_paths(existing, excluded)

    for path in existing:
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            if is_recursive:
                shutil.rmtree(path)
            else:
                path.rmdir()
        else:
            raise OSError(
                f"Unsupported filesystem path: {path}"
            )


def rename_filesystem_path(
    source: str,
    target: str,
) -> None:
    source = Path(source)
    target = Path(target)

    if not source.exists() and not source.is_symlink():
        return

    if target.exists() or target.is_symlink():
        raise FileExistsError(target)

    validate_unprotected_filesystem_paths(
        [source, target],
        [],
    )

    source.rename(target)


def move_filesystem_path(
    source: str,
    target: str,
) -> None:
    source = Path(source)
    target = Path(target)

    if not source.exists() and not source.is_symlink():
        return

    if target.exists() or target.is_symlink():
        raise FileExistsError(target)

    validate_unprotected_filesystem_paths(
        [source, target],
        [],
    )

    shutil.move(str(source), str(target))


def copy_filesystem_paths(
    sources: Sequence[str],
    targets: Sequence[str],
) -> None:
    pairs: list[tuple[Path, Path]] = []

    for source_value in sources:
        source = Path(source_value)

        if not source.exists() and not source.is_symlink():
            continue

        if not source.is_file() and not source.is_dir() and not source.is_symlink():
            raise OSError(
                f"Unsupported source path: {source}"
            )

        for target_value in targets:
            target = Path(target_value) / source.name

            if target.exists() or target.is_symlink():
                raise FileExistsError(target)

            pairs.append((source, target))

    validate_unprotected_filesystem_paths(
        [
            path
            for pair in pairs
            for path in pair
        ],
        [],
    )

    for target_value in targets:
        Path(target_value).mkdir(
            parents=True,
            exist_ok=True,
        )

    for source, target in pairs:
        if source.is_symlink():
            target.symlink_to(
                source.readlink(),
                target_is_directory=source.is_dir(),
            )
        elif source.is_dir():
            shutil.copytree(source, target)
        elif source.is_file():
            shutil.copy2(source, target)


def build_parser() -> argparse.ArgumentParser:
    console_parser = argparse.ArgumentParser(
        prog="cli",        
        description="Redundant CLI Commands For QLogicae Projects",
    )
    commands = console_parser.add_subparsers(
        dest="command",
        metavar="",
    )



    run_command = commands.add_parser(
        "run-script",
        help="run scripts",
    )
    run_command.add_argument(
        "--targets",
        "-t",
        dest="targets",
        help="one or more target scripts",
        nargs="+",
        default=tuple(),
        required=True,
    )
    run_command.add_argument(
        "--is-atmoic",
        "-ia",
        dest="is_atmoic",
        help="continue executing scripts after failed execution",
        type=parse_bool,
        default=True,
        metavar="{true,false}",
    )



    create_command = commands.add_parser(
        "create-filesystem-path",
        help="create filesystem paths",
    )
    create_command.add_argument(
        "--targets",
        "-t",
        dest="targets",
        help="one or more target filesystem paths",
        nargs="+",
        default=tuple(),
        required=True,
    )



    remove_command = commands.add_parser(
        "remove-filesystem-path",
        help="remove filesystem paths",
    )
    remove_command.add_argument(
        "--targets",
        "-t",
        dest="targets",
        help="one or more targets filesystem paths",
        nargs="+",
        default=tuple(),
        required=True,
    )
    remove_command.add_argument(
        "--is-recursive",
        "-ir",
        dest="is_recursive",
        help="to include child filesystem paths",
        type=parse_bool,
        default=False,
        metavar="{true,false}",
    )



    rename_command = commands.add_parser(
        "rename-filesystem-path",
        help="rename filesystem paths",
    )
    rename_command.add_argument(
        "--source",
        "-s",
        dest="source",
        help="source filesystem path",
        required=True
    )
    rename_command.add_argument(
        "--target",
        "-t",
        dest="target",
        help="target filesystem path",
        required=True
    )



    move_command = commands.add_parser(
        "move-filesystem-path",
        help="move filesystem paths",
    )
    move_command.add_argument(
        "--source",
        "-s",
        dest="source",
        help="one source filesystem path",
        required=True
    )
    move_command.add_argument(
        "--target",
        "-t",
        dest="target",
        help="one target filesystem path",
        required=True
    )



    copy_command = commands.add_parser(
        "copy-filesystem-path",
        help="copy filesystem paths",
    )
    copy_command.add_argument(
        "--sources",
        "-s",
        dest="sources",
        help="one or more source filesystem paths",
        nargs="+",
        default=tuple(),
        required=True,
    )
    copy_command.add_argument(
        "--targets",
        "-t",
        dest="targets",
        help="one or more target filesystem paths",
        nargs="+",
        default=tuple(),
        required=True,
    )

    return console_parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        console_parser = build_parser()
        console_arguments = console_parser.parse_args(argv)

        if console_arguments.command in {
            "run-script",
        }:
            run_script(
                console_arguments.targets,
                console_arguments.is_atmoic,
            )

        elif console_arguments.command in {
            "create-filesystem-path",
        }:
            create_filesystem_path(
                console_arguments.targets,
            )

        elif console_arguments.command in {
            "remove-filesystem-path",
        }:
            remove_filesystem_path(
                console_arguments.targets,
                console_arguments.is_recursive,
            )

        elif console_arguments.command in {
            "rename-filesystem-path",
        }:
            rename_filesystem_path(
                console_arguments.source,
                console_arguments.target,
            )

        elif console_arguments.command in {
            "move-filesystem-path",
        }:
            move_filesystem_path(
                console_arguments.source,
                console_arguments.target,
            )

        elif console_arguments.command in {
            "copy-filesystem-path",
        }:
            copy_filesystem_paths(
                console_arguments.sources,
                console_arguments.targets,
            )
                
        return 0

    except (OSError, ValueError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
