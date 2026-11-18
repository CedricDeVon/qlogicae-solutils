
def main():
    from qlogicae_solutils.v1.library.application_manager import ApplicationManager

    result = (
        ApplicationManager()
            .get_singleton()
            .run()
    )

    return result


if __name__ == "__main__":
    raise SystemExit(main())

