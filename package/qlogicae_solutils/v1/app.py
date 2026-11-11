from __future__ import annotations


def main() -> int:
    from qlogicae_solutils.library.console_manager import ConsoleManager

    console_manager_singleton = (
        ConsoleManager
            .singleton()
    )

    console_return_code: int = (
        console_manager_singleton
            .run()
    )

    return (
        console_return_code
    )


if __name__ == "__main__":
    raise SystemExit(main())


