
def main():
    from .library import python_entry_script_manager

    return (
        python_entry_script_manager.run_script(
            __file__,
            ("main.py",)
        )
    )

if __name__ == "__main__":
    raise SystemExit(main())
