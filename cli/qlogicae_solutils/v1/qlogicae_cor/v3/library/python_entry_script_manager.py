__all__ = (
    "run_script",
)

_sys = None
_pathlib = None
_subprocess = None


def run_script(
    script_filesystem_path,
    executable_filesystem_path,
):
    global _sys
    global _pathlib
    global _subprocess

    if (
        not script_filesystem_path or
        not isinstance(script_filesystem_path, (object))
    ):
        raise TypeError("")

    if (
        not isinstance(executable_filesystem_path, (tuple, list)) or
        not executable_filesystem_path
    ):
        raise TypeError("")

    if not _sys:
        import subprocess  # nosec B404
        import sys  # nosec B404
        import pathlib

        _sys = (
            sys
        )
        _subprocess = (
            subprocess
        )
        _pathlib = (
            pathlib
        )

    try:
        result = (
            _subprocess.run( # nosec B603
                [
                    _sys.executable,
                    str(_pathlib.Path(
                        script_filesystem_path
                    ).resolve().parent / _pathlib.Path(
                        *executable_filesystem_path
                    )),
                    *_sys.argv[1:],
                ],
                check=False, # nosec B603
                shell=False, # nosec B603
            )
        )
        return (
            result.returncode
        )

    except (OSError, ValueError, RuntimeError) as error:
        print(f"{error}", file=sys.stderr)
        
        return 1
    

