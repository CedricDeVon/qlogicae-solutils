

def main():
    try:
        import sys

        from plugin import root
        from qlogicae_cliq.v1.library.cli_app_manager import CliAppManager

        result = CliAppManager().get_singleton().run(
            external_dependency={
                "is_pre_allocated": False,
            },
            plugin={
                "is_recursive": True,
                "imported_modules": (
                    root,
                ),
                "raw_export_data": (),
                # "initial_export_data": {},
            },
        )

        return result

    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
