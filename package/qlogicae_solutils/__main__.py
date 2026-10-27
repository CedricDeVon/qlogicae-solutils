from __future__ import annotations

import subprocess
import sys

from pathlib import Path


def main() -> int:
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parent.resolve() / "v0" / "__main__.py"),
            *sys.argv[1:],
        ],
        check=False,
    )

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
